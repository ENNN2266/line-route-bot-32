from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

# 環境變數設定 (Render → Environment)
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 32 家保養廠資料
shops = {
    "義和": ("義和汽車修配廠", "https://maps.app.goo.gl/e3J3GgXZFdEuwphj9", 23.4216702, 120.4409688),
    "國順": ("SUM國順汽車", "https://maps.app.goo.gl/4cPP4As2gFpbQozY7", 23.4376108, 120.4013589),
    "聰勝": ("聰勝汽車保修廠", "https://maps.app.goo.gl/W51NYW2HyRff1m6YA", 23.5077754, 120.5136020),
    "詠昇": ("詠昇汽車修理廠", "https://maps.app.goo.gl/NFVj6T3JA5pUi9SK6", 23.4690378, 120.4412752),
    "詠晟": ("詠晟汽車", "https://maps.app.goo.gl/dHoFZxZnjEkuUczH9", 23.4802038, 120.4822644),
    "鴻利": ("鴻利馬牌輪胎", "https://maps.app.goo.gl/RP6fSqw7Rd2YJMF48", 23.4776612, 120.4769557),
    "尚宸": ("尚宸汽車", "https://maps.app.goo.gl/emRNLMPb4TT16s4t9", 23.4667945, 120.4602934),
    "倍強": ("倍強汽車保養廠", "https://maps.app.goo.gl/UzZFur4DzmscfaAf7", 23.4632328, 120.4574915),
    "阿信": ("阿信汽車（倍強裡面）", "https://maps.app.goo.gl/UzZFur4DzmscfaAf7", 23.4632328, 120.4574915),
    "技安": ("技安汽車修理廠", "https://maps.app.goo.gl/tEehZ6CYouTYtVtK7", 23.4461621, 120.4699786),
    "永安": ("永安汽車保養場", "https://maps.app.goo.gl/tyrD2N1aS76gc6Hn8", 23.4479579, 120.4586747),
    "宏凱": ("宏凱汽車", "https://maps.app.goo.gl/EcefMvaMimjKyLsw8", 23.4138971, 120.5150387),
    "力源": ("力源汽車修理廠", "https://maps.app.goo.gl/mLanjMwuL7GkoMeS8", 23.4518654, 120.4757027),
    "旺泰": ("旺泰汽車", "https://maps.app.goo.gl/XALPhH4XNWSE1Mr4A", 23.4333238, 120.4952916),
    "和美": ("和美汽車", "https://maps.app.goo.gl/rQLkNTDQVhb9kdZ99", 23.4415000, 120.4978889),
    "翔燦": ("翔燦汽車修護廠", "https://maps.app.goo.gl/ZBCjF756fBJEhk8m8", 23.4515695, 120.4765282),
    "合豐": ("合豐車工坊", "https://maps.app.goo.gl/b66HTVSUm5P4GSFJA", 23.4598740, 120.4716174),
    "福音": ("福音汽車商行", "https://maps.app.goo.gl/VwFLjN7D4ZMe6izU7", 23.4872063, 120.4290112),
    "國鼎": ("國鼎汽車商行", "https://maps.app.goo.gl/3NQ6BAyiqptnK1Hg9", 23.4742160, 120.4252983),
    "駿吉": ("駿吉輪胎行", "https://maps.app.goo.gl/6RhQTJeCHoLTDmbA7", 23.4973088, 120.4616285),
    "鴻元": ("鴻元汽車修護廠", "https://maps.app.goo.gl/JUvswbP5Rnz5GNRA8", 23.4908363, 120.4388773),
    "鴻興": ("鴻興汽車保養工場", "https://maps.app.goo.gl/knVB6MT42kLuoJqz7", 23.4488769, 120.4130188),
    "東光": ("東光汽車電機行", "https://maps.app.goo.gl/ymycaeiK7ApPvmz76", 23.4666069, 120.4582177),
    "肚臍": ("肚臍", "https://maps.app.goo.gl/JxqpEVxnCRQ71Ds18", 23.4806531, 120.4177952),
    "林岳欽": ("林岳欽", "https://maps.app.goo.gl/H5mRbm1guMzkCYzy9", 23.5001389, 120.3664722),
    "宏昇": ("宏昇汽車修護廠", "https://maps.app.goo.gl/8FN41dTXGEsmf3oT8", 23.4640312, 120.2706579),
    "展慶": ("展慶汽車修護廠", "https://maps.app.goo.gl/cJrUS5PsmZ5WzY3r7", 23.4413048, 120.4190961),
    "河南": ("河南輪胎保養場", "https://maps.app.goo.gl/UJ7E88Q5uNuYSEb77", 23.4766319, 120.4362883),
    "嘉義輪胎": ("嘉義輪胎", "https://maps.app.goo.gl/LJk6zpRgt1oDZU9K6", 23.4890107, 120.4434237),
    "明昌": ("明昌汽車修理廠", "https://maps.app.goo.gl/VA3fjvooiHnkaGPx9", 23.5127738, 120.5468198),
    "進興": ("進興汽車保養場", "https://maps.app.goo.gl/ztZfmE1GyWHKSftYA", 23.4855212, 120.5558662),
    "慶順": ("慶順汽車保養廠", "https://maps.app.goo.gl/Hbh8sqp4RMmuwFWy6", 23.4817629, 120.5601896),
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
    text = event.message.text.strip()
    found_shops = []

    for key, (name, url, lat, lng) in shops.items():
        if key in text:
            found_shops.append((name, url, lat, lng))

    # 沒找到
    if not found_shops:
        reply = "⚠️ 請輸入有效的店名，例如: 國順 義和"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))
        return

    # 如果輸入包含 "導航"
    if "導航" in text and len(found_shops) >= 2:
        base_url = "https://www.google.com/maps/dir/?api=1"
        waypoints = "|".join([f"{lat},{lng}" for _, _, lat, lng in found_shops[:-1]])
        destination = f"{found_shops[-1][2]},{found_shops[-1][3]}"
        maps_url = f"{base_url}&origin=Current+Location&destination={destination}&waypoints={waypoints}"

        reply = "🗺️ 導航路線:\n" + maps_url
    else:
        reply_lines = []
        for name, url, _, _ in found_shops:
            reply_lines.append(f"{name} 導航：{url}")
        reply = "\n".join(reply_lines)

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
