import httpx
import flet as ft
from flet_route import Params, Basket
import requests
import datetime
from internal.lib.style.style import *
from config import HOST

get_schedule = HOST + "/app/nhl/schedule"
get_last_schedule = HOST + "/app/nhl/schedule/last/10"
get_team = HOST + "/app/nhl/teams"
get_all_roster = HOST + "/app/nhl/players"

class NHLMainContent(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.spacing = 10

        self.img_url = "https://i.pinimg.com/originals/2e/90/56/2e90565fe94bad7fdcb0b06b8ddb9179.jpg"
        self.img_container = ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            bgcolor=ft.colors.BLUE_800,
            content=ft.Image(
                src=self.img_url,
                fit=ft.ImageFit.CONTAIN,
                repeat=ft.ImageRepeat.NO_REPEAT,
                border_radius=ft.border_radius.all(10),
            ),
            on_click=self.slide_container,
            offset=ft.transform.Offset(0, 0),
            animate_offset=ft.animation.Animation(500, "easeInOut"),
        )

        self.schedule_container = ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            bgcolor=ft.colors.BLUE_800,
            content=ft.Column(
                controls=[
                    ft.ProgressRing(),
                    ft.Text("Загрузка последних матчей...", size=16)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
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
        self.data_loaded = False

    async def slide_container(self, e):
        if not self.is_slided:
            self.img_container.offset = ft.transform.Offset(1, 0)
            self.schedule_container.offset = ft.transform.Offset(0, 0)

            if not self.data_loaded:
                await self.load_schedule_data()
                self.data_loaded = True
        else:
            self.img_container.offset = ft.transform.Offset(0, 0)
            self.schedule_container.offset = ft.transform.Offset(1, 0)

        self.is_slided = not self.is_slided
        await self.main_stack.update_async()

    async def load_schedule_data(self):
        try:
            token = self.page.session.get("auth_token")
            headers = {"Authorization": f"Bearer {token}"} if token else {}
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{get_last_schedule}",
                    headers=headers
                )
            data = response.json()

            if not data:
                self.schedule_container.content = ft.Text(
                    "Нет данных о последних матчах",
                    size=16,
                    color=defaultFontColor
                )
                await self.schedule_container.update_async()
                return

            schedule_table = self._create_schedule_table(data)

            self.schedule_container.content = ft.Container(
                content=schedule_table,
                expand=True,
                padding=10,
            )

            await self.schedule_container.update_async()

        except Exception as e:
            self.schedule_container.content = ft.Text(
                f"Ошибка загрузки данных: {str(e)}",
                size=16,
                color=defaultFontColor
            )
            await self.schedule_container.update_async()

    def _create_schedule_table(self, data):
        russian_weekdays = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        russian_months = [
            "янв", "фев", "мар", "апр", "мая", "июн",
            "июл", "авг", "сен", "окт", "ноя", "дек"
        ]

        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Дата", color=defaultFontColor)),
                ft.DataColumn(ft.Text("Время", color=defaultFontColor)),
                ft.DataColumn(ft.Text("Гость", color=defaultFontColor)),
                ft.DataColumn(ft.Text("Г", color=defaultFontColor)),
                ft.DataColumn(ft.Text("Х", color=defaultFontColor)),
                ft.DataColumn(ft.Text("Хозяин", color=defaultFontColor)),
                ft.DataColumn(ft.Text("ОТ", color=defaultFontColor)),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(self._format_date(game, russian_weekdays, russian_months)),
                        ft.DataCell(self._format_time(game)),
                        ft.DataCell(ft.Text(game['visitor_team'], color=defaultFontColor)),
                        ft.DataCell(ft.Text(str(game['visitor_score']) if game['visitor_score'] is not None else "-", color=defaultFontColor)),
                        ft.DataCell(ft.Text(str(game['home_score']) if game['home_score'] is not None else "-", color=defaultFontColor)),
                        ft.DataCell(ft.Text(game['home_team'], color=defaultFontColor)),
                        ft.DataCell(ft.Text("✓" if game.get("is_overtime", False) else "-", color=defaultFontColor)),
                    ]
                ) for game in data
            ],
            heading_row_color=ft.colors.BLACK38,
        )

    def _format_date(self, game, weekdays, months):
        try:
            date_obj = datetime.datetime.strptime(game['date_game'], "%Y-%m-%dT%H:%M:%SZ")
            weekday = weekdays[date_obj.weekday()]
            month = months[date_obj.month - 1]
            return ft.Text(f"{weekday}, {date_obj.day} {month}", color=defaultFontColor)
        except:
            return ft.Text(game.get('date_game', 'TBD'), color=defaultFontColor)

    def _format_time(self, game):
        try:
            if 'time_game' in game and game['time_game']:
                return ft.Text(game['time_game'][11:16], color=defaultFontColor)  # ("19:30")
            else:
                time_obj = datetime.datetime.strptime(game['date_game'], "%Y-%m-%dT%H:%M:%SZ")
                return ft.Text(time_obj.strftime("%H:%M"), color=defaultFontColor)
        except:
            return ft.Text("TBD", color=defaultFontColor)

