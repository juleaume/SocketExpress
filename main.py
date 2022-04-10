from kivy.app import App
from kivy.clock import mainthread
from kivy.event import EventDispatcher
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from client import Client


class Signal(EventDispatcher):
    def __init__(self, **kwargs):
        self.register_event_type('on_trigger')
        super(Signal, self).__init__(**kwargs)

    def emit(self, value):
        # when do_something is called, the 'trigger' event will be
        # dispatched with the value
        self.dispatch('on_trigger', value)

    def on_trigger(self, *args):
        print("I am dispatched", args)


class SocketExpress(Widget):
    message_signal = Signal()

    def __init__(self):
        super(SocketExpress, self).__init__()
        self.client = Client(self.message_signal)
        self.client.address = ("192.168.1.12", 7878)
        # self.message_signal.connect(
        #     lambda: self._update_dialog(self.client.message)
        # )

        self.message_signal.bind(on_trigger=self.recv_text)

        box = BoxLayout(orientation='vertical')
        box.size_hint = (None, None)
        box.width = 500
        box.height = 500
        self.history = TextInput()
        box.add_widget(self.history)
        send_box = BoxLayout()
        self.message = TextInput()
        send_box.add_widget(self.message)
        send_box.height = 200
        self.send_button = Button()
        self.send_button.text = "send"
        self.send_button.bind(on_press=self.send_message)
        send_box.add_widget(self.send_button)
        box.add_widget(send_box)
        self.add_widget(box)
        self.client.start()

    def send_message(self, instance):
        if self.message.text:
            text = f"[{self.client.name}] {self.message.text}\n"
            self.message.text = ''
            self._update_dialog(text)
            self.client.send_message(text)

    def recv_text(self, instance, text):
        self._update_dialog(text)

    @mainthread
    def _update_dialog(self, text):
        print("got text", text)
        history = self.history.text
        dialog = f"{history}{text}"
        self.history.text = dialog

    def __del__(self):
        self.client.is_running = False


class SEApp(App):
    def build(self):
        return SocketExpress()


if __name__ == '__main__':
    SEApp().run()
