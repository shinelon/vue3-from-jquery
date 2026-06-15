// 一个最小的 Vite 插件：把代码里的 __HELLO__ 占位符替换成一句话。
// 插件 = 返回对象的函数，对象里的方法是"钩子"。
export default function helloPlugin(options = {}) {
  const greeting = options.greeting || '来自插件'
  return {
    name: 'vite-plugin-hello',      // 插件名（调试/报错时能看到）
    transform(code, id) {
      // 只处理 .js 文件，把 __HELLO__ 替换掉
      if (id.endsWith('.js')) {
        return code.replace(/__HELLO__/g, JSON.stringify(greeting))
      }
      // 返回 undefined = 不处理这个文件
    }
  }
}
