#sin libreria: http://konrad.foerstner.org/kokoko/using-python-to-send-messages-to-an-onesocialweb-server/
#con libreria: http://sleekxmpp.com/getting_started/sendlogout.html
#Asíncrona: https://stackoverflow.com/questions/17791783/sleekxmpp-send-a-message-at-will-and-still-listen-for-incoming-messages/25620054

import slixmpp

class Client(slixmpp.ClientXMPP):

    def __init__(self, jid, password):
        super().__init__(jid, password)

        # start event
        self.add_event_handler('session_start', self.start)
        # message event
        self.add_event_handler('message', self.message)

    def start(self, event):
        # <presence />
        self.send_presence()
        # <iq type=get>
        #   <query xmlns="data:iq:rooster" />
        # </iq>
        self.get_roster()

    def message(self, msg):
        if msg['type'] in ('normal', 'chat'):
            # Do something
            print(msg['body'])
        else:
            # Error
            print('Error')
            print(msg['body'])

