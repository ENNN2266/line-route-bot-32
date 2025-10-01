import os
import urllib.parse
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "")
CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET", "")
ORIGIN_NAME = os.getenv("ORIGIN_NAME", "瑞昌汽車材料行")

if not CHANNEL_ACCESS_TOKEN or not CHANNEL_SECRET:
    raise RuntimeError("Please set LINE_CHANNEL_ACCESS_TOKEN and LINE_CHANNEL_SECRET.")

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

PLACE_LINKS = {'義和': 'https://maps.app.goo.gl/e3J3GgXZFdEuwphj9', '國順': 'https://maps.app.goo.gl/4cPP4As2gFpbQozY7', '聰勝': 'https://maps.app.goo.gl/W51NYW2HyRff1m6YA', '詠昇': 'https://maps.app.goo.gl/NFVj6T3JA5pUi9SK6', '詠晟': 'https://maps.app.goo.gl/dHoFZxZnjEkuUczH9', '鴻利': 'https://maps.app.goo.gl/RP6fSqw7Rd2YJMF48', '尚宸': 'https://maps.app.goo.gl/emRNLMPb4TT16s4t9', '倍強': 'https://maps.app.goo.gl/UzZFur4DzmscfaAf7', '阿信': 'https://maps.app.goo.gl/UzZFur4DzmscfaAf7', '技安': 'https://maps.app.goo.gl/tEehZ6CYouTYtVtK7', '永安': 'https://maps.app.goo.gl/tyrD2N1aS76gc6Hn8', '宏凱': 'https://maps.app.goo.gl/EcefMvaMimjKyLsw8', '力源': 'https://maps.app.goo.gl/mLanjMwuL7GkoMeS8', '旺泰': 'https://maps.app.goo.gl/XALPhH4XNWSE1Mr4A', '和美': 'https://maps.app.goo.gl/rQLkNTDQVhb9kdZ99', '翔燦': 'https://maps.app.goo.gl/ZBCjF756fBJEhk8m8', '合豐': 'https://maps.app.goo.gl/b66HTVSUm5P4GSFJA', '福音': 'https://maps.app.goo.gl/VwFLjN7D4ZMe6izU7', '國鼎': 'https://maps.app.goo.gl/3NQ6BAyiqptnK1Hg9', '駿吉': 'https://maps.app.goo.gl/6RhQTJeCHoLTDmbA7', '鴻元': 'https://maps.app.goo.gl/JUvswbP5Rnz5GNRA8', '鴻興': 'https://maps.app.goo.gl/knVB6MT42kLuoJqz7', '東光': 'https://maps.app.goo.gl/ymycaeiK7ApPvmz76', '肚臍': 'https://maps.app.goo.gl/JxqpEVxnCRQ71Ds18', '林岳欽': 'https://maps.app.goo.gl/H5mRbm1guMzkCYzy9', '宏昇': 'https://maps.app.goo.gl/8FN41dTXGEsmf3oT8', '展慶': 'https://maps.app.goo.gl/cJrUS5PsmZ5WzY3r7', '河南': 'https://maps.app.goo.gl/UJ7E88Q5uNuYSEb77', '嘉義輪胎': 'https://maps.app.goo.gl/LJk6zpRgt1oDZU9K6', '明昌': 'https://maps.app.goo.gl/VA3fjvooiHnkaGPx9', '進興': 'https://maps.app.goo.gl/ztZfmE1GyWHKSftYA', '慶順': 'https://maps.app.goo.gl/Hbh8sqp4RMmuwFWy6'}

def tokenize(text):
    seps = [",", "，", "、", " ", "->", "→", "|", "\n"]
    for sep in ["->", "→", "|"]:
        text = text.replace(sep, ",")
    for sep in ["，", "、", " "]:
        text = text.replace(sep, ",")
    parts = [p.strip() for p in text.split(",") if p.strip()]
    return parts

def build_maps_dir(origin_name, stops):
    path = "/".join([origin_name] + stops)
    return "https://www.google.com/maps/dir/" + urllib.parse.quote(path, safe="/")

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK", 200

@handler.add(MessageEvent, message=TextMessage)
def on_message(event):
    text = event.message.text.strip()
    reply_lines = []

    if text.startswith("路線"):
        places = tokenize(text[2:])
        if places:
            url = build_maps_dir(ORIGIN_NAME, places)
            reply_lines.append(f"出發點：{ORIGIN_NAME}")
            reply_lines.append("依序路線導航：")
            reply_lines.append(url)
        else:
            reply_lines.append("格式錯誤，請輸入：路線 義和 國順 ...")
    else:
        places = tokenize(text)
        if places:
            for p in places:
                if p in PLACE_LINKS:
                    reply_lines.append(f"{p} 導航：{PLACE_LINKS[p]}")
        if not reply_lines:
            reply_lines.append("請輸入店名（例如：義和、國順、尚宸）或使用：路線 義和 國順")

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="\n".join(reply_lines)))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
