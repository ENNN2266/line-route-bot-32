from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import re

app = Flask(__name__)

line_bot_api = LineBotApi("你的Channel access token")
handler = WebhookHandler("你的Channel secret")

# 你的保養廠字典
shop_dict = {
    "義和": ["義和汽車修配廠", "https://maps.app.goo.gl/e3J3GgXZFdEuwphj9"],
    "國順": ["SUM國順汽車", "https://maps.app.goo.gl/4cPP4As2gFpbQozY7"],
    "聰勝": ["聰勝汽車保修廠", "https://maps.app.goo.gl/W51NYW2HyRff1m6YA"],
    "詠昇": ["詠昇汽車修理廠", "https://maps.app.goo.gl/NFVj6T3JA5pUi9SK6"],
    "詠晟": ["詠晟汽車", "https://maps.app.goo.gl/dHoFZxZnjEkuUczH9"],
    "鴻利": ["鴻利馬牌輪胎", "https://maps.app.goo.gl/RP6fSqw7Rd2YJMF48"],
    "尚宸": ["尚宸汽車", "https://maps.app.goo.gl/emRNLMPb4TT16s4t9"],
    "倍強": ["倍強汽車保養廠", "https://maps.app.goo.gl/UzZFur4DzmscfaAf7"],
    "阿信": ["阿信汽車（倍強裡面）", "https://maps.app.goo.gl/UzZFur4DzmscfaAf7"],
    "技安": ["技安汽車修理廠", "https://maps.app.goo.gl/tEehZ6CYouTYtVtK7"],
    "永安": ["永安汽車保養場", "https://maps.app.goo.gl/tyrD2N1aS76gc6Hn8"],
    "宏凱": ["宏凱汽車", "https://maps.app.goo.gl/EcefMvaMimjKyLsw8"],
    "力源": ["力源汽車修理廠", "https://maps.app.goo.gl/mLanjMwuL7GkoMeS8"],
    "旺泰": ["旺泰汽車", "https://maps.app.goo.gl/XALPhH4XNWSE1Mr4A"],
    "和美": ["和美汽車", "https://maps.app.goo.gl/rQLkNTDQVhb9kdZ99"],
    "翔燦": ["翔燦汽車修護廠", "https://maps.app.goo.gl/ZBCjF756fBJEhk8m8"],
    "合豐": ["合豐車工坊", "https://maps.app.goo.gl/b66HTVSUm5P4GSFJA"],
    "福音": ["福音汽車商行", "https://maps.app.goo.gl/VwFLjN7D4ZMe6izU7"],
    "國鼎": ["國鼎汽車商行", "https://maps.app.goo.gl/3NQ6BAyiqptnK1Hg9"],
    "駿吉": ["駿吉輪胎行", "https://maps.app.goo.gl/6RhQTJeCHoLTDmbA7"],
    "鴻元": ["鴻元汽車修護廠", "https://maps.app.goo.gl/JUvswbP5Rnz5GNRA8"],
    "鴻興": ["鴻興汽車保養工場", "https://maps.app.goo.gl/knVB6MT42kLuoJqz7"],
    "東光": ["東光汽車電機行", "https://maps.app.goo.gl/ymycaeiK7ApPvmz76"],
    "肚臍": ["肚臍", "https://maps.app.goo.gl/JxqpEVxnCRQ71Ds18"],
    "林岳欽": ["林岳欽", "https://maps.app.goo.gl/H5mRbm1guMzkCYzy9"],
    "宏昇": ["宏昇汽車修護廠", "https://maps.app.goo.gl/8FN41dTXGEsmf3oT8"],
    "展慶": ["展慶汽車修護廠", "https://maps.app.goo.gl/cJrUS5PsmZ5WzY3r7"],
    "河南": ["河南輪胎保養場", "https://maps.app.goo.gl/UJ7E88Q5uNuYSEb77"],
    "嘉義輪胎": ["嘉義輪胎", "https://maps.app.goo.gl/LJk6zpRgt1oDZU9K6"],
    "明昌": ["明昌汽車修理廠", "https://maps.app.goo.gl/VA3fjvooiHnkaGPx9"],
    "進興": ["進興汽車保養場", "https://maps.app.goo.gl/ztZfmE1GyWHKSftYA"],
    "慶順": ["慶順汽車保養廠", "https://maps.app.goo.gl/Hbh8sqp4RMmuwFWy6"]
}

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text.strip()
    words = user_text.split()

    results = []
    route_links = []

    for word in words:
        if word in shop_dict:
            name, link = shop_dict[word]
            results.append(f"{name}：{link}")
            route_links.append(link)

    reply = "\n".join(results) if results else "⚠️ 請輸入有效的店名，例如：國順 義和"

    # 如果最後一個字是「導航」，加總路線
    if user_text.endswith("導航") and route_links:
        maps_route = "https://www.google.com/maps/dir/" + "/".join(route_links)
        reply += f"\n\n🛣️ 多點導航路線：{maps_route}"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )
