from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 換成你自己的 Channel Access Token 和 Channel Secret
line_bot_api = LineBotApi("你的 Channel Access Token")
handler = WebhookHandler("你的 Channel Secret")

# ==============================
# 保養廠資料庫
# ==============================
shops = {
    "義和": {"url": "https://maps.app.goo.gl/e3J3GgXZFdEuwphj9?g_st=ipc", "lat": 23.4216702, "lng": 120.4409688},
    "國順": {"url": "https://maps.app.goo.gl/4cPP4As2gFpbQozY7?g_st=ipc", "lat": 23.4376108, "lng": 120.4013589},
    "聰勝": {"url": "https://maps.app.goo.gl/W51NYW2HyRff1m6YA?g_st=ipc", "lat": 23.5077754, "lng": 120.5136020},
    "詠昇": {"url": "https://maps.app.goo.gl/NFVj6T3JA5pUi9SK6?g_st=ipc", "lat": 23.4690378, "lng": 120.4412752},
    "詠晟": {"url": "https://maps.app.goo.gl/dHoFZxZnjEkuUczH9?g_st=ipc", "lat": 23.4802038, "lng": 120.4822644},
    "鴻利": {"url": "https://maps.app.goo.gl/RP6fSqw7Rd2YJMF48?g_st=ipc", "lat": 23.4776612, "lng": 120.4769557},
    "尚宸": {"url": "https://maps.app.goo.gl/emRNLMPb4TT16s4t9?g_st=ipc", "lat": 23.4667945, "lng": 120.4602934},
    "倍強": {"url": "https://maps.app.goo.gl/UzZFur4DzmscfaAf7?g_st=ipc", "lat": 23.4632328, "lng": 120.4574915},
    "阿信": {"url": "https://maps.app.goo.gl/UzZFur4DzmscfaAf7?g_st=ipc", "lat": 23.4632328, "lng": 120.4574915},
    "技安": {"url": "https://maps.app.goo.gl/tEehZ6CYouTYtVtK7?g_st=ipc", "lat": 23.4461621, "lng": 120.4699786},
    "永安": {"url": "https://maps.app.goo.gl/tyrD2N1aS76gc6Hn8?g_st=ipc", "lat": 23.4479579, "lng": 120.4586747},
    "宏凱": {"url": "https://maps.app.goo.gl/EcefMvaMimjKyLsw8?g_st=ipc", "lat": 23.4138971, "lng": 120.5150387},
    "力源": {"url": "https://maps.app.goo.gl/mLanjMwuL7GkoMeS8?g_st=ipc", "lat": 23.4518654, "lng": 120.4757027},
    "旺泰": {"url": "https://maps.app.goo.gl/XALPhH4XNWSE1Mr4A", "lat": 23.4333238, "lng": 120.4952916},
    "和美": {"url": "https://maps.app.goo.gl/rQLkNTDQVhb9kdZ99?g_st=ipc", "lat": 23.4415000, "lng": 120.4978889},
    "翔燦": {"url": "https://maps.app.goo.gl/ZBCjF756fBJEhk8m8?g_st=ipc", "lat": 23.4515695, "lng": 120.4765282},
    "合豐": {"url": "https://maps.app.goo.gl/b66HTVSUm5P4GSFJA?g_st=ipc", "lat": 23.4598740, "lng": 120.4716174},
    "福音": {"url": "https://maps.app.goo.gl/VwFLjN7D4ZMe6izU7?g_st=ipc", "lat": 23.4872063, "lng": 120.4290112},
    "國鼎": {"url": "https://maps.app.goo.gl/3NQ6BAyiqptnK1Hg9?g_st=ipc", "lat": 23.4742160, "lng": 120.4252983},
    "駿吉": {"url": "https://maps.app.goo.gl/6RhQTJeCHoLTDmbA7?g_st=ipc", "lat": 23.4973088, "lng": 120.4616285},
    "鴻元": {"url": "https://maps.app.goo.gl/JUvswbP5Rnz5GNRA8?g_st=ipc", "lat": 23.4908363, "lng": 120.4388773},
    "鴻興": {"url": "https://maps.app.goo.gl/knVB6MT42kLuoJqz7?g_st=ipc", "lat": 23.4488769, "lng": 120.4130188},
    "東光": {"url": "https://maps.app.goo.gl/ymycaeiK7ApPvmz76?g_st=ipc", "lat": 23.4666069, "lng": 120.4582177},
    "肚臍": {"url": "https://maps.app.goo.gl/JxqpEVxnCRQ71Ds18", "lat": 23.4806531, "lng": 120.4177952},
    "林岳欽": {"url": "https://maps.app.goo.gl/H5mRbm1guMzkCYzy9?g_st=ipc", "lat": 23.5001389, "lng": 120.3664722},
    "宏昇": {"url": "https://maps.app.goo.gl/8FN41dTXGEsmf3oT8?g_st=ipc", "lat": 23.4640312, "lng": 120.2706579},
    "展慶": {"url": "https://maps.app.goo.gl/cJrUS5PsmZ5WzY3r7?g_st=ipc", "lat": 23.4413048, "lng": 120.4190961},
    "河南": {"url": "https://maps.app.goo.gl/UJ7E88Q5uNuYSEb77?g_st=ipc", "lat": 23.4766319, "lng": 120.4362883},
    "嘉義輪胎": {"url": "https://maps.app.goo.gl/LJk6zpRgt1oDZU9K6?g_st=ipc", "lat": 23.4890107, "lng": 120.4434237},
    "明昌": {"url": "https://maps.app.goo.gl/VA3fjvooiHnkaGPx9?g_st=ipc", "lat": 23.5127738, "lng": 120.5468198},
    "進興": {"url": "https://maps.app.goo.gl/ztZfmE1GyWHKSftYA?g_st=ipc", "lat": 23.4855212, "lng": 120.5558662},
    "慶順": {"url": "https://maps.app.goo.gl/Hbh8sqp4RMmuwFWy6?g_st=ipc", "lat": 23.4817629, "lng": 120.5601896},
}

# ==============================
# LINE Webhook
# ==============================
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK", 200

# ==============================
# 訊息處理
# ==============================
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text.strip()

    # 拆字，可能一次輸入多個店名
    names = user_text.replace("導航", "").split()
    found_shops = []

    for name in names:
        if name in shops:
            found_shops.append((name, shops[name]))

    reply_messages = []

    # 如果找不到
    if not found_shops:
        reply_messages.append(TextSendMessage(text="⚠️ 請輸入有效的店名，例如：國順 義和"))
    else:
        # 列出各別店家
        for name, info in found_shops:
            reply_messages.append(
                TextSendMessage(text=f"{name} 導航：{info['url']}")
            )

        # 如果文字包含「導航」→ 組合路線
        if "導航" in user_text and len(found_shops) > 1:
            waypoints = "/".join([f"{s[1]['lat']},{s[1]['lng']}" for s in found_shops])
            gmap_url = f"https://www.google.com/maps/dir/{waypoints}"
            reply_messages.append(TextSendMessage(text=f"🛵 多站路線導航：{gmap_url}"))

    line_bot_api.reply_message(event.reply_token, reply_messages)

# ==============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
