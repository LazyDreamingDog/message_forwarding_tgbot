# Telegram 消息转发 Bot

监听 Telegram 源群组中指定用户的消息，自动转发到另一个 Telegram 群组。

## 安装

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 配置

```bash
cp .env.example .env
```

| 变量 | 说明 |
|------|------|
| `TELEGRAM_BOT_TOKEN` | 从 @BotFather 获取的 Bot Token |
| `SOURCE_CHAT_ID` | 源群组 Chat ID（要监听的群） |
| `TARGET_USER_IDS` | 要监听的用户 ID，逗号分隔 |
| `TARGET_CHAT_ID` | 转发目标群组的 Chat ID |

## 前置准备

1. 在 Telegram 找 **@BotFather**，发送 `/newbot` 创建 Bot，获取 Token
2. 将 Bot 加入**源群组**（设为管理员，这样无需关闭 Privacy Mode 也能读取消息）
3. 将 Bot 加入**目标群组**（需要发消息权限）

## 获取 Chat ID

在 Telegram 搜索 **@RawDataBot**，拉入群组后它会自动回复群组的 Chat ID（负数），拿到后移除即可。

## 获取用户 ID

在 Telegram 搜索 **@userinfobot**，将目标用户的消息转发给它，会回复该用户的 ID。

## 运行

```bash
source venv/bin/activate
python bot.py
```

### 后台运行（服务器部署）

```bash
nohup python bot.py > bot.log 2>&1 &
```
