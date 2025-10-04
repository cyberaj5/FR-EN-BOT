from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from deep_translator import GoogleTranslator
from typing import Final

token: Final = "7947988246:AAH0LxIyG2iq5695Dro6SJgy5860pEZ5Z-4"
Bot_username: Final = "@french_english_bot"


# Start command with inline buttons
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("English to French", callback_data="en_fr"),
            InlineKeyboardButton("French to English", callback_data="fr_en"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Welcome! I am  Translai👨🏾‍🏫, your trusty translating fr-en ☺ .\n\nPlease choose the language you are translating today:",
        reply_markup=reply_markup
    )
    context.user_data.clear()

# Handle inline button presses
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "en_fr":
        context.user_data["translation_direction"] = ("en", "fr")
        await query.edit_message_text("You chose: English to French.\n\nSend me text to translate. Type /exit to change direction.")
    elif query.data == "fr_en":
        context.user_data["translation_direction"] = ("fr", "en")
        await query.edit_message_text("You chose: French to English.\n\nSend me text to translate. Type /exit to change direction.")

# Handle translation and /exit
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()

    # Sentient responses
    if "who created you" in text:
        await update.message.reply_text("I was created by my trusty fr-en, a developer who wanted to help people with language barrier,AJani Oluwaferanmi Emmanuel.")
        return
    if "why were you created" in text or "what is your purpose" in text:
        await update.message.reply_text("I was created to assist with translating between French and English, making communication easier for everyone In a Frenc!")
        return

    direction = context.user_data.get("translation_direction")
    if not direction:
        await update.message.reply_text("Please use /start to select a translation direction.")
        return

    src, dest = direction
    translated = GoogleTranslator(source=src, target=dest).translate(update.message.text)
    await update.message.reply_text(f"Translated: {translated}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use /start to begin and /exit to change translation direction.")

async def exit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_command(update, context)
    return

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

if __name__ == "__main__":
    print("Starting bot...")
    # Initialize the bot application with the token
    application = Application.builder().token(token).build()
    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("exit", exit_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT, handle_message))
    application.add_error_handler(error)

    print("Bot started successfully!")
    application.run_polling()
