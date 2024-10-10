import flet as ft
from click import clear
from flet_route import Routing, path
from pages.auth.signIn import SignInPage
from pages.auth.signUp import SignUpPage
from pages.auth.success_page import SuccessPage
from pages.intro.intro import IntroVideoPage
from pages.welcome.welcome_page import WelcomePage

class Router:
    def __init__(self, page: ft.Page, log):
        self.page = page
        self.log = log
        self.signInPage = SignInPage(log)
        self.signUpPage = SignUpPage(log)
        self.success = SuccessPage(log)
        self.intro = IntroVideoPage(log)
        self.welcome = WelcomePage(log)
        self.app_routes = [
            path(url='/', clear=True, view=self.signInPage.view),
            path(url='/signup', clear=False, view=self.signUpPage.view),
            path(url='/success', clear=False, view=self.success.view),
            path(url='/intro', clear=False, view=self.intro.view),
            path(url='/welcome', clear=False, view=self.welcome.view),
        ]

        Routing(
            page=self.page,
            app_routes = self.app_routes,
        )

        self.page.go(self.page.route)