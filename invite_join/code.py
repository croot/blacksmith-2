# coding: utf-8

#  BlackSmith mark.2
exp_name = "invite_join" # /code.py v.x5
#  Id: 08~4b
#  Code © (2009-2012) by WitcherGeralt [alkorgun@gmail.com]

expansion_register(exp_name)

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	def Chat_check(self, conf):
		Numb = itypes.Number()
		while Chats.has_key(conf):
			if Chats[conf].IamHere != None:
				break
			time.sleep(.4)
			if Numb.plus() >= 50:
				break

	def get_invite(self, stanza, isConf, ltype, source, body, isToBs, disp):
		if not isConf and "normal" == stanza.getType():
			conf = source[1].lower()
			if conf.count("@") and conf.count(".") >= 2:
				for Node in stanza.getTags("x", namespace = xmpp.NS_MUC_USER):
					for Node in Node.getTags("invite"):
						inst = (Node.getAttr("from"))
						if inst:
							inst = (inst.split(chr(47)))[0].lower()
							if enough_access(inst, None, 7):
								confname = dynamic % (conf)
								if not check_nosimbols(confname):
									confname = encode_filename(confname)
								if not os.path.exists(confname):
									try:
										os.makedirs(confname, 0755)
									except:
										confname = None
								if confname:
									codename, disp_, cPref, nick, body = None, None, None, DefNick, Node.getTagData("reason")
									if body:
										ls = body.split()
										while ls:
											x = ls.pop()
											if x.startswith("1="):
												x = x.split("1=", 1)
												if len(x) == 2 and x[1]:
													x = x[1].lower()
													if Clients.has_key(x):
														disp_ = x
											elif x.startswith("2="):
												x = x.split("2=", 1)
												if len(x) == 2 and x[1]:
													if len(x[1]) <= 16:
														nick = x[1]
											elif x.startswith("3="):
												x = x.split("3=", 1)
												if len(x) == 2 and x[1]:
													if x[1] in cPrefs:
														cPref = x[1]
											elif x.startswith("4="):
												x = x.split("4=", 1)
												if len(x) == 2 and x[1]:
													codename = x[1]
									if GodName != inst:
										delivery(ControlAnsBase[0] % (inst, inst, conf))
									if not disp_:
										disp_ = IdleClient()
									Chats[conf] = sConf(conf, disp_, codename, cPref, nick)
									Chats[conf].load_all()
									Chats[conf].join()
									self.Chat_check(conf)
									if Chats.has_key(conf) and Chats[conf].IamHere:
										Msend(conf, ControlAnsBase[7] % (ProdName, inst), disp_)
									else:
										Chats[conf].full_leave()
							else:
								confname = dynamic % (conf)
								if not check_nosimbols(confname):
									confname = encode_filename(confname)
								if not os.path.exists(confname):
									try:
										os.makedirs(confname, 0755)
									except:
										confname = None
								if confname:
									if conf.endswith("@conference.qip.ru"):
										cls = dict()
										for dp in Clients.keys():
											if online(dp) and dp.endswith("@qip.ru"):
												cls[dp] = 0
										for conf in Chats.keys():
											dp = Chats[conf].disp
											if cls.has_key(dp):
												cls[dp] += 1
										if cls:
											idle = min(cls.values())
											for dp, chats in cls.items():
												if chats == idle:
													disp_ = dp
													break
										else:
											disp_ = None
									else:
										disp_ = IdleClient()
									if disp_:
										if GodName != inst:
											delivery(ControlAnsBase[0] % (inst, inst, conf))
										Chats[conf] = sConf(conf, disp_)
										Chats[conf].load_all()
										Chats[conf].join()
										self.Chat_check(conf)
										if Chats.has_key(conf):
											if Chats[conf].IamHere:
												Msend(conf, ControlAnsBase[7] % (ProdName, inst), disp_)
											else:
												Chats[conf].full_leave()
							break

	handlers = ((get_invite, "01eh"),)
