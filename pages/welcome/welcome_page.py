import flet as ft
from flet_route import Params, Basket
from typing import Callable, Optional
from internal.lib.style.style import *

class WelcomePageUI:
    def __init__(self):
        self.welcome_text = ft.Text(
            "Welcome to the club, buddy",
            color=defaultFontColor,
            size=25,
            weight=ft.FontWeight.BOLD,
            font_family="Special Elite",
            # expand=3,
            # text_align=ft.TextAlign.CENTER,
        )

    def create_view(self, page: ft.Page) -> ft.View:
        return ft.View(
            "/welcome",
            controls=[
                ft.Column(
                    expand=True,
                    controls=[
                        self.create_upper_panel(page),
                        self.create_middle_panel(page),
                        self.create_lower_panel(page)
                    ]
                )
            ],
            bgcolor=defaultBgColor,
            padding=0,
        )

    @staticmethod
    def create_upper_panel(page: ft.Page) -> ft.Container:
        return ft.Container(
            expand=1,
            bgcolor="WHITE",
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(
                            "Welcome to the club, buddy",
                            color=defaultFontColor,
                            size=25,
                            weight=ft.FontWeight.BOLD,
                            font_family="Special Elite",
                            # expand=3,
                            # text_align=ft.TextAlign.CENTER,
                        ),
                        alignment=ft.alignment.center,
                        expand=True,
                    )
                ],
            )
        )

    def create_middle_panel(self, page: ft.Page) -> ft.Container:
        return ft.Container(
            expand=5,
            bgcolor="Blue",
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(
                            "Welcome to the club, buddy",
                            color=defaultFontColor,
                            size=25,
                            weight=ft.FontWeight.BOLD,
                            font_family="Special Elite",
                            # expand=3,
                            # text_align=ft.TextAlign.CENTER,
                        ),
                        alignment=ft.alignment.center,
                        expand=True,
                    )
                ],
            )
        )

    def create_lower_panel(self, page: ft.Page) -> ft.Container:
        return ft.Container(
            expand=1,
            bgcolor="RED",
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(
                            "Welcome to the club, buddy",
                            color=defaultFontColor,
                            size=25,
                            weight=ft.FontWeight.BOLD,
                            font_family="Special Elite",
                            # expand=3,
                            # text_align=ft.TextAlign.CENTER,
                        ),
                        alignment=ft.alignment.center,
                        expand=True,
                    )
                ],
            )
        )

class WelcomePage:
    def __init__(self, log):
        self.log = log
        self.page: Optional[ft.Page] = None

        self.ui = WelcomePageUI()

    def view(self, page: ft.Page, params: Params, basket: Basket) -> ft.View:
        self.page = page
        page.title = 'Welcome'
        page.window_width = defaultWidthWindow
        page.window_height = defaultHeightWindow
        page.window.min_width = 800
        page.window.min_height = 400
        page.fonts = {"Special Elite": "../assets/fonts/specialelite-cyrillic.ttf"}

        view = self.ui.create_view(page)
        return view

