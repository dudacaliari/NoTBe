import flet as ft

def SplashView(page: ft.Page):
    return ft.View(
        "/",
        [
            ft.Container(
                width=page.window_width,
                height=page.window_height,
                gradient=ft.LinearGradient(
                    colors=["#885D9A", "#4B83A7"],
                    begin=ft.Alignment(-1, -1),
                    end=ft.Alignment(1, 1)
                ),
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "NoTBe",
                            style=ft.TextThemeStyle.HEADLINE_LARGE,
                            color=ft.colors.WHITE
                        ),
                        ft.Text(
                            "Note Tracker Beaver",
                            style=ft.TextThemeStyle.TITLE_MEDIUM,
                            color=ft.colors.WHITE
                        ),
                        ft.IconButton(
                            icon=ft.icons.ARROW_FORWARD,
                            on_click=lambda _: page.go("/home")
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20
                )
            )
        ]
    )
