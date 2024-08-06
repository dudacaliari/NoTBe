import flet as ft
from database import get_all_materias, update_faltas

def FaltasView(page: ft.Page):
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
                    content=ft.Column(
                        controls=[
                            ft.Text(nome, size=18, color="#9CA1BA"),
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Column(
                                            controls=[
                                                ft.Text("Faltas", color="#8F8F8F"),
                                                ft.Container(
                                                    content=ft.Text(f"{faltas}", size=16, color="#8F8F8F"),
                                                    width=80,
                                                    height=40,
                                                    bgcolor="#F7EDFF",
                                                    border_radius=25,
                                                    alignment=ft.Alignment(0, 0)
                                                )
                                            ]
                                        ),
                                        ft.Column(
                                            controls=[
                                                ft.IconButton(
                                                    icon=ft.icons.ADD,
                                                    icon_color="#FFFFFF",
                                                    on_click=lambda e, id=materia_id, f=faltas: add_falta(e, id, f),
                                                    bgcolor="#D7BDE2"
                                                ),
                                                ft.IconButton(
                                                    icon=ft.icons.REMOVE,
                                                    icon_color="#FFFFFF",
                                                    on_click=lambda e, id=materia_id, f=faltas: remove_falta(e, id, f),
                                                    bgcolor="#D7BDE2",
                                                )
                                            ]
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    spacing=10
                                ),
                                padding=10,
                                margin=10,
                                bgcolor="#E0E0F9",
                                border_radius=8
                            )
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=10  # Espaçamento interno dos controles do card
                    ),
                    padding=10,
                    margin=0,  # Espaçamento entre os cards
                    border_radius=8,
                    height=page.window_height * 0.25,
                )
            )
        page.update()

    faltas_list = ft.ListView(expand=True)  # Removido o spacing do ListView

    refresh_view()

    return ft.View(
        "/faltas",
        [
            ft.Container(
                width=page.window.width,
                height=page.window.height,
                gradient=ft.LinearGradient(
                    colors=["#F5F5F5", "#ffffff"],
                    begin=ft.Alignment(-1, -1),
                    end=ft.Alignment(1, 1)
                ),
                content=ft.Stack( 
                    controls=[
                        ft.Container(
                            width=page.window_width,
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        "Faltas",
                                        size=30,
                                        weight=ft.FontWeight.W_300,
                                        color="#7A7A7A"
                                    ),
                                    ft.Divider(color="#7A7A7A", thickness=2),
                                    ft.Container(
                                        content=faltas_list,
                                        height=page.window.height,
                                        expand=True,  # Permite que a lista se expanda
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                horizontal_alignment=ft.CrossAxisAlignment.START,
                                spacing=20,
                                height=page.window.height * 0.77,
                                expand=True  # Permite a expansão vertical do conteúdo
                            ),
                            padding=20
                        )
                    ]
                )
            ),
            ft.BottomAppBar(
                content=ft.Row(
                    controls=[
                        ft.IconButton(icon=ft.icons.ALARM, icon_color="#5e4e69", bgcolor="#c5a4de", on_click=lambda _: page.go("/faltas")),
                        ft.IconButton(icon=ft.icons.HOME, icon_color="#785494", on_click=lambda _: page.go("/home")),
                        ft.IconButton(icon=ft.icons.EVENT, icon_color="#785494", on_click=lambda _: page.go("/calendario"))
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND
                ),
                bgcolor="#dec5f0",
                padding=10,
            )
        ]
    )
