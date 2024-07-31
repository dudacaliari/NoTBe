import flet as ft
from database import get_all_materias

def HomeView(page: ft.Page):
    def update_materias_list():
        materias_list.controls.clear()
        materias = get_all_materias()
        for materia in materias:
            media_minima = materia[2]
            media_atual = materia[3]
            nota_necessaria = materia[4]
            materia_card = ft.Container(
                content=ft.Column([
                    ft.Text(f"Nome: {materia[1]}", size=18),
                    ft.Text(f"Média Atual: {media_atual:.2f}", size=16),
                    ft.Text(f"Média Mínima: {media_minima:.2f}", size=16),
                    ft.Text(f"Nota Necessária (de acordo com os pesos restantes): {nota_necessaria:.2f}", size=16)
                ], spacing=5),
                padding=10,
                border_radius=10,
                bgcolor="#E3F2FD"
            )
            materias_list.controls.append(materia_card)
        page.update()

    materias_list = ft.ListView(controls=[], height=400, spacing=10)
    update_materias_list()  # Atualiza a lista de matérias ao carregar a página

    return ft.View(
        "/home",
        [
            ft.Container(
                width=page.window.width,
                height=page.window.height,
                gradient=ft.LinearGradient(
                    colors=["#F5F5F5", "#ffffff"],
                    begin=ft.Alignment(-1, -1),
                    end=ft.Alignment(1, 1)
                ),
                content=ft.Column(
                    controls=[
                        ft.Text("Matérias", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                        materias_list,
                        ft.ElevatedButton("Adicionar Matéria", on_click=lambda _: page.go("/materias")),
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
