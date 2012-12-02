# coding: utf-8

if DefLANG in ("RU", "UA"):
	AnsBase_temp = tuple([line.decode("utf-8") for line in (
		"Логгер выключен.", # 0
		"Логгер включен.", # 1
		"Логгер полностью отключен, эта команда не доступна.", # 2
		"Ничего не записано." # 3
					)])
else:
	AnsBase_temp = (
		"The logger is off.", # 0
		"The logger is on.", # 1
		"The logger is totally disabled, this command is unavailable.", # 2
		"Nothing was logged." # 3
					)