# 飞书通知 Hook

当 Claude Code 需要用户输入或任务结束时，通过飞书自定义机器人发送通知。

## 文件说明

- `notify.py` - 飞书通知发送脚本
- `config.json` - 配置文件

## 配置步骤

### 1. 配置飞书机器人

1. 在飞书群聊中添加自定义机器人
2. 获取 Webhook 地址和签名密钥 (secret)

### 2. 修改配置文件

编辑 `config.json`，替换为实际的 Webhook 地址和密钥：

```json
{
  "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "secret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}
```

### 3. 配置 Claude Code Hook

已在 `settings.local.json` 中自动配置。

## 支持的事件

| 事件 | 触发时机 |
|-----|---------|
| Notification | 需要用户输入时 |
| Stop | 任务结束时 |

## 通知内容

- 通知类型
- 通知内容 (来自 stdin JSON 数据)
- 触发时间
- 项目目录
