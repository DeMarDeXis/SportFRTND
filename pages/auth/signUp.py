import flet as ft
import requests
from flet_route import Params, Basket
from internal.lib.style.style import *

class SignUpPage:

    def __init__(self, log):
        self.log = log

        self.nameJSON = ""
        self.usernameJSON = ""

        self.snack_bar = ft.SnackBar(
            content=ft.Row([
                ft.Icon(name=ft.icons.ERROR_OUTLINE, color=ft.colors.WHITE),
                ft.Text("Failed to send data. Please check your connection.", color=ft.colors.WHITE),
            ]),
            bgcolor=ft.colors.RED,
            duration=4000,
            open=False,
        )

        self.name = ft.Container(
            content=ft.TextField(label='Input your name',
                                 bgcolor=secondaryBgColor,
                                 border=ft.InputBorder.NONE,
                                 filled=True,
                                 color=secondaryFontColor,
                                 on_change= self.on_name_change,
                                 ),
            border_radius=15
        )

        self.username = ft.Container(
            content=ft.TextField(label='Input your username',
                                 bgcolor=secondaryBgColor,
                                 border=ft.InputBorder.NONE,
                                 filled=True,
                                 color=secondaryFontColor,
                                 on_change = self.on_username_change,
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

    def on_username_change(self, e):
        self.usernameJSON = e.control.value

    def on_name_change(self, e):
        self.nameJSON = e.control.value

    def send_data_to_server(self):
        data = {
            "name": self.nameJSON,
            "username": self.usernameJSON
        }
        self.log.info(f"Sending data to server: {data}")

        try:
            response = requests.post("http://localhost:8080/auth/sign-up", json=data)
            response.raise_for_status()
            self.log.info("Data sent successfully")
            self.log.info(f"Server response: {response.status_code}")
            self.log.info(f"Server response data: {response.json()}")
        except requests.exceptions.RequestException as e:
            self.log.error(f"Failed to send data: {e}")
            self.show_error_message("Failed to send data. Please check your connection.")

    def show_error_message(self, message):
        self.log.error(f"Error message shown: {message}")
        self.snack_bar.content.controls[1].value = message
        self.snack_bar.bgcolor = ft.colors.RED
        self.snack_bar.open = True
        self.page.update()

    def view(self, page: ft.Page, params: Params, basket: Basket):
        page.title = 'Sign Up page'
        page.window.width = defaultWidthWindow
        page.window.height = defaultHeightWindow
        page.window.min_width = 800
        page.window.min_height = 400
        page.fonts = {"Special Elite": "assets/fonts/specialelite-cyrillic.ttf"}

                # ft.ElevatedButton('Sign IN', on_click=lambda e: page.go('/'))
        return ft.View(
            "/",
            controls = [
                ft.Row(
                    expand=True,
                    controls=[
                        ft.Container(
                            expand=2,
                            image_src="https://i.pinimg.com/736x/d2/a8/e0/d2a8e0b3aa2a0e876c7bfc8b9ba94508.jpg",
                            image_fit=ft.ImageFit.COVER,
                            content=ft.Column(
                                #MAYBE ADD A LOGO HERE
                            )
                        ),
                        ft.Container(
                            expand=3,
                            padding=ft.padding.all(40),
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Text(
                                        "Bienvenido",
                                        color=defaultFontColor,
                                        size=40,
                                        weight=ft.FontWeight.BOLD,
                                        font_family="Special Elite",
                                    ),
                                    self.name,
                                    self.username,
                                    self.password_input,
                                    ft.Container(
                                        ft.Text('Sign Up', color=defaultFontColor),
                                        on_click= lambda e: self.send_data_to_server(),
                                        alignment=ft.alignment.center,
                                        # bgcolor=hoverBgColor,
                                        height=40
                                    ),

                                    ft.Container(
                                        on_click=lambda e: page.go('/'),
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