class NHLTeamsContent(ft.Column):
    def __init__(self, page: ft.Page, content_container: ft.Container):
        super().__init__()
        self.page = page
        self.scroll = ft.ScrollMode.AUTO
        self.expand = True
        self.spacing = 10
        self.teams_list_view = ft.ListView(expand=True, spacing=10)
        self.content_container = content_container
        # IF necessary, add from team_nhl -> info_panel_nhl_team

        self.controls = [
            ft.Text("Teams Content", size=24, color=defaultFontColor),
            ft.ProgressRing(),
        ]

    def did_mount(self):
        #TODO: delete this
        #self.load_data_from_json()
        self.load_data()

    def create_list_teams(self, teams_list: list) -> ft.ListView:
        teams_list_view = self.teams_list_view
        for team in teams_list:
            current_team = team
            team_data = team.copy()
            teams_list_view.controls.append(
                ft.ListTile(
                    leading=ft.Text(current_team['abbr'], weight=ft.FontWeight.BOLD),
                    title=ft.Text(current_team['name']),
                    on_click= self.create_team_click_handler(team_data), # TODO: add method (I guess description of team)
                    trailing=ft.Icon(ft.icons.ARROW_FORWARD_IOS),
                )
            )
        return teams_list_view

    def create_team_click_handler(self, team):
        def handle_click(e):
            # Create and show team detail content
            team_detail_content = NHLTeamDetailContent(self.page, team['id'])

            # Replace current content with team detail
            self.content_container.content = team_detail_content
            self.content_container.update()

        return handle_click

    def load_data(self):
        try:
            token = self.page.session.get("auth_token")
            headers = {"Authorization": f"Bearer {token}"} if token else {}
            response = requests.get(get_team, headers=headers)
            response.raise_for_status()
            data = response.json()

            self.controls = [self.controls[0]]

            if not data:
                self.controls.append(ft.Text("No data available", size=16, color=defaultFontColor))
                self.update()
                return

            scroll_container = ft.Container(
                bgcolor=ft.colors.BLUE_300,
                content=self.create_list_teams(data),
                height=600, # Set the desired height for the scrollable container
                border=ft.border.all(1, ft.colors.WHITE70),
                border_radius=ft.border_radius.all(5),
            )

            self.controls.append(scroll_container)
            self.update()

        except requests.RequestException as e:
            self.controls.append(ft.Text(f"Error fetching data: {str(e)}", size=16, color=defaultFontColor))
            self.update()

        except Exception as e:
            self.controls.append(ft.Text(f"An error occurred: {str(e)}", size=16, color=defaultFontColor))
            self.update()


