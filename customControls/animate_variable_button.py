import flet
from flet import *
import time
from typing import Callable, Optional

class AnimatedIconButton(Container):
    def __init__(self, icon, on_click, selected=False):
        super().__init__()
        self.icon = icon
        self.selected = selected
        self.on_click = on_click
        self.content = self.build()

    def build(self):
        return IconButton(
            icon=self.icon,
            icon_size=32,
            icon_color="white" if self.selected else "white54",
            selected=self.selected,
            on_click=self.handle_click,
        )

    def handle_click(self, e):
        self.animate_icon()
        if self.on_click:
            self.on_click(e)

    def animate_icon(self):
        self.scale = transform.Scale(0.65)
        self.update()
        time.sleep(0.15)
        self.scale = transform.Scale(1)
        self.update()
        self.content.selected = True
        self.content.icon_color = "white"
        self.update()


class AnimatedIconsUI(Container):
    def __init__(self, on_exit_click: Callable):
        super().__init__()
        self.on_exit_click = on_exit_click
        self.icon_list = [
            (icons.FAVORITE_ROUNDED, self.on_favourite_click),
            (icons.PERSON_ADD, self.on_person_add_click),
            (icons.EXIT_TO_APP, self.on_exit_click),
            (icons.NOTIFICATION_ADD_ROUNDED, self.on_bell_click),
            (icons.SEARCH_ROUNDED, self.on_notification_click),
        ]
        self.content = self.build()

    def build(self):
        main_row = Row(alignment=MainAxisAlignment.CENTER)
        for icon, on_click in self.icon_list:
            button = AnimatedIconButton(icon, on_click, selected=(icon == icons.DISCORD_ROUNDED))
            main_row.controls.append(button)

        return Container(
            width=580,
            height=260,
            rotate=transform.Rotate(0, alignment=alignment.center),
            animate_rotation=animation.Animation(duration=500, curve=AnimationCurve.DECELERATE),
            border_radius=35,
            bgcolor="black",
            alignment=alignment.bottom_center,
            padding=20,
            content=Column(
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[main_row],
            ),
        )

    def on_favourite_click(self, e):
        print("Discord button clicked")

    def on_person_add_click(self, e):
        print("Person Add button clicked")

    def on_bell_click(self, e):
        print("Bell button clicked")

    def on_notification_click(self, e):
        print("Notification button clicked")

class AnimatedIcons(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.ui = AnimatedIconsUI(self.on_exit_click)
        self.content = self.build()

    def on_exit_click(self, e):
        self.page.window_destroy()

    # def build(self):
    #     return Container(
    #         width=1400,
    #         height=800,
    #         gradient=LinearGradient(
    #             begin=alignment.bottom_left,
    #             end=alignment.top_right,
    #             colors=["blue800", "blue100"],
    #         ),
    #         padding=50,
    #         content=Column(
    #             alignment=MainAxisAlignment.END,
    #             horizontal_alignment=CrossAxisAlignment.CENTER,
    #             controls=[self.ui],
    #         ),
    #     )

    def build(self):
        return Container(
            width=580/1.5,
            height=260/1.5,
            bgcolor="black",
            border_radius=35,
            padding=20/2,
            content=self.ui,
        )

# def main(page: Page):
#     page.title = "Flet Animated Icons"
#     page.horizontal_alignment = "center"
#     page.vertical_alignment = "center"
#     page.add(AnimatedIcons())
#
# if __name__ == "__main__":
#     flet.app(target=main, view=AppView.FLET_APP)
