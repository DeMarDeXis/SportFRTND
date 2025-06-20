import flet as ft
from flet_route import Params, Basket
from typing import Optional
from internal.lib.style.style import *
from config import HOST
from .contentOfContainer.content import NBAMainContent, NBATeamsContent, NBARosterContent, NBAScheduleContent

class NBAMainPageUI:
    def __init__(self, page: ft.Page):
        self.page = page
        self.current_content = None
        self.content_container = ft.Container(expand=True)

        self.logo = ft.Container(
            padding=ft.padding.symmetric(17, 13),
            content=ft.Row(
                controls=[
                    ft.Image(src='assets/images/icon.ico', width=45, height=32, fit=ft.ImageFit.FILL),
                    ft.Text('SportThunder', expand=True, color=defaultFontColor, font_family='cuprum', size=16),
                ],
                alignment=ft.MainAxisAlignment.START,
            )
        )

        style_menu = ft.ButtonStyle(
            color={
                ft.MaterialState.HOVERED: ft.colors.WHITE,
                ft.MaterialState.DEFAULT: ft.colors.random_color()
            },
            icon_size=14,
            overlay_color=hoverBgColor,
            shadow_color=hoverBgColor
        )

        self.sidebar_menu = ft.Container(
            padding=ft.padding.symmetric(0, 13),
            content=ft.Column(
                controls=[
                    ft.Text('Menu', color='#291919', font_family='cuprum', size=12),
                    ft.TextButton(
                        "Main",
                        icon=ft.icons.SPACE_DASHBOARD_ROUNDED,
                        style=style_menu,
                        on_click=self.show_main_content
                    ),
                    ft.TextButton(
                        "Teams",
                        icon=ft.icons.GROUPS,
                        style=style_menu,
                        on_click=self.show_teams_content
                    ),
                    ft.TextButton(
                        "Roster",
                        icon=ft.icons.PERSON_SEARCH,
                        style=style_menu,
                        on_click=self.show_roster_content
                    ),
                    ft.TextButton(
                        "Schedule",
                        icon=ft.icons.CALENDAR_MONTH,
                        style=style_menu,
                        on_click=self.show_schedule_content
                    )
                ]
            )
        )

        self.header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text("Панель управления", color=defaultBgColor, size=20, font_family='cuprum'),
                    ft.Row(
                        controls=[
                            ft.CircleAvatar(
                                foreground_image_url='assets/images/undefined.jpg',
                                content=ft.Text('A'),
                            ),
                            ft.IconButton(
                                icon=ft.icons.NOTIFICATIONS_ROUNDED,
                                icon_size=20,
                                tooltip="Notifications",
                                style=ft.ButtonStyle(
                                    overlay_color=hoverBgColor,
                                    color=defaultFontColor
                                ),
                            ),
                            ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                icon_size = 20,
                                tooltip="Arrow",
                                style=ft.ButtonStyle(
                                    overlay_color=hoverBgColor,
                                    color=defaultFontColor
                                ),
                                on_click=lambda e: self.page.go("/welcome") # TODO:MAYBE check token
                            ),
                            ft.IconButton(
                                icon=ft.icons.EXIT_TO_APP,
                                icon_size=20,
                                tooltip="Arrow",
                                style=ft.ButtonStyle(
                                    overlay_color=hoverBgColor,
                                    color=defaultFontColor
                                ),
                                on_click=lambda e: self.page.window_destroy()
                            )
                        ],
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        )

    def show_main_content(self, e):
        self.content_container.content = NBAMainContent(self.page)
        self.content_container.update()

    def show_teams_content(self, e):
        self.content_container.content = NBATeamsContent(self.page)
        self.content_container.update()

    def show_roster_content(self, e):
        self.content_container.content = NBARosterContent(self.page)
        self.content_container.update()

    def show_schedule_content(self, e):
        self.content_container.content = NBAScheduleContent(self.page)
        self.content_container.update()

    def create_view(self) -> ft.View:
        # Set default content
        self.content_container.content = NBAMainContent(self.page)

        return ft.View(
            "/mainNBA",
            controls=[
                ft.Row(
                    expand=True,
                    spacing=0,
                    controls=[
                        # left panel
                        ft.Container(
                            expand=1,
                            content=ft.Column(
                                spacing=0,
                                controls=[
                                    self.logo,
                                    self.sidebar_menu
                                ]
                            ),
                            bgcolor=secondaryBgColor,
                        ),
                        # right panel
                        ft.Container(
                            expand=4,
                            padding=ft.padding.symmetric(15, 10),
                            content=ft.Column(
                                spacing=0,
                                controls=[
                                    self.header,
                                    self.content_container
                                ]
                            )
                        )
                    ]
                )
            ],
            bgcolor=defaultBgColor,
            padding=0,
        )


class NBAMainPage:
    def __init__(self):
        self.ui = None

    def view(self, page: ft.Page, params: Params, basket: Basket) -> ft.View:
        self.ui = NBAMainPageUI(page)
        page.title = "NBA"
        page.window_width = defaultWidthWindow
        page.window_height = defaultHeightWindow
        page.window_min_width = 1000
        page.window_min_height = 600
        page.fonts = {
            "Special Elite": "../assets/fonts/specialelite-cyrillic.ttf",
            "cuprum": "../assets/fonts/cuprum.ttf"
        }

        page.theme = ft.Theme(font_family="cuprum")

        return self.ui.create_view()