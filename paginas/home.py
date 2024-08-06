import flet as ft
from database import get_all_materias, delete_materia

def HomeView(page: ft.Page):
    def update_materias_list():
        materias_list.controls.clear()
        materias = get_all_materias()
        for materia in materias:
            media_atual = materia[3]
            media_minima = materia[2]
            nota_necessaria = materia[4]

            # Define as cores para os círculos
            media_atual_color = "#D7BDE2"  # Lilás claro
            if nota_necessaria == 0:
                nota_necessaria_color = "#28A745"  # Verde
            else:
                nota_necessaria_color = "#DC3545"  # Vermelho

            # Container para o círculo
            def create_circle(value, color):
                return ft.Container(
                    content=ft.Text(f"{value:.2f}", size=16, color="#FFFFFF"),
                    width=50,
                    height=50,
                    bgcolor=color,
                    border_radius=25,  # Círculo perfeito
                    alignment=ft.Alignment(0, 0),  # Centraliza o conteúdo
                    margin=5
                )

            # Layout das informações
            materia_card = ft.Container(
                content=ft.Column([
                    ft.Row(
                        controls=[
                            ft.Text(
                                f"{materia[1]}",
                                size=22,
                                color="#9170B1",
                                weight=ft.FontWeight.W_400
                            ),
                            ft.IconButton(
                                icon=ft.icons.CLOSE, 
                                on_click=lambda e, materia_id=materia[0]: confirm_delete_materia(materia_id),
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
                                icon=ft.icons.EDIT, on_click=lambda e, 
                                materia_id=materia[0]: edit_materia_view(materia_id), 
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
                expand=True  # Permite que o container se expanda lateralmente
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
            title=ft.Text("Confirmar Exclusão", color="#45287a", weight=ft.FontWeight.BOLD),
            content=ft.Text("Você tem certeza que deseja excluir esta matéria?", color="#45287a"),
            actions=[
                ft.TextButton("Cancelar", on_click=on_cancel),
                ft.TextButton("Excluir", on_click=on_confirm),
            ],
            open=True
        )
        page.update()

    materias_list = ft.ListView(expand=True, spacing=10)
    update_materias_list()

    return ft.View(
        "/home",
        [
            ft.Container(
                width=page.window.width,
                height=page.window.height,
                bgcolor="#FFFFFF", 
                content=ft.Stack(  # Usando Stack para sobrepor o conteúdo
                    controls=[
                        # Meio círculo no fundo
                        ft.Container(
                            width=page.window.width,
                            height=page.window.height * 0.4,  # Proporcional ao tamanho da página
                            bgcolor="#D7BDE2",  # Cor lilás clara
                            gradient=ft.LinearGradient(
                                colors=["#885D9A", "#4B83A7"],
                                begin=ft.Alignment(-1, -1),
                                end=ft.Alignment(1, 1)
                            ),
                            border_radius=ft.BorderRadius(0, 0, 100, 100),  # Meio círculo
                            alignment=ft.Alignment(-1, -1),  # Alinha ao topo
                        ),
                        # Conteúdo principal
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Container(
                                        content=ft.Column(
                                            controls=[
                                                ft.Text(
                                                    "Matérias Cadastradas",
                                                    style=ft.TextStyle(
                                                        size=30,  # Ajuste o tamanho conforme necessário
                                                        weight=ft.FontWeight.W_300,  # Ajuste o peso da fonte
                                                        color=ft.colors.WHITE  # Ajuste a cor conforme necessário
                                                    )
                                                ),
                                                ft.IconButton(
                                                    icon=ft.icons.ADD,
                                                    icon_color="#906BAB",
                                                    icon_size=20,
                                                    bgcolor="#F5F5F5",
                                                    on_click=lambda e: page.go("/materias"),
                                                )
                                            ],
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # Alinha os itens com espaço entre eles
                                            spacing=20,
                                            expand=True  # Permite a expansão horizontal
                                        ),
                                        padding=20,
                                        width=page.window.width,
                                        height=page.window.height * 0.2,  # Limita a altura a 20% da altura da janela
                                    ),
                                    # Container com a lista de matérias
                                    ft.Container(
                                        content=materias_list,
                                        padding=10,
                                        border_radius=12,  # Bordas arredondadas
                                        expand=True  # Permite que o container se expanda lateralmente
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=20,
                                height=page.window.height * 0.8,
                                expand=True  # Permite a expansão vertical
                            ),
                            padding=20,
                            expand=True  # Permite a expansão vertical
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
                bgcolor="#dec5f0",  # Cor roxa com opacidade
                padding=10,
            )
        ]
    )
