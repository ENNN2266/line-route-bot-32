@handler.add(MessageEvent, message=TextMessage)
def on_message(event):
    text = event.message.text.strip()
    reply_lines = []

    # 把輸入用空格拆開，例如 "國順 義和 旺泰 導航"
    parts = text.split()

    if not parts:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請輸入店名")
        )
        return

    # 判斷是否要做導航
    if "導航" in parts:
        # 移除「導航」關鍵字
        places = [p for p in parts if p != "導航"]

        if places:
            # Google Maps 多點路線
            url = "https://www.google.com/maps/dir/" + "/".join(places)
            reply_lines.append("依序路線導航：")
            reply_lines.append(url)
        else:
            reply_lines.append("請輸入要導航的店名")
    else:
        # 如果沒有導航，就回覆每個店的獨立連結
        for p in parts:
            url = f"https://www.google.com/maps/search/?api=1&query={p}"
            reply_lines.append(f"{p}：{url}")

    # 把回覆送出去
    line_bot_api.reply_message(
        event.reply_token,
        [TextSendMessage(text=line) for line in reply_lines]
    )
