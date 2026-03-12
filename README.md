# Telegram 消息转发 Bot

监听 Telegram 群组中指定用户的消息，自动转发到另一个 Telegram 群组。

## 安装

```bash
pip install -r requirements.txt
```

## 配置

```bash
cp .env.example .env
```

| 变量 | 说明 |
|------|------|
| `TELEGRAM_BOT_TOKEN` | 从 @BotFather 获取的 Bot Token |
| `TARGET_USER_IDS` | 要监听的用户 ID，逗号分隔 |
| `TARGET_CHAT_ID` | 转发目标群组的 Chat ID |

> Bot 需要同时加入源群组和目标群组，并拥有发消息权限。

## 获取 Chat ID

将 Bot 加入目标群组后，访问 `https://api.telegram.org/bot<TOKEN>/getUpdates`，在返回的 JSON 中找到群组的 `chat.id`（通常是负数）。

## 获取用户 ID

将 [bot.py](bot.py) 中日志级别改为 `DEBUG`，运行后让目标用户发消息，日志会打印用户 ID。

## 运行

```bash
python bot.py
```
