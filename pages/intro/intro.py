import random
import flet as ft
from flet_route import Params, Basket
from internal.lib.style.style import *
from typing import Callable, Optional

class IntroVideoUI:
    def __init__(self, handle_volume_change: Callable, handle_playback_rate_change: Callable,
                 handle_pause: Callable, handle_play_or_pause: Callable,
                 handle_play: Callable, handle_stop: Callable,
                 handle_next: Callable, handle_previous: Callable, handle_seek: Callable,
                 handle_add_media: Callable, handle_remove_media: Callable, handle_jump: Callable):
        self.sample_media = [
            ft.VideoMedia(
                # "https://user-images.githubusercontent.com/28951144/229373720-14d69157-1a56-4a78-a2f4-d7a134d7c3e9.mp4"
                "C:/Users/User/Documents/GitHub/TrainerForDiplom/ClientDiplom/assets/images/san-jose.mp4"
            ),
            ft.VideoMedia(
                # "https://user-images.githubusercontent.com/28951144/229373718-86ce5e1d-d195-45d5-baa6-ef94041d0b90.mp4"
                "C:/Users/User/Documents/GitHub/TrainerForDiplom/ClientDiplom/assets/images/tampa-bay.mp4"
            ),
            # ft.VideoMedia(
            #     "https://user-images.githubusercontent.com/28951144/229373716-76da0a4e-225a-44e4-9ee7-3e9006dbc3e3.mp4"
            # ),
            # ft.VideoMedia(
            #     "https://user-images.githubusercontent.com/28951144/229373695-22f88f13-d18f-4288-9bf1-c3e078d83722.mp4"
            # ),
            ft.VideoMedia(
                "C:/Users/User/Documents/GitHub/TrainerForDiplom/ClientDiplom/assets/images/utah.mp4",
                extras={
                    "artist": "Thousand Foot Krutch",
                    "album": "The End Is Where We Begin",
                },
                http_headers={
                    "Foo": "Bar",
                    "Accept": "*/*",
                },
            ),
        ]

        self.video = ft.Video(
            expand=True,
            playlist=self.sample_media[0:2],
            playlist_mode=ft.PlaylistMode.LOOP,
            fill_color=ft.colors.BLUE_400,
            aspect_ratio=16/9,
            volume=100,
            autoplay=False,
            filter_quality=ft.FilterQuality.HIGH,
            muted=False,
            on_loaded=lambda e: print("Video loaded successfully!"),
            on_enter_fullscreen=lambda e: print("Video entered fullscreen!"),
            on_exit_fullscreen=lambda e: print("Video exited fullscreen!"),
        )

        self.volume = ft.Slider(
            min=0,
            value=100,
            max=100,
            label="Volume = {value}%",
            divisions=10,
            width=400,
            on_change=handle_volume_change,
        )

        self.playback_rate = ft.Slider(
            min=1,
            value=1,
            max=3,
            label="PlaybackRate = {value}X",
            divisions=6,
            width=400,
            on_change=handle_playback_rate_change,
        )

        self.button_play = ft.ElevatedButton("Play", on_click=handle_play)
        self.button_pause = ft.ElevatedButton("Pause", on_click=handle_pause)
        self.button_play_or_pause = ft.ElevatedButton("Play Or Pause", on_click=handle_play_or_pause)
        self.button_stop = ft.ElevatedButton("Stop", on_click=handle_stop)
        self.button_next = ft.ElevatedButton("Next", on_click=handle_next)
        self.button_previous = ft.ElevatedButton("Previous", on_click=handle_previous)
        self.button_seek = ft.ElevatedButton("Seek s=10", on_click=handle_seek)
        self.button_jump_TfM = ft.ElevatedButton("Jump to first Media", on_click=handle_jump)
        self.button_play_ARanM = ft.ElevatedButton("Add Random Media", on_click=handle_add_media)
        self.button_play_RRanM = ft.ElevatedButton("Remove Random Media", on_click=handle_remove_media)

    def create_view(self) -> ft.View:
        return ft.View(
            route="/intro",
            controls=[
                self.video,
                ft.Row(
                    wrap=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        self.button_play,
                        self.button_pause,
                        self.button_play_or_pause,
                        self.button_stop,
                        self.button_next,
                        self.button_previous,
                        self.button_seek,
                        self.button_jump_TfM,
                        self.button_play_ARanM,
                        self.button_play_RRanM,
                    ],
                ),
                self.volume,
                self.playback_rate,
            ]
        )



class IntroVideoPage:
    def __init__(self, log):
        self.log = log
        self.page = Optional[ft.Page]
        self.ui = IntroVideoUI(
            handle_pause=self.handle_pause,
            handle_play=self.handle_play,
            handle_play_or_pause=self.handle_play_or_pause,
            handle_stop=self.handle_stop,
            handle_next=self.handle_next,
            handle_previous=self.handle_previous,
            handle_seek=self.handle_seek,
            handle_jump=self.handle_jump,
            handle_add_media=self.handle_add_media,
            handle_remove_media=self.handle_remove_media,
            handle_volume_change=self.handle_volume_change,
            handle_playback_rate_change=self.handle_playback_rate_change,
        )





    def handle_pause(self, e):
        self.ui.video.pause()
        print("Video.pause()")

    def handle_play_or_pause(self, e):
        self.ui.video.play_or_pause()
        print("Video.play_or_pause()")

    def handle_play(self, e):
        self.ui.video.play()
        print("Video.play()")

    def handle_stop(self, e):
        self.ui.video.stop()
        print("Video.stop()")

    def handle_next(self, e):
        self.ui.video.next()
        print("Video.next()")

    def handle_previous(self, e):
        self.ui.video.previous()
        print("Video.previous()")

    def handle_volume_change(self, e):
        self.ui.video.volume = e.control.value
        self.page.update()
        print(f"Video.volume = {e.control.value}")

    def handle_playback_rate_change(self, e):
        self.ui.video.playback_rate = e.control.value
        self.page.update()
        print(f"Video.playback_rate = {e.control.value}")

    def handle_seek(self, e):
        self.ui.video.seek(10000)
        print(f"Video.seek(10000)")

    def handle_add_media(self, e):
        self.ui.video.playlist_add(random.choice(self.ui.sample_media))
        print(f"Video.playlist_add(random.choice(sample_media))")

    def handle_remove_media(self, e):
        r = random.randint(0, len(self.ui.video.playlist) - 1)
        self.ui.video.playlist_remove(r)
        print(f"Popped Item at index: {r} (position {r+1})")

    def handle_jump(self, e):
        print(f"Video.jump_to(0)")
        self.ui.video.jump_to(0)

    def view(self, page: ft.Page, params: Params, basket: Basket):
        self.page = page
        page.title = "INTRO VIDEO"
        page.window.width = defaultWidthWindow
        page.window.height = defaultHeightWindow
        page.window.min_width = 800
        page.window.min_height = 400


        # page.fonts = {"Special Elite": "../assets/fonts/specialelite-cyrillic.ttf"}
        # page.theme_mode = ft.ThemeMode.DARK
        # page.window.always_on_top = True
        # page.spacing = 20
        # page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        view = self.ui.create_view()
        return view
