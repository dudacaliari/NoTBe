import flet as ft
from database import get_all_materias, delete_materia

def HomeView(page: ft.Page):
    # Função para atualizar a lista de matérias
    def update_materias_list():
        materias_list.controls.clear()  # Limpa a lista de matérias
        materias = get_all_materias()  # Obtém todas as matérias do banco de dados
        for materia in materias:
            media_atual = materia[3]
            media_minima = materia[2]
            nota_necessaria = materia[4]

            # Determina a cor da média atual e da nota necessária
            media_atual_color = "#D7BDE2"
            nota_necessaria_color = "#28A745" if nota_necessaria == 0 else "#DC3545"

            # Função para criar um círculo com valor e cor
            def create_circle(value, color):
                return ft.Container(
                    content=ft.Text(f"{value:.2f}", size=16, color="#FFFFFF"),
                    width=50,
                    height=50,
                    bgcolor=color,
                    border_radius=25,  # Torna o container redondo
                    alignment=ft.Alignment(0, 0),  # Centraliza o texto
                    margin=5
                )

            # Layout das informações da matéria
            materia_card = ft.Container(
                content=ft.Column([
                    ft.Row(
                        controls=[
                            ft.Text(
                                f"{materia[1]}",  # Nome da matéria
                                size=22,
                                color="#9170B1",
                                weight=ft.FontWeight.W_400
                            ),
                            ft.IconButton(
                                icon=ft.icons.CLOSE, 
                                on_click=lambda e, materia_id=materia[0]: confirm_delete_materia(materia_id),  # Confirma a exclusão
                                icon_color="#AE93C1"
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Text(f"média mínima: {media_minima:.2f}", size=16, color="#9170B1"),
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text("média atual", size=16, color="#707070"),
                                    create_circle(media_atual, media_atual_color)
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=10
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text("nota necessária", size=16, color="#707070"),
                                    create_circle(nota_necessaria, nota_necessaria_color)
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=10
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20
                    ),
                    ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.EDIT, 
                                on_click=lambda e, materia_id=materia[0]: edit_materia_view(materia_id),  # Edita a matéria
                                icon_color="#AE93C1"
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        spacing=10
                    ),
                ]),
                padding=20,
                margin=10,
                bgcolor="#EBEBEB",
                border_radius=12,
                expand=True  # Expande o container para preencher o espaço disponível
            )
            materias_list.controls.append(materia_card)  # Adiciona o card da matéria à lista
        page.update()  # Atualiza a página para refletir as mudanças

    # Função para navegar para a tela de edição da matéria
    def edit_materia_view(materia_id):
        page.go(f"/materias/{materia_id}")  # Navega para a tela de edição da matéria

    # Função para confirmar a exclusão de uma matéria
    def confirm_delete_materia(materia_id):
        def on_confirm(e):
            delete_materia(materia_id)  # Exclui a matéria do banco de dados
            page.dialog.open = False
            update_materias_list()  # Atualiza a lista de matérias
            page.update()

        def on_cancel(e):
            page.dialog.open = False
            page.update()

        # Exibe um diálogo de confirmação
        page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar Exclusão", color="#45287a", weight=ft.FontWeight.BOLD),
            content=ft.Text("Você tem certeza que deseja excluir esta matéria?", color="#45287a"),
            actions=[
                ft.TextButton("Cancelar", on_click=on_cancel),
                ft.TextButton("Excluir", on_click=on_confirm),
            ],
            open=True
        )
        page.update()

    materias_list = ft.ListView(expand=True, spacing=10)  # Lista para exibir as matérias
    update_materias_list()  # Carrega e exibe as matérias

    return ft.View(
        "/home",
        [
            ft.Container(
                width=page.window.width,
                height=page.window.height,
                bgcolor="#FFFFFF", 
                content=ft.Stack(
                    controls=[
                        ft.Container(
                            width=page.window.width,
                            height=page.window.height * 0.4,  
                            bgcolor="#D7BDE2",  
                            gradient=ft.LinearGradient(
                                colors=["#885D9A", "#4B83A7"],
                                begin=ft.Alignment(-1, -1),
                                end=ft.Alignment(1, 1)
                            ),
                            border_radius=ft.BorderRadius(0, 0, 100, 100),  
                            alignment=ft.Alignment(-1, -1),
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Container(
                                        content=ft.Column(
                                            controls=[
                                                ft.Text(
                                                    "Matérias Cadastradas",
                                                    style=ft.TextStyle(
                                                        size=30,  
                                                        weight=ft.FontWeight.W_300,  
                                                        color=ft.colors.WHITE  
                                                    )
                                                ),
                                                ft.IconButton(
                                                    icon=ft.icons.ADD,
                                                    icon_color="#906BAB",
                                                    icon_size=20,
                                                    bgcolor="#F5F5F5",
                                                    on_click=lambda e: page.go("/materias"),  # Navega para a tela de adição de matérias
                                                )
                                            ],
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  
                                            spacing=20,
                                            expand=True  
                                        ),
                                        padding=20,
                                        width=page.window.width,
                                        height=page.window.height * 0.2,  
                                    ),
                                    ft.Container(
                                        content=materias_list,
                                        padding=10,
                                        border_radius=12,  
                                        expand=True  
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=20,
                                height=page.window.height * 0.8,
                                expand=True  
                            ),
                            padding=20,
                            expand=True  
                        ),
                    ]
                ),
            ),
            ft.BottomAppBar(
                content=ft.Row(
                    controls=[
                        ft.IconButton(icon=ft.icons.ALARM, icon_color="#785494", on_click=lambda _: page.go("/faltas")),
                        ft.IconButton(icon=ft.icons.HOME, icon_color="#5e4e69", bgcolor="#c5a4de", on_click=lambda _: page.go("/home")),
                        ft.IconButton(icon=ft.icons.EVENT, icon_color="#785494", on_click=lambda _: page.go("/calendario"))
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND
                ),
                bgcolor="#dec5f0",  
                padding=10,
            )
        ]
    )
