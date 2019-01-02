# -*- coding: utf-8 -*-
def msg_handler(messages):
	for message in messages:
		msg = message
		text = msg.text
		if msg is None or text is None:
			return
		else:
			return