import flet as ft
import requests
from flet_route import Params, Basket
from typing import Callable, Optional
from internal.lib.style.style import *
from config import HOST

API_URL = HOST + "/auth/sign-in"
image_sign_in = "https://i.pinimg.com/originals/19/a7/09/19a70927aff373b1097a611a2f5bf28e.jpg"
# image_sign_in = "https://sun9-52.userapi.com/impf/c638825/v638825500/5cfa9/NEKNKs0V3ro.jpg?size=1280x966&quality=96&sign=a2f2f70ef5c950ee757faae5b7904fa4&c_uniq_tag=SdiA6flKyqfG7i5oqsatO8iz-iPrg_OIepUzMSjy7nY&type=album"

class SignInUI:
    def __init__(self, on_username_change: Callable, on_password_change: Callable,
                 on_sign_in: Callable, on_sign_up: Callable, close_app: Callable):
        self.username = ft.Container(
            content=ft.TextField(
                label='Input your username',
                bgcolor=secondaryBgColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
                on_change=on_username_change
            ),
            border_radius=15
        )

        self.password_input = ft.Container(
            content=ft.TextField(
                label='Input password',
                password=True,
                can_reveal_password=True,
                bgcolor=secondaryBgColor,
                border=ft.InputBorder.NONE,
                filled=True,
                color=secondaryFontColor,
                on_change=on_password_change
            ),
            border_radius=15
        )

        self.sign_in_button = ft.Container(
            ft.Text('Sign In', color=defaultBgColor),
            alignment=ft.alignment.center,
            height=40,
            bgcolor=hoverBgColor,
            on_click=on_sign_in
        )

        self.sign_up_button = ft.Container(
            ft.Text('Sign Up', color=defaultFontColor),
            alignment=ft.alignment.center,
            height=40,
            on_click=on_sign_up,
            # on_click=lambda _: page.go('/welcome')
        )

        self.exit_button = ft.IconButton(
            icon=ft.icons.EXIT_TO_APP,
            # icon_color=defaultFontColor,
            # icon_color="RED",
            icon_size=30,
            on_click=close_app,
            style=ft.ButtonStyle(
                bgcolor=secondaryBgColor,
                color="RED",
            )
        )

    def create_view(self, page: ft.Page) -> ft.View:
        return ft.View(
            "/",
            controls=[
                ft.Row(
                    expand=True,
                    controls=[
                        self.create_left_panel(page),
                        SignInUI.create_right_panel()
                    ]
                )
            ],
            bgcolor=defaultBgColor,
            padding=0
        )

    def create_left_panel(self, page: ft.Page) -> ft.Container:
        return ft.Container(
            expand=2,
            padding=ft.padding.all(40),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Buenos Dias", color=defaultFontColor, size=25, weight=ft.FontWeight.NORMAL, font_family="Special Elite"),
                    self.username,
                    self.password_input,
                    self.sign_in_button,
                    self.sign_up_button,
                    self.exit_button
                ]
            )
        )

    @staticmethod
    def create_right_panel() -> ft.Container:
        return ft.Container(
            expand=3,
            image_src=image_sign_in,
            image_fit=ft.ImageFit.COVER,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(name=ft.icons.SPORTS_BASEBALL_OUTLINED, color=hoverBgColor, size=140),
                    ft.Text('SportThunder', color=hoverBgColor, size=25, weight=ft.FontWeight.BOLD)
                ]
            )
        )

class SignInPage:
    def __init__(self, log, basket):
        self.log = log
        self.basket = basket
        self.page: Optional[ft.Page] = None
        self.username_json = ""
        self.password_json = ""
        self.ui = SignInUI(self.on_username_change, self.on_password_change, self.send_data_to_server,
                           self.sign_up, self.close_app)
        self.snack_bar = self.create_snack_bar()

    def create_snack_bar(self) -> ft.SnackBar:
        return ft.SnackBar(
            content=ft.Row([
                ft.Icon(name=ft.icons.ERROR_OUTLINE, color=ft.colors.WHITE),
                ft.Text("Failed to send data. Please check your connection.", color=ft.colors.WHITE),
                ft.TextButton("Retry", on_click=self.retry_send_data, col=ft.colors.WHITE),
            ]),
            bgcolor=ft.colors.RED,
            duration=4000,
            open=False,
        )

    def sign_up(self, _):
        # self.page.go('/signup')
        self.page.go('/welcome')

    def close_app(self, _):
        self.page.window_destroy()

    def on_username_change(self, e):
        self.username_json = e.control.value

    def on_password_change(self, e):
        self.password_json = e.control.value

    def send_data_to_server(self, _):
        data = {"username": self.username_json, "password": self.password_json}
        self.log.info(f"Sending data to server: {data}")

        try:
            response = requests.post(API_URL, json=data)
            response.raise_for_status()
            self.handle_successful_response(response)
        except requests.exceptions.RequestException as e:
            self.handle_request_exception(e)

    def handle_successful_response(self, response: requests.Response):
        self.log.info("Data sent successfully")
        self.log.info(f"Server response: {response.status_code}")
        self.log.info(f"Server response data: {response.json()}")

        response_data = response.json()
        token = response_data.get('token')
        if token:
            self.log.info(f"Received token: {token}")
            self.page.session.set("auth_token", token)
            self.page.session.set("username", self.username_json)
            self.log.info(f"{token} and {self.username_json} saved in basket")

            self.page.go('/welcome')
        else:
            self.show_error_message("Token not received from server.")

    def handle_request_exception(self, e: requests.exceptions.RequestException):
        self.log.error(f"An error occurred: {e}")
        if isinstance(e, requests.exceptions.HTTPError) and e.response.status_code == 500:
            self.show_error_message("Invalid data. Please check your input.")
        else:
            self.show_error_message("Failed to send data. Please try again later.")

    def show_error_message(self, message: str):
        self.log.error(f"Error message shown: {message}")
        self.snack_bar.content.controls[1].value = message
        self.snack_bar.bgcolor = ft.colors.RED
        self.snack_bar.open = True
        self.page.update()

    def retry_send_data(self, _):
        self.send_data_to_server(None)

    def view(self, page: ft.Page, params: Params, basket: Basket):
        self.page = page
        page.title = 'Sign In page'
        page.window.width = defaultWidthWindow
        page.window.height = defaultHeightWindow
        page.window.min_width = 1000
        page.window.min_height = 600
        page.fonts = {"Special Elite": "../assets/fonts/specialelite-cyrillic.ttf"}

        view = self.ui.create_view(page)
        view.controls.insert(0, self.snack_bar)
        return view
