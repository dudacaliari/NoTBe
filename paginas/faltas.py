import flet as ft
from database import get_all_materias, update_faltas

def FaltasView(page: ft.Page):
    materias = get_all_materias()
    faltas_list = ft.Column(controls=[], spacing=10)

    def add_falta(e, materia_id, faltas):
        faltas += 1
        update_faltas(materia_id, faltas)
        refresh_view()

    def remove_falta(e, materia_id, faltas):
        if faltas > 0:
            faltas -= 1
            update_faltas(materia_id, faltas)
        refresh_view()

    def refresh_view():
        materias = get_all_materias()
        faltas_list.controls.clear()
        for materia in materias:
            materia_id, nome, media_minima, media_atual, nota_necessaria, faltas = materia
            faltas_list.controls.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(f"{nome}: {faltas} faltas", weight=ft.FontWeight.BOLD, color="#45287a"),
                            ft.IconButton(icon=ft.icons.ADD, on_click=lambda e, id=materia_id, f=faltas: add_falta(e, id, f), bgcolor="#D7BDE2"),
                            ft.IconButton(icon=ft.icons.REMOVE, on_click=lambda e, id=materia_id, f=faltas: remove_falta(e, id, f), bgcolor="#D7BDE2")
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        spacing=10
                    ),
                    margin=ft.Margin(left=0, top=0, right=0, bottom=10),
                    bgcolor="#F9F9F9",
                    border_radius=8
                )
            )
        page.update()

    refresh_view()

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
                            style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                            color="#45287a"
                        ),
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
                        ft.IconButton(icon=ft.icons.HOME, on_click=lambda _: page.go("/home")),
                        ft.IconButton(icon=ft.icons.ALARM, on_click=lambda _: page.go("/faltas")),
                        ft.IconButton(icon=ft.icons.EVENT, on_click=lambda _: page.go("/calendario"))
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND
                ),
                padding=10
            )
        ]
    )
