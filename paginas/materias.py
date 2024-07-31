import flet as ft
from paginas.home import HomeView
from paginas.home import materias  # Importe a lista materias de home.py

def MateriasView(page: ft.Page):
    nome_materia_input = ft.TextField(label="Nome da Matéria")
    media_input = ft.TextField(label="Média Mínima")
    notas_list = ft.ListView(controls=[], height=400, spacing=10)

    notas = []  # Lista para armazenar as notas e seus respectivos pesos

    def add_nota(e):
        try:
            nota = float(nota_input.value)
            peso = float(peso_input.value)
            if nota and peso:
                notas.append((nota, peso))
                notas_list.controls.append(ft.Text(f"Nota: {nota}, Peso: {peso}"))
                nota_input.value = ""
                peso_input.value = ""
                page.update()
        except ValueError:
            pass

    def calcular_media():
        if not notas:
            return 0.0
        soma_ponderada = 0.0
        soma_pesos = 0.0
        for nota, peso in notas:
            soma_ponderada += nota * peso
            soma_pesos += peso
        return soma_ponderada if soma_pesos != 0 else 0.0

    def calcular_nota_necessaria(media_minima, soma_pesos, soma_ponderada):
        peso_restante = 1 - soma_pesos  # Considera que a soma dos pesos é no máximo 1
        if peso_restante <= 0:
            return 0.0  # Caso todos os pesos já tenham sido usados
        nota_necessaria = (media_minima * (soma_pesos + peso_restante) - soma_ponderada) / peso_restante
        return max(0.0, nota_necessaria)

    nota_input = ft.TextField(label="Adicionar Nota")
    peso_input = ft.TextField(label="Adicionar Peso")

    def save_materia(e):
        media_minima = float(media_input.value)
        media_atual = calcular_media()
        soma_ponderada = sum(nota * peso for nota, peso in notas)
        soma_pesos = sum(peso for nota, peso in notas)
        nota_necessaria = calcular_nota_necessaria(media_minima, soma_pesos, soma_ponderada)
        materias.append({
            "nome": nome_materia_input.value,
            "media": media_atual,
            "media_minima": media_minima,
            "nota_necessaria": nota_necessaria
        })
        nome_materia_input.value = ""
        media_input.value = ""
        notas.clear()
        notas_list.controls.clear()
        page.go("/home")  # Redireciona para a página inicial após salvar a matéria
        HomeView(page).controls[0].content.controls[1].update()  # Atualiza a lista de matérias na Home

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
                        peso_input,
                        ft.ElevatedButton("Adicionar Nota", on_click=add_nota),
                        ft.ElevatedButton("Salvar Matéria", on_click=save_materia),
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