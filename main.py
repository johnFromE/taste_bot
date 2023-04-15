import telegram
import openai

# Set up the Telegram bot
bot = telegram.Bot(token="5737216854:AAEzEb7If0vA_zpLlKxq5vIujMjK6nEfSD0")

# Set up OpenAI API
openai.api_key = "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"

# Define a function to handle incoming messages
def handle_message(update, context):
    message_text = update.message.text
    response_text = get_response_from_chatgpt(message_text)
    update.message.reply_text("bot: "+response_text)

# Define a function to get a response from ChatGPT
def get_response_from_chatgpt(prompt):
    # Send a prompt to ChatGPT and get a response
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=100
    )
    response_text = response.choices[0].text.strip()
    return response_text

# Set up a handler for incoming messages
message_handler = telegram.ext.MessageHandler(
    telegram.ext.Filters.text, handle_message)

# Set up the dispatcher and add the message handler
dispatcher = telegram.ext.Dispatcher(bot, None)
dispatcher.add_handler(message_handler)

# Start the bot
bot_updater = telegram.ext.Updater(bot.token, use_context=True)
bot_updater.dispatcher = dispatcher
bot_updater.start_polling()
