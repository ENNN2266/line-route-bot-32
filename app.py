from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

# 從環境變數讀取
line_bot_api = LineBotApi(os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("LINE_CHANNEL_SECRET"))

# 32 家保養廠：url 用來單獨回覆，coord 用來串接導航
shops = {
    "義和": {"url": "https://maps.app.goo.gl/e3J3GgXZFdEuwphj9", "coord": "23.4216702,120.4409688"},
    "國順": {"url": "https://maps.app.goo.gl/4cPP4As2gFpbQozY7", "coord": "23.4376108,120.4013589"},
    "聰勝": {"url": "https://maps.app.goo.gl/W51NYW2HyRff1m6YA", "coord": "23.5077754,120.5136020"},
    "詠昇": {"url": "https://maps.app.goo.gl/NFVj6T3JA5pUi9SK6", "coord": "23.4690378,120.4412752"},
    "詠晟": {"url": "https://maps.app.goo.gl/dHoFZxZnjEkuUczH9", "coord": "23.4802038,120.4822644"},
    "鴻利": {"url": "https://maps.app.goo.gl/RP6fSqw7Rd2YJMF48", "coord": "23.4776612,120.4769557"},
    "尚宸": {"url": "https://maps.app.goo.gl/emRNLMPb4TT16s4t9", "coord": "23.4667945,120.4602934"},
    "倍強": {"url": "https://maps.app.goo.gl/UzZFur4DzmscfaAf7", "coord": "23.4632328,120.4574915"},
    "阿信": {"url": "https://maps.app.goo.gl/UzZFur4DzmscfaAf7", "coord": "23.4632328,120.4574915"},
    "技安": {"url": "https://maps.app.goo.gl/tEehZ6CYouTYtVtK7", "coord": "23.4461621,120.4699786"},
    "永安": {"url": "https://maps.app.goo.gl/tyrD2N1aS76gc6Hn8", "coord": "23.4479579,120.4586747"},
    "宏凱": {"url": "https://maps.app.goo.gl/EcefMvaMimjKyLsw8", "coord": "23.4138971,120.5150387"},
    "力源": {"url": "https://maps.app.goo.gl/mLanjMwuL7GkoMeS8", "coord": "23.4518654,120.4757027"},
    "旺泰": {"url": "https://maps.app.goo.gl/XALPhH4XNWSE1Mr4A", "coord": "23.4333238,120.4952916"},
    "和美": {"url": "https://maps.app.goo.gl/rQLkNTDQVhb9kdZ99", "coord": "23.4415000,120.4978889"},
    "翔燦": {"url": "https://maps.app.goo.gl/ZBCjF756fBJEhk8m8", "coord": "23.4515695,120.4765282"},
    "合豐": {"url": "https://maps.app.goo.gl/b66HTVSUm5P4GSFJA", "coord": "23.4598740,120.4716174"},
    "福音": {"url": "https://maps.app.goo.gl/VwFLjN7D4ZMe6izU7", "coord": "23.4872063,120.4290112"},
    "國鼎": {"url": "https://maps.app.goo.gl/3NQ6BAyiqptnK1Hg9", "coord": "23.4742160,120.4252983"},
    "駿吉": {"url": "https://maps.app.goo.gl/6RhQTJeCHoLTDmbA7", "coord": "23.4973088,120.4616285"},
    "鴻元": {"url": "https://maps.app.goo.gl/JUvswbP5Rnz5GNRA8", "coord": "23.4908363,120.4388773"},
    "鴻興": {"url": "https://maps.app.goo.gl/knVB6MT42kLuoJqz7", "coord": "23.4488769,120.4130188"},
    "東光": {"url": "https://maps.app.goo.gl/ymycaeiK7ApPvmz76", "coord": "23.4666069,120.4582177"},
    "肚臍": {"url": "https://maps.app.goo.gl/JxqpEVxnCRQ71Ds18", "coord": "23.4806531,120.4177952"},
    "林岳欽": {"url": "https://maps.app.goo.gl/H5mRbm1guMzkCYzy9", "coord": "23.5001389,120.3664722"},
    "宏昇": {"url": "https://maps.app.goo.gl/8FN41dTXGEsmf3oT8", "coord": "23.4640312,120.2706579"},
    "展慶": {"url": "https://maps.app.goo.gl/cJrUS5PsmZ5WzY3r7", "coord": "23.4413048,120.4190961"},
    "河南": {"url": "https://maps.app.goo.gl/UJ7E88Q5uNuYSEb77", "coord": "23.4766319,120.4362883"},
    "嘉義輪胎": {"url": "https://maps.app.goo.gl/LJk6zpRgt1oDZU9K6", "coord": "23.4890107,120.4434237"},
    "明昌": {"url": "https://maps.app.goo.gl/VA3fjvooiHnkaGPx9", "coord": "23.5127738,120.5468198"},
    "進興": {"url": "https://maps.app.goo.gl/ztZfmE1GyWHKSftYA", "coord": "23.4855212,120.5558662"},
    "慶順": {"url": "https://maps.app.goo.gl/Hbh8sqp4RMmuwFWy6", "coord": "23.4817629,120.5601896"}
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
            shop = shops[word]
            # 單一回覆短網址
            replies.append(f"{word} 導航：{shop['url']}")
            # 多點導航用經緯度
            nav_links.append(shop["coord"])

    # 如果最後是「導航」 → 多點導航
    if user_msg.endswith("導航") and nav_links:
        route_url = "https://www.google.com/maps/dir/current+location/" + "/".join(nav_links)
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
