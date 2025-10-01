from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

# 環境變數 (Render 後台設定)
line_bot_api = LineBotApi(os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("LINE_CHANNEL_SECRET"))

# 保養廠資料 (32家)
shops = {
    "義和": "https://maps.app.goo.gl/e3J3GgXZFdEuwphj9",
    "國順": "https://maps.app.goo.gl/4cPP4As2gFpbQozY7",
    "聰勝": "https://maps.app.goo.gl/W51NYW2HyRff1m6YA",
    "詠昇": "https://maps.app.goo.gl/NFVj6T3JA5pUi9SK6",
    "詠晟": "https://maps.app.goo.gl/dHoFZxZnjEkuUczH9",
    "鴻利": "https://maps.app.goo.gl/RP6fSqw7Rd2YJMF48",
    "尚宸": "https://maps.app.goo.gl/emRNLMPb4TT16s4t9",
    "倍強": "https://maps.app.goo.gl/UzZFur4DzmscfaAf7",
    "阿信": "https://maps.app.goo.gl/UzZFur4DzmscfaAf7",
    "技安": "https://maps.app.goo.gl/tEehZ6CYouTYtVtK7",
    "永安": "https://maps.app.goo.gl/tyrD2N1aS76gc6Hn8",
    "宏凱": "https://maps.app.goo.gl/EcefMvaMimjKyLsw8",
    "力源": "https://maps.app.goo.gl/mLanjMwuL7GkoMeS8",
    "旺泰": "https://maps.app.goo.gl/XALPhH4XNWSE1Mr4A",
    "和美": "https://maps.app.goo.gl/rQLkNTDQVhb9kdZ99",
    "翔燦": "https://maps.app.goo.gl/ZBCjF756fBJEhk8m8",
    "合豐": "https://maps.app.goo.gl/b66HTVSUm5P4GSFJA",
    "福音": "https://maps.app.goo.gl/VwFLjN7D4ZMe6izU7",
    "國鼎": "https://maps.app.goo.gl/3NQ6BAyiqptnK1Hg9",
    "駿吉": "https://maps.app.goo.gl/6RhQTJeCHoLTDmbA7",
    "鴻元": "https://maps.app.goo.gl/JUvswbP5Rnz5GNRA8",
    "鴻興": "https://maps.app.goo.gl/knVB6MT42kLuoJqz7",
    "東光": "https://maps.app.goo.gl/ymycaeiK7ApPvmz76",
    "肚臍": "https://maps.app.goo.gl/JxqpEVxnCRQ71Ds18",
    "林岳欽": "https://maps.app.goo.gl/H5mRbm1guMzkCYzy9",
    "宏昇": "https://maps.app.goo.gl/8FN41dTXGEsmf3oT8",
    "展慶": "https://maps.app.goo.gl/cJrUS5PsmZ5WzY3r7",
    "河南": "https://maps.app.goo.gl/UJ7E88Q5uNuYSEb77",
    "嘉義輪胎": "https://maps.app.goo.gl/LJk6zpRgt1oDZU9K6",
    "明昌": "https://maps.app.goo.gl/VA3fjvooiHnkaGPx9",
    "進興": "https://maps.app.goo.gl/ztZfmE1GyWHKSftYA",
    "慶順": "https://maps.app.goo.gl/Hbh8sqp4RMmuwFWy6"
}

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK", 200


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_msg = event.message.text.strip()
    words = user_msg.split()

    replies = []
    nav_links = []

    for word in words:
        if word in shops:
            url = shops[word]
            replies.append(f"{word} 導航：{url}")
            nav_links.append(url)

    # 如果最後一個字是「導航」，就串 Google Maps 路線
    if user_msg.endswith("導航") and nav_links:
        route_url = "https://www.google.com/maps/dir/" + "/".join(nav_links)
        replies.append(f"📍 路線規劃：{route_url}")

    if not replies:
        replies = ["⚠️ 請輸入有效的店名，例如：國順 義和"]

    line_bot_api.reply_message(
        event.reply_token,
        [TextSendMessage(text=msg) for msg in replies]
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
