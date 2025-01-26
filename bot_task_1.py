from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext


async def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    # TODO
    await update.message.reply_text("Hi! I am an AI assistant. How can I help you today?")


async def process(update: Update, context: CallbackContext) -> None:
    """Process the user message."""
    # TODO
    await update.message.reply_text(f"Received: {update.message.text}")


def main() -> None:
    """Start the bot."""
    API_TOKEN = "My_Token"

    # Create application
    application = Application.builder().token(API_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process))

    # Start the bot
    print("Starting bot...")
    application.run_polling()


if __name__ == "__main__":
    main()