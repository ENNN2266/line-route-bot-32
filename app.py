import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 從環境變數讀取 Channel Access Token 和 Secret
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# 店家地圖連結
PLACE_LINKS = {
    "義和": "https://maps.app.goo.gl/e3J3GgXZFdEuwphj9?g_st=ipc",
    "國順": "https://maps.app.goo.gl/4cPP4As2gFpbQozY7?g_st=ipc",
    "聰勝": "https://maps.app.goo.gl/W51NYW2HyRff1m6YA?g_st=ipc",
    "詠昇": "https://maps.app.goo.gl/NFVj6T3JA5pUi9SK6?g_st=ipc",
    "詠晟": "https://maps.app.goo.gl/dHoFZxZnjEkuUczH9?g_st=ipc",
    "鴻利": "https://maps.app.goo.gl/RP6fSqw7Rd2YJMF48?g_st=ipc",
    "尚宸": "https://maps.app.goo.gl/emRNLMPb4TT16s4t9?g_st=ipc",
    "倍強": "https://maps.app.goo.gl/UzZFur4DzmscfaAf7?g_st=ipc",
    "阿信": "https://maps.app.goo.gl/UzZFur4DzmscfaAf7?g_st=ipc",
    "技安": "https://maps.app.goo.gl/tEehZ6CYouTYtVtK7?g_st=ipc",
    "永安": "https://maps.app.goo.gl/tyrD2N1aS76gc6Hn8?g_st=ipc",
    "宏凱": "https://maps.app.goo.gl/EcefMvaMimjKyLsw8?g_st=ipc",
    "力源": "https://maps.app.goo.gl/mLanjMwuL7GkoMeS8?g_st=ipc",
    "旺泰": "https://maps.app.goo.gl/XALPhH4XNWSE1Mr4A",
    "和美": "https://maps.app.goo.gl/rQLkNTDQVhb9kdZ99?g_st=ipc",
    "翔燦": "https://maps.app.goo.gl/ZBCjF756fBJEhk8m8?g_st=ipc",
    "合豐": "https://maps.app.goo.gl/b66HTVSUm5P4GSFJA?g_st=ipc",
    "福音": "https://maps.app.goo.gl/VwFLjN7D4ZMe6izU7?g_st=ipc",
    "國鼎": "https://maps.app.goo.gl/3NQ6BAyiqptnK1Hg9?g_st=ipc",
    "駿吉": "https://maps.app.goo.gl/6RhQTJeCHoLTDmbA7?g_st=ipc",
    "鴻元": "https://maps.app.goo.gl/JUvswbP5Rnz5GNRA8?g_st=ipc",
    "鴻興": "https://maps.app.goo.gl/knVB6MT42kLuoJqz7?g_st=ipc",
    "東光": "https://maps.app.goo.gl/ymycaeiK7ApPvmz76?g_st=ipc",
    "肚臍": "https://maps.app.goo.gl/JxqpEVxnCRQ71Ds18",
    "林岳欽": "https://maps.app.goo.gl/H5mRbm1guMzkCYzy9?g_st=ipc",
    "宏昇": "https://maps.app.goo.gl/8FN41dTXGEsmf3oT8?g_st=ipc",
    "展慶": "https://maps.app.goo.gl/cJrUS5PsmZ5WzY3r7?g_st=ipc",
    "河南": "https://maps.app.goo.gl/UJ7E88Q5uNuYSEb77?g_st=ipc",
    "嘉義輪胎": "https://maps.app.goo.gl/LJk6zpRgt1oDZU9K6?g_st=ipc",
    "明昌": "https://maps.app.goo.gl/VA3fjvooiHnkaGPx9?g_st=ipc",
    "進興": "https://maps.app.goo.gl/ztZfmE1GyWHKSftYA?g_st=ipc",
    "慶順": "https://maps.app.goo.gl/Hbh8sqp4RMmuwFWy6?g_st=ipc"
}

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK', 200

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text.strip()
    if text in PLACE_LINKS:
        reply = f"{text} 導航：{PLACE_LINKS[text]}"
    else:
        reply = "請輸入店名，例如：義和、國順、詠晟"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
