from kivy.app import App
from kivy.clock import mainthread
from kivy.core.window import Window
from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from client import Client

Window.softinput_mode = 'below_target'


class Signal(EventDispatcher):
    def __init__(self, **kwargs):
        self.register_event_type('on_trigger')
        super(Signal, self).__init__(**kwargs)

    def emit(self, value):
        # when do_something is called, the 'trigger' event will be
        # dispatched with the value
        self.dispatch('on_trigger', value)

    def on_trigger(self, *args):
        pass


class Dialog(TextInput):
    def keyboard_on_textinput(self, window, text):
        pass

    def set_bottom_text(self):
        pass
    # add a way to push the text to down of the window


class Texter(TextInput):
    pass


class SocketExpress(Widget):
    message_signal = Signal()
    history = ObjectProperty(None)
    out_text = ObjectProperty(None)
    send_button = ObjectProperty(None)

    def __init__(self):
        super(SocketExpress, self).__init__()
        self.client = Client(self.message_signal)
        self.client.address = ("192.168.1.12", 7979)
        self.message_signal.bind(on_trigger=self.recv_text)

        self.out_text.keyboard_on_key_down = self._on_enter_pressed

        self.send_button.bind(on_press=self.send_message)
        self.client.start()

    def _on_enter_pressed(self, window, keycode, text, modifiers):
        if keycode[1] == "enter" and "shift" not in modifiers:
            self.send_message(self.out_text)
        else:
            Texter.keyboard_on_key_down(
                self.out_text, window, keycode, text, modifiers
            )

    def send_message(self, instance):
        if self.out_text.text:
            text = f"[{self.client.name}] {self.out_text.text}\n"
            self.out_text.text = ''
            self._update_dialog(text)
            self.client.send_message(text)

    def recv_text(self, instance, text):
        self._update_dialog(text)

    @mainthread
    def _update_dialog(self, text):
        history = self.history.text
        dialog = f"{history}{text}"
        self.history.text = dialog
        self.history.set_bottom_text()

    def __del__(self):
        self.client.is_running = False


class SEApp(App):
    def build(self):
        return SocketExpress()


if __name__ == '__main__':
    SEApp().run()
