# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.clock import Clock
import socket
import threading


class PhoneToPcLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10

        # Заголовок
        self.add_widget(Label(
            text='Отправка текста на ПК',
            size_hint_y=None,
            height=40,
            font_size='20sp'
        ))

        # Поле ввода IP сервера (БЕЗ input_filter='str' — это баг Kivy 2.3.1)
        self.ip_input = TextInput(
            hint_text='IP адрес ПК (например: 192.168.1.100)',
            text='192.168.1.100',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        self.add_widget(self.ip_input)

        # Поле ввода порта (input_filter='int' работает нормально)
        self.port_input = TextInput(
            hint_text='Порт (по умолчанию 5000)',
            text='5000',
            multiline=False,
            size_hint_y=None,
            height=40,
            input_filter='int'
        )
        self.add_widget(self.port_input)

        # Поле ввода сообщения
        self.message_input = TextInput(
            hint_text='Введите сообщение...',
            multiline=True,
            size_hint_y=1
        )
        self.add_widget(self.message_input)

        # Кнопка отправки
        self.send_button = Button(
            text='Отправить',
            size_hint_y=None,
            height=60
        )
        self.send_button.bind(on_press=self.send_message)
        self.add_widget(self.send_button)

    def send_message(self, instance):
        ip = self.ip_input.text.strip()
        port_text = self.port_input.text.strip()
        message = self.message_input.text.strip()

        if not ip:
            self.show_popup('Ошибка', 'Введите IP адрес ПК')
            return
        if not port_text.isdigit():
            self.show_popup('Ошибка', 'Введите корректный порт')
            return
        if not message:
            self.show_popup('Ошибка', 'Введите сообщение')
            return

        port = int(port_text)

        # Блокируем кнопку на время отправки
        self.send_button.disabled = True
        self.send_button.text = 'Отправка...'

        # Отправка в отдельном потоке, чтобы не блокировать UI
        threading.Thread(
            target=self._send_thread,
            args=(ip, port, message),
            daemon=True
        ).start()

    def _send_thread(self, ip, port, message):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((ip, port))
            sock.sendall(message.encode('utf-8'))
            sock.close()

            # Успех — очищаем поле и возвращаем кнопку
            Clock.schedule_once(lambda dt: self._on_success())
        except socket.timeout:
            Clock.schedule_once(
                lambda dt: self.show_popup('Ошибка', 'Тайм-аут подключения')
            )
            Clock.schedule_once(lambda dt: self._reset_button())
        except ConnectionRefusedError:
            Clock.schedule_once(
                lambda dt: self.show_popup('Ошибка', 'Сервер отклонил подключение.\nЗапущен ли server.py на ПК?')
            )
            Clock.schedule_once(lambda dt: self._reset_button())
        except OSError as e:
            Clock.schedule_once(
                lambda dt: self.show_popup('Ошибка', f'Сетевая ошибка:\n{str(e)[:80]}')
            )
            Clock.schedule_once(lambda dt: self._reset_button())
        except Exception as e:
            Clock.schedule_once(
                lambda dt: self.show_popup('Ошибка', f'Неизвестная ошибка:\n{str(e)[:80]}')
            )
            Clock.schedule_once(lambda dt: self._reset_button())

    def _on_success(self):
        self.message_input.text = ''
        self.send_button.text = 'Отправить ✓'
        self.send_button.disabled = False
        # Возвращаем обычный текст через секунду
        Clock.schedule_once(lambda dt: setattr(self.send_button, 'text', 'Отправить'), 1)

    def _reset_button(self):
        self.send_button.text = 'Отправить'
        self.send_button.disabled = False

    def show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.8, 0.4)
        )
        popup.open()


class PhoneToPcApp(App):
    def build(self):
        self.title = 'Phone → PC Console'
        return PhoneToPcLayout()


if __name__ == '__main__':
    PhoneToPcApp().run()