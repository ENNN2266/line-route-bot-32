from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import os

app = Flask(__name__)

# 這裡放你的 LINE Channel Access Token & Secret
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 店家連結（你可以繼續增加）
PLACE_LINKS = {
    "國順": "https://maps.app.goo.gl/4cPP4As2gFpbQozY7",
    "義和": "https://maps.app.goo.gl/e3J3GgXZFdEuwphj9",
    "聰勝": "https://maps.app.goo.gl/W51NYW2HyRff1m6YA",
    "詠昇": "https://maps.app.goo.gl/NFVj6T3JA5pUi9SK6",
    "詠晟": "https://maps.app.goo.gl/dHoFZxZnjEkuUczH9"
}

# 路線導航
def build_maps_dir(origin, stops):
    path = "/".join([origin] + stops)
    return f"https://www.google.com/maps/dir/{path}"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK", 200

# 文字訊息處理
@handler.add(MessageEvent, message=TextMessage)
def on_message(event):
    text = event.message.text.strip()
    tokens = text.split()

    reply_lines = []

    # 如果最後一個字是「導航」→ 生成路線
    if tokens[-1] == "導航" and len(tokens) > 1:
        stops = [p for p in tokens[:-1] if p in PLACE_LINKS]
        if stops:
            url = build_maps_dir("我的位置", stops)
            reply_lines.append("🛵 多點路線導航：")
            reply_lines.append(url)
        else:
            reply_lines.append("❌ 找不到任何有效的店名")
    else:
        # 單店 / 多店：直接列出連結
        for p in tokens:
            if p in PLACE_LINKS:
                reply_lines.append(f"{p} 導航：{PLACE_LINKS[p]}")
        if not reply_lines:
            reply_lines.append("⚠️ 請輸入有效的店名，例如：國順 義和")

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage("\n".join(reply_lines))
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
