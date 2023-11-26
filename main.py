# main.py

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import StringProperty
import requests
from kivy.uix.gridlayout import GridLayout

class AppScreen(Screen):
    def show_popup(self, title, content):
        box_layout = BoxLayout(orientation='vertical', padding=10)
        box_layout.add_widget(Label(text=content))
        ok_button = Button(text='OK', size_hint=(None, None), size=(100, 50))
        ok_button.bind(on_press=self.dismiss_popup)
        box_layout.add_widget(ok_button)
        popup = Popup(title=title, content=box_layout, size_hint=(None, None), size=(300, 200))
        popup.open()

    def dismiss_popup(self, instance):
        instance.parent.parent.dismiss()



class LoginScreen(AppScreen):
    username_input_text = StringProperty('')
    password_input_text = StringProperty('')

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        self.orientation = 'vertical'
        self.padding = 20

        self.logo = Image(source='black_taxi.jpg', size_hint_y=None, height=200)
        self.username_input = TextInput(
            hint_text='Username', multiline=False,
            size_hint=(None, None), height=30, width=200,
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            text=self.username_input_text
        )
        self.password_input = TextInput(
            hint_text='Password', password=True,
            multiline=False, size_hint=(None, None),
            height=30, width=200,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            text=self.password_input_text
        )
        self.login_button = Button(
            text='Login', on_press=self.login,
            size_hint=(None, None), height=30, width=100,
            pos_hint={'center_x': 0.5, 'center_y': 0.4}
        )
        self.result_label = Label(text='', size_hint_y=None, height=30)

        self.create_account_button = Button(
            text='Create Account', on_press=self.go_to_create_account,
            size_hint=(None, None), height=30, width=150,
            pos_hint={'center_x': 0.5, 'center_y': 0.3}
        )

        centering_layout = BoxLayout(orientation='vertical', spacing=10)
        centering_layout.add_widget(self.logo)
        centering_layout.add_widget(Label())
        centering_layout.add_widget(self.username_input)
        centering_layout.add_widget(self.password_input)
        centering_layout.add_widget(self.login_button)
        centering_layout.add_widget(self.create_account_button)

        self.add_widget(centering_layout)
        self.add_widget(self.result_label)

    def login(self,_):
        username = self.username_input_text
        password = self.password_input_text

        api_url = 'http://localhost:3000/api/login'
        data = {'username': username, 'password': password}

        try:
            response = requests.post(api_url, json=data)
            result = response.json()

            if result.get('success'):
                self.result_label.text = 'Login successful!'
                self.manager.current = 'calendar'
            else:
                self.show_popup('Wrong Login', 'Invalid username or password.')

        except requests.RequestException as e:
            print(f"Error connecting to the API: {e}")
            self.show_popup('Error', 'Failed to connect to the server.')


    def go_to_create_account(self, instance):
        self.manager.current = 'create_account'


class CreateAccountScreen(AppScreen):
    username_input_text = StringProperty('')
    password_input_text = StringProperty('')

    def __init__(self, **kwargs):
        super(CreateAccountScreen, self).__init__(**kwargs)

        self.orientation = 'vertical'
        self.padding = 20

        self.username_input = TextInput(
            hint_text='New Username', multiline=False,
            size_hint=(None, None), height=30, width=200,
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            text=self.username_input_text
        )
        self.password_input = TextInput(
            hint_text='New Password', password=True,
            multiline=False, size_hint=(None, None),
            height=30, width=200,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            text=self.password_input_text
        )
        self.create_account_button = Button(
            text='Create Account', on_press=self.create_account,
            size_hint=(None, None), height=30, width=150,
            pos_hint={'center_x': 0.5, 'center_y': 0.4}
        )
        self.result_label = Label(text='', size_hint_y=None, height=30)

        centering_layout = BoxLayout(orientation='vertical', spacing=10)
        centering_layout.add_widget(Label())
        centering_layout.add_widget(self.username_input)
        centering_layout.add_widget(self.password_input)
        centering_layout.add_widget(self.create_account_button)

        self.add_widget(centering_layout)
        self.add_widget(self.result_label)

    def create_account(self,_):

        username = self.username_input_text
        password = self.password_input_text

        api_url = 'http://localhost:3000/api/register'
        data = {'username': username, 'password': password}

        try:
            response = requests.post(api_url, json=data)
            result = response.json()

            if result.get('success'):
                self.result_label.text = 'Account created successfully!'
                self.manager.current = 'login'  # Go back to the login screen after account creation
            else:
                self.show_popup('Wrong Login', 'Invalid username or password.')

        except requests.RequestException as e:
            print(f"Error connecting to the API: {e}")
            self.show_popup('Error', 'Failed to connect to the server.')





class CalendarScreen(Screen):
    def __init__(self, **kwargs):
        super(CalendarScreen, self).__init__(**kwargs)
        self.grid_layout = GridLayout(cols=7, spacing=5)
        self.add_widget(self.grid_layout)

        for day in range(1, 32):  # Example: Display days 1 to 31
            button = Button(text=str(day), on_press=self.show_popup)
            button.bind(on_press=self.on_button_click)
            self.grid_layout.add_widget(button)

    def on_button_click(self, instance):
        day = instance.text
        instance.background_color = (0, 1, 0, 1)
        self.send_day_to_server(day)

    def show_popup(self, instance):
        self.dismiss_popup()
        day = instance.text
        content = f"You clicked on day {day}."
        popup = Popup(title="Day Details", content=Label(text=content), size_hint=(None, None), size=(300, 200))
        popup.open()

    def dismiss_popup(self):
        for child in self.children:
            if isinstance(child, Popup):
                child.dismiss()
                break

    def send_day_to_server(self, day):
        api_url = 'http://localhost:3000/api/save_day'
        data = {'day': day}

        try:
            response = requests.post(api_url, json=data)
            result = response.json()

            if result.get('success'):
                print(f"Day {day} saved successfully!")
            else:
                print(f"Failed to save day {day}.")

        except requests.RequestException as e:
            print(f"Error connecting to the API: {e}")
            # Handle the error appropriately, e.g., show a popup


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(CreateAccountScreen(name='create_account'))
        sm.add_widget(CalendarScreen(name='calendar'))
        return sm


if __name__ == '__main__':
    MyApp().run()