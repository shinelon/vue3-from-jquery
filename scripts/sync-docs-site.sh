#!/usr/bin/env bash
# =============================================================================
# sync-docs-site.sh — 把仓库「原件」同步生成 MkDocs 内容根 docs-site/
# -----------------------------------------------------------------------------
# 唯一真源（改教程请改这里，再跑本脚本）：
#   docs/                 → vue3 教程正文
#   demos/                → vue3 基础章 demo
#   project/              → vue3 CRUD 项目
#   vite-tutorial/docs/   → vite 教程正文
#   vite-tutorial/demos/  → vite demo
#   git 分支 vite/08-final → vite-notes 项目（main 工作树为空，取分支最终成品）
#
# 生成目标：docs-site/{vue3,vite}/
#   docs-site/index.md 与 mkdocs.yml 为站点专用，不在本脚本范围。
#
# 期间做的 MkDocs 适配（原文件不动，仅作用于生成副本）：
#   1. vite 第0章跨教程链接 ../../docs/ → ../../vue3/docs/
#   2. vite 第11章 lib-mode 无 index.html，目录链接改指 README.md
#   3. 删除与 index.html 冲突的 README.md（MkDocs 以 index.html 为准，本就被丢弃）
#
# 用法： bash scripts/sync-docs-site.sh
# =============================================================================
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
SITE="docs-site"

# 仅复制 git 跟踪文件（排除 node_modules/dist 等未跟踪产物），保留目录结构
copy_tracked() {
  local src="$1" dst="$2"
  mkdir -p "$dst"
  local n=0
  while IFS= read -r f; do
    [ -z "$f" ] && continue
    local rel="${f#$src/}"
    local target="$dst/$rel"
    mkdir -p "$(dirname "$target")"
    cp "$f" "$target"
    n=$((n+1))
  done < <(git -c core.quotepath=false ls-files -- "$src")
  echo "  $src → $dst ($n 文件)"
}

echo "==> 清理旧内容树（保留 index.md）"
rm -rf "$SITE/vue3" "$SITE/vite"
mkdir -p "$SITE/vue3" "$SITE/vite"

echo "==> 复制原件"
copy_tracked docs                "$SITE/vue3/docs"
copy_tracked demos               "$SITE/vue3/demos"
copy_tracked project             "$SITE/vue3/project"
copy_tracked vite-tutorial/docs  "$SITE/vite/docs"
copy_tracked vite-tutorial/demos "$SITE/vite/demos"

echo "==> 提取 vite-notes（git 分支 vite/08-final 最终成品）"
mkdir -p "$SITE/vite/project/vite-notes"
git archive vite/08-final -- vite-tutorial/project/vite-notes \
  | tar -x -C "$SITE/vite/project/vite-notes" --strip-components=3
# vite-notes 有 index.html，删除与之冲突的 README（与其它 project 一致）
rm -f "$SITE/vite/project/vite-notes/README.md"

echo "==> 应用 MkDocs 链接适配"
# 1) vite 第0章跨教程链接
sed -i 's#\.\./\.\./docs/#../../vue3/docs/#g' "$SITE/vite/docs/00-为什么是Vite.md"
# 2) vite 第11章 lib-mode 无 index.html，目录链接改指 README.md
sed -i 's#(\.\./demos/lib-mode/)#(../demos/lib-mode/README.md)#g' "$SITE/vite/docs/11-库模式.md"

echo "==> 删除与 index.html 冲突的 README"
rm -f "$SITE/vue3/demos/ch04-vite-start/README.md" \
      "$SITE/vue3/demos/ch05-components/README.md" \
      "$SITE/vue3/project/user-admin/README.md" \
      "$SITE/vue3/project/user-admin-ts/README.md"

echo "==> 统一换行符为 LF（配合 .gitattributes，保证跨平台幂等）"
# docs-site 仅含文本（md/代码/json/env），无二进制；故全部归一化
find "$SITE" -type f -print0 | xargs -0 -r sed -i 's/\r$//'

echo "==> 校验：mkdocs build --strict（零 WARNING 方为通过）"
mkdocs build --strict

echo ""
echo "✓ docs-site 已从原件重新生成，strict 构建通过。"
echo "  改教程请改原件（docs/、vite-tutorial/docs/ 等），再跑： bash scripts/sync-docs-site.sh"
