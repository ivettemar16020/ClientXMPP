import sys
import sleekxmpp

HOST = '@alumchat.xyz'
PORT = 5222

class myBot(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password):
        super(myBot, self).__init__(jid, password)

        self.add_event_handler('sign_in', self.signin)
        self.add_event_handler('out_message', self.out_message)
        self.add_event_handler('message', self.message)

    def signin(self, event):
        self.send_presence()
        self.get_roster()
    

    def out_message(self, recipient, message):
        self.message_info = message
        self.recipient_msg = recipient
        self.send_message(mto=self.recipient_msg, mbody=self.message_info)

    
    def message(self, message):
        print(message)
        message.reply("Hey you").send()

    def dissconect(self):
        self.disconnect(wait=True)

if __name__ == '__main__':
    user = input("username: ")
    password = input("password: ")

    xmpp = myBot(user + HOST, password)

    if xmpp.connect(address=HOST):
        print("CONNECTED")
        xmpp.process()
        # xmpp.disconnect()
    else:
        print("Error")