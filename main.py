#!python
import kivy
kivy.require('1.10.0')
from kivy import platform
if platform!='android':
    from kivy.config import Config
    Config.set('graphics', 'show_cursor', '1')
    Config.set('kivy', 'log_level', 'warning')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import DictProperty,StringProperty
from kivy import metrics
try:
    from kivy.garden.xpopup import XError, XProgress, XAuthorization, XConfirmation
except:
    from xpopup import XError, XProgress, XAuthorization, XConfirmation

class AuthEx(XAuthorization):

    required_fields = DictProperty(
        {'login': 'Login', 'password': 'Password', 'host': 'Host'})
    host = StringProperty(u'')

    def _get_form(self):
        layout = super(AuthEx, self)._get_form()
        pnl = BoxLayout(size_hint_y=None, height=metrics.dp(28), spacing=5)
        pnl.add_widget(Label(text='Host:', halign='right',
                             size_hint_x=None, width=metrics.dp(80)))
        pnl.add_widget(TextInput(id='host', multiline=False, font_size=14,
                                 text=self.host))
        layout.add_widget(pnl)
        layout.add_widget(Widget())
        return layout

class AppMainUI(BoxLayout):
    # Auth properties
    login = StringProperty(u'')
    password = StringProperty(u'')
    host = StringProperty('')

    def __init__(self):
        super(AppMainUI, self).__init__()
        pkm = BoxLayout()
        pkm.add_widget(Button(text = 'start', on_press = self.get_command_start))
        self.add_widget(pkm)

    def _login_dismiss(self, instance):
        if instance.is_canceled():
            App.get_running_app().stop()
            return
        self.login = instance.get_value('login')
        self.password = instance.get_value('password')
        self.host = instance.get_value('host')

    def _get_auth(self):
        print 1

    def _send_request(self, url, success=None, error=None, params=None):
        print url

    def _login(self):
        AuthEx(login=self.login, password=self.password, host=self.host,
               autologin=None, pos_hint={'top': 0.99},
               on_dismiss=self._login_dismiss)
    def get_command_start(self):
        pass
    def start(self):
        if not self.login or not self.password or not self.host:
            self._login()


class AppMain(App):
    remote = None
    def build(self):
        config = self.config
        self.remote = AppMainUI()
        return self.remote
    def on_stop(self):
        self.config.write()
    def on_start(self):
        self.remote.start()

if __name__ == '__main__':
    AppMain().run()
