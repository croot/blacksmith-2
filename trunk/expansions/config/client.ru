система управления клиентами
клиент (удалить/добавить/пароль) (jid/хост) (аккаунт/пароль) (пароль/записать) (порт) (сервер)
*/клиент
бот покажет текущие настройки
*/клиент удалить bs@xmpp.ru
отключит клиент с jid`ом bs@xmpp.ru, при этом перезайдёт в комнаты за которыми закреплён этот jid с других клиентов
*/клиент добавить xmpp.ru bs xxx 5222 jabber.ru
запустит клиент с jid`ом bs@xmpp.ru (если хост равен серверу, его указывать необязательно, как и порт, если он равен 5222)
*/клиент пароль bs@xmpp.ru xxx
бот сменит пароль к jid`у (если не указать пароль бот сгеренирует его автоматически. при параметре "записать" после пароля, бот его запишет, даже если его не удастся сменить)