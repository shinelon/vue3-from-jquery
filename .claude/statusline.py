#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Claude Code StatusLine — Catppuccin Mocha 256-color, two-row minimalist"""

import sys
import json
import os
import time
import re

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


# ===== ANSI 256-color (Catppuccin Mocha) =====
ESC = "\033["
RESET = ESC + "0m"
BOLD = ESC + "1m"


def _fg(n):
    return ESC + "38;5;" + str(n) + "m"


def _bg(n):
    return ESC + "48;5;" + str(n) + "m"


C = {
    "text": _fg(254),
    "subtext": _fg(246),
    "overlay": _fg(240),
    "blue": _fg(110),
    "green": _fg(114),
    "yellow": _fg(179),
    "red": _fg(210),
    "mauve": _fg(201),
    "peach": _fg(215),
    "teal": _fg(108),
    "surface0": _bg(236),
    "surface1": _bg(238),
    "base": _bg(234),
    "mantle": _bg(233),
}


# ===== icons =====
ICO_MODEL = "*"
ICO_SPEED = "~"
ICO_TOK_IN = "^"
ICO_PROMPT = "#"
ICO_GIT = "@"
ICO_SEP = " | "


# ===== stdin reader =====


def load_input():
    try:
        raw = sys.stdin.read()
        if raw.strip():
            return json.loads(raw)
    except Exception:
        pass
    return {}


# ===== cache helpers =====
_TMP = os.environ.get("TEMP", "/tmp")


def _read_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _write_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception:
        pass


def _cache_paths(session_id):
    tag = session_id[:8] if session_id else "default"
    return (
        os.path.join(_TMP, "claude-speed-" + tag + ".json"),
        os.path.join(_TMP, "claude-prompt-" + tag + ".json"),
    )


# ===== model name parser =====
_VER_RE = re.compile(r"[-.](\d+)[-._](\d+)")
_GLM5_RE = re.compile(r"glm-5[.-]?(\d+)?")
_GLM4_RE = re.compile(r"glm-4[.-]?(\w+)?")
_GPT4_RE = re.compile(r"gpt-4[.-]?(\d+)?")

_MODEL_TABLE = [
    ("opus", "Opus", _VER_RE),
    ("sonnet", "Sonnet", _VER_RE),
    ("haiku", "Haiku", _VER_RE),
    ("glm-5", "GLM-5", _GLM5_RE),
    ("glm-4", "GLM-4", _GLM4_RE),
    ("gpt-4o", "GPT-4o", None),
    ("gpt-4", "GPT-4", _GPT4_RE),
    ("gpt-3", "GPT-3.5", None),
]


def model_display_name(data):
    try:
        model = data.get("model", {})
        raw = ""
        if isinstance(model, dict):
            raw = model.get("id", "") or model.get("display_name", "")
        else:
            raw = str(model)
        if not raw:
            return ""
        clean = raw.replace("models/", "").replace("anthropic/", "")
        low = clean.lower()
        for pattern, display, ver_re in _MODEL_TABLE:
            if pattern not in low:
                continue
            if ver_re is None:
                return display
            m = ver_re.search(low)
            if m and m.group(1):
                sep = "." if ver_re is _VER_RE else ("." if pattern == "glm-5" else "-")
                suffix = m.group(1).upper() if pattern == "glm-4" else m.group(1)
                return display + sep + suffix + ("." + m.group(2) if ver_re is _VER_RE and m.group(2) else "")
            return display
        return clean[:25]
    except Exception:
        return ""


# ===== git info (zero subprocess) =====


