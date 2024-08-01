import flet as ft
from database import get_all_materias, delete_materia

def HomeView(page: ft.Page):
    def update_materias_list():
        materias_list.controls.clear()
        materias = get_all_materias()
        for materia in materias:
            materia_card = ft.Container(
                content=ft.Column([
                    ft.Text(f"Nome: {materia[1]}", size=18),
                    ft.Text(f"Média Atual: {materia[3]:.2f}", size=16),
                    ft.Text(f"Média Mínima: {materia[2]:.2f}", size=16),
                    ft.Text(f"Nota Necessária: {materia[4]:.2f}", size=16),
                    ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, materia_id=materia[0]: confirm_delete_materia(materia_id)),
                    ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e, materia_id=materia[0]: edit_materia_view(materia_id))
                ]),
                padding=10,
                margin=10,
                bgcolor="#f0f0f0",
                border_radius=10
            )
            materias_list.controls.append(materia_card)
        page.update()

    def edit_materia_view(materia_id):
        page.go(f"/materias/{materia_id}")  # Redireciona para a tela de edição com o ID da matéria

    def confirm_delete_materia(materia_id):
        def on_confirm(e):
            delete_materia(materia_id)
            page.dialog.open = False
            update_materias_list()
            page.update()

        def on_cancel(e):
            page.dialog.open = False
            page.update()

        page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar Exclusão"),
            content=ft.Text("Você tem certeza que deseja excluir esta matéria?"),
            actions=[
                ft.TextButton("Cancelar", on_click=on_cancel),
                ft.TextButton("Excluir", on_click=on_confirm),
            ],
        )
        page.dialog.open = True
        page.update()

    materias_list = ft.ListView()
    update_materias_list()

    return ft.View(
        "/home",
        [
            ft.Column(
                controls=[
                    ft.Text("Matérias", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                    materias_list,
                    ft.ElevatedButton("Adicionar Matéria", on_click=lambda e: page.go("/materias")),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=10
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
