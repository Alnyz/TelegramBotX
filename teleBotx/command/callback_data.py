# -*- coding: utf-8 -*-
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
	chatIds = call.message.chat.id
	msgIds = call.message.message_id
	from_   = call.message.from_user.id
	ids        =  call.id
	reply_from = call.from_user.id
	get_admin = bot.get_chat_administrators(chatIds)
	admins = [x.user.id for x in get_admin]
	if call.data == "verified" and reply_from in DATA["user_join"]:
		bot.restrict_chat_member(chatIds,reply_from,can_send_messages=True)
		bot.delete_message(chatIds,msgIds)
		DATA['user_join'].remove(reply_from)
		backupjson()
	if call.data == "default_yes" and reply_from in DATA["data_group"][str(chatIds)]["admin"]:
		ret = {
				"user_ban":{},
				"white_list":{},
				"options":{"restricted":False,"anti_link":False},
				"admin":admins
			}
		DATA["data_group"][str(chatIds)].update(ret)
		backupjson()
		try:
			bot.edit_message_text(f"Current status:\n{json.dumps(ret,indent=4)}",chatIds,msgIds)
		except:pass
	if call.data == "default_no" and reply_from in DATA["data_group"][str(chatIds)]["admin"]:
		try:
			text = f"Operation cancelled\nby ~[{call.from_user.first_name}](tg://user?id={reply_from})"
			bot.edit_message_text(text,chatIds,msgIds,parse_mode="Markdown")
		except:pass
	if call.data == "update_status_yes" and reply_from in admins:
		try:
			bot.edit_message_text(update_status(call.message),chatIds,msgIds)
		except:pass