#!/usr/bin/env python3
"""
Claude Code 飞书通知 Hook
当 Claude 需要用户输入时，通过飞书自定义机器人发送通知
"""

# 设置 UTF-8 编码，解决 Windows 终端乱码问题
import sys
import io
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import base64
import hashlib
import hmac
import json
import os
import sys
import time
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")


def load_config():
    """加载配置文件"""
    if not os.path.exists(CONFIG_FILE):
        print(f"错误: 配置文件不存在: {CONFIG_FILE}")
        sys.exit(1)

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = json.load(f)

    if "webhook_url" not in config or "secret" not in config:
        print("错误: 配置文件中缺少 webhook_url 或 secret")
        sys.exit(1)

    return config


def generate_signature(timestamp, secret):
    """生成飞书签名"""
    string_to_sign = f"{timestamp}\n{secret}"
    hmac_code = hmac.new(
        string_to_sign.encode("utf-8"),
        digestmod=hashlib.sha256
    ).digest()
    return base64.b64encode(hmac_code).decode("utf-8")


def send_feishu_notification(webhook_url, secret, notification_text, hook_type="Notification"):
    """发送飞书通知"""
    # 获取当前时间戳（秒）
    timestamp = str(int(time.time()))

    # 生成签名
    signature = generate_signature(timestamp, secret)

    # 消息内容 - 清理无效的 Unicode 代理字符
    project_dir = os.getcwd()
    trigger_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 过滤掉无效的代理字符
    cleaned_text = notification_text.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')

    # 根据 hook 类型显示不同的消息
    if hook_type == "Stop":
        title = "任务结束"
        emoji = "✅"
    elif hook_type == "SessionStart":
        title = "会话开始"
        emoji = "🆕"
    else:
        title = "需要用户输入"
        emoji = "🔔"

    message_content = f"""【Claude Code 通知】

{emoji} 类型: {title}

📝 内容:
{cleaned_text}

⏰ 触发时间: {trigger_time}

📁 项目目录: {project_dir}
"""

    # 构造请求数据
    data = {
        "msg_type": "text",
        "content": {
            "text": message_content
        },
        "timestamp": timestamp,
        "sign": signature
    }

    json_data = json.dumps(data, ensure_ascii=False).encode("utf-8")

    # 发送请求
    request = Request(
        webhook_url,
        data=json_data,
        headers={"Content-Type": "application/json"}
    )

    try:
        with urlopen(request, timeout=10) as response:
            result = json.loads(response.read().decode("utf-8"))
            if result.get("code") == 0:
                print("飞书通知发送成功")
                return True
            else:
                print(f"飞书通知发送失败: {result.get('msg')}")
                return False
    except HTTPError as e:
        print(f"HTTP 错误: {e.code} - {e.reason}")
        return False
    except URLError as e:
        print(f"URL 错误: {e.reason}")
        return False
    except Exception as e:
        print(f"发送通知时出错: {e}")
        return False


def main():
    """主函数"""
    # 获取 hook 类型（通过环境变量）
    hook_type = os.environ.get("hook", "Notification")

    # 从 stdin 读取 JSON 数据（使用 buffer 避免编码问题）
    notification_text = ""
    try:
        # 使用 stdin.buffer 直接读取原始字节，强制 UTF-8 解码
        stdin_bytes = sys.stdin.buffer.read()
        stdin_text = stdin_bytes.decode('utf-8')
        input_data = json.loads(stdin_text)

        # 根据不同 hook 类型获取通知内容
        if hook_type == "Stop":
            # Stop 事件：包含 session 相关信息
            session = input_data.get("session", {})
            stop_reason = input_data.get("stop_reason", "未知")
            notification_text = f"任务已结束，停止原因: {stop_reason}"
        elif hook_type == "SessionStart":
            # SessionStart 事件
            notification_text = "新会话已开始"
        else:
            # Notification 事件（默认）
            notification_text = input_data.get("notification_text", "")

    except json.JSONDecodeError:
        print("错误: 无法解析输入的 JSON 数据")
        notification_text = ""
    except Exception as e:
        print(f"读取输入时出错: {e}")
        notification_text = ""

    if not notification_text:
        print("警告: 未获取到通知内容")
        notification_text = "（无具体内容）"

    # 加载配置
    config = load_config()

    # 发送通知
    send_feishu_notification(
        config["webhook_url"],
        config["secret"],
        notification_text,
        hook_type
    )


if __name__ == "__main__":
    main()
