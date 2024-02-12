from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import (MessageEvent,
                            TextMessage,
                            TextSendMessage)

import openai
openai.api_key = "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"
model_use = "text-davinci-003"

channel_secret = "5e6718e26058080da3e21971f1fdcd60"
channel_access_token = "n1YOEdbK2PQBhoaJx4TwbPyME8rgzoSaItl6Y0Hsyn2Jqo6jm09v4LfiIznpfFNzHxdOpOZrPkHd4rMNlkXNX8goqjCpSdX/w5gMnEUxXG7g6nyKgC5F4v5A7iMgzfOtNLaa18smX4vdBDGTMXm00AdB04t89/1O/w1cDnyilFU="

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
    try:
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)
        handler.handle(body, signature)
    except:
        pass
    
    return "Hello Line Chatbot"

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    print(text)

    if text.startswith("ถาม:"):
        prompt_text = text[5:].strip()  # Extract text after "ถาม:" and remove leading/trailing spaces
        response = openai.Completion.create(
            model=model_use,
            prompt=prompt_text,  
            max_tokens=1024
        )
        text_out = response.choices[0].text 
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text_out))

if __name__ == "__main__":          
    app.run()

