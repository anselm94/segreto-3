import os.path
from kivy.config import Config
Config.set('graphics', 'window_state', 'maximized')
Config.set('kivy', 'exit_on_escape', '0')
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SwapTransition
from segreto.uix.loginscreen import LoginScreen
from segreto.uix.ideascreen import IdeaScreen
from segreto.idea import IdeaCollection
import configparser
import threading
import jsonpickle
import simplecrypt
'''
The App implementation
'''


class SegretoApp(App):

    def build(self):
        self.icon = 'data/icon/segreto_icon.png' # Don't know why icon isn't set :(
        self.title = 'Segreto 3'
        self.init()
        return self.screenmanager

    def init(self):
        self.username = ''
        self.password = ''
        self.crypt_file_path = ''
        self.screenmanager = ScreenManager(transition=SwapTransition())
        self.loginscreen = LoginScreen(name='screen-login')
        self.loginscreen.bind(on_login=self.login)
        self.ideascreen = IdeaScreen(name='screen-idea')
        self.ideascreen.bind(on_quit_app=self.quit)
        self.screenmanager.add_widget(self.loginscreen)
        self.screenmanager.add_widget(self.ideascreen)
        self.screenmanager.current = 'screen-login'

    def encrypt_store_data(self, crypt_file_path, password, idea_collection):
        self.screenmanager.clear_widgets()
        ser_data = jsonpickle.encode(idea_collection)
        enc_data = simplecrypt.encrypt(password, ser_data)
        with open(crypt_file_path, 'wb') as f:
            f.write(enc_data)
        self.stop()

    def login(self, *args):
        uname = self.loginscreen.ids['grid'].username
        paswd = self.loginscreen.ids['grid'].password
        config = configparser.ConfigParser()
        config.read('settings.ini')
        for section in config.sections():
            username = config.get(section, 'username')
            if username == uname:
                self.crypt_file_path = config.get(section, 'file')
                self.username = uname
                with open(self.crypt_file_path, 'ab+') as f:
                    f.seek(0)
                    crypt_data = f.read()
                    if crypt_data == b'':
                        self.password = paswd
                        self.screenmanager.current = 'screen-idea'
                    else:
                        self.start_decrypt_thread(crypt_data, paswd)
        if self.username == '':
            self.loginscreen.login_failure('User not found')
            self.username = ''
            self.password = ''
            self.crypt_file_path = ''

    def decrypt_data(self, crypt_data, password):
        try:
            dec_data = simplecrypt.decrypt(password, crypt_data)
            self.password = password
            self.idea_collection = jsonpickle.decode(dec_data.decode('utf8'))
            self.ideascreen.set_idea_collection(self.idea_collection)
            self.screenmanager.current = 'screen-idea'
        except simplecrypt.DecryptionException:
            self.loginscreen.login_failure('Password error')
            self.username = ''
            self.password = ''
            self.crypt_file_path = ''

    def start_decrypt_thread(self, crypt_data, paswd):
        t = threading.Thread(target=self.decrypt_data,
                             args=(crypt_data, paswd))
        t.daemon = True
        t.start()

    def start_encrypt_thread(self, crypt_file_path, password, idea_collection):
        t = threading.Thread(target=self.encrypt_store_data, args=(
            crypt_file_path, password, idea_collection))
        t.daemon = True
        t.start()

    def quit(self, *args):
        idea_collection = self.ideascreen.idea_collection
        self.start_encrypt_thread(
            self.crypt_file_path, self.password, idea_collection)

    def on_pause(self):
        return True
