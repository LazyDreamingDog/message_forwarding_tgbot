import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

load_dotenv()

# 清除代理，直连 Telegram API
for key in ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "all_proxy", "ALL_PROXY"]:
    os.environ.pop(key, None)

# ============ 配置 ============
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TARGET_USER_IDS = [
    int(uid.strip())
    for uid in os.getenv("TARGET_USER_IDS", "").split(",")
    if uid.strip()
]
SOURCE_CHAT_ID = int(os.getenv("SOURCE_CHAT_ID", "0"))
TARGET_CHAT_ID = int(os.getenv("TARGET_CHAT_ID", "0"))

# ============ 日志 ============
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ============ Telegram 消息处理 ============
async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    if message is None:
        return

    user = message.from_user
    if user is None:
        return

    # 打印每条消息的用户信息，方便获取用户 ID
    logger.info(
        "收到消息 - 用户: %s, ID: %d, 群组: %s (%d)",
        user.full_name, user.id, message.chat.title or "私聊", message.chat_id,
    )

    # 只处理源群组的消息
    if SOURCE_CHAT_ID and message.chat_id != SOURCE_CHAT_ID:
        return

    # 只转发目标用户的消息
    if TARGET_USER_IDS and user.id not in TARGET_USER_IDS:
        return

    user_display = user.full_name or user.username or str(user.id)
    chat_title = message.chat.title or "私聊"
    text = message.text or message.caption or "[非文本消息]"

    forward_text = f"来自 {user_display} ({chat_title}):\n\n{text}"

    logger.info("转发用户 %s (%d) 的消息", user_display, user.id)

    try:
        await context.bot.send_message(chat_id=TARGET_CHAT_ID, text=forward_text)
    except Exception:
        logger.exception("转发消息失败")


# ============ 主函数 ============
def main() -> None:
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("请在 .env 中设置 TELEGRAM_BOT_TOKEN")
    if not TARGET_CHAT_ID:
        raise ValueError("请在 .env 中设置 TARGET_CHAT_ID")

    logger.info("Bot 启动中...")
    logger.info("监听的目标用户 ID: %s", TARGET_USER_IDS or "全部用户")
    logger.info("转发到群组: %s", TARGET_CHAT_ID)

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT | filters.CAPTION, on_message))

    logger.info("Bot 已启动，开始监听消息...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
