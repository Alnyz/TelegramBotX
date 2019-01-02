# -*- coding: utf-8 -*-
@bot.message_handler(func=lambda msg: True, content_types=['text'])
def banned(messages):
	for message in messages:
		msg = message
		if msg.text is None:
			return
		text = msg.text.lower()
		if msg.chat.type in ["group","supergroup"]:
			get_admin = bot.get_chat_administrators(msg.chat.id)
			admin = [x.user.id for x in get_admin]
			is_bot = bot.get_me().id
			if text.startswith("kick") or text.startswith("/kick"):
				if msg.reply_to_message:
					if msg.from_user.id in admin and is_bot in admin:
						id = msg.reply_to_message.from_user.id
						name = msg.reply_to_message.from_user.first_name
						sp = text.split(None,1)
						if id in admin:
							bot.reply_to(msg,"Cannot Banned administrator")
						else:
							ret = {
									str(msg.chat.id):{
											"user_ban":{
												name:id
												}
										}
								}
							if str(msg.chat.id) not in DATA["data_group"]:
								DATA["data_group"].update(ret)
								backupjson()
							else:
								DATA["data_group"][str(msg.chat.id)]["user_ban"].update({name:id})
								backupjson()
							date = datetime.now() + timedelta(minutes=11)
							now = datetime.now()
							if len(sp) == 1:
								bot.reply_to(msg,f"This user was getting banned {timeago.format(date,now)}")
								bot.kick_chat_member(msg.chat.id,id,until_date=date)
							if len(sp) >= 2:
								dtime = datetime.now() + timedelta(minutes=int(sp[1]))
								bot.reply_to(msg,f"This user was getting banned {timeago.format(dtime,now)}")
								bot.kick_chat_member(msg.chat.id,id,dtime)
					else:
						bot.reply_to(msg,NO_ACCESS)
				else:
					bot.reply_to(msg,BANNED_HELP,parse_mode="Markdown")
			if text.startswith("banlist") or text.startswith("/banlist"):
				if str(msg.chat.id) not in DATA["data_group"] or DATA["data_group"][str(msg.chat.id)]["user_ban"] == {}:
					bot.reply_to(msg,f"Banned at *{msg.chat.title}*\nEmpty!",parse_mode="Markdown")
				else:
					txt = f"Banned at *{msg.chat.title}*\n"
					no = 0
					for x,y in DATA["data_group"][str(msg.chat.id)]["user_ban"].items():
						no += 1
						txt+=f"{no}. [{x}](tg://user?id={y})\n"
					bot.reply_to(msg,txt,parse_mode="Markdown")
			if text.startswith("unban") or text.startswith("/unban"):
				if msg.from_user.id in admin:
					sp = text.split(None,1)
					if len(sp) == 1:
						bot.reply_to(msg,BANNED_HELP,parse_mode="Markdown")
					else:
						data = DATA["data_group"][str(msg.chat.id)]["user_ban"]
						lists = list()
						ids = list()
						for i in data:
							lists.append(data[i])
							ids.append(i)
						try:
							bot.unban_chat_member(msg.chat.id,lists[int(sp[1]) - 1])
							bot.reply_to(msg,f"[{ids[int(sp[1]) - 1]}](tg://user?id={lists[int(sp[1]) - 1]}) Deleted",parse_mode="Markdown")
							data.pop(ids[int(sp[1]) - 1])
							backupjson()
						except (IndexError, ValueError):
							return
			
bot.set_update_listener(banned)