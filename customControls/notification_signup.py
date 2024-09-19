import flet as ft
import asyncio

class SignUpNotification(ft.UserControl):
    def __init__(self, message: str, emoji: str, duration: int = 4000):
        super().__init__()
        self.message = message
        self.emoji = emoji
        self.duration = duration
        self.offset = ft.transform.Offset(0, -1)

    def build(self):
        return ft.Container(
            content=ft.Row([
                ft.Text(self.emoji, size=24),
                ft.Text(self.message),
            ]),
            bgcolor=ft.colors.GREEN_100,
            padding=10,
            border_radius=8,
            offset=self.offset,
            animate_offset=ft.animation.Animation(1000, ft.AnimationCurve.EASE_IN_OUT),
        )

    async def show_notification(self):
        self.offset = ft.transform.Offset(0, 0)
        await self.update_async()
        await asyncio.sleep(self.duration / 1000)
        await self.hide_notification()

    async def hide_notification(self):
        self.offset = ft.transform.Offset(0, -1)
        await self.update_async()

