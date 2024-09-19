import flet as ft
import requests
from flet_route import Params, Basket
from internal.lib.style.style import *
from typing import Callable, Optional

class SignUpUi:

    def __init__(self, on_name_change: Callable, on_username_change: Callable, on_sign_up: Callable, back_button: Callable):
        self.welcome_text = ft.Text(
                                    "Bienvenido",
                                    color=defaultFontColor,
                                    size=40,
                                    weight=ft.FontWeight.BOLD,
                                    font_family="Special Elite",
                                )


        self.name = ft.Container(
            content=ft.TextField(label='Input your name',
                                 bgcolor=secondaryBgColor,
                                 border=ft.InputBorder.NONE,
                                 filled=True,
                                 color=secondaryFontColor,
                                 on_change=on_name_change,
                                 ),
            border_radius=15
        )

        self.username = ft.Container(
            content=ft.TextField(label='Input your username',
                                 bgcolor=secondaryBgColor,
                                 border=ft.InputBorder.NONE,
                                 filled=True,
                                 color=secondaryFontColor,
                                 on_change=on_username_change,
                                 ),
            border_radius=15
        )


        self.password_input = ft.Container(
            content=ft.TextField(label='Input password',
                                 password=True, can_reveal_password=True,
                                 bgcolor=secondaryBgColor,
                                 border=ft.InputBorder.NONE,
                                 filled=True,
                                 color=secondaryFontColor),
            border_radius=15
        )

        self.sign_up_button = ft.Container(
            ft.Text('Sign Up', color=defaultBgColor),
            alignment=ft.alignment.center,
            height=40,
            bgcolor=hoverBgColor,
            on_click=on_sign_up
        )

        self.back_button = ft.Container(
            # ft.Text('Back', color=defaultBgColor),
            ft.Icon(name=ft.icons.ARROW_BACK_IOS_NEW, color=defaultBgColor),
            alignment=ft.alignment.center,
            height=40,
            bgcolor=hoverBgColor,
            on_click=back_button #lambda e: page.go('/'),
        )

    def create_view(self, page: ft.Page) -> ft.View:
        return ft.View(
            "/",
            controls=[
                ft.Row(
                    expand=True,
                    controls=[
                        SignUpUi.create_left_panel(),
                        self.create_right_panel(page),
                    ]
                )
            ],
            bgcolor=defaultBgColor,
            padding=0
        )

    @staticmethod
    def create_left_panel() -> ft.Container:
        return ft.Container(
        expand=2,
        image_src="https://i.pinimg.com/736x/d2/a8/e0/d2a8e0b3aa2a0e876c7bfc8b9ba94508.jpg",
        image_fit=ft.ImageFit.COVER,
        content=ft.Column(
            #MAYBE ADD A LOGO HERE
        )
    )

    def create_right_panel(self, page: ft.Page) -> ft.Container:
        return ft.Container(
                        expand=3,
                        padding=ft.padding.all(40),
                        content=ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                self.welcome_text,
                                self.name,
                                self.username,
                                self.password_input,
                                self.sign_up_button,
                                self.back_button,
                            ]
                        )
                    )



class SignUpPage:

    def __init__(self, log):
        self.log = log
        self.page = Optional[ft.Page]
        self.nameJSON = ""
        self.usernameJSON = ""
        self.passwordJSON = ""
        self.ui = SignUpUi(self.on_name_change, self.on_username_change, self.send_data_to_server, self.back_button)
        self.snack_bar = SignUpPage.create_snack_bar()
        # self.note_success = SignUpNotification("Success", "🔥")


    @staticmethod
    def create_snack_bar() -> ft.SnackBar:
        snack_bar = ft.SnackBar(
            content=ft.Row([
                ft.Icon(name=ft.icons.ERROR_OUTLINE, color=ft.colors.WHITE),
                ft.Text("Failed to send data. Please check your connection.", color=ft.colors.WHITE),
            ]),
            bgcolor=ft.colors.RED,
            duration=4000,
            open=False,
        )
        return snack_bar


    def on_username_change(self, e):
        self.usernameJSON = e.control.value

    def on_name_change(self, e):
        self.nameJSON = e.control.value

    def back_button(self, e):
        self.log.info("Back button clicked")
        self.page.go('/success')

    def send_data_to_server(self, _):
        #TODO: add password to data
        data = {"name": self.nameJSON, "username": self.usernameJSON,
                # "password": self.passwordJSON
                }
        self.log.info(f"Sending data to server: {data}")

        try:
            response = requests.post("http://localhost:8080/auth/sign-up", json=data)
            response.raise_for_status()
            self.success_handler(response)
        except requests.exceptions.RequestException as e:
            self.except_handler(e)

    def success_handler(self, response: requests.Response):
        self.log.info("Data sent successfully")
        self.log.info(f"Server response: {response.status_code}")
        self.log.info(f"Server response data: {response.json()}")

        self.show_success_message("Data sent successfully")



        self.page.go('/success')

    def show_success_message(self, message):
        self.log.info(f"Success message shown: {message}")
        self.snack_bar.content.controls[1].value = message
        self.snack_bar.bgcolor = ft.colors.GREEN
        self.snack_bar.open = True
        self.page.update()

    def except_handler(self, e):
        self.log.error(f"Failed to send data: {e}")
        self.show_error_message("Failed to send data. Please check your connection.")

    def show_error_message(self, message):
        self.log.error(f"Error message shown: {message}")
        self.snack_bar.content.controls[1].value = message
        self.snack_bar.bgcolor = ft.colors.RED
        self.snack_bar.open = True
        self.page.update()

    def view(self, page: ft.Page, params: Params, basket: Basket) -> ft.View:
        self.page = page
        page.title = 'Sign Up page'
        page.window.width = defaultWidthWindow
        page.window.height = defaultHeightWindow
        page.window.min_width = 800
        page.window.min_height = 400
        page.fonts = {"Special Elite": "assets/fonts/specialelite-cyrillic.ttf"}


        view = self.ui.create_view(page)
        view.controls.insert(0, self.snack_bar)
        return view
