# Небольшой гайд по фронтенду.
## Как не нужно делать при вёрстке.
Чтобы не было проблем с расположением элементов на странице, нужно использовать блочные элементы.(**CONTAINER**, row, col)
* Неправильный код:
```
    def create_view(self,page: ft.Page) -> ft.View:
        return ft.View(
            "/success",
            controls=[
                ft.Column(
                    expand=True,
                    # width=400,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        self.welcome_text,
                        self.back_button
                    ],
                ),
            ],
            bgcolor=defaultBgColor,
            padding=20,
        )
```

* Правильный код:
```
def create_view(self, page: ft.Page) -> ft.View:
    return ft.View(
        "/success",
        controls=[
            ft.Container(
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        self.welcome_text,
                        self.back_button
                    ],
                ),
                expand=True,
                alignment=ft.alignment.center
            ),
        ],
        bgcolor=defaultBgColor,
        padding=20,
    )
```
