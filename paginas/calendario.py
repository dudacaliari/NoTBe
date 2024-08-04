import datetime
import flet as ft
from database import add_evento, get_eventos_by_data, get_all_eventos, delete_evento, update_evento

# Função que define a visualização do calendário
def CalendarioView(page: ft.Page):
    # Campo de entrada para adicionar eventos
    evento_input = ft.TextField(
        label="Adicionar Evento",
        bgcolor="#FFFFFF"  # Cor de fundo branca
    )
    # Lista para exibir todos os eventos
    proximos_eventos_list = ft.ListView(controls=[], spacing=10, expand=True)
    # Dicionário para armazenar eventos por data
    eventos = {}
    selected_date = None

    # Função para carregar eventos do banco de dados
    def load_eventos():
        for data, descricao in get_all_eventos():
            if data not in eventos:
                eventos[data] = []
            eventos[data].append(descricao)
        update_proximos_eventos()

    # Função para lidar com a mudança de data
    def handle_change(e):
        nonlocal selected_date
        selected_date = e.control.value.strftime('%Y-%m-%d')
        selected_date_label.value = f"Data Selecionada: {selected_date}"
        update_proximos_eventos()
        page.update()

    # Função para lidar com o fechamento do DatePicker
    def handle_dismissal(e):
        page.add(ft.Text("DatePicker dismissed"))

    # Função para adicionar um evento à data selecionada
    def add_evento_handler(e):
        if not selected_date:
            page.add(ft.Text("Por favor, selecione uma data."))
            return
        evento = evento_input.value
        if evento:
            add_evento(selected_date, evento)
            if selected_date not in eventos:
                eventos[selected_date] = []
            eventos[selected_date].append(evento)
            update_proximos_eventos()
            evento_input.value = ""
            page.update()

    # Função para atualizar a lista de próximos eventos
    def update_proximos_eventos():
        proximos_eventos_list.controls.clear()
        for date, eventos_data in sorted(eventos.items(), reverse=True):
            for evento in eventos_data:
                proximos_eventos_list.controls.append(create_event_row(date, evento))
        page.update()

    # Função para criar uma linha para cada evento com opções de editar e excluir
    def create_event_row(date, event):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(f"{date}: {event}", color="#45287a", weight=ft.FontWeight.BOLD),
                    ft.Row(
                        controls=[
                            ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e: edit_event(date, event)),
                            ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e: confirm_delete_event(date, event))
                        ],
                        alignment=ft.MainAxisAlignment.END
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=10,
            bgcolor="#E8DAEF",  # Cor lilás claro
            border=ft.Border(
                left=ft.BorderSide(color="#A569BD", width=1),
                right=ft.BorderSide(color="#A569BD", width=1),
                top=ft.BorderSide(color="#A569BD", width=1),
                bottom=ft.BorderSide(color="#A569BD", width=1)
            ),
            border_radius=8
        )

    # Função para confirmar a exclusão do evento
    def confirm_delete_event(date, event):
        def delete_event(e):
            evento_id = next((id for id, desc in get_eventos_by_data(date) if desc == event), None)
            if evento_id:
                delete_evento(evento_id)
                eventos[date].remove(event)
                if not eventos[date]:
                    del eventos[date]
                update_proximos_eventos()
            page.dialog.open = False
            page.update()

        page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar Exclusão", color="#45287a", weight=ft.FontWeight.BOLD),
            content=ft.Text(f"Tem certeza que deseja excluir o evento '{event}'?", color="#45287a"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: close_dialog()),
                ft.TextButton("Excluir", on_click=delete_event)
            ],
            open=True
        )
        page.update()

    # Função para fechar o diálogo
    def close_dialog():
        page.dialog.open = False
        page.update()

    # Função para editar um evento
    def edit_event(date, event):
        event_edit_input.value = event
        event_edit_date_picker.value = datetime.datetime.strptime(date, '%Y-%m-%d')
        page.dialog = ft.AlertDialog(
            title=ft.Text("Editar Evento", color="#45287a", weight=ft.FontWeight.BOLD),
            content=ft.Column([
                event_edit_input,
                event_edit_date_picker
            ]),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: close_dialog()),
                ft.TextButton("Salvar", on_click=lambda e: save_event(date, event))
            ],
            open=True
        )
        page.update()

    # Função para salvar o evento editado
    def save_event(old_date, old_event):
        new_event = event_edit_input.value
        new_date = event_edit_date_picker.value.strftime('%Y-%m-%d')
        evento_id = next((id for id, desc in get_eventos_by_data(old_date) if desc == old_event), None)
        if evento_id:
            update_evento(evento_id, new_date, new_event)
            if new_date != old_date:
                eventos[old_date].remove(old_event)
                if not eventos[old_date]:
                    del eventos[old_date]
                if new_date not in eventos:
                    eventos[new_date] = []
                eventos[new_date].append(new_event)
            else:
                index = eventos[old_date].index(old_event)
                eventos[old_date][index] = new_event
            update_proximos_eventos()
            close_dialog()

    # Label para exibir a data selecionada
    selected_date_label = ft.Text("", color="#FFFFFF", weight=ft.FontWeight.BOLD)
    # Campo de entrada para editar eventos
    event_edit_input = ft.TextField(
        label="Editar Evento",
        bgcolor="#FFFFFF"  # Cor de fundo branca
    )
    # DatePicker para editar a data do evento
    event_edit_date_picker = ft.DatePicker(
        first_date=datetime.datetime(year=2023, month=10, day=1),
        last_date=datetime.datetime(year=2024, month=10, day=1)
    )

    # Carrega os eventos do banco de dados ao iniciar a visualização
    load_eventos()

    return ft.View(
        "/calendario",
        [
            ft.Container(
                width=page.window.width,
                height=page.window.height,
                bgcolor="#FFFFFF",  # Fundo branco
                content=ft.Column(
                    controls=[
                        # Container com o fundo degradê
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    # Barra com degradê e os elementos dentro
                                    ft.Container(
                                        content=ft.Column(
                                            controls=[
                                                ft.Text(
                                                    "Calendário",
                                                    style=ft.TextStyle(
                                                        size=24,  # Ajuste o tamanho conforme necessário
                                                        weight=ft.FontWeight.BOLD,  # Ajuste o peso da fonte
                                                        color=ft.colors.WHITE  # Ajuste a cor conforme necessário
                                                    )
                                                ),
                                                ft.ElevatedButton(
                                                    "Escolher Data",
                                                    icon=ft.icons.CALENDAR_MONTH,
                                                    on_click=lambda e: page.open(
                                                        ft.DatePicker(
                                                            first_date=datetime.datetime(year=2023, month=10, day=1),
                                                            last_date=datetime.datetime(year=2024, month=10, day=1),
                                                            on_change=handle_change,
                                                            on_dismiss=handle_dismissal,
                                                        )
                                                    ),
                                                    bgcolor="#FFFFFF"  # Cor de fundo
                                                ),
                                                selected_date_label,  # Adiciona a data selecionada aqui
                                                evento_input,
                                                ft.ElevatedButton(
                                                    "Adicionar Evento",
                                                    on_click=add_evento_handler,
                                                    bgcolor="#FFFFFF"  # Cor de fundo
                                                )
                                            ],
                                            alignment=ft.MainAxisAlignment.START,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            spacing=20
                                        ),
                                        padding=20,
                                        bgcolor="#D7BDE2",  # Cor lilás clara
                                        gradient=ft.LinearGradient(
                                            colors=["#885D9A", "#4B83A7"],
                                            begin=ft.Alignment(-1, -1),
                                            end=ft.Alignment(1, 1)
                                        ),
                                        border_radius=12,
                                    ),
                                    # Container para a lista de próximos eventos
                                    ft.Container(
                                        height=page.window.height * 0.5,  # Proporcional ao tamanho da página
                                        content=ft.Column([
                                            ft.Text("Próximos Eventos: ", color="#45287a", weight=ft.FontWeight.BOLD),
                                            proximos_eventos_list
                                        ], expand=True),
                                        padding=10,
                                        bgcolor="#D7BDE2",  # Cor lilás clara
                                        border_radius=12  # Bordas arredondadas
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=20,
                                expand=True  # Permite a expansão vertical
                            )
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                    expand=True  # Permite a expansão vertical
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
