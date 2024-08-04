import flet as ft
from database import add_materia, get_materia, update_materia, get_notas_by_materia, add_nota, delete_notas_by_materia

def MateriasView(page: ft.Page, materia_id=None):
    nome_materia_input = ft.TextField(label="Nome da Matéria", bgcolor="#FFFFFF", border_color="#D7BDE2")
    media_input = ft.TextField(label="Média Mínima", bgcolor="#FFFFFF", border_color="#D7BDE2")
    notas_list = ft.ListView(controls=[], height=200, spacing=10)

    notas = []  # Lista para armazenar as notas e seus respectivos pesos

    nota_input = ft.TextField(label="Adicionar Nota", bgcolor="#FFFFFF", border_color="#D7BDE2")
    peso_input = ft.TextField(label="Adicionar Peso", bgcolor="#FFFFFF", border_color="#D7BDE2")

    if materia_id:  # Se um ID de matéria for fornecido, preenche os campos
        materia = get_materia(materia_id)
        if materia:
            nome_materia_input.value = materia[1]
            media_input.value = str(materia[2])  # Converte para string para exibir no TextField
            # Carrega notas associadas à matéria
            notas = get_notas_by_materia(materia_id)
            for nota, peso in notas:
                notas_list.controls.append(ft.Text(f"Nota: {nota}, Peso: {peso}", color="#FFFFFF", weight=ft.FontWeight.BOLD))

    def add_nota_view(e):
        try:
            nota = float(nota_input.value)
            peso = float(peso_input.value)
            if nota is not None and peso is not None:  # Permite adicionar 0
                notas.append((nota, peso))
                notas_list.controls.append(ft.Text(f"Nota: {nota}, Peso: {peso}", color="#45287a", weight=ft.FontWeight.BOLD))
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
            delete_notas_by_materia(materia_id)  # Deleta notas antigas
            for nota, peso in notas:
                add_nota(materia_id, nota, peso)  # Adiciona notas novamente
        else:  # Adiciona nova matéria
            add_materia_id = add_materia(nome, media_minima, media_atual, nota_necessaria)
            for nota, peso in notas:
                add_nota(add_materia_id, nota, peso)
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
            ft.Container(
                width=page.window.width,
                height=page.window.height,
                bgcolor="#FFFFFF", 
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    nome_materia_input,
                                    media_input,
                                    ft.Row(
                                        controls=[
                                            ft.Container(
                                                content=nota_input,
                                                width=150,  # Ajusta a largura do campo
                                                margin=ft.Margin(left=0, top=0, right=10, bottom=0)  # Ajusta a margem
                                            ),
                                            ft.Container(
                                                content=peso_input,
                                                width=150  # Ajusta a largura do campo
                                            ),
                                            ft.IconButton(
                                                icon=ft.icons.ADD, 
                                                on_click=add_nota_view,
                                                bgcolor="#D7BDE2",
                                                width=50,
                                                height=50
                                            )
                                        ],
                                        alignment=ft.MainAxisAlignment.START,
                                        spacing=10
                                    ),
                                    ft.ElevatedButton("Salvar Matéria", on_click=salvar_materia, bgcolor="#D7BDE2"),
                                    notas_list,
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=20,
                                expand=True
                            ),
                            padding=20,
                            bgcolor="#D7BDE2",  # Cor lilás clara
                            gradient=ft.LinearGradient(
                                colors=["#885D9A", "#4B83A7"],
                                begin=ft.Alignment(-1, -1),
                                end=ft.Alignment(1, 1)
                            ),
                            border_radius=12,
                            width=page.window.width,
                            height=page.window.height * 0.8  # Ajusta a altura para o restante da tela
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                    expand=True
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
