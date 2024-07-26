import flet as ft

def MateriasView(page: ft.Page):
    notas = []
    nome_materia_input = ft.TextField(label="Nome da Matéria")
    media_input = ft.TextField(label="Média para Passar")
    notas_list = ft.ListView(controls=[], height=400, spacing=10)

    def add_nota(e):
        nota = nota_input.value
        if nota:
            notas.append(nota)
            notas_list.controls.append(ft.Text(nota))
            nota_input.value = ""
            page.update()

    nota_input = ft.TextField(label="Adicionar Nota")
    return ft.View(
        "/materias",
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
                        ft.Text("Adicionar Matéria", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                        nome_materia_input,
                        media_input,
                        nota_input,
                        ft.ElevatedButton("Adicionar Nota", on_click=add_nota),
                        notas_list
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
