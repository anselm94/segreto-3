from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from segreto.uix.widget import Toast
from kivy.clock import Clock


class LoginScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._show_loader(False)
        self.register_event_type('on_login')

    def _show_toast(self, text):
        self.ids['toast'].show(text)

    def _show_loader(self, show):
        if show:
            self.ids['loader'].opacity = 1.0
        else:
            self.ids['loader'].opacity = 0.0

    def try_login(self):
        self._show_loader(True)
        self.ids['grid'].disabled = True
        if self.ids['grid'].username is '':
            self.login_failure('Username is empty')
        elif self.ids['grid'].password is '':
            self.login_failure('Password is empty')
        else:
            self.dispatch('on_login')

    def login_failure(self, error):
        self._show_toast(error)
        self.ids['grid'].disabled = False
        self._show_loader(False)

    def on_login(self):
        pass


class LoginGrid(BoxLayout):
    username = ''
    password = ''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_login')

    def on_password(self, value):
        if len(value) > len(self.password):
            if not u"\u2022" in value[-1:]:
                self.password += value[-1:]
        elif len(value) < len(self.password):
            self.password = self.password[:(len(value) - len(self.password))]
        else:
            return
        self.ids['inp_password'].text = len(self.password) * u"\u2022"

    def on_username(self,value):
        self.username = value

    def on_disabled(self, instance, disabled):
        super().on_disabled(instance, disabled)
        if disabled:
            self.ids['inp_username'].hint_text = self.username
            self.ids['inp_password'].hint_text = len(self.password) * u"\u2022"
        else:
            self.ids['inp_username'].hint_text = 'Username'
            self.ids['inp_password'].hint_text = 'Password'

    def on_login(self):
        pass