class NHLTeamDetailContent(ft.Column):
    def __init__(self, page: ft.Page, team_id: int):
        super().__init__()
        self.page = page
        self.team_id = team_id
        self.team_data = None
        self.scroll = ft.ScrollMode.AUTO
        self.expand = True
        self.spacing = 10

        # Инициализация элементов UI
        self.back_button = ft.IconButton(
            icon=ft.icons.ARROW_BACK,
            on_click=self.go_back_to_teams,
            icon_color=defaultFontColor
        )

        self.title_text = ft.Text("Загрузка информации о команде...", size=20, color=defaultFontColor)
        self.loading_indicator = ft.ProgressRing()

        # Элементы заголовка
        self.team_logo = ft.Image(
            width=100,
            height=100,
            border_radius=ft.border_radius.all(10))

        self.team_name = ft.Text(size=28, weight=ft.FontWeight.BOLD, color=defaultFontColor)
        self.team_conference = ft.Text(size=16, color=defaultFontColor)
        self.team_division = ft.Text(size=16, color=defaultFontColor)

        # Вкладки
        self.tabs = ft.Tabs(expand=True)
        self.roster_tab_content = ft.Container(padding=10)
        self.schedule_tab_content = ft.Container(padding=10)

        # Инициализация элементов управления
        self.controls = [
            ft.Row(
                controls=[self.back_button, self.title_text],
                alignment=ft.MainAxisAlignment.START
            ),
            self.loading_indicator
        ]

        # Начало загрузки данных
        self.load_team_data()

    def go_back_to_teams(self, e):
        # Возврат к предыдущему виду
        self.page.views.pop()
        self.page.update()

    def load_team_data(self):
        # Используем threading для избежания блокировки UI
        import threading
        threading.Thread(target=self._load_data_thread, daemon=True).start()

    def _load_data_thread(self):
        try:
            token = self.page.session.get("auth_token")
            headers = {"Authorization": f"Bearer {token}"} if token else {}

            # Загрузка информации о команде
            team_response = requests.get(
                f"{HOST}/app/nhl/team/{self.team_id}",
                headers=headers
            )
            team_response.raise_for_status()
            team_data = team_response.json()

            # Загрузка данных о составе
            roster_response = requests.get(
                f"{HOST}/app/nhl/team/{self.team_id}/roster",
                headers=headers
            )
            roster_response.raise_for_status()
            roster_data = roster_response.json()

            # Загрузка данных расписания
            try:
                schedule_response = requests.get(
                    f"{HOST}/app/nhl/schedule/last/10",
                    headers=headers
                )
                schedule_response.raise_for_status()
                schedule_data = schedule_response.json()

                # Фильтрация расписания только для текущей команды
                if isinstance(schedule_data, list):
                    filtered_schedule = [
                        game for game in schedule_data
                        if isinstance(game, dict) and
                           (game.get('home_team') == team_data.get('name') or
                            game.get('visitor_team') == team_data.get('name'))
                    ]  # Правильно закрыты все скобки
                    schedule_data = filtered_schedule

            except requests.RequestException as e:
                schedule_data = []

            # Обновление UI
            self._update_ui(team_data, roster_data, schedule_data)

        except requests.RequestException as e:
            self.show_error_message(f"Ошибка загрузки данных: {str(e)}")
        except Exception as e:
            self.show_error_message(f"Произошла ошибка: {str(e)}")

    def _update_ui(self, team_data: dict, roster_data: list, schedule_data: list):
        self.team_data = team_data

        # Обновление заголовка
        self.team_logo.src = team_data.get('img_url', '')
        self.team_name.value = team_data.get('name', 'Неизвестная команда')
        self.team_conference.value = f"{team_data.get('conference', 'Неизвестная')} конференция"
        self.team_division.value = f"Дивизион: {team_data.get('division', 'Неизвестный')}"

        # Создание строки заголовка
        header = ft.Row(
            controls=[
                self.team_logo,
                ft.Column(
                    controls=[
                        self.team_name,
                        self.team_conference,
                        self.team_division,
                    ],
                    spacing=5
                )
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.START,
        )

        # Обновление вкладки состава
        self.roster_tab_content.content = self._create_roster_section(roster_data)

        # Обновление вкладки расписания
        self.schedule_tab_content.content = self._create_schedule_section(schedule_data)

        # Настройка вкладок
        self.tabs.tabs = [
            ft.Tab(
                text="Состав",
                content=self.roster_tab_content,
            ),
            ft.Tab(
                text="Календарь",
                content=self.schedule_tab_content
            )
        ]

        # Обновление основных элементов управления
        self.controls = [
            ft.Row(
                controls=[self.back_button, ft.Text(team_data.get('name', 'Команда'), size=20, color=defaultFontColor)],
                alignment=ft.MainAxisAlignment.START
            ),
            ft.Divider(height=10, color=secondaryBgColor),
            header,
            ft.Divider(height=20, color=secondaryBgColor),
            self.tabs
        ]

        self.update()

    def show_error_message(self, message: str):
        self.controls = [
            ft.Row(
                controls=[
                    self.back_button,
                    ft.Text("Ошибка", size=20, color=defaultFontColor)
                ],
                alignment=ft.MainAxisAlignment.START
            ),
            ft.Text(message, size=16, color=ft.colors.RED_400)
        ]
        self.update()

    def _create_roster_section(self, roster_data: list) -> ft.Column:
        if not roster_data or not isinstance(roster_data, dict) or 'roster' not in roster_data:
            return ft.Column(
                controls=[ft.Text("Нет данных о составе команды", size=16, color=defaultFontColor)],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )

        players = roster_data['roster']
        if not players:
            return ft.Column(
                controls=[ft.Text("Нет данных о составе команды", size=16, color=defaultFontColor)],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )

        roster_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("№", weight=ft.FontWeight.BOLD, color=defaultFontColor)),
                ft.DataColumn(ft.Text("Игрок", weight=ft.FontWeight.BOLD, color=defaultFontColor)),
                ft.DataColumn(ft.Text("Позиция", weight=ft.FontWeight.BOLD, color=defaultFontColor)),
                ft.DataColumn(ft.Text("Рук.", weight=ft.FontWeight.BOLD, color=defaultFontColor)),
                ft.DataColumn(ft.Text("Возраст", weight=ft.FontWeight.BOLD, color=defaultFontColor)),
                ft.DataColumn(ft.Text("Статус", weight=ft.FontWeight.BOLD, color=defaultFontColor)),
            ],
            rows=[],
            heading_row_color=ft.colors.GREY_700,
            column_spacing=20,
            bgcolor=ft.colors.GREY_800,
        )

        for player in players:
            if not isinstance(player, dict):
                continue

            full_name = f"{player.get('surname', '')} {player.get('name', '')}"
            status = "Травма" if player.get('injured', False) else "Активен"

            roster_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(player.get('number', '')), color=defaultFontColor)),
                        ft.DataCell(ft.Text(full_name, color=defaultFontColor)),
                        ft.DataCell(ft.Text(player.get('position', ''), color=defaultFontColor)),
                        ft.DataCell(ft.Text(player.get('s/f', ''), color=defaultFontColor)),
                        ft.DataCell(ft.Text(str(player.get('age', '')), color=defaultFontColor)),
                        ft.DataCell(
                            ft.Text(
                                status,
                                color=ft.colors.RED if player.get('injured', False) else ft.colors.GREEN
                            )
                        ),
                    ]
                )
            )

        return ft.Column(
            controls=[
                ft.Text(f"Состав команды ({len(players)} игроков)", size=18, color=defaultFontColor),
                ft.Container(
                    content=roster_table,
                    border=ft.border.all(1, ft.colors.WHITE24),
                    border_radius=ft.border_radius.all(5),
                    padding=10,
                    bgcolor=ft.colors.GREY_800,
                )
            ],
            spacing=10
        )

    def _create_schedule_section(self, schedule_data: list) -> ft.Column:
        if not schedule_data or not isinstance(schedule_data, list):
            return ft.Column(
                controls=[ft.Text("Нет данных о календаре команды", size=16, color=defaultFontColor)],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )

        russian_weekdays = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        russian_months = [
            "янв", "фев", "мар", "апр", "мая", "июн",
            "июл", "авг", "сен", "окт", "ноя", "дек"
        ]

        schedule_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Дата", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Соперник", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Счет", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Место", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Статус", weight=ft.FontWeight.BOLD)),
            ],
            rows=[],
            heading_row_color=ft.colors.BLUE_GREY_100,
        )

        for game in schedule_data:
            if not isinstance(game, dict):
                continue

            # Обработка даты
            try:
                date_str = game.get('date_game', '')
                if date_str:
                    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
                    weekday = russian_weekdays[date_obj.weekday()]
                    month = russian_months[date_obj.month - 1]
                    game_date = f"{weekday}, {date_obj.day} {month}"
                else:
                    game_date = "TBD"
            except:
                game_date = "TBD"

            # Обработка времени
            try:
                time_str = "TBD"
                if 'time_game' in game and game['time_game']:
                    time_str = game['time_game'][11:16]
                elif date_str:
                    time_obj = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
                    time_str = time_obj.strftime("%H:%M")
            except:
                time_str = "TBD"

            # Определение соперника и места проведения
            is_home = False
            opponent = "TBD"
            if self.team_data:
                team_name = self.team_data.get('name', '')
                home_team = game.get('home_team', '')
                visitor_team = game.get('visitor_team', '')

                is_home = home_team == team_name
                opponent = visitor_team if is_home else home_team

            location = "Дома" if is_home else "В гостях"

            # Обработка счета и результата
            home_score = game.get('home_score')
            visitor_score = game.get('visitor_score')

            if home_score is not None and visitor_score is not None:
                if is_home:
                    score = f"{home_score}-{visitor_score}"
                    win = home_score > visitor_score
                else:
                    score = f"{visitor_score}-{home_score}"
                    win = visitor_score > home_score

                result = "Победа" if win else "Поражение"
                if home_score == visitor_score:
                    result = "Ничья"

                if game.get("is_overtime", False):
                    result += " (ОТ)"
            else:
                score = "vs"
                result = "Запланирован"

            schedule_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(f"{game_date} {time_str}", color=defaultFontColor)),
                        ft.DataCell(ft.Text(opponent, color=defaultFontColor)),
                        ft.DataCell(ft.Text(score, color=defaultFontColor)),
                        ft.DataCell(ft.Text(location, color=defaultFontColor)),
                        ft.DataCell(
                            ft.Text(
                                result,
                                color=ft.colors.GREEN if "Победа" in result else
                                ft.colors.RED if "Поражение" in result else
                                ft.colors.YELLOW
                            )
                        ),
                    ]
                )
            )

        return ft.Column(
            controls=[
                ft.Text("Последние матчи", size=18, color=defaultFontColor),
                ft.Container(
                    content=schedule_table,
                    border=ft.border.all(1, ft.colors.WHITE24),
                    border_radius=ft.border_radius.all(5),
                    padding=10,
                )
            ],
            spacing=10
        )

