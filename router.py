import flet as ft
from flet_route import Routing, path
from pages.signIn import SignInPage
from pages.signUp import SignUpPage

class Router:
    def __init__(self, page: ft.Page):
        self.page = page
        self.signUpPage = SignUpPage()
        self.app_routes = [
            path(url='/', clear=True, view=SignInPage().view),
            path(url='/signup', clear=False, view=self.signUpPage()),
        ]

        Routing(
            page=self.page,
            app_routes = self.app_routes,
        )

        self.page.go(self.page.route)