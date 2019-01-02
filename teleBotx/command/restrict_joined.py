# -*- coding: utf-8 -*-
@bot.message_handler(func=lambda msg: True, content_types=["new_chat_members"])
def new_participant(to):
	try:
		if str(to.chat.id) not in DATA["data_group"]:
			pass
		elif DATA["data_group"][str(to.chat.id)]["options"]['restricted'] == True and to.new_chat_member.is_bot == False:
			uid = to.from_user.id
			get_admin = bot.get_chat_administrators(to.chat.id)
			bot_id = bot.get_me().id
			bot.restrict_chat_member(to.chat.id,to.from_user.id,can_send_messages=False)
			markup = InlineKeyboardMarkup()
			markup.add(InlineKeyboardButton("Verified", callback_data="verified"))
			DATA['user_join'].append(uid)
			backupjson()
			text = f"You've Restricted from this group.\nPlease verified" \
					" you're hooman by Clicking 'Verified'!"
			bot.reply_to(to,text,reply_markup=markup)
	except:
		handler_error()
	
@bot.message_handler(func=lambda msg: True, content_types=['text'])
def messages(message):
	try:
		msg = message
		text = msg.text.lower()
		if text is None:
			pass
		else:
			if msg.chat.type in ["supergroup","group"]:
				if text.startswith("restrict") or text.startswith("/restrict"):
					sp = text.split(" ")
					msgs = RESTRICTIONS.format(DATA["data_group"][str(msg.chat.id)]["options"]['restricted'])
					if len(sp) == 2:
						trigger_restrict(str(sp[1]),msg)
					elif len(sp) == 1 or len(sp) >= 3:
						bot.reply_to(msg,msgs,parse_mode="Markdown")
	except:
		handler_error()
def trigger_restrict(sp,to):
	try:
		get_admin = bot.get_chat_administrators(to.chat.id)
		bot_id = bot.get_me().id
		i = [x.user.id for x in get_admin]
		if to.from_user.id in i and bot_id in i:
			if sp == "on":
				DATA["data_group"][str(to.chat.id)]["options"]["restricted"] = True
				backupjson()
				bot.reply_to(to,f"Restricted set to on...")
			elif sp == "off":
				DATA["data_group"][str(to.chat.id)]["options"]["restricted"] = False
				backupjson()
				bot.reply_to(to,f"Restricted set to off...")
		else:
			bot.reply_to(to,"i've no access to do that,or u are not Admins in this group")
	except:handler_error()