class NHLRosterContent(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.scroll = ft.ScrollMode.AUTO
        self.expand = True
        self.spacing = 10
        self.team_tabs = ft.Tabs(expand=True)

        self.controls = [
            ft.Text("Состав команд", size=24, color=defaultFontColor),
            ft.ProgressRing(),
        ]

    def did_mount(self):
        self.load_roster_data()

    def create_roster_list(self, roster_data: list) -> ft.Tabs:
        if not roster_data:
            return ft.Tabs()

        tabs = []

        for team in roster_data:
            if not team or 'roster' not in team or not team['roster']:
                continue

            players_table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("№", color=defaultFontColor)),
                    ft.DataColumn(ft.Text("Игрок", color=defaultFontColor)),
                    ft.DataColumn(ft.Text("Поз.", color=defaultFontColor)),
                    ft.DataColumn(ft.Text("Рук.", color=defaultFontColor)),
                    ft.DataColumn(ft.Text("Возр.", color=defaultFontColor)),
                    ft.DataColumn(ft.Text("Статус", color=defaultFontColor)),
                ],
                rows=[],
                heading_row_color=ft.colors.BLACK38,
                column_spacing=20,
            )

            for player in team['roster']:
                if not player:
                    continue

                full_name = f"{player['surname']} {player['name']}"
                status = "Травма" if player['injured'] else "Активен"

                players_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(player['number'], color=defaultFontColor)),
                            ft.DataCell(ft.Text(full_name, color=defaultFontColor)),
                            ft.DataCell(ft.Text(player['position'], color=defaultFontColor)),
                            ft.DataCell(ft.Text(player['s/f'], color=defaultFontColor)),
                            ft.DataCell(ft.Text(player['age'], color=defaultFontColor)),
                            ft.DataCell(
                                ft.Text(status, color=ft.colors.RED if player['injured'] else ft.colors.GREEN)
                            ),
                        ]
                    )
                )

            # Calculate player count
            player_count = len(team['roster'])

            tab_content = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(f"Всего игроков: {player_count}", size=16, color=defaultFontColor),
                        ft.Container(
                            content=ft.Column(
                                [players_table],
                                scroll=ft.ScrollMode.AUTO,
                                expand=True,
                            ),
                            expand=True,
                            padding=10,
                        )
                    ],
                    expand=True,
                ),
                expand=True,
            )

            tabs.append(
                ft.Tab(
                    text=team['name'],
                    content=tab_content
                )
            )

        self.team_tabs.tabs = tabs
        return self.team_tabs

    def load_roster_data(self):
        try:
            token = self.page.session.get("auth_token")
            headers = {"Authorization": f"Bearer {token}"} if token else {}
            response = requests.get(get_all_roster, headers=headers)
            response.raise_for_status()
            data = response.json()

            self.controls = [self.controls[0]]  # Keep the title

            if not data:
                self.controls.append(ft.Text("Нет данных о составе", size=16, color=defaultFontColor))
                self.update()
                return

            scroll_container = ft.Container(
                bgcolor=ft.colors.BLUE_800,
                content=self.create_roster_list(data),
                height=600,
                border=ft.border.all(1, ft.colors.WHITE70),
                border_radius=ft.border_radius.all(5),
            )

            self.controls.append(scroll_container)
            self.update()

        except requests.RequestException as e:
            self.controls.append(ft.Text(f"Ошибка загрузки данных: {str(e)}", size=16, color=defaultFontColor))
            self.update()

        except Exception as e:
            self.controls.append(ft.Text(f"Произошла ошибка: {str(e)}", size=16, color=defaultFontColor))
            self.update()



