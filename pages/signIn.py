import flet as ft
from flet_route import Params, Basket
from internal.lib.style.style import *


class SignInPage:

    username = ft.Container(
        content=ft.TextField(label='Input your username',
                             bgcolor=secondaryBgColor,
                             border=ft.InputBorder.NONE,
                             filled=True,
                             color=secondaryFontColor),
        border_radius=15
    )

    #TODO: add password input
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
        page.title = 'Sign In page'
        page.window.width = defaultWidthWindow
        page.window.height = defaultHeightWindow
        page.window.min_width = 800
        page.window.min_height = 400
        page.fonts = { "Special Elite": "assets/fonts/specialelite-cyrillic.ttf"}

        return ft.View(
            "/",
            controls = [
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
                                    #self.password_input,
                                    ft.Container(
                                        ft.Text('Sign In', color=defaultBgColor),
                                        alignment=ft.alignment.center,
                                        height=40,
                                        bgcolor=hoverBgColor
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

