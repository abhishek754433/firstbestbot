# bot.py
from telegram.ext import Updater, CommandHandler, MessageHandler, filters
from telegram import Update
# Import the token and name from our config file
from config import BOT_TOKEN, BOT_NAME 
import logging
import sys

# --- Logging Setup ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Command Handlers ---

def start(update: Update, context):
    """Handles the /start command."""
    user = update.effective_user
    
    # Custom Reply on /start, ensuring **user.first_name** is bolded.
    welcome_message = (
        f"Hello **{user.first_name}**! 👋\n"
        f"I am **{BOT_NAME}**, your simple chat bot. I'm ready to talk!\n"
        "Try sending me messages like 'hello', 'what is your name', or 'thank you'."
    )
    
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=welcome_message,
        parse_mode='Markdown'
    )

def help_command(update: Update, context):
    """Handles the /help command."""
    help_text = (
        "🤖 **Available Commands:**\n"
        "/start - Get a welcome message\n"
        "/help - See this help message\n\n"
        "I respond to keywords like 'hello', 'name', and 'thank' in your messages."
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=help_text,
        parse_mode='Markdown'
    )

# --- Message Handler (The Custom Reply Logic) ---

def custom_reply_logic(update: Update, context):
    """Handles all incoming text messages and provides custom replies."""
    # Ensure the update has text before processing
    if not update.message or not update.message.text:
        return
        
    user_message = update.message.text.lower()
    reply_text = ""

    # --- Keyword Matching Logic ---
    if "hello" in user_message or "hi" in user_message:
        reply_text = "Hi! I hope you are having a wonderful day."
        
    elif "name" in user_message or "bot" in user_message:
        reply_text = f"My name is **{BOT_NAME}**. I am an AI designed to assist you."
        
    elif "thank" in user_message or "thanks" in user_message:
        reply_text = "You are absolutely welcome! Is there anything else I can do?"
        
    else:
        # Default reply
        reply_text = f"I see you sent: '**{update.message.text}**'. I'm not sure how to respond to that, but feel free to ask me something else!"
        
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=reply_text,
        parse_mode='Markdown'
    )

# --- Main Function to Run the Bot ---

def main():
    """Start the bot."""
    # Check if the token is the default placeholder
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ ERROR: Please update the BOT_TOKEN in config.py with your actual token.")
        sys.exit(1) # Exit if token is not set

    # Initialize the Updater with the token
    updater = Updater(BOT_TOKEN, use_context=True)

    dp = updater.dispatcher

    # Register Handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(filters.Text & ~filters.COMMAND, custom_reply_logic))

    # Start Polling
    updater.start_polling()
    logger.info(f"**{BOT_NAME}** started successfully. Talking to Telegram...")

    # Keep the bot running
    updater.idle()

if __name__ == '__main__':
    main()
