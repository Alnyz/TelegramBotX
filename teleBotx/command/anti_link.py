def anti_link(messages):
	for message in messages:
		msg = message
		if msg.content_type == "text" and msg.chat.type in ["group","supergroup"]:
			pattern = r"(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+"
			get_admin = bot.get_chat_administrators(msg.chat.id)
			bot_id = bot.get_me().id
			admin = [x.user.id for x in get_admin]
			match = re.findall(pattern,msg.text)
			if match and msg.from_user.id not in admin and msg.from_user.id != bot_id:
				if DATA["data_group"][str(msg.chat.id)]["options"]["anti_link"] == True:
					bot.delete_message(msg.chat.id,msg.message_id)
			else:
				return
			
def anti_link_trigger(messages):
	for message in messages:
		msg = message
		if msg.content_type == "text" and msg.chat.type in ["group","supergroup"]:
			text = msg.text.lower()
			if text.startswith("nolink") or text.startswith("/nolink"):
				sp = text.split(" ")
				if len(sp) == 1:
					bot.reply_to(msg,HELPER_NOLINK.format(DATA["data_group"][str(msg.chat.id)]["options"]["anti_link"]),parse_mode="Markdown")
				elif len(sp) > 1 and sp[1] == "on":
					if DATA["data_group"][str(msg.chat.id)]["options"]["anti_link"] == True:
						bot.reply_to(msg,"This function already enable.")
					else:
						DATA["data_group"][str(msg.chat.id)]["options"]["anti_link"] = True
						backupjson()
						bot.reply_to(msg,"Anti link set to Enable")
				elif len(sp) > 1 and sp[1] == "off":
					if DATA["data_group"][str(msg.chat.id)]["options"]["anti_link"] == False:
						bot.reply_to(msg,"This function already enable.")
					else:
						DATA["data_group"][str(msg.chat.id)]["options"]["anti_link"] = False
						backupjson()
						bot.reply_to(msg,"Anti link set to Disable")
		
bot.set_update_listener(anti_link_trigger)
bot.set_update_listener(anti_link)