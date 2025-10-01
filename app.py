from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import os

app = Flask(__name__)

# 記得改成你自己的
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "你的token")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET", "你的secret")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 保養廠資料
shops = {
    "義和": {"name": "義和汽車修配廠", "url": "https://maps.app.goo.gl/e3J3GgXZFdEuwphj9", "lat": 23.4216702, "lng": 120.4409688},
    "國順": {"name": "SUM國順汽車", "url": "https://maps.app.goo.gl/4cPP4As2gFpbQozY7", "lat": 23.4376108, "lng": 120.4013589},
    "聰勝": {"name": "聰勝汽車保修廠", "url": "https://maps.app.goo.gl/W51NYW2HyRff1m6YA", "lat": 23.5077754, "lng": 120.5136020},
    "詠昇": {"name": "詠昇汽車修理廠", "url": "https://maps.app.goo.gl/NFVj6T3JA5pUi9SK6", "lat": 23.4690378, "lng": 120.4412752},
    "詠晟": {"name": "詠晟汽車", "url": "https://maps.app.goo.gl/dHoFZxZnjEkuUczH9", "lat": 23.4802038, "lng": 120.4822644},
    "鴻利": {"name": "鴻利馬牌輪胎", "url": "https://maps.app.goo.gl/RP6fSqw7Rd2YJMF48", "lat": 23.4776612, "lng": 120.4769557},
    "尚宸": {"name": "尚宸汽車", "url": "https://maps.app.goo.gl/emRNLMPb4TT16s4t9", "lat": 23.4667945, "lng": 120.4602934},
    "倍強": {"name": "倍強汽車保養廠", "url": "https://maps.app.goo.gl/UzZFur4DzmscfaAf7", "lat": 23.4632328, "lng": 120.4574915},
    "阿信": {"name": "阿信汽車（倍強裡面）", "url": "https://maps.app.goo.gl/UzZFur4DzmscfaAf7", "lat": 23.4632328, "lng": 120.4574915},
    "技安": {"name": "技安汽車修理廠", "url": "https://maps.app.goo.gl/tEehZ6CYouTYtVtK7", "lat": 23.4461621, "lng": 120.4699786},
    "永安": {"name": "永安汽車保養場", "url": "https://maps.app.goo.gl/tyrD2N1aS76gc6Hn8", "lat": 23.4479579, "lng": 120.4586747},
    "宏凱": {"name": "宏凱汽車", "url": "https://maps.app.goo.gl/EcefMvaMimjKyLsw8", "lat": 23.4138971, "lng": 120.5150387},
    "力源": {"name": "力源汽車修理廠", "url": "https://maps.app.goo.gl/mLanjMwuL7GkoMeS8", "lat": 23.4518654, "lng": 120.4757027},
    "旺泰": {"name": "旺泰汽車", "url": "https://maps.app.goo.gl/XALPhH4XNWSE1Mr4A", "lat": 23.4333238, "lng": 120.4952916},
    "和美": {"name": "和美汽車", "url": "https://maps.app.goo.gl/rQLkNTDQVhb9kdZ99", "lat": 23.4415000, "lng": 120.4978889},
    "翔燦": {"name": "翔燦汽車修護廠", "url": "https://maps.app.goo.gl/ZBCjF756fBJEhk8m8", "lat": 23.4515695, "lng": 120.4765282},
    "合豐": {"name": "合豐車工坊", "url": "https://maps.app.goo.gl/b66HTVSUm5P4GSFJA", "lat": 23.4598740, "lng": 120.4716174},
    "福音": {"name": "福音汽車商行", "url": "https://maps.app.goo.gl/VwFLjN7D4ZMe6izU7", "lat": 23.4872063, "lng": 120.4290112},
    "國鼎": {"name": "國鼎汽車商行", "url": "https://maps.app.goo.gl/3NQ6BAyiqptnK1Hg9", "lat": 23.4742160, "lng": 120.4252983},
    "駿吉": {"name": "駿吉輪胎行", "url": "https://maps.app.goo.gl/6RhQTJeCHoLTDmbA7", "lat": 23.4973088, "lng": 120.4616285},
    "鴻元": {"name": "鴻元汽車修護廠", "url": "https://maps.app.goo.gl/JUvswbP5Rnz5GNRA8", "lat": 23.4908363, "lng": 120.4388773},
    "鴻興": {"name": "鴻興汽車保養工場", "url": "https://maps.app.goo.gl/knVB6MT42kLuoJqz7", "lat": 23.4488769, "lng": 120.4130188},
    "東光": {"name": "東光汽車電機行", "url": "https://maps.app.goo.gl/ymycaeiK7ApPvmz76", "lat": 23.4666069, "lng": 120.4582177},
    "肚臍": {"name": "肚臍", "url": "https://maps.app.goo.gl/JxqpEVxnCRQ71Ds18", "lat": 23.4806531, "lng": 120.4177952},
    "林岳欽": {"name": "林岳欽", "url": "https://maps.app.goo.gl/H5mRbm1guMzkCYzy9", "lat": 23.5001389, "lng": 120.3664722},
    "宏昇": {"name": "宏昇汽車修護廠", "url": "https://maps.app.goo.gl/8FN41dTXGEsmf3oT8", "lat": 23.4640312, "lng": 120.2706579},
    "展慶": {"name": "展慶汽車修護廠", "url": "https://maps.app.goo.gl/cJrUS5PsmZ5WzY3r7", "lat": 23.4413048, "lng": 120.4190961},
    "河南": {"name": "河南輪胎保養場", "url": "https://maps.app.goo.gl/UJ7E88Q5uNuYSEb77", "lat": 23.4766319, "lng": 120.4362883},
    "嘉義輪胎": {"name": "嘉義輪胎", "url": "https://maps.app.goo.gl/LJk6zpRgt1oDZU9K6", "lat": 23.4890107, "lng": 120.4434237},
    "明昌": {"name": "明昌汽車修理廠", "url": "https://maps.app.goo.gl/VA3fjvooiHnkaGPx9", "lat": 23.5127738, "lng": 120.5468198},
    "進興": {"name": "進興汽車保養場", "url": "https://maps.app.goo.gl/ztZfmE1GyWHKSftYA", "lat": 23.4855212, "lng": 120.5558662},
    "慶順": {"name": "慶順汽車保養廠", "url": "https://maps.app.goo.gl/Hbh8sqp4RMmuwFWy6", "lat": 23.4817629, "lng": 120.5601896},
}

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

@app.route("/", methods=["GET"])
def home():
    return "Line bot is running!"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_msg = event.message.text.strip()
    parts = user_msg.split()

    result_msgs = []
    nav_points = []

    for p in parts:
        if p in shops:
            shop = shops[p]
            result_msgs.append(f"{shop['name']}：{shop['url']}")
            nav_points.append(f"{shop['lat']},{shop['lng']}")

    # 如果有 "導航" 關鍵字
    if "導航" in user_msg and nav_points:
        # 用 saddr=My+Location 讓起點是目前位置
        waypoints = "/".join(nav_points)
        nav_url = f"https://www.google.com/maps/dir/?api=1&origin=My+Location&destination={nav_points[-1]}&waypoints={'|'.join(nav_points[:-1])}"
        result_msgs.append(f"導航路線：{nav_url}")

    if not result_msgs:
        result_msgs.append("⚠️ 請輸入有效的店名，例如：國順 義和")

    line_bot_api.reply_message(
        event.reply_token,
        [TextSendMessage(text=msg) for msg in result_msgs]
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
