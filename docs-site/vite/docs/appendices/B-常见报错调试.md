# 附录 B · 常见报错与调试

用 Vite 开发踩到的常见坑，这里给原因和解法。卡住时先来这找。

---

## 🐛 常见错误

### 1. 端口被占用：`Port 5173 is in use`

**原因**：另一个 dev 服务器（或别的程序）占了 5173。
**解决**：Vite 会自动换端口（5174、5175...），看终端输出的实际端口。或关掉占用程序。

---

### 2. 跨域：`CORS` / `Access-Control-Allow-Origin`

**原因**：前端直接请求别的域 / 端口的接口，浏览器拦。
**解决**：dev 用 `server.proxy`（第 5 章）；上线同域部署或 nginx 反代。

---

### 3. `Failed to resolve import '@/xxx'`

**原因**：用了 `@` 别名，但没配 `resolve.alias`，或 jsconfig 没配（编辑器报错）。
**解决**：vite.config 配 alias（第 3 章）；编辑器加 `jsconfig.json`。

---

### 4. 改了 `.env` 不生效

**原因**：HMR 不监听 `.env` 文件。
**解决**：**重启 dev**（Ctrl+C 后重新 `npm run dev`）。

---

### 5. 部署后刷新 404（SPA）

**原因**：history 路由 + 服务器没配 SPA fallback。
**解决**：nginx 加 `try_files $uri $uri/ /index.html;`（第 10 章）。

---

### 6. 部署后资源 404（白屏）

**原因**：部署在子路径，但没配 `base`。
**解决**：vite.config 配 `base: '/你的子路径/'`（第 10 章）。

---

### 7. `manualChunks is not a function`

**原因**：Vite 8（Rolldown）下用了对象形式 `manualChunks: {...}`。
**解决**：改用**函数形式** `manualChunks(id) { ... }`（第 9 章）。

---

### 8. `[vite] Failed to resolve dependency`

**原因**：import 了一个没装的包。
**解决**：`npm install xxx` 装上。

---

## 🛠️ 调试利器

### 看请求：浏览器 F12 → Network
- 看接口状态码、请求 / 响应内容；
- 排查代理是否生效、跨域、404。

### 看编译产物：`npm run build` 后看 `dist/`
- 看 chunk 拆分对不对、体积大不大。

### 看插件是否生效：dev 终端日志
- 插件的 `name`、`configureServer` 的 log 会出现在终端。

### 清缓存：删 `node_modules/.vite`
- dev 行为诡异（缓存导致），删 `.vite` 重启。

---

## 💡 调试小技巧

1. **怀疑请求不对？** F12 → Network 看请求 URL 和响应；
2. **怀疑构建不对？** `npm run build` 看 dist 产物；
3. **怀疑缓存？** 删 `.vite` / hard refresh（Ctrl+Shift+R）；
4. **报错看不懂？** 复制关键错误信息搜，或查 Vite GitHub Issues。
