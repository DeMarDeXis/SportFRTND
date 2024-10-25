import flet as ft
from flet import (
    Container,
    animation,
    border,
    alignment,
    Text,
    Column,
    Row,
    colors,
    Card,
    transform,
)
from flet_core import MainAxisAlignment, CrossAxisAlignment, FontWeight
# from typing import Callable, Optional

class AnimatedCard:
    def __init__(self, title, desc, animate_text, image_source):
        self.img_src = image_source
        self.title = title
        self.desc = desc
        self.animate_text = animate_text
        self.create_ui()
        self.setup_event_handlers()

    def create_ui(self):
        self.icon_container = Container(
            width=120,
            height=35,
            bgcolor=colors.BLUE_800,
            border_radius=25,
            animate_opacity=200,
            offset=transform.Offset(0, 0.25),
            animate_offset=animation.Animation(duration=900, curve=ft.AnimationCurve.EASE),
            visible=False,
            content=Row(
                alignment=MainAxisAlignment.CENTER,
                vertical_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Text(
                        self.animate_text,
                        size=12,
                        weight=FontWeight.W_600,
                    ),
                ],
            ),
        )

        self.container = Container(
            width=280,
            height=380,
            bgcolor=colors.WHITE,
            border_radius=12,
            animate=animation.Animation(600, ft.AnimationCurve.EASE),
            border=border.all(2, colors.WHITE24),
            image_src=self.img_src,
            image_fit=ft.ImageFit.COVER,
            content=Column(
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.START,
                spacing=0,
                controls=[
                    Container(
                        padding=20,
                        alignment=alignment.bottom_center,
                        content=Text(
                            self.title,
                            color=colors.BLACK,
                            size=28,
                            weight=FontWeight.W_800,
                        ),
                    ),
                    Container(
                        padding=20,
                        alignment=alignment.top_center,
                        content=Text(
                            self.desc,
                            color=colors.BLACK,
                            size=14,
                            weight=FontWeight.W_500,
                        ),
                    ),
                ],
            ),
        )

        self.card = Card(
            elevation=0,
            content=Container(
                content=Column(
                    spacing=0,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        self.container,
                    ],
                ),
            ),
        )

        self.main_column = Column(
            horizontal_alignment=CrossAxisAlignment.CENTER,
            spacing=0,
            controls=[
                self.card,
                self.icon_container,
            ],
        )

    def setup_event_handlers(self):
        self.container.on_hover = self.animated_card_hover

    def animated_card_hover(self, e):
        self.icon_container.visible = True
        self.icon_container.update()

        if e.data == "true":
            for _ in range(20):
                self.card.elevation += 1
                self.card.update()

            self.container.border = border.all(4, colors.BLUE_800)
            self.container.update()

            self.icon_container.offset = transform.Offset(0, -0.75)
            self.icon_container.opacity = 1
            self.icon_container.update()
        else:
            for _ in range(20):
                self.card.elevation -= 1
                self.card.update()

            self.container.border = border.all(4, colors.WHITE24)
            self.container.update()

            self.icon_container.offset = transform.Offset(0, 0.5)
            self.icon_container.opacity = 0
            self.icon_container.update()

    def build(self):
        return self.main_column