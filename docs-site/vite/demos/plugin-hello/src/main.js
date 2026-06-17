// 注意：这里的 __HELLO__ 是个占位符——直接跑会报"未定义"。
// 但 vite-plugin-hello 插件会在 transform 阶段把它替换成字符串。
const greeting = __HELLO__
document.querySelector('#app').textContent = greeting
