from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 你的 LINE BOT Channel Access Token & Secret
line_bot_api = LineBotApi("你的_CHANNEL_ACCESS_TOKEN")
handler = WebhookHandler("你的_CHANNEL_SECRET")

# 保養廠資料庫
location_map = {
    "義和": {"url": "https://maps.app.goo.gl/e3J3GgXZFdEuwphj9", "lat": "23.4216702", "lng": "120.4409688"},
    "國順": {"url": "https://maps.app.goo.gl/4cPP4As2gFpbQozY7", "lat": "23.4376108", "lng": "120.4013589"},
    "聰勝": {"url": "https://maps.app.goo.gl/W51NYW2HyRff1m6YA", "lat": "23.5077754", "lng": "120.5136020"},
    "詠昇": {"url": "https://maps.app.goo.gl/NFVj6T3JA5pUi9SK6", "lat": "23.4690378", "lng": "120.4412752"},
    "詠晟": {"url": "https://maps.app.goo.gl/dHoFZxZnjEkuUczH9", "lat": "23.4802038", "lng": "120.4822644"},
    "鴻利": {"url": "https://maps.app.goo.gl/RP6fSqw7Rd2YJMF48", "lat": "23.4776612", "lng": "120.4769557"},
    "尚宸": {"url": "https://maps.app.goo.gl/emRNLMPb4TT16s4t9", "lat": "23.4667945", "lng": "120.4602934"},
    "倍強": {"url": "https://maps.app.goo.gl/UzZFur4DzmscfaAf7", "lat": "23.4632328", "lng": "120.4574915"},
    "阿信": {"url": "https://maps.app.goo.gl/UzZFur4DzmscfaAf7", "lat": "23.4632328", "lng": "120.4574915"},
    "技安": {"url": "https://maps.app.goo.gl/tEehZ6CYouTYtVtK7", "lat": "23.4461621", "lng": "120.4699786"},
    "永安": {"url": "https://maps.app.goo.gl/tyrD2N1aS76gc6Hn8", "lat": "23.4479579", "lng": "120.4586747"},
    "宏凱": {"url": "https://maps.app.goo.gl/EcefMvaMimjKyLsw8", "lat": "23.4138971", "lng": "120.5150387"},
    "力源": {"url": "https://maps.app.goo.gl/mLanjMwuL7GkoMeS8", "lat": "23.4518654", "lng": "120.4757027"},
    "旺泰": {"url": "https://maps.app.goo.gl/XALPhH4XNWSE1Mr4A", "lat": "23.4333238", "lng": "120.4952916"},
    "和美": {"url": "https://maps.app.goo.gl/rQLkNTDQVhb9kdZ99", "lat": "23.4415000", "lng": "120.4978889"},
    "翔燦": {"url": "https://maps.app.goo.gl/ZBCjF756fBJEhk8m8", "lat": "23.4515695", "lng": "120.4765282"},
    "合豐": {"url": "https://maps.app.goo.gl/b66HTVSUm5P4GSFJA", "lat": "23.4598740", "lng": "120.4716174"},
    "福音": {"url": "https://maps.app.goo.gl/VwFLjN7D4ZMe6izU7", "lat": "23.4872063", "lng": "120.4290112"},
    "國鼎": {"url": "https://maps.app.goo.gl/3NQ6BAyiqptnK1Hg9", "lat": "23.4742160", "lng": "120.4252983"},
    "駿吉": {"url": "https://maps.app.goo.gl/6RhQTJeCHoLTDmbA7", "lat": "23.4973088", "lng": "120.4616285"},
    "鴻元": {"url": "https://maps.app.goo.gl/JUvswbP5Rnz5GNRA8", "lat": "23.4908363", "lng": "120.4388773"},
    "鴻興": {"url": "https://maps.app.goo.gl/knVB6MT42kLuoJqz7", "lat": "23.4488769", "lng": "120.4130188"},
    "東光": {"url": "https://maps.app.goo.gl/ymycaeiK7ApPvmz76", "lat": "23.4666069", "lng": "120.4582177"},
    "肚臍": {"url": "https://maps.app.goo.gl/JxqpEVxnCRQ71Ds18", "lat": "23.4806531", "lng": "120.4177952"},
    "林岳欽": {"url": "https://maps.app.goo.gl/H5mRbm1guMzkCYzy9", "lat": "23.5001389", "lng": "120.3664722"},
    "宏昇": {"url": "https://maps.app.goo.gl/8FN41dTXGEsmf3oT8", "lat": "23.4640312", "lng": "120.2706579"},
    "展慶": {"url": "https://maps.app.goo.gl/cJrUS5PsmZ5WzY3r7", "lat": "23.4413048", "lng": "120.4190961"},
    "河南": {"url": "https://maps.app.goo.gl/UJ7E88Q5uNuYSEb77", "lat": "23.4766319", "lng": "120.4362883"},
    "嘉義輪胎": {"url": "https://maps.app.goo.gl/LJk6zpRgt1oDZU9K6", "lat": "23.4890107", "lng": "120.4434237"},
    "明昌": {"url": "https://maps.app.goo.gl/VA3fjvooiHnkaGPx9", "lat": "23.5127738", "lng": "120.5468198"},
    "進興": {"url": "https://maps.app.goo.gl/ztZfmE1GyWHKSftYA", "lat": "23.4855212", "lng": "120.5558662"},
    "慶順": {"url": "https://maps.app.goo.gl/Hbh8sqp4RMmuwFWy6", "lat": "23.4817629", "lng": "120.5601896"},
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
    user_message = event.message.text

    # 多店查詢
    found_locations = [name for name in location_map if name in user_message]

    if "導航" in user_message:
        if found_locations:
            links = []
            coords = []
            for loc in found_locations:
                info = location_map[loc]
                links.append(f"{loc}：{info['url']}")
                coords.append(f"{info['lat']},{info['lng']}")

            # Google Maps 路線串接（從目前位置開始）
            route_url = "https://www.google.com/maps/dir/current+location/" + "/".join(coords)

            reply = "\n".join(links) + "\n\n🚗 路線規劃：\n" + route_url + \
                    "\n\n⚠️ 提醒：如果顯示『放置圖釘』，請按『開始導航』才會以你目前位置為起點。"
        else:
            reply = "⚠️ 請輸入有效的店名，例如：國順 義和"

    elif found_locations:
        replies = []
        for loc in found_locations:
            info = location_map[loc]
            replies.append(f"{loc} 導航：{info['url']}")
        reply = "\n".join(replies)
    else:
        reply = "⚠️ 請輸入有效的店名，例如：國順 義和"

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
