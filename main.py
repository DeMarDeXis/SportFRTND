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

#TODO: add exit-button to all pages
#TODO: make util Title
#TODO: add team page in NHL (10.05.2025)
#TODO: i guess all url should be in config.py include API_URL (10.05.2025)

# TODO: delete the next debug lines after 10.06.2025 and after 16.06.2025
     # button sign up
# TODO: To learn all code from new pages