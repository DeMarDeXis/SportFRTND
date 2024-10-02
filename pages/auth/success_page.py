import flet as ft
from flet_route import Params, Basket
from internal.lib.style.style import *
from typing import Callable, Optional


#TODO: find out how to show image in flet and fix it
class SuccessPageUI:
    def __init__(self, back_button: Callable):
        self.welcome_text = ft.Text("Welcome to the club, buddy",
            size=30,
            weight=ft.FontWeight.BOLD,
            # expand=3,
            color=defaultFontColor,
            font_family="Special Elite",
            text_align=ft.TextAlign.CENTER,
        )

        self.back_button = ft.Container(
            ft.Icon(name=ft.icons.ARROW_BACK_IOS_NEW, color=defaultBgColor),
            alignment=ft.alignment.center,
            height=40,
            width=40,
            bgcolor=hoverBgColor,
            on_click=back_button,  # lambda e: page.go('/'),
            margin = ft.margin.only(top=20),
        )

    def create_view(self, page: ft.Page) -> ft.View:
        return ft.View(
            "/success",
            controls=[
                ft.Container(
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            self.welcome_text,
                            self.back_button
                        ],
                    ),
                    expand=True,
                    alignment=ft.alignment.center
                ),
            ],
            bgcolor=defaultBgColor,
            padding=20,
        )

class SuccessPage:
    def __init__(self, log):
        self.log = log
        self.ui = SuccessPageUI(self.back_button)
        self.page = Optional[ft.Page]

    def back_button(self, e):
        self.page.go('/')

    def view(self, page: ft.Page, params: Params, basket: Basket) -> ft.View:
        self.page = page
        page.title = "Success"
        page.window.width = defaultWidthWindow
        page.window.height = defaultHeightWindow
        page.window.min_width = 800
        page.window.min_height = 400
        page.fonts = {"Special Elite": "assets/fonts/specialelite-cyrillic.ttf"}

        view = self.ui.create_view(page)
        return view