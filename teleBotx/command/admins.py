@bot.message_handler(commands=["admin"])
def list_admin(to):
	if to.chat.type in ["group","supergroup"]:
		admins = bot.get_chat_administrators(to.chat.id)
		ret = f"_{to.chat.title.upper()}_ Admin's\n\n*Creator*\n"
		no = 0
		for res in reversed(admins):
			if res.status == "creator":
				ret+=f"~ [{res.user.first_name.strip(']')}](tg://user?id={res.user.id})" \
						"\n_Administrator_\n"
			if res.status == "administrator":
				no+=1
				ret+=f"{no}. [{res.user.first_name.strip(']')}](tg://user?id={res.user.id})\n"
		bot.reply_to(to,ret,parse_mode="Markdown")