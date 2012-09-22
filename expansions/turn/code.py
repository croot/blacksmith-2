# coding: utf-8

#  BlackSmith mark.2
exp_name = "turn" # /code.py v.x2
#  Id: 21~2b
#  Code © (2011) by WitcherGeralt [alkorgun@gmail.com]

expansion_register(exp_name)

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	TableRU = '''ёйцукенгшщзхъфывапролджэячсмитьбю.!"№;%:?*()_+/-=\ЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ.'''.decode("utf-8")
	TableEN = '''`qwertyuiop[]asdfghjkl;'zxcvbnm,./!@#;%^&*()_+.-=\~QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>/'''

	TurnBase = {}

	def command_turn(self, ltype, source, body, disp):
		
		def Turn(self, conf, body):
			desc = {}
			for nick in Chats[conf].get_nicks():
				if Chats[conf].isHereTS(nick):
					for x in (["%s%s" % (nick, Key) for Key in [":",",",">"]] + [nick]):
						if body.count(x):
							Numb = "*%s*" % str(len(desc.keys()) + 1)
							desc[Numb] = x
							body = body.replace(x, Numb)
			Turned = ""
			for x in body:
				if x in self.TableEN:
					Turned += self.TableRU[self.TableEN.index(x)]
				elif x in self.TableRU:
					Turned += self.TableEN[self.TableRU.index(x)]
				else:
					Turned += x
			return sub_desc(Turned, desc)
		
		if Chats.has_key(source[1]):
			if body:
				answer = "*\ %s" % Turn(source[1], body)
			else:
				source_ = get_source(source[1], source[2])
				if source_ and self.TurnBase[source[1]].has_key(source_):
					(Time, body) = self.TurnBase[source[1]].pop(source_)
					body = "Turn\->\n[%s] <%s>: %s" % (Time, source[2], Turn(self, source[1], body))
					Msend(source[1], body, disp)
				else:
					answer = AnsBase[7]
		else:
			answer = AnsBase[0]
		if locals().has_key(Types[12]):
			Answer(answer, ltype, source, disp)

	def collect_turnable(self, stanza, isConf, ltype, source, body, isToBs, disp):
		if isConf and ltype == Types[1] and source[2]:
			source_ = get_source(source[1], source[2])
			if source_:
				self.TurnBase[source[1]][source_] = (strTime("%H:%M:%S", False), body)

	def init_Turn_Base(self, conf):
		self.TurnBase[conf] = {}

	def edit_Turn_Base(self, conf):
		del self.TurnBase[conf]

	commands = ((command_turn, "turn", 1,),)

	handlers = (
		(init_Turn_Base, "01si"),
		(edit_Turn_Base, "04si"),
		(collect_turnable, "01eh")
					)
