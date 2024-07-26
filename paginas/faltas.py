import flet as ft

faltas = []

def FaltasView(page: ft.Page):
    falta_input = ft.TextField(label="Adicionar Falta")
    faltas_list = ft.ListView(controls=[], height=400, spacing=10)

    def add_falta(e):
        falta = falta_input.value
        if falta:
            faltas.append(falta)
            faltas_list.controls.append(ft.Text(falta))
            falta_input.value = ""
            page.update()

    return ft.View(
        "/faltas",
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
                            "Registro de Faltas",
                            style=ft.TextThemeStyle.HEADLINE_MEDIUM
                        ),
                        falta_input,
                        ft.ElevatedButton("Adicionar Falta", on_click=add_falta),
                        faltas_list
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
