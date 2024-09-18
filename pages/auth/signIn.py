import flet as ft
import requests
from flet_route import Params, Basket
from internal.lib.style.style import *

API_URL="http://localhost:8080/auth/sign-in"

class SignInPage:

    def __init__(self, log):
        self.log = log
        self.page = None
        self.usernameJSON = ""
        self.passwordJSON = ""

        self.snack_bar = ft.SnackBar(
            content=ft.Row([
                ft.Icon(name=ft.icons.ERROR_OUTLINE, color=ft.colors.WHITE),
                ft.Text("Failed to send data. Please check your connection.", color=ft.colors.WHITE),
                ft.TextButton("Retry", on_click=self.retry_send_data, col=ft.colors.WHITE),
            ]),
            bgcolor=ft.colors.RED,
            duration=4000,
            open=False,
        )

        self.username = ft.Container(
            content=ft.TextField(label='Input your username',
                                 bgcolor=secondaryBgColor,
                                 border=ft.InputBorder.NONE,
                                 filled=True,
                                 color=secondaryFontColor,
                                 on_change= self.on_username_change
                                 ),
            border_radius=15
        )

        #TODO: add password input + json
        self.password_input = ft.Container(
            content=ft.TextField(label='Input password',
                                 password=True, can_reveal_password=True,
                                 bgcolor=secondaryBgColor,
                                 border=ft.InputBorder.NONE,
                                 filled=True,
                                 color=secondaryFontColor,
                                 on_change=self.on_password_change
                                 ),
            border_radius=15
        )

    def on_username_change(self, e):
        self.usernameJSON = e.control.value

    def on_password_change(self, e):
        self.passwordJSON = e.control.value

    def send_data_to_server(self):
        data = {
            "username": self.usernameJSON
        }
        response = None
        self.log.info(f"Sending data to server: {data}")

        try:
            response = requests.post(API_URL, json=data)
            response.raise_for_status()
            self.log.info("Data sent successfully")
            self.log.info(f"Server response: {response.status_code}")
            self.log.info(f"Server response data: {response.json()}")

            response_data = response.json()
            token = response_data.get('token')
            if token:
                self.log.info(f"Received token: {token}")
            else:
                self.show_error_message("Token not received from server.")

        except requests.exceptions.HTTPError as e:
            self.log.error(f"HTTP error occurred: {e}")
            if response.status_code == 500:
                self.show_error_message("Invalid data. Please check your input.")

        except requests.exceptions.RequestException as e:
            self.log.error(f"An error occurred: {e}")
            self.show_error_message("Failed to send data. Please try again later.")

    def show_error_message(self, message):
        self.log.error(f"Error message shown: {message}")
        self.snack_bar.content.controls[1].value = message
        self.snack_bar.bgcolor = ft.colors.RED
        self.snack_bar.open = True
        self.page.update()

    def retry_send_data(self, e):
        self.send_data_to_server()

    def view(self, page: ft.Page, params: Params, basket: Basket):
        self.page = page
        page.title = 'Sign In page'
        page.window.width = defaultWidthWindow
        page.window.height = defaultHeightWindow
        page.window.min_width = 800
        page.window.min_height = 400
        page.fonts = { "Special Elite": "../assets/fonts/specialelite-cyrillic.ttf"}

        return ft.View(
            "/",
            controls = [
                self.snack_bar,
                ft.Row(
                    expand=True,
                    controls=[
                        ft.Container(
                            expand=2,
                            padding=ft.padding.all(40),
                            content =ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Text("Buenos Dias",
                                                 color=defaultFontColor,
                                                 size=25,
                                                weight=ft.FontWeight.NORMAL,
                                                font_family="Special Elite",
                                            ),
                                    self.username,
                                    #TODO: add password input
                                    self.password_input,
                                    ft.Container(
                                        ft.Text('Sign In', color=defaultBgColor),
                                        alignment=ft.alignment.center,
                                        height=40,
                                        bgcolor=hoverBgColor,
                                        on_click=lambda e: self.send_data_to_server(),
                                    ),

                                    ft.Container(
                                        ft.Text('Sign Up', color=defaultFontColor),
                                        on_click=lambda e: page.go('/signup'),
                                        alignment=ft.alignment.center,
                                        # bgcolor=hoverBgColor,
                                        height=40
                                    ),
                                ]
                            )
                        ),
                        ft.Container(
                            expand=3,
                            image_src="https://avatars.mds.yandex.net/i?id=9e57baa961c6dfd8be9d0a1eb0cddc5f_l-5221319-images-thumbs&n=13",
                            image_fit=ft.ImageFit.COVER,
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Icon(name=ft.icons.LOCK_PERSON_ROUNDED,
                                            color=hoverBgColor,
                                            size=140),
                                    ft.Text('Sign In',
                                            color=hoverBgColor,
                                            size=25,
                                            weight=ft.FontWeight.BOLD
                                            )
                                ]
                            )
                        )
                    ]
                )
            ],
            bgcolor=defaultBgColor,
            padding=0
        )