def get_git_info(cwd):
    if not cwd:
        return "", False
    cwd = cwd.replace("\\", "/")

    current = cwd.rstrip("/")
    git_path = None
    while True:
        candidate = os.path.join(current, ".git")
        if os.path.exists(candidate):
            git_path = candidate
            break
        parent = os.path.dirname(current)
        if parent == current:
            return "", False
        current = parent

    is_dir = os.path.isdir(git_path)
    head_path = os.path.join(git_path, "HEAD") if is_dir else None
    git_dir = git_path if is_dir else None

    if head_path is None:
        try:
            with open(git_path, "r", encoding="utf-8") as f:
                line = f.read().strip()
            if line.startswith("gitdir: "):
                rel = line[8:]
                git_dir = os.path.normpath(os.path.join(os.path.dirname(git_path), rel))
                head_path = os.path.join(git_dir, "HEAD")
        except Exception:
            return "", False

    if not head_path or not os.path.isfile(head_path):
        return "", False

    try:
        with open(head_path, "r", encoding="utf-8") as f:
            head = f.read().strip()
    except Exception:
        return "", False

    if head.startswith("ref: refs/heads/"):
        branch = head[16:]
    else:
        branch = head[:7]

    dirty = os.path.exists(os.path.join(git_dir, "MERGE_HEAD")) if git_dir else False

    return branch, dirty


# ===== speed tracking (dual-channel EMA) =====
_GAP_MAX = 30.0


def compute_stream_state(data, speed_cache_path):
    try:
        ctx = data.get("context_window", {})
        total_in = ctx.get("total_input_tokens", 0) or 0
        total_out = ctx.get("total_output_tokens", 0) or 0
        if total_in == 0 and total_out == 0:
            return 0.0, 0.0

        now = time.time()
        prev = _read_json(speed_cache_path) or {}

        prev_ts = prev.get("ts", 0)
        prev_in = prev.get("total_input", 0)
        prev_out = prev.get("total_output", 0)
        prev_itps = prev.get("input_tps", 0.0)
        prev_otps = prev.get("output_tps", 0.0)

        itps = 0.0
        otps = 0.0

        if prev_ts > 0:
            delta_s = now - prev_ts
            if delta_s > 0.1:
                alpha = 1.0 if delta_s > _GAP_MAX else 0.5
                delta_in = total_in - prev_in
                delta_out = total_out - prev_out
                instant_in = delta_in / delta_s if delta_in > 0 else 0
                instant_out = delta_out / delta_s if delta_out > 0 else 0
                itps = alpha * instant_in + (1 - alpha) * prev_itps
                otps = alpha * instant_out + (1 - alpha) * prev_otps
            else:
                itps = prev_itps
                otps = prev_otps

        _write_json(
            speed_cache_path,
            {
                "ts": now,
                "total_input": total_in,
                "total_output": total_out,
                "input_tps": itps,
                "output_tps": otps,
            },
        )
        return itps, otps
    except Exception:
        return 0.0, 0.0


# ===== prompt count =====


def compute_prompt_count(data, prompt_cache_path):
    try:
        session_id = data.get("session_id", "")
        ctx = data.get("context_window", {})
        total_in = ctx.get("total_input_tokens", 0) or 0

        prev = _read_json(prompt_cache_path)

        if prev and prev.get("session_id") == session_id:
            count = prev.get("count", 0)
            if total_in > prev.get("total_input", 0):
                count += 1
                _write_json(
                    prompt_cache_path,
                    {"session_id": session_id, "count": count, "total_input": total_in},
                )
            return count
        else:
            count = 1 if total_in > 0 else 0
            _write_json(
                prompt_cache_path,
                {"session_id": session_id, "count": count, "total_input": total_in},
            )
            return count
    except Exception:
        return 0


# ===== rendering helpers =====

_ANSI_RE = re.compile(r"\033\[[0-9;]*m")


def _visible_width(s):
    return len(_ANSI_RE.sub("", s))


def progress_bar(ratio, width=6, color=None):
    filled = round(ratio * width)
    empty = width - filled
    fg = color or C["green"]
    return fg + "▓" * filled + C["overlay"] + "░" * empty


def fmt_num(n, decimals=False):
    if n >= 1000000:
        return "%.1fM" % (n / 1000000)
    if n >= 1000:
        return "%.1fk" % (n / 1000)
    return "%.1f" % n if decimals else str(int(n))


def _ctx_color(pct):
    if pct >= 90:
        return C["red"]
    if pct >= 70:
        return C["yellow"]
    return C["green"]


def _tps_color(speed):
    if speed >= 80:
        return C["green"]
    if speed >= 40:
        return C["blue"]
    if speed >= 15:
        return C["yellow"]
    if speed > 0:
        return C["red"]
    return C["overlay"]


