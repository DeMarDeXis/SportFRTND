import flet as ft
from internal.lib.style.style import *
import asyncio
import requests
from config import HOST

get_nfl_team = HOST + "/app/nfl/teams"

class NFLMainContent(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.spacing = 10

        self.img_container = ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            bgcolor=ft.colors.GREY_300,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(ft.icons.CONSTRUCTION, size=100, color=ft.colors.ORANGE_800),
                    ft.Text("NFL Dashboard", size=24, weight=ft.FontWeight.BOLD),
                    ft.Text("Нажмите для просмотра расписания", size=16),
                    ft.Container(
                        width=200,
                        height=5,
                        bgcolor=ft.colors.ORANGE_500,
                        border_radius=5,
                        animate=ft.animation.Animation(1000, "easeInOut"),
                        offset=ft.transform.Offset(0, 0),
                        animate_offset=ft.animation.Animation(1000, "easeInOut"),
                    )
                ]
            ),
            on_click=self.slide_container,
            offset=ft.transform.Offset(0, 0),
            animate_offset=ft.animation.Animation(500, "easeInOut"),
        )

        self.schedule_container = ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            bgcolor=ft.colors.GREY_300,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(ft.icons.SCHEDULE, size=100, color=ft.colors.BLUE_800),
                    ft.Text("Расписание матчей", size=24, weight=ft.FontWeight.BOLD),
                    ft.Text("Раздел в разработке", size=16),
                    ft.ElevatedButton(
                        "Обновить",
                        icon=ft.icons.REFRESH,
                        on_click=self._animate_button,
                    )
                ]
            ),
            offset=ft.transform.Offset(1, 0),
            animate_offset=ft.animation.Animation(500, "easeInOut"),
            on_click=self.slide_container,
        )

        self.main_stack = ft.Stack(
            controls=[self.schedule_container, self.img_container],
            expand=True
        )

        self.controls = [self.main_stack]
        self.is_slided = False

    async def _animate_button(self, e):
        e.control.scale = ft.transform.Scale(0.9)
        await e.control.update_async()
        await asyncio.sleep(0.1)
        e.control.scale = ft.transform.Scale(1)
        await e.control.update_async()

    async def slide_container(self, e):
        if not self.is_slided:
            self.img_container.offset = ft.transform.Offset(1, 0)
            self.schedule_container.offset = ft.transform.Offset(0, 0)
        else:
            self.img_container.offset = ft.transform.Offset(0, 0)
            self.schedule_container.offset = ft.transform.Offset(1, 0)

        self.is_slided = not self.is_slided
        await self.main_stack.update_async()


class NFLTeamsContent(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.scroll = ft.ScrollMode.AUTO
        self.expand = True
        self.spacing = 10
        self.teams_list_view = ft.GridView(
            expand=True,
            runs_count=3,  # 3 колонки
            max_extent=300,  # максимальная ширина элемента
            child_aspect_ratio=1.2,  # соотношение сторон
            spacing=10,
            run_spacing=10,
        )

        self.controls = [
            ft.Text("NFL Teams", size=24, color=defaultFontColor, weight=ft.FontWeight.BOLD),
            ft.ProgressRing(),
        ]

    def did_mount(self):
        self.load_data()

    def create_team_card(self, team: dict) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Image(
                        src=team['img_url'],
                        width=120,
                        height=120,
                        fit=ft.ImageFit.CONTAIN,
                        border_radius=ft.border_radius.all(10),),
                    ft.Text(team['name'], size=16, weight=ft.FontWeight.BOLD),
                    ft.Text(f"{team['conference']} • {team['division']}", size=12),
                    ft.Text(team['abbr'], size=14, color=ft.colors.BLUE_700),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
            ),
            padding=15,
            border=ft.border.all(1, ft.colors.GREY_400),
            border_radius=10,
            bgcolor=ft.colors.GREY_100,
            on_click=self.create_team_click_handler(team),
            animate=ft.animation.Animation(300, "easeInOut"),
            on_hover=lambda e: self._animate_card(e),
        )

    def _animate_card(self, e):
        e.control.scale = ft.transform.Scale(1.05) if e.data == "true" else ft.transform.Scale(1)
        e.control.bgcolor = ft.colors.GREY_200 if e.data == "true" else ft.colors.GREY_100
        e.control.update()

    def create_list_teams(self, teams_list: list) -> ft.GridView:
        for team in teams_list:
            self.teams_list_view.controls.append(self.create_team_card(team))
        return self.teams_list_view

    @staticmethod
    def create_team_click_handler(team):
        def handle_click(e):
            print(f"Clicked {team['name']}")
            # Здесь можно добавить переход на детальную страницу команды

        return handle_click

    def load_data(self):
        try:
            token = self.page.session.get("auth_token")
            headers = {"Authorization": f"Bearer {token}"} if token else {}
            response = requests.get(get_nfl_team, headers=headers)
            response.raise_for_status()
            data = response.json()

            self.controls = [self.controls[0]]  # Оставляем только заголовок

            if not data:
                self.controls.append(ft.Text("No data available", size=16, color=defaultFontColor))
                self.update()
                return

            scroll_container = ft.Container(
                content=self.create_list_teams(data),
                padding=10,
            )

            self.controls.append(scroll_container)
            self.update()

        except requests.RequestException as e:
            self.controls.append(ft.Text(f"Error fetching data: {str(e)}", size=16, color=defaultFontColor))
            self.update()
        except Exception as e:
            self.controls.append(ft.Text(f"An error occurred: {str(e)}", size=16, color=defaultFontColor))
            self.update()

