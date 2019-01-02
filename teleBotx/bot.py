#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, time, json, re
import telebot, traceback
import timeago
from datetime import datetime, timedelta
from telebot import *
from telebot.types import *
try:
    from importlib import reload 
except ImportError:
    from imp import reload
    
reload(sys)

with open("config.py","r") as fp: 
	exec(compile(open(fp.name).read(), fp.name, "exec"))
with open("backup.json","r", encoding="utf-8") as fo:
	DATA = json.load(fo)

#== RUN THE BOT ==#
bot = TeleBot(TOKEN, skip_pending=True, num_threads=4)
try:
	for plugin in enabled_plugins:
		with open("command/"+plugin+".py", "r") as foo:
			exec(compile(open(foo.name).read(), foo.name, "exec"))
			print(f"Enabled plugin {plugin} [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
except:
	print(traceback.format_exc())
def backupjson():
	with open("backup.json","w") as fp:
		return json.dump(DATA, fp, indent=4)
def handler_error():
	return print(traceback.format_exc())
	
bot.polling(True)