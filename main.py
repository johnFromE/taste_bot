import telegram
import os
import openai
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("5737216854:AAEzEb7If0vA_zpLlKxq5vIujMjK6nEfSD0")
OPENAI_API_KEY = os.getenv("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")

bot = telegram.Bot(token=TELEGRAM_TOKEN)

def generate_response(message_text, chat_id):
    # Use the OpenAI API to generate a response based on the message
    openai.api_key = OPENAI_API_KEY
    response = openai.Completion.create(
        engine="davinci",
        prompt=message_text,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    message_response = response.choices[0].text.strip()
    if message_response == "":
        message_response = "I'm sorry, I don't have a response for that."

    # Use the Telegram API to send the response to the user
    bot.send_message(chat_id=chat_id, text=message_response)

def lambda_handler(event, context):
    # Retrieve the message sent by the user
    update = telegram.Update.de_json(event["body"], bot)
    message_text = update.message.text
    chat_id = update.message.chat_id

    # If the user sends the /start command, send a welcome message
    if message_text == "/start":
        bot.send_message(chat_id=chat_id, text="Welcome to my chatbot! How can I assist you?")

    # If this is not the /start command, use the previous messages to generate a more relevant response
    else:
        chat_history = [message.text for message in bot.history(chat_id=chat_id, limit=5)][::-1]
        chat_history.append(message_text)
        prompt = "Conversation history:\n" + "\n".join([f"{i}. {chat_history[i]}" for i in range(len(chat_history)-1)]) + "\n\nUser message:\n" + chat_history[-1] + "\n\nBot response:"
        generate_response(prompt, chat_id)
