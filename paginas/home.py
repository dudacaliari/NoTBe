import flet as ft

materias = []

def HomeView(page: ft.Page):
    def add_materia(e):
        materia_input = materia_input_field.value
        if materia_input:
            materias.append({"nome": materia_input, "notas": [], "media": 0})
            materia_input_field.value = ""
            update_materias_list()
            page.update()

    def update_materias_list():
        materias_list.controls.clear()
        for materia in materias:
            materias_list.controls.append(ft.Text(f"{materia['nome']} - Média: {materia['media']:.2f}"))
        materias_list.controls.append(ft.ElevatedButton("Adicionar Matéria", on_click=add_materia))

    materia_input_field = ft.TextField(label="Adicionar Matéria")
    materias_list = ft.ListView(controls=[], height=400, spacing=10)

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
                        ft.Text(
                            "Matérias",
                            style=ft.TextThemeStyle.HEADLINE_MEDIUM
                        ),
                        materia_input_field,
                        ft.ElevatedButton("Adicionar Matéria", on_click=add_materia),
                        materias_list
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
