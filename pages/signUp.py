import flet as ft
from flet_route import Params, Basket

class SignUpPage:
    def view(self, page: ft.Page, params: Params, basket: Basket):
        page.title = 'Sign Up'
        return ft.View(
            "/",
            controls = [
                ft.Text('Sign Up page'),
                ft.ElevatedButton('Sign IN', on_click=lambda e: page.go('/'))
            ]
        )