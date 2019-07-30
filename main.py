import sys
import logging
import getpass
import sleekxmpp
import time
import ssl

from optparse import OptionParser
from sleekxmpp.exceptions import IqError, IqTimeout
from menu import *

class EchoBot(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password, optmen):

        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        #Evento de start
        print("The option is: ", optmen)
        if(optmen == 1): 
          self.add_event_handler("session_start", self.start)
          self.add_event_handler("register", self.register)
        elif(optmen == 2):
          self.add_event_handler("session_start", self.start)
          self.add_event_handler("message", self.message)
  

    #Process event: session_start
    def start(self, event):
        print('Session start')
        self.send_presence()
        self.get_roster()

    #Receive message
    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            msg.reply("Sent\n%(body)s" % msg).send()
            print(msg)

    def register(self, iq):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password
        try:
            resp.send(now=True)
            logging.info("Register succesfull: %s!" % self.boundjid)
        except IqError as e:
            logging.error("Error: unable to register %s" %
                    e.iq['error']['text'])
            self.disconnect()
        except IqTimeout:
            logging.error("Error: no response from server")
            self.disconnect()

    #Get all users and print them
    def get_users(self):
        print(self.get_roster())

    def delete_user(self):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['from'] = self.boundjid.user
        resp['register'] = ' '
        resp['register']['remove'] = ' '
        try:
            resp.send(now=True)
            print("Account deleted for %s!" % self.boundjid)
        except IqError as e:
            logging.error("Could not delete account: %s" %
                    e.iq['error']['text'])
            self.disconnect()
        except IqTimeout:
            logging.error("No response from server.")
            self.disconnect()
    

if __name__ == '__main__':
    optp = OptionParser()

    #Verbose
    optp.add_option('-q', '--quiet', help='set logging to ERROR',
                    action='store_const', dest='loglevel',
                    const=logging.ERROR, default=logging.INFO)
    optp.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)
    optp.add_option('-v', '--verbose', help='set logging to COMM',
                    action='store_const', dest='loglevel',
                    const=5, default=logging.INFO)

    #Information: jid, password, to, message
    optp.add_option("-j", "--jid", dest="jid",
                    help="JID to use")
    optp.add_option("-p", "--password", dest="password",
                    help="password to use")
    optp.add_option("-t", "--to", dest="to",
                    help="JID to send the message to")
    optp.add_option("-m", "--message", dest="message",
                    help="message to send")

    opts, args = optp.parse_args()

    #Login
    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')

    """
    if opts.jid is None:
        opts.jid = input("Username: ")
    if opts.password is None:
        opts.password = getpass.getpass("Password: ")
    if opts.to is None:
        opts.to = input("Send To: ")
    if opts.message is None:
        opts.message = input("Message: ")
    """

    optmen = int(menu())

    opts.jid = input("Username: ")
    opts.password = getpass.getpass("Password: ")

    xmpp = EchoBot(opts.jid, opts.password, optmen)
    
    #Register plugins
    xmpp.register_plugin('xep_0004') # Data forms
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0045') # Multichat
    xmpp.register_plugin('xep_0060') # PubSub
    xmpp.register_plugin('xep_0066') # Out-of-band Data
    xmpp.register_plugin('xep_0077') # In-band Registration
    xmpp.register_plugin('xep_0199') # Ping
    xmpp['xep_0077'].force_registration = True

    #Server connection
    #if xmpp.connect():
    if xmpp.connect(('alumchat.xyz', 5222)):
        xmpp.process(block=False) #True or false? 
        while(1): 
            choice = int(menu_in())
            if(choice == 1):
                print("Contacts: \n")
                print(xmpp.client_roster) 
                """
                i = 0 
                y = 0
                for i in range (len(xmpp.client_roster)):
                    print(xmpp.client_roster[i][y])
                    i = i + 1
                """
            elif(choice == 2):
                new_contact = input("username: \n")
                xmpp.send_presence(pto = new_contact, ptype ='subscribe')
            elif(choice == 6): 
                print("See you later")
                xmpp.disconnect()
                break
            else: 
                print("Invalid option")
       
    else:
        print("Unable to connect :(")