class NHLScheduleContent(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.scroll = ft.ScrollMode.AUTO
        self.expand = True
        self.spacing = 10
        self.controls = [
            ft.Text("Main Schedule Dashboard Content", size=24, color=defaultFontColor),
            ft.ProgressRing(),
        ]

    def did_mount(self):
        # TODO: DELETE THIS
        # self.load_data_from_json()
        self.load_data()

    def load_data(self):
        try:
            token = self.page.session.get("auth_token")
            headers = {"Authorization": f"Bearer {token}"} if token else {}
            response = requests.get(
                get_schedule,
                headers=headers
            )
            response.raise_for_status()
            data = response.json()

            self.controls = [self.controls[0]]

            if not data:
                self.controls.append(ft.Text("No data available", size=16, color=defaultFontColor))
                self.update()
                return

            schedule_table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Date")),
                    ft.DataColumn(ft.Text("Time")),
                    ft.DataColumn(ft.Text("Visitor Team")),
                    ft.DataColumn(ft.Text("Home Team")),
                    ft.DataColumn(ft.Text("Visitor Score")),
                    ft.DataColumn(ft.Text("Home Score")),
                    ft.DataColumn(ft.Text("OT")),
                ],
                rows=[],
            )

            russian_weekdays = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
            russian_months = [
                "янв", "фев", "мар", "апр", "мая", "июн",
                "июл", "авг", "сен", "окт", "ноя", "дек"
            ]

            for game in data:
                try:
                    date_obj = datetime.datetime.strptime(game['date_game'], "%Y-%m-%dT%H:%M:%SZ")
                    weekday = russian_weekdays[date_obj.weekday()]
                    month = russian_months[date_obj.month - 1]
                    game_date = f"{weekday}, {date_obj.day} {month} {date_obj.year}"
                except:
                    game_date = game['date_game']

                try:
                    if 'time_game' in game and game['time_game']:
                        time_str = game['time_game'][11:16]  # ("19:30")
                    else:
                        time_obj = datetime.datetime.strptime(game['date_game'], "%Y-%m-%dT%H:%M:%SZ")
                        time_str = time_obj.strftime("%H:%M")
                except Exception as e:
                    print(f"Error parsing time: {e}")
                    time_str = "TBD"

                visitor_score = game['visitor_score'] if game['visitor_score'] is not None else "-"
                home_score = game['home_score'] if game['home_score'] is not None else "-"

                schedule_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(game_date)),
                            ft.DataCell(ft.Text(time_str)),
                            ft.DataCell(ft.Text(game['visitor_team'])),
                            ft.DataCell(ft.Text(game['home_team'])),
                            ft.DataCell(ft.Text(visitor_score)),
                            ft.DataCell(ft.Text(home_score)),
                            ft.DataCell(ft.Text("OT" if game["is_overtime"] else "-")),
                        ]
                    )
                )

            scroll_container = ft.Container(
                bgcolor=ft.colors.RED_300,
                content=schedule_table,
                # height=600, # Set the desired height for the scrollable container
                expand=True,
                border=ft.border.all(1, ft.colors.WHITE70),
                border_radius=ft.border_radius.all(5),
            )

            self.controls.append(scroll_container)
            self.update()


        except requests.RequestException as e:
            self.controls.append(ft.Text(f"Error fetching data: {str(e)}", size=16, color=defaultFontColor))
            self.update()

        except Exception as e:
            self.controls.append(ft.Text(f"An error occurred: {str(e)}", size=16, color=defaultFontColor))
            self.update()


