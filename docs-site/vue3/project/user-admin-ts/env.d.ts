/// <reference types="vite/client" />

// 让 TS 认得 .vue 文件（Vite + vue-tsc 需要这个声明）
declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<Record<string, unknown>, Record<string, unknown>, unknown>
  export default component
}
