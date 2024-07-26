import flet as ft

eventos = []

def CalendarioView(page: ft.Page):
    evento_input = ft.TextField(label="Adicionar Evento")
    eventos_list = ft.ListView(controls=[], height=400, spacing=10)

    def add_evento(e):
        evento = evento_input.value
        if evento:
            eventos.append(evento)
            eventos_list.controls.append(ft.Text(evento))
            evento_input.value = ""
            page.update()

    return ft.View(
        "/calendario",
        [
            ft.Container(
                width=page.window_width,
                height=page.window_height,
                gradient=ft.LinearGradient(
                    colors=["#F5F5F5", "#ffffff"],
                    begin=ft.Alignment(-1, -1),
                    end=ft.Alignment(1, 1)
                ),
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Calendário",
                            style=ft.TextThemeStyle.HEADLINE_MEDIUM
                        ),
                        evento_input,
                        ft.ElevatedButton("Adicionar Evento", on_click=add_evento),
                        eventos_list
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20
                ),
                padding=20
            ),
            ft.BottomAppBar(
                content=ft.Row(
                    controls=[
                        ft.IconButton(icon=ft.icons.HOME, on_click=lambda _: page.go("/")),
                        ft.IconButton(icon=ft.icons.NOTE, on_click=lambda _: page.go("/notas")),
                        ft.IconButton(icon=ft.icons.BOOK, on_click=lambda _: page.go("/materias")),
                        ft.IconButton(icon=ft.icons.ALARM, on_click=lambda _: page.go("/faltas")),
                        ft.IconButton(icon=ft.icons.EVENT, on_click=lambda _: page.go("/calendario"))
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND
                ),
                padding=10
            )
        ]
    )
