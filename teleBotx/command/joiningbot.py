# -*- coding: utf-8 -*-
def bot_join(messages):
	for message in messages:
		msg = message
		is_bot = bot.get_me().id
		get_admin = bot.get_chat_administrators(msg.chat.id)
		admin = [x.user.id for x in get_admin]
		if msg.content_type == "new_chat_members" and msg.new_chat_member.id == is_bot:
			if str(msg.chat.id) not in DATA["data_group"]:
				ret = {
							str(msg.chat.id):{
									"user_ban":{},
									"white_list":{},
									"options":{"restricted":False,"anti_link":False},
									"admin":admin
							}
						}
				DATA["data_group"].update(ret)
				backupjson()
				
def update_config(messages):
	for message in messages:
		msg = message
		admin = bot.get_chat_administrators(msg.chat.id)
		is_admin = [x.user.id for x in admin]
		if msg.content_type == "text" and msg.chat.type in ["group","supergroup"] and msg.from_user.id in is_admin:
			text = msg.text.lower()
			if text.startswith("default") or text.startswith("/default"):
				mrk = InlineKeyboardMarkup()
				mrk.add(InlineKeyboardButton("Yes",callback_data="default_yes"),
							  InlineKeyboardButton("Hell no!",callback_data="default_no"))
				bot.send_message(msg.chat.id,RESET_STATUS,reply_markup=mrk,parse_mode="Markdown")
			if text.startswith("status") or text.startswith("/status"):
				if str(msg.chat.id) not in DATA["data_group"]:
					mrk = InlineKeyboardMarkup()
					mrk.add(InlineKeyboardButton("Update!",callback_data="update_status_yes"),
								  InlineKeyboardButton("Not now",callback_data="update_status_no"))
					bot.reply_to(msg,"Sorry no have current data from this group,please update status of this group!",reply_markup=mrk)
				else:
					bot.reply_to(msg,json.dumps(DATA["data_group"][str(msg.chat.id)], indent=4))

def update_status(msg):
	if msg.content_type == "text" and msg.chat.type in ["group","supergroup"]:
		get_admin = bot.get_chat_administrators(msg.chat.id)
		admin = [x.user.id for x in get_admin]
		ret = {
					str(msg.chat.id):{
							"user_ban":{},
							"white_list":{},
							"options":{"restricted":False,"anti_link":False},
							"admin":admin
					}
				}
		DATA["data_group"].update(ret)
		backupjson()
		text = f"Status update!\n{json.dumps(ret,indent=4)}"
		bot.reply_to(msg,text)
	
bot.set_update_listener(update_config)
bot.set_update_listener(bot_join)