class NHLMainPageUI:
    def __init__(self, page: ft.Page):
        self.page = page
        self.current_content = None
        self.content_container = ft.Container(expand=True)

        self.logo = ft.Container(
            padding=ft.padding.symmetric(17, 13),
            content=ft.Row(
                controls=[
                    ft.Image(src='assets/images/icon.ico', width=45, height=32, fit=ft.ImageFit.FILL),
                    ft.Text('SportThunder', expand=True, color=defaultFontColor, font_family='cuprum', size=16),
                ],
                alignment=ft.MainAxisAlignment.START,
            )
        )

        style_menu = ft.ButtonStyle(
            color={
                ft.MaterialState.HOVERED: ft.colors.WHITE,
                ft.MaterialState.DEFAULT: ft.colors.random_color()
            },
            icon_size=14,
            overlay_color=hoverBgColor,
            shadow_color=hoverBgColor
        )

        # Create sidebar with navigation buttons
        self.sidebar_menu = ft.Container(
            padding=ft.padding.symmetric(0, 13),
            content=ft.Column(
                controls=[
                    ft.Text('Menu', color=defaultFontColor, font_family='cuprum', size=12),
                    ft.TextButton(
                        "Main",
                        icon=ft.icons.SPACE_DASHBOARD_ROUNDED,
                        style=style_menu,
                        on_click=self.show_main_content
                    ),
                    ft.TextButton(
                        "Teams",
                        icon=ft.icons.GROUPS,
                        style=style_menu,
                        on_click=self.show_teams_content
                    ),
                    ft.TextButton(
                        "Roster",
                        icon=ft.icons.PERSON_SEARCH,
                        style=style_menu,
                        on_click=self.show_roster_content
                    ),
                    ft.TextButton(
                        "Schedule",
                        icon=ft.icons.CALENDAR_MONTH,
                        style=style_menu,
                        on_click=self.show_schedule_content
                    )
                ]
            )
        )

        self.header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text("Панель управления", color=defaultBgColor, size=20, font_family='cuprum'),
                    ft.Row(
                        controls=[
                            ft.CircleAvatar(
                                foreground_image_url='assets/images/undefined.jpg',
                                content=ft.Text('A'),
                            ),
                            ft.IconButton(
                                icon=ft.icons.NOTIFICATIONS_ROUNDED,
                                icon_size=20,
                                tooltip="Notifications",
                                style=ft.ButtonStyle(
                                    overlay_color=hoverBgColor,
                                    color=defaultFontColor
                                ),
                            ),
                            ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                icon_size = 20,
                                tooltip="Arrow",
                                style=ft.ButtonStyle(
                                    overlay_color=hoverBgColor,
                                    color=defaultFontColor
                                ),
                                on_click=lambda e: self.page.go("/welcome") # TODO:MAYBE check token
                            ),
                            ft.IconButton(
                                icon=ft.icons.EXIT_TO_APP,
                                icon_size=20,
                                tooltip="Arrow",
                                style=ft.ButtonStyle(
                                    overlay_color=hoverBgColor,
                                    color=defaultFontColor
                                ),
                                on_click=lambda e: self.page.window_destroy()
                            )
                        ],
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        )

    # Navigation handlers - changed to synchronous
    def show_main_content(self, e):
        self.content_container.content = NHLMainContent(self.page)
        self.content_container.update()

    def show_teams_content(self, e):
        self.content_container.content = NHLTeamsContent(self.page, self.content_container)
        self.content_container.update()

    def show_roster_content(self, e):
        self.content_container.content = NHLRosterContent(self.page)
        self.content_container.update()

    def show_schedule_content(self, e):
        self.content_container.content = NHLScheduleContent(self.page)
        self.content_container.update()

    def create_view(self) -> ft.View:
        # Set default content
        self.content_container.content = NHLMainContent(self.page)

        return ft.View(
            "/mainNhl",
            controls=[
                ft.Row(
                    expand=True,
                    spacing=0,
                    controls=[
                        # left panel
                        ft.Container(
                            expand=1,
                            content=ft.Column(
                                spacing=0,
                                controls=[
                                    self.logo,
                                    self.sidebar_menu
                                ]
                            ),
                            bgcolor=secondaryBgColor,
                        ),
                        # right panel
                        ft.Container(
                            expand=4,
                            padding=ft.padding.symmetric(15, 10),
                            content=ft.Column(
                                spacing=0,
                                controls=[
                                    self.header,
                                    self.content_container
                                ]
                            )
                        )
                    ]
                )
            ],
            bgcolor=defaultBgColor,
            padding=0,
        )


class NHLMainPage:
    def __init__(self):
        self.ui = None

    def view(self, page: ft.Page, params: Params, basket: Basket) -> ft.View:
        self.ui = NHLMainPageUI(page)
        page.title = "NHL"
        page.window_width = defaultWidthWindow
        page.window_height = defaultHeightWindow
        page.window_min_width = 1000
        page.window_min_height = 600
        page.fonts = {
            "Special Elite": "../assets/fonts/specialelite-cyrillic.ttf",
            "cuprum": "../assets/fonts/cuprum.ttf"
        }

        page.theme = ft.Theme(font_family="cuprum")

        return self.ui.create_view()