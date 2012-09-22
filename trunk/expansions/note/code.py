# coding: utf-8

#  BlackSmith mark.2
exp_name = "note" # /code.py v.x5
#  Id: 22~4b
#  Code © (2010-2011) by WitcherGeralt [alkorgun@gmail.com]

expansion_register(exp_name)

class expansion_temp(expansion):

	def __init__(self, name):
		expansion.__init__(self, name)

	NoteFile = dynamic % ("notepad.db")

	def command_note(self, ltype, source, body, disp):
		source_ = get_source(source[1], source[2])
		if source_:
			if body:
				list_ = body.split()
				x = (list_.pop(0)).lower()
				if x in ("clear", "чисть".decode("utf-8")):
					with database(self.NoteFile) as db:
						db("select * from note where jid=?", (source_,))
						db_desc = db.fetchone()
						if db_desc:
							db("delete from note where jid=?", (source_,))
							db.commit()
							answer = AnsBase[4]
						else:
							answer = self.AnsBase[0]
				elif list_:
					if x == "+":
						body = body[2:].lstrip()
						if len(body) <= 512:
							date = strTime(local = False)
							with database(self.NoteFile) as db:
								db("select * from note where jid=?", (source_,))
								db_desc = db.fetchone()
								if db_desc:
									Numb = itypes.Number()
									for line in db_desc:
										if not line:
											db("update note set line_%s=? where jid=?" % (Numb._str()), ("[%s] %s" % (date, body), source_))
											db.commit()
											answer = self.AnsBase[7] % (Numb._str())
											break
										Numb.plus()
									else:
										answer = self.AnsBase[3]
								else:
									db("insert into note values (%s)" % (",".join(["?" for x in xrange(17)])), (source_, "[%s] %s" % (date, body), "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""))
									db.commit()
									answer = AnsBase[4]
						else:
							answer = self.AnsBase[1]
					elif x in ("-", "*"):
						Numb = list_.pop(0)
						if isNumber(Numb):
							Numb = int(Numb)
							if Numb in xrange(1, 17):
								with database(self.NoteFile) as db:
									db("select * from note where jid=?", (source_,))
									db_desc = db.fetchone()
									if db_desc:
										if x == "*":
											if db_desc[Numb]:
												answer = db_desc[Numb]
											else:
												answer = self.AnsBase[5]
										elif not db_desc[Numb]:
											answer = self.AnsBase[8]
										else:
											db("update note set line_%d=? where jid=?" % (Numb), ("", source_))
											db.commit()
											answer = AnsBase[4]
									else:
										answer = self.AnsBase[0]
							else:
								answer = self.AnsBase[4]
						else:
							answer = AnsBase[30]
					else:
						answer = AnsBase[2]
				else:
					answer = AnsBase[2]
			else:
				with database(self.NoteFile) as db:
					db("select * from note where jid=?", (source_,))
					db_desc = db.fetchone()
					if db_desc:
						Notes, Numb = str(), itypes.Number()
						for line in db_desc:
							if not Numb._int():
								Numb.plus()
								continue
							if line:
								Notes += "\nLine[%s] %s" % (Numb._str(), line)
							Numb.plus()
						if Notes:
							Notes = (self.AnsBase[6] % (Notes))
							if ltype == Types[1]:
								Answer(AnsBase[11], ltype, source, disp)
							Msend(source[0], Notes, disp)
						else:
							db("delete from note where jid=?", (source_,))
							db.commit()
							answer = self.AnsBase[0]
					else:
						answer = self.AnsBase[0]
		else:
			answer = self.AnsBase[2]
		if locals().has_key(Types[12]):
			Answer(answer, ltype, source, disp)

	def init_note_file(self):
		if not os.path.isfile(self.NoteFile):
			with database(self.NoteFile) as db:
				db("create table note (jid text, %s)" % (", ".join(["line_%s text" % (Numb) for Numb in xrange(1, 17)])))
				db.commit()

	commands = ((command_note, "note", 2,),)

	handlers = ((init_note_file, "00si"),)
