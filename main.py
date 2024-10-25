import flet as ft

from internal.logger.logretty.loggerpretty import setup_logger
from router import Router
from config import currentEnv

def main(page: ft.Page):
    logg = setup_logger(currentEnv)
    logg.info("Application started")
    page.window.frameless = True
    page.window.icon = "../assets/images/icon.ico"
    Router(page, logg)

if __name__ == '__main__':
    ft.app(target=main, assets_dir="assets")

#TODO: i guess i have to fix photo in signIn
#TODO: add exit-button to all pages
#TODO: make util Title
#TODO: make util List for sports
