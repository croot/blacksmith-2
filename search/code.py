# coding: utf-8

#  BlackSmith mark.2
exp_name = "search" # /code.py v.x1
#  Id: 33~1b
#  Code © (2012) by WitcherGeralt [alkorgun@gmail.com]

expansion_register(exp_name)

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	busy = False
	date = 0

	CharsCY = "етуоранкхсвм".decode("utf-8")
	CharsLA = "etyopahkxcbm"

	eqMap = tuple([(CharsCY[numb], char) for numb, char in enumerate(CharsLA)])

	del CharsCY, CharsLA

	def command_disco_search(self, ltype, source, body, disp):
		if body:
			body = body.split(None, 1)
			if len(body) == 2:
				if not self.busy:
					self.busy = True
					self.date = time.time()
					Answer(self.AnsBase[0], ltype, source, disp)
					server, body = body
					server, body = server.lower(), body.lower()
					chats = itypes.Number()
					count = []
					iq = xmpp.Iq(to = server, typ = Types[10])
					iq.addChild(Types[18], {}, [], xmpp.NS_DISCO_ITEMS)
					iq.setID("Bs-i%d" % Info["outiq"].plus())
					CallForResponse(disp, iq, self.answer_disco_search_start, {"chats": chats, "count": count, "ltype": ltype, "source": source, "body": sub_desc(body, self.eqMap)})
					for x in xrange(600):
						time.sleep(0.2)
						if not self.busy:
							answer = self.AnsBase[1] % server
							break
					else:
						self.busy = False
						if count:
							Message(source[0], self.AnsBase[2] % (chats._str(), len(count), enumerated_list(sorted(count)[:96])), disp)
						else:
							answer = self.AnsBase[3] % chats._str()
				else:
					answer = self.AnsBase[4] % Time2Text(120 - (time.time() - self.date))
			else:
				answer = AnsBase[2]
		else:
			answer = AnsBase[1]
		if locals().has_key(Types[12]):
			Answer(answer, ltype, source, disp)

	def answer_disco_search_start(self, disp, stanza, chats, count, ltype, source, body):
		if xmpp.isResultNode(stanza):
			cls = [dr for dr in Clients.values() if dr.isConnected()] or [disp]
			cllen = len(cls)
			control = lambda numb: (numb if numb < cllen else 0)
			iters = 0
			for node in stanza.getQueryChildren():
				if not self.busy:
					break
				if node and node != "None":
					chat = node.getAttr("jid")
					if chat:
						iq = xmpp.Iq(to = chat, typ = Types[10])
						iq.addChild(Types[18], {}, [], xmpp.NS_DISCO_ITEMS)
						iq.setID("Bs-i%d" % Info["outiq"].plus())
						iters = control(iters + 1)
						CallForResponse(cls[iters], iq, self.answer_disco_search, {"chats": chats, "count": count, "chat": chat, "body": body})
						time.sleep(0.12)
		else:
			self.busy = False

	def answer_disco_search(self, disp, stanza, chats, count, chat, body):
		if self.busy and xmpp.isResultNode(stanza):
			chats.plus()
			for node in stanza.getQueryChildren():
				if node and node != "None":
					name = node.getAttr("name")
					if name and body in sub_desc(name.lower(), self.eqMap):
						count.append("%s (%s)" % (chat, name))

	commands = ((command_disco_search, "find", 2,),)
