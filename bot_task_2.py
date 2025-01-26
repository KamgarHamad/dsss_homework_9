from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from transformers import pipeline


# Initialize the model pipeline
def init_model():
    """Initialize the TinyLlama model"""
    try:
        print("Loading model...")
        generator = pipeline(
            "text-generation",
            model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            torch_dtype="auto",
            device_map="auto"
        )
        print("Model loaded successfully!")
        return generator
    except Exception as e:
        print(f"Error loading model: {e}")
        return None


# Initialize the model globally
model = init_model()


async def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text("Hi! I am an AI assistant. How can I help you today?")


async def process(update: Update, context: CallbackContext) -> None:
    """Process the user message with the LLM."""
    if model is None:
        await update.message.reply_text("Sorry, I'm having trouble with my AI model. Please try again later.")
        return

    user_message = update.message.text

    try:
        # Format the prompt for better response
        prompt = f"User: {user_message}\nAssistant: Let me help you with that. "

        # Generate response
        response = model(
            prompt,
            max_length=200,
            num_return_sequences=1,
            temperature=0.7,
            do_sample=True
        )

        # Extract and clean the response
        ai_response = response[0]['generated_text'].split("Assistant:")[-1].strip()

        await update.message.reply_text(ai_response)
    except Exception as e:
        print(f"Error generating response: {e}")
        await update.message.reply_text("I apologize, but I encountered an error processing your request.")


def main() -> None:
    """Start the bot."""
    # Replace with your bot token
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