def render_context(data):
    try:
        ctx = data.get("context_window", {})
        pct = ctx.get("used_percentage")
        if pct is None or pct <= 0:
            return BOLD + progress_bar(0, 6) + C["overlay"] + " --%" + RESET
        pct = round(pct)
        if not pct:
            return BOLD + progress_bar(0, 6) + C["overlay"] + " --%" + RESET

        color = _ctx_color(pct)
        bar = progress_bar(pct / 100, 6, color)

        usage = ctx.get("current_usage", {})
        used = (usage.get("input_tokens", 0) or 0) + (usage.get("output_tokens", 0) or 0)
        total = ctx.get("context_window_size", 0) or 0
        size = ""
        if total > 0:
            size = " " + fmt_num(used) + "/" + fmt_num(total)

        return BOLD + bar + color + " " + str(pct) + "%" + size + RESET
    except Exception:
        return BOLD + progress_bar(0, 6) + C["overlay"] + " --%" + RESET


def render_speed(in_tps, out_tps):
    in_str = fmt_num(in_tps, decimals=True) if in_tps > 0 else "--"
    out_str = fmt_num(out_tps, decimals=True) if out_tps > 0 else "--"
    return BOLD + C["yellow"] + ICO_SPEED + " spd " + _tps_color(in_tps) + in_str + C["overlay"] + "/" + _tps_color(out_tps) + out_str + RESET


def render_tokens(data):
    try:
        usage = data.get("context_window", {}).get("current_usage", {})
        in_t = usage.get("input_tokens", 0) or 0
        out_t = usage.get("output_tokens", 0) or 0
        cache_t = usage.get("cache_read_input_tokens", 0) or 0
        in_s = fmt_num(in_t) if in_t > 0 else "--"
        out_s = fmt_num(out_t) if out_t > 0 else "--"
        cache_s = fmt_num(cache_t) if cache_t > 0 else None
        tok = BOLD + C["blue"] + ICO_TOK_IN + " tok " + C["teal"] + in_s + C["overlay"] + "/" + C["peach"] + out_s
        if cache_s:
            tok += C["overlay"] + "/" + C["yellow"] + cache_s
        return tok + RESET
    except Exception:
        return BOLD + C["blue"] + ICO_TOK_IN + " tok " + C["teal"] + "--" + C["overlay"] + "/" + C["peach"] + "--" + RESET


def render_prompt(count):
    return BOLD + C["blue"] + ICO_PROMPT + " ask " + C["peach"] + str(count) + RESET


def render_project(dir_name, branch, dirty):
    if not dir_name:
        return ""
    text = BOLD + C["blue"] + ICO_GIT + " " + C["peach"] + dir_name
    if branch:
        text += C["blue"] + " @ " + branch
        if dirty:
            text += C["red"] + "*"
    return text + RESET


# ===== main =====


def main():
    data = load_input()

    session_id = data.get("session_id", "")
    speed_path, prompt_path = _cache_paths(session_id)

    model = model_display_name(data)
    cwd = data.get("cwd", "") or os.getcwd()
    dir_name = os.path.basename(cwd.replace("\\", "/").rstrip("/")) if cwd else ""
    branch, dirty = get_git_info(cwd)

    in_tps, out_tps = compute_stream_state(data, speed_path)
    prompt_count = compute_prompt_count(data, prompt_path)

    def _model_seg():
        return BOLD + C["red"] + ICO_MODEL + " " + model + RESET

    cols = [
        (_model_seg() if model else "", render_speed(in_tps, out_tps)),
        (render_context(data), render_tokens(data)),
        (render_project(dir_name, branch, dirty),
         render_prompt(prompt_count) if session_id and prompt_count > 0 else ""),
    ]

    sep = C["yellow"] + " " + ICO_SEP + " " + RESET

    row1_parts, row2_parts = [], []
    for c in range(len(cols)):
        w0 = _visible_width(cols[c][0])
        w1 = _visible_width(cols[c][1])
        mw = max(w0, w1)
        row1_parts.append(cols[c][0] + " " * (mw - w0))
        row2_parts.append(cols[c][1] + " " * (mw - w1))

    sys.stdout.write(sep.join(row1_parts) + "\n" + sep.join(row2_parts))


main()
