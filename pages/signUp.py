import flet as ft
import requests
from flet_route import Params, Basket
from internal.lib.style.style import *

class SignUpPage:

    nameJSON = ""
    usernameJSON = ""

    name = ft.Container(
        content=ft.TextField(label='Input your name',
                             bgcolor=secondaryBgColor,
                             border=ft.InputBorder.NONE,
                             filled=True,
                             color=secondaryFontColor,
                             on_change= lambda e: print(e.control.value),
                             ),
        border_radius=15
    )

    username = ft.Container(
        content=ft.TextField(label='Input your username',
                             bgcolor=secondaryBgColor,
                             border=ft.InputBorder.NONE,
                             filled=True,
                             color=secondaryFontColor,
                             on_change = lambda e: print(e.control.value),
                             ),
        border_radius=15
    )

    # password_input = ft.Container(
    #     content=ft.TextField(label='Input password',
    #                          password=True, can_reveal_password=True,
    #                          bgcolor=secondaryBgColor,
    #                          border=ft.InputBorder.NONE,
    #                          filled=True,
    #                          color=secondaryFontColor),
    #     border_radius=15
    # )

    def view(self, page: ft.Page, params: Params, basket: Basket):
        page.title = 'Sign Up page'
        page.window.width = defaultWidthWindow
        page.window.height = defaultHeightWindow
        page.window.min_width = 800
        page.window.min_height = 400
        page.fonts = {"Special Elite": "assets/fonts/specialelite-cyrillic.ttf"}

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
                                    # self.password_input,
                                    ft.Container(
                                        ft.Text('Sign Up', color=defaultFontColor),
                                        on_click=lambda e: page.go('/'),
                                        alignment=ft.alignment.center,
                                        # bgcolor=hoverBgColor,
                                        height=40
                                    ),

                                    ft.Container(

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
                # ft.ElevatedButton('Sign IN', on_click=lambda e: page.go('/'))
