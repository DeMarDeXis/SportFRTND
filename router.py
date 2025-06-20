import flet as ft
from click import clear
from flet_route import Routing, path
from flet_route import Params, Basket
from pages.auth.signIn import SignInPage
from pages.auth.signUp import SignUpPage
from pages.auth.success_page import SuccessPage
from pages.welcome.welcome_page import WelcomePage
from pages.sportsPages.nhl.main_page_nhl import NHLMainPage
from pages.sportsPages.nba.main_page_nba import NBAMainPage
from pages.sportsPages.nfl.main_page_nfl import NFLMainPage
from pages.sportsPages.mlb.main_page_mlb import MLBMainPage

class Router:
    def __init__(self, page: ft.Page, log):
        self.page = page
        self.log = log
        self.basket = Basket()
        self.signInPage = SignInPage(log, self.basket)
        self.signUpPage = SignUpPage(log)
        self.success = SuccessPage(log)
        self.welcome = WelcomePage(log, self.basket)
        self.nhl_main = NHLMainPage()
        self.nba_main = NBAMainPage()
        self.nfl_main = NFLMainPage()
        self.mlb_main = MLBMainPage()
        self.app_routes = [
            path(url='/', clear=True, view=self.signInPage.view),
            path(url='/signup', clear=False, view=self.signUpPage.view),
            path(url='/success', clear=False, view=self.success.view),
            path(url='/welcome', clear=False, view=self.welcome.view),
            path(url='/mainNHL', clear=False, view=self.nhl_main.view),
            path(url='/mainNBA', clear=False, view=self.nba_main.view),
            path(url='/mainNFL', clear=False, view=self.nfl_main.view),
            path(url='/mainMLB', clear=False, view=self.mlb_main.view),
        ]

        Routing(
            page=self.page,
            app_routes = self.app_routes,
        )

        self.page.go(self.page.route)