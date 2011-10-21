# coding: utf-8

#  BlackSmith mark.2
exp_name = "clear_stats" # /code.py v.x2
#  Id: 12~2a
#  Code © (2011) by WitcherGeralt [WitcherGeralt@rocketmail.com]

expansion_register(exp_name)

def join_clear(conf, nick, instance, role, disp):
	if instance:
		for obj in Chats[conf].get_users():
			if obj.source == instance and not obj.ishere and obj.nick != nick:
				if Chats[conf].isHere(obj.nick):
					Chats[conf].users.pop(obj.nick)

def exit_clear(conf, nick, status, scode, disp):
	instance = get_source(conf, nick)
	if instance:
		delete = False
		for obj in Chats[conf].get_users():
			if obj.source == instance and obj.ishere:
				delete = True
				break
		if delete and Chats[conf].isHere(nick):
			Chats[conf].users.pop(nick)

expansions[exp_name].funcs_add([join_clear, exit_clear])

handler_register(join_clear, "04eh", exp_name)
handler_register(exit_clear, "05eh", exp_name)
