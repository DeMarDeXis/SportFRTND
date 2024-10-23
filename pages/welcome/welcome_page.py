import flet as ft
from flet_route import Params, Basket
from typing import Callable, Optional
from internal.lib.style.style import *

from customControls.animate_variable_card import AnimatedCard
from customControls.animate_variable_button import AnimatedIcons

mlb_img = "https://i.pinimg.com/originals/cd/61/c9/cd61c94d547830bf2df2dde4c94ce05a.jpg"
nhl_img = "https://oboi-download.ru/files/wallpapers/5874/nkhl-oboi-na-telefon-8.jpg"
nfl_img = "https://i.pinimg.com/736x/c1/a9/dc/c1a9dc0fd33531867c05981ff1040e15.jpg"
nba_img = "https://i.pinimg.com/736x/4c/1e/21/4c1e21b3522b35ff00d0ddd8dfb71214.jpg"

class WelcomePageUI:
    def __init__(self, username):
        self.welcome_text = ft.Text(
            f"Welcome to the club, {username}",
            color=defaultFontColor,
            # color="RED",
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
                    spacing=0,
                    controls=[
                        self.create_upper_panel(page),
                        self.create_middle_panel(page),
                        self.create_lower_panel(page)
                    ],
                )
            ],
            bgcolor=defaultBgColor,
            padding=0,
        )

    def create_upper_panel(self,page: ft.Page) -> ft.Container:
        return ft.Container(
            expand=1,
            bgcolor=defaultBgColor,
            content=ft.Row(
                controls=[
                    ft.Container(
                        content= self.welcome_text,
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
                    AnimatedCard("MLB", "", "GO to Baseball, bro", mlb_img).build(),
                    AnimatedCard("NBA", "", "AAAAND ONE", nba_img).build(),
                    AnimatedCard("NFL", "", "Exit light!!!",nfl_img).build(),
                    AnimatedCard("NHL", "", "Where's my teeth?", nhl_img).build()
                ],
            )
        )

    def create_lower_panel(self, page: ft.Page) -> ft.Container:
        return ft.Container(
            expand=1,
            bgcolor=defaultBgColor,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    AnimatedIcons().build()
                ],
            )
        )

class WelcomePage:
    def __init__(self, log, basket: Basket):
        self.log = log
        self.basket = basket
        self.page: Optional[ft.Page] = None
        self.ui = None


    def view(self, page: ft.Page, params: Params, basket: Basket) -> ft.View:
        self.page = page
        page.title = 'Welcome'
        page.window_width = defaultWidthWindow
        page.window_height = defaultHeightWindow
        page.window.min_width = 800
        page.window.min_height = 400
        page.fonts = {"Special Elite": "../assets/fonts/specialelite-cyrillic.ttf"}

        username = page.session.get("username")
        token = page.session.get("auth_token")
        self.log.info(f"username: {username}")
        self.log.info(f"token: {token}")
        if username is None or token is None:
            username = "None"
            token = "None"

        self.ui = WelcomePageUI(username)
        view = self.ui.create_view(page)
        return view

