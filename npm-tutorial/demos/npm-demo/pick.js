// npm 速查教程配套 demo
// 用法：先 `npm install`（把 lodash 装进 node_modules），再 `npm run pick`
//
// 这个 demo 演示两件事：
//   1. npm install 拉来的依赖（lodash），可以直接 import 用；
//   2. package.json 里定义的 script（pick），用 npm run 来跑。

import _ from 'lodash'

const todos = ['学 npm', '学 Vite', '学 Vue3', '学 Pinia', '学部署']

// lodash 的 _.sample：从数组里随机挑一个（演示「装了依赖就能用它的方法」）
const pick = _.sample(todos)

console.log(`📋 今天先做这件：${pick}`)
console.log(`\n✅ npm install + npm run pick 跑通了——lodash 已从 node_modules 加载。`)