class NFLRosterContent(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.scroll = ft.ScrollMode.AUTO
        self.expand = True
        self.spacing = 10

        # Анимированный контейнер с эффектом смены цветов
        self.color_animation = ft.Animation(2000, "linear")
        self.current_color = 0
        self.colors = [
            ft.colors.BLUE_100,
            ft.colors.GREEN_100,
            ft.colors.ORANGE_100,
            ft.colors.PURPLE_100
        ]

        self.controls = [
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(ft.icons.PEOPLE_ALT, size=100, color=ft.colors.BLUE_800),
                        ft.Text("Составы команд", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_800),
                        ft.Text("Раздел в разработке", size=16, color=ft.colors.BLUE_800),
                        ft.Text("Скоро здесь появятся данные о составе команд", size=14, color=ft.colors.BLUE_800),
                        ft.Container(
                            width=300,
                            height=10,
                            bgcolor=ft.colors.BLUE_500,
                            border_radius=5,
                            animate=self.color_animation,
                            on_animation_end=self._change_color
                        )
                    ]
                ),
                on_click=self._change_color_click,
            )
        ]

    def _change_color(self, e):
        self.current_color = (self.current_color + 1) % len(self.colors)
        e.control.bgcolor = self.colors[self.current_color]
        e.control.update()

    async def _change_color_click(self, e):
        e.control.content.controls[-1].bgcolor = ft.colors.RED_500
        await e.control.content.controls[-1].update_async()
        await asyncio.sleep(200)
        e.control.content.controls[-1].bgcolor = self.colors[self.current_color]
        await e.control.content.controls[-1].update_async()

class NFLScheduleContent(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.scroll = ft.ScrollMode.AUTO
        self.expand = True
        self.spacing = 10

        # Анимированный текст с эффектом печатания
        self.full_text = "Расписание NFL - в разработке..."
        self.displayed_text = ""
        self.text_index = 0

        self.typing_animation = ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(ft.icons.CALENDAR_TODAY, size=100, color=ft.colors.GREEN_800),
                    ft.Text("", size=24, weight=ft.FontWeight.BOLD, key="typing-text"),
                    ft.Text("Скоро здесь появится полное расписание", size=16),
                    ft.ProgressRing(width=50, height=50, stroke_width=3)
                ]
            ),
            bgcolor=ft.colors.GREY_100,
            border_radius=10,
            padding=20
        )

        self.controls = [self.typing_animation]
        self.page.run_task(self._typing_effect)

    async def _typing_effect(self):
        while self.text_index < len(self.full_text):
            self.displayed_text += self.full_text[self.text_index]
            self.text_index += 1
            typing_text = self.typing_animation.content.controls[1]
            typing_text.value = self.displayed_text
            await self.typing_animation.update_async()
            await asyncio.sleep(0.1)

        # Бесконечная анимация
        while True:
            await asyncio.sleep(2)
            self.displayed_text = ""
            self.text_index = 0
            typing_text.value = ""
            await self.typing_animation.update_async()
            await self._typing_effect()
