import flet as ft
import requests
from flet_route import Params, Basket
from typing import Callable, Optional
from internal.lib.style.style import *

API_URL = "http://localhost:8080/auth/sign-in"

class SignInUI:
    def __init__(self, on_username_change: Callable, on_password_change: Callable, on_sign_in: Callable):
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

    def create_view(self, page: ft.Page) -> ft.View:
        return ft.View(
            "/",
            controls=[
                ft.Row(
                    expand=True,
                    controls=[
                        self.create_left_panel(page),
                        self.create_right_panel()
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
                    ft.Container(
                        ft.Text('Sign Up', color=defaultFontColor),
                        on_click=lambda _: page.go('/signup'),
                        alignment=ft.alignment.center,
                        height=40
                    ),
                ]
            )
        )

    def create_right_panel(self) -> ft.Container:
        return ft.Container(
            expand=3,
            image_src="https://avatars.mds.yandex.net/i?id=9e57baa961c6dfd8be9d0a1eb0cddc5f_l-5221319-images-thumbs&n=13",
            image_fit=ft.ImageFit.COVER,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(name=ft.icons.LOCK_PERSON_ROUNDED, color=hoverBgColor, size=140),
                    ft.Text('Sign In', color=hoverBgColor, size=25, weight=ft.FontWeight.BOLD)
                ]
            )
        )

class SignInPage:
    def __init__(self, log):
        self.log = log
        self.page: Optional[ft.Page] = None
        self.username_json = ""
        self.password_json = ""
        self.ui = SignInUI(self.on_username_change, self.on_password_change, self.send_data_to_server)
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
        page.window.min_width = 800
        page.window.min_height = 400
        page.fonts = {"Special Elite": "../assets/fonts/specialelite-cyrillic.ttf"}

        view = self.ui.create_view(page)
        view.controls.insert(0, self.snack_bar)
        return view
