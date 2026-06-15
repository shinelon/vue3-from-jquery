import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import express from 'express'
import { createServer as createViteServer } from 'vite'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

async function createServer() {
  const app = express()

  // 以中间件模式启动 Vite（不独立起 dev 服务器）
  const vite = await createViteServer({
    server: { middlewareMode: true },
    appType: 'custom'
  })
  app.use(vite.middlewares)

  // 每个请求：渲染 Vue 应用，把 HTML 塞进模板返回
  app.use('*', async (req, res) => {
    try {
      const template = fs.readFileSync(path.resolve(__dirname, 'index.html'), 'utf-8')
      const transformed = await vite.transformIndexHtml(req.originalUrl, template)
      const { render } = await vite.ssrLoadModule('/src/entry-server.js')
      const appHtml = await render(req.originalUrl)
      const html = transformed.replace('<!--ssr-outlet-->', appHtml)
      res.status(200).set({ 'Content-Type': 'text/html' }).end(html)
    } catch (e) {
      vite.ssrFixStacktrace(e)
      console.error(e)
      res.status(500).end(e.stack)
    }
  })

  app.listen(3000, () => console.log('SSR: http://localhost:3000'))
}

createServer()
