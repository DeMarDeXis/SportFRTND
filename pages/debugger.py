import flet as ft
from customControls.notification_signup import SignUpNotification


async def main(page: ft.Page):
    page.title = "SignUpNotification Test"

    notification = SignUpNotification("Test Notification", "🚀", duration=4000)

    async def show_notification(e):
        page.add(notification)
        await notification.show_notification()
        page.update()

    page.add(
        ft.ElevatedButton("Show Notification", on_click=show_notification)
    )


ft.app(target=main)
