"""Script to push IRC message to a RCON server"""
import sys
import configparser
import irc.bot
import irc.strings
from MCRcon import mcrcon
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr

class IrcRconBot(irc.bot.SingleServerIRCBot):
    def __init__(self, config):
        self.config = config
        irc.bot.SingleServerIRCBot.__init__(self, [(config['irc']['Host'], config.getint('irc', 'Port'), config['irc']['Password'])], config['irc']['Nickname'], config['irc']['Nickname'])
        self.channel = config['irc']['Channel']
        self.rcon = mcrcon.MCRcon()
        self.rcon.connect(config['rcon']['Host'], config.getint('rcon', 'Port'))
        self.rcon.login(config['rcon']['Password'])

    def on_nicknameinuse(self, c, e):
        print('IRC : Nickname already in use.')
        c.nick(c.get_nickname() + '_')

    def on_welcome(self, c, e):
        print('IRC : Connected successfully.')
        c.join(self.channel)

    def on_privmsg(self, c, e):
        pass

    def on_pubmsg(self, c, e):
        if self.config.getboolean('irc', 'TwitchUsernameFilter'):
            emit_username = e.source.split('!', 1)[0]
        else:
            emit_username = e.source
        print( emit_username, e.arguments[0])
        self.rcon.command(self.config['rcon']['CommandToCallOnMessage'] + ' ' + self.config['rcon']['MessagePrefix'] + emit_username + ' ' + e.arguments[0])
        return
    def on_join(self, c, e):
        print( 'User ',e.source, e.target, e.arguments, ' join our channel.')
        return

def main(argv):
    """Main entry point for the script."""
    config = configparser.ConfigParser()
    config.read(argv[0])
    bot = IrcRconBot(config)
    bot.start()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
