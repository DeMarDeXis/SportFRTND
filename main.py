import flet as ft

from internal.logger.logretty.loggerpretty import setup_logger
from router import Router

currentEnv = "local"
HOST = "http://localhost:8080"

def main(page: ft.Page):
    # TODO: add logger
    logg = setup_logger(currentEnv)
    logg.info("Application started")
    Router(page, logg)

if __name__ == '__main__':
    ft.app(target=main, assets_dir="assets")
