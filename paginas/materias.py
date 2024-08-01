import flet as ft
from database import add_materia, get_materia, update_materia, get_notas_by_materia, calcular_nota_necessaria

def MateriasView(page: ft.Page, materia_id=None):
    nome_materia_input = ft.TextField(label="Nome da Matéria")
    media_input = ft.TextField(label="Média Mínima")
    notas_list = ft.ListView(controls=[], height=200, spacing=10)

    notas = []  # Lista para armazenar as notas e seus respectivos pesos

    nota_input = ft.TextField(label="Adicionar Nota")
    peso_input = ft.TextField(label="Adicionar Peso")

    if materia_id:  # Se um ID de matéria for fornecido, preenche os campos
        materia = get_materia(materia_id)
        if materia:
            nome_materia_input.value = materia[1]
            media_input.value = str(materia[2])  # Converte para string para exibir no TextField
            # Carrega notas associadas à matéria
            notas = get_notas_by_materia(materia_id)
            for nota, peso in notas:
                notas_list.controls.append(ft.Text(f"Nota: {nota}, Peso: {peso}"))

    def add_nota_view(e):
        try:
            nota = float(nota_input.value)
            peso = float(peso_input.value)
            if nota is not None and peso is not None:  # Permite adicionar 0
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
        soma_ponderada = sum(nota * peso for nota, peso in notas)
        soma_pesos = sum(peso for _, peso in notas)
        return soma_ponderada if soma_pesos != 0 else 0.0

    def salvar_materia(e):
        nome = nome_materia_input.value
        media_minima = float(media_input.value)
        media_atual = calcular_media()
        nota_necessaria = calcular_nota_necessaria(media_minima, sum(peso for _, peso in notas), sum(nota * peso for nota, peso in notas))
        if materia_id:  # Atualiza matéria existente
            update_materia(materia_id, nome, media_minima, media_atual, nota_necessaria)
        else:  # Adiciona nova matéria
            add_materia(nome, media_minima, media_atual, nota_necessaria)
        page.go("/home")

    def calcular_nota_necessaria(media_minima, soma_pesos, soma_ponderada):
        peso_restante = 1 - soma_pesos  # Considera que a soma dos pesos é no máximo 1
        if peso_restante <= 0:
            return 0.0  # Caso todos os pesos já tenham sido usados
        nota_necessaria = (media_minima * (soma_pesos + peso_restante) - soma_ponderada) / peso_restante
        return max(0.0, nota_necessaria)


    return ft.View(
        f"/materias/{materia_id}" if materia_id else "/materias",
        [
            ft.Column(
                controls=[
                    nome_materia_input,
                    media_input,
                    ft.Row(
                        controls=[
                            nota_input,
                            peso_input,
                            ft.IconButton(icon=ft.icons.ADD, on_click=add_nota_view)
                        ]
                    ),
                    ft.ElevatedButton("Salvar Matéria", on_click=salvar_materia),
                    notas_list,
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