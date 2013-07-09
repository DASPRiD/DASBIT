import os
from dasbit.core import Config

class Nickserv:
    help = "https://github.com/DASPRiD/DASBiT/wiki/nickserv-plugin"
    
    def __init__(self, manager):
        self.client = manager.client
        self.config = Config(os.path.join(manager.dataPath, 'nickserv'))
    
        manager.registerCommand('nickserv', 'register', 'nickserv-register', '(?P<password>[^ ]+) (?P<email_address>[^ ]+)', self.register)
        manager.registerCommand('nickserv', 'validate', 'nickserv-validate', '(?P<validation_code>[^ ]+)', self.validate)
        manager.registerCommand('nickserv', 'identify', 'nickserv-identify', '', self.identify)
        manager.registerCommand('nickserv', 'ghost',    'nickserv-ghost', '', self.ghost)
        manager.registerCommand('nickserv', 'release',  'nickserv-release', '', self.release)
        manager.registerCommand('nickserv', 'release',  'nickserv-set-password', '(?P<password>[^ ]+)', self.set_password)
        manager.registerCommand('nickserv', 'release',  'nickserv-set-nickname', '(?P<nickname>[^ ]+)', self.set_nickname)
        manager.registerCommand('nickserv', 'protect',  'nickserv-protect-nick', '', self.protect)
        manager.registerCommand('nickserv', 'auto-identify', 'nickserv-auto-identify', '(?P<flag>[^ ]+)', self.set_auto_identify)
        manager.registerNumeric('nickserv', [422, 376], self.connected)

    def register(self, source, password, email_address):
        self.config['password'] = password
        self.config['nickname'] = self.client.config['nickname'] # TODO: read current nick and store it here!
        self.config.save()
        self.client.sendPrivMsg('nickserv', 'register %s %s' % (password, email_address))
        self.client.reply(source, 'Registration sent, await email on %s and remember to validate me!' % email_address, 'notice')

    def validate(self, source, validation_code):
        self.client.sendPrivMsg('nickserv', 'verify register %s %s' % (self.client.config['nickname'], validation_code))
        self.client.reply(source, 'Validation sent', 'notice')

    def identify(self, source):
        if not 'password' in self.config:
            self.client.reply(source, 'Please save my password first', 'notice')
            return

        if not 'nickname' in self.config:
            self.client.reply(source, 'Please save my nickname first', 'notice')
            return

        self.send_identify(self.config['nickname'], self.config['password'])
        self.client.reply(source, 'I should now be identified, please check me with /whois', 'notice');

    def ghost(self, source):
        if not 'password' in self.config:
            self.client.reply(source, 'Please save my password first', 'notice')
            return
        if not 'nickname' in self.config:
            self.client.reply(source, 'Please save my nickname first', 'notice')
            return
        self.send_identify(self.config['nickname'], self.config['password'])
        self.client.sendPrivMsg('nickserv', 'ghost %s' % self.client.config['nickname'])
        self.client.sendPrivMsg('nickserv', 'release %s' % self.client.config['nickname'])
        self.client.send('NICK', self.client.config['nickname'], 50, 1)
        self.client.reply(source, 'I should now be back to my old self!', 'notice')

    def release(self, source):
        if not 'password' in self.config:
            self.client.reply(source, 'Please save my password first', 'notice')
            return
        if not 'nickname' in self.config:
            self.client.reply(source, 'Please save my nickname first', 'notice')
            return
        self.send_identify(self.config['nickname'], self.config['password'])
        self.client.sendPrivMsg('nickserv', 'release %s' % self.client.config['nickname'])
        self.client.sendPrivMsg('nickserv', 'release %s' % self.client.config['nickname'])
        self.client.send('NICK', self.client.config['nickname'], 50, 1)
        self.client.reply(source, 'I should now be back to my old self!', 'notice')

    def protect(self, source):
        self.client.sendPrivMsg('nickserv', 'set enforce on');
        self.client.reply(source, 'I have asked nickserv to protect me!', 'notice')

    def set_auto_identify(self, source, flag):
        if flag == 'On':
            self.config['autoidentify'] = 'On'
            self.client.reply(source, 'Enabled auto-identify', 'notice')
            return
        if flag == 'Off':
            self.config['autoidentify'] = 'Off'
            self.client.reply(source, 'Disabled auto-identify', 'notice')
            return
        self.client.reply(source, 'Invalid setting "%s" for auto-identify, value settings are "On" or "Off"' % flag    )

    def set_password(self, source, password):
        self.config['password'] = password
        self.client.reply(source, 'Nickserv Password saved', 'notice')
        self.config.save()

    def set_nickname(self, source, nickname):
        self.config['nickname'] = nickname
        self.client.reply(source, 'Nickserv nickname saved', 'notice')
        self.config.save()

    def send_identify(self, nick, password):
        self.client.sendPrivMsg('nickserv', 'identify %s %s' % (nick, password))

    def connected(self, message):
        if not 'autoidentify' in self.config:
            return

        if not 'password' in self.config:
            return

        if not 'nickname' in self.config:
            return

        if self.config['autoidentify'] == 'On':
            self.client.sendPrivMsg('nickserv', 'identify %s %s' % (self.config['nickname'], self.config['password']))
