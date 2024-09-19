import flet as ft
from flet_route import Routing, path
from pages.auth.signIn import SignInPage
from pages.auth.signUp import SignUpPage

class Router:
    def __init__(self, page: ft.Page, log):
        self.page = page
        self.log = log
        self.signInPage = SignInPage(log)
        self.signUpPage = SignUpPage(log)
        self.app_routes = [
            path(url='/', clear=True, view=self.signInPage.view),
            path(url='/signup', clear=False, view=self.signUpPage.view),
        ]

        Routing(
            page=self.page,
            app_routes = self.app_routes,
        )

        self.page.go(self.page.route)