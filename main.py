import configparser
import logging

import requests
from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

config = configparser.ConfigParser()
config.read("config.ini")
TELEGRAM_TOKEN = config["security"]["telegram_token"]
GIPHY_TOKEN = config["security"]["giphy_token"]


async def giphy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a GIF to your message."""
    str_args = " ".join(context.args)
    if str_args:
        url = f"https://api.giphy.com/v1/gifs/translate?api_key={GIPHY_TOKEN}&s={str_args}"
        resp = requests.get(url)
        data = resp.json()["data"]["images"]["original"]["url"]
        logger.info(f"User {update.message.from_user.username} asked giphy - {str_args}")
        await update.message.reply_animation(data)
    else:
        await update.message.reply_text("После комманды отправьте слово или целое предложение :)")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Help message to user."""
    logger.info(f"User {update.message.from_user.username} click help.")
    await update.message.reply_text(
        "Введите команду\n<b>/giphy {Ваше сообщение}</b>\nДля получения GIF от сервиса Giphy.", parse_mode="HTML")


def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    # Command sends a GIF to your message
    application.add_handler(CommandHandler("giphy", giphy))
    # Help Command
    application.add_handler(CommandHandler("help", help))
    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
