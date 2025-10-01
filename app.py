from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# ⚠️ 換成你自己的
line_bot_api = LineBotApi("你的 Channel Access Token")
handler = WebhookHandler("你的 Channel Secret")

# ====== 保養廠資料庫 ======
shops = {
    "義和": {"name": "義和汽車修配廠","url": "https://maps.app.goo.gl/e3J3GgXZFdEuwphj9?g_st=ipc","lat": "23.4216702","lng": "120.4409688"},
    "國順": {"name": "SUM國順汽車","url": "https://maps.app.goo.gl/4cPP4As2gFpbQozY7?g_st=ipc","lat": "23.4376108","lng": "120.4013589"},
    "聰勝": {"name": "聰勝汽車保修廠","url": "https://maps.app.goo.gl/W51NYW2HyRff1m6YA?g_st=ipc","lat": "23.5077754","lng": "120.5136020"},
    "詠昇": {"name": "詠昇汽車修理廠","url": "https://maps.app.goo.gl/NFVj6T3JA5pUi9SK6?g_st=ipc","lat": "23.4690378","lng": "120.4412752"},
    "詠晟": {"name": "詠晟汽車","url": "https://maps.app.goo.gl/dHoFZxZnjEkuUczH9?g_st=ipc","lat": "23.4802038","lng": "120.4822644"},
    "鴻利": {"name": "鴻利馬牌輪胎","url": "https://maps.app.goo.gl/RP6fSqw7Rd2YJMF48?g_st=ipc","lat": "23.4776612","lng": "120.4769557"},
    "尚宸": {"name": "尚宸汽車","url": "https://maps.app.goo.gl/emRNLMPb4TT16s4t9?g_st=ipc","lat": "23.4667945","lng": "120.4602934"},
    "倍強": {"name": "倍強汽車保養廠","url": "https://maps.app.goo.gl/UzZFur4DzmscfaAf7?g_st=ipc","lat": "23.4632328","lng": "120.4574915"},
    "阿信": {"name": "阿信汽車（倍強裡面）","url": "https://maps.app.goo.gl/UzZFur4DzmscfaAf7?g_st=ipc","lat": "23.4632328","lng": "120.4574915"},
    "技安": {"name": "技安汽車修理廠","url": "https://maps.app.goo.gl/tEehZ6CYouTYtVtK7?g_st=ipc","lat": "23.4461621","lng": "120.4699786"},
    "永安": {"name": "永安汽車保養場","url": "https://maps.app.goo.gl/tyrD2N1aS76gc6Hn8?g_st=ipc","lat": "23.4479579","lng": "120.4586747"},
    "宏凱": {"name": "宏凱汽車","url": "https://maps.app.goo.gl/EcefMvaMimjKyLsw8?g_st=ipc","lat": "23.4138971","lng": "120.5150387"},
    "力源": {"name": "力源汽車修理廠","url": "https://maps.app.goo.gl/mLanjMwuL7GkoMeS8?g_st=ipc","lat": "23.4518654","lng": "120.4757027"},
    "旺泰": {"name": "旺泰汽車","url": "https://maps.app.goo.gl/XALPhH4XNWSE1Mr4A","lat": "23.4333238","lng": "120.4952916"},
    "和美": {"name": "和美汽車","url": "https://maps.app.goo.gl/rQLkNTDQVhb9kdZ99?g_st=ipc","lat": "23.4415000","lng": "120.4978889"},
    "翔燦": {"name": "翔燦汽車修護廠","url": "https://maps.app.goo.gl/ZBCjF756fBJEhk8m8?g_st=ipc","lat": "23.4515695","lng": "120.4765282"},
    "合豐": {"name": "合豐車工坊","url": "https://maps.app.goo.gl/b66HTVSUm5P4GSFJA?g_st=ipc","lat": "23.4598740","lng": "120.4716174"},
    "福音": {"name": "福音汽車商行","url": "https://maps.app.goo.gl/VwFLjN7D4ZMe6izU7?g_st=ipc","lat": "23.4872063","lng": "120.4290112"},
    "國鼎": {"name": "國鼎汽車商行","url": "https://maps.app.goo.gl/3NQ6BAyiqptnK1Hg9?g_st=ipc","lat": "23.4742160","lng": "120.4252983"},
    "駿吉": {"name": "駿吉輪胎行","url": "https://maps.app.goo.gl/6RhQTJeCHoLTDmbA7?g_st=ipc","lat": "23.4973088","lng": "120.4616285"},
    "鴻元": {"name": "鴻元汽車修護廠","url": "https://maps.app.goo.gl/JUvswbP5Rnz5GNRA8?g_st=ipc","lat": "23.4908363","lng": "120.4388773"},
    "鴻興": {"name": "鴻興汽車保養工場","url": "https://maps.app.goo.gl/knVB6MT42kLuoJqz7?g_st=ipc","lat": "23.4488769","lng": "120.4130188"},
    "東光": {"name": "東光汽車電機行","url": "https://maps.app.goo.gl/ymycaeiK7ApPvmz76?g_st=ipc","lat": "23.4666069","lng": "120.4582177"},
    "肚臍": {"name": "肚臍","url": "https://maps.app.goo.gl/JxqpEVxnCRQ71Ds18","lat": "23.4806531","lng": "120.4177952"},
    "林岳欽": {"name": "林岳欽","url": "https://maps.app.goo.gl/H5mRbm1guMzkCYzy9?g_st=ipc","lat": "23.5001389","lng": "120.3664722"},
    "宏昇": {"name": "宏昇汽車修護廠","url": "https://maps.app.goo.gl/8FN41dTXGEsmf3oT8?g_st=ipc","lat": "23.4640312","lng": "120.2706579"},
    "展慶": {"name": "展慶汽車修護廠","url": "https://maps.app.goo.gl/cJrUS5PsmZ5WzY3r7?g_st=ipc","lat": "23.4413048","lng": "120.4190961"},
    "河南": {"name": "河南輪胎保養場","url": "https://maps.app.goo.gl/UJ7E88Q5uNuYSEb77?g_st=ipc","lat": "23.4766319","lng": "120.4362883"},
    "嘉義輪胎": {"name": "嘉義輪胎","url": "https://maps.app.goo.gl/LJk6zpRgt1oDZU9K6?g_st=ipc","lat": "23.4890107","lng": "120.4434237"},
    "明昌": {"name": "明昌汽車修理廠","url": "https://maps.app.goo.gl/VA3fjvooiHnkaGPx9?g_st=ipc","lat": "23.5127738","lng": "120.5468198"},
    "進興": {"name": "進興汽車保養場","url": "https://maps.app.goo.gl/ztZfmE1GyWHKSftYA?g_st=ipc","lat": "23.4855212","lng": "120.5558662"},
    "慶順": {"name": "慶順汽車保養廠","url": "https://maps.app.goo.gl/Hbh8sqp4RMmuwFWy6?g_st=ipc","lat": "23.4817629","lng": "120.5601896"}
}

# ====== Webhook ======
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK", 200

# ====== 處理訊息 ======
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text.strip()
    parts = user_text.split()
    shop_keys = [p for p in parts if p in shops]
    need_nav = "導航" in parts

    reply = []
    coords = []

    for key in shop_keys:
        shop = shops[key]
        reply.append(f"{shop['name']}：{shop['url']}")
        coords.append(f"{shop['lat']},{shop['lng']}")

    if need_nav and coords:
        nav_url = "https://www.google.com/maps/dir/?api=1&destination=" + coords[-1]
        if len(coords) > 1:
            nav_url += "&waypoints=" + "|".join(coords[:-1])
        nav_url += "&travelmode=driving"
        reply.append(f"導航路線：{nav_url}")

    if not reply:
        reply.append("⚠️ 請輸入有效的店名，例如：國順 義和")

    line_bot_api.reply_message(
        event.reply_token,
        [TextSendMessage(text=r) for r in reply]
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
