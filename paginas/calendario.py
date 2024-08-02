import datetime
import flet as ft
from database import add_evento, get_eventos_by_data, get_all_eventos, delete_evento, update_evento

# Função que define a visualização do calendário
def CalendarioView(page: ft.Page):
    # Campo de entrada para adicionar eventos
    evento_input = ft.TextField(label="Adicionar Evento")
    # Lista para exibir todos os eventos
    eventos_list = ft.ListView(controls=[], height=400, spacing=10)
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
        update_event_list()

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
            update_event_list()
            update_proximos_eventos()
            evento_input.value = ""
            page.update()

    # Função para atualizar a lista de eventos para a data selecionada
    def update_event_list():
        eventos_list.controls.clear()
        if selected_date and selected_date in eventos:
            for evento in eventos[selected_date]:
                eventos_list.controls.append(create_event_row(selected_date, evento))
        page.update()

    # Função para atualizar a lista de próximos eventos
    def update_proximos_eventos():
        proximos_eventos_list.controls.clear()
        for date, eventos_data in sorted(eventos.items()):
            for evento in eventos_data:
                proximos_eventos_list.controls.append(ft.Text(f"{date}: {evento}"))
        page.update()

    # Função para criar uma linha para cada evento com opções de editar e excluir
    def create_event_row(date, event):
        return ft.Row(
            controls=[
                ft.Text(f"{date}: {event}"),
                ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e: edit_event(date, event)),
                ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e: confirm_delete_event(date, event))
            ]
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
                update_event_list()
                update_proximos_eventos()
            page.dialog.open = False
            page.update()

        page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar Exclusão"),
            content=ft.Text(f"Tem certeza que deseja excluir o evento '{event}'?"),
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
            title=ft.Text("Editar Evento"),
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
            update_event_list()
            update_proximos_eventos()
            close_dialog()

    # Label para exibir a data selecionada
    selected_date_label = ft.Text("")
    # Campo de entrada para editar eventos
    event_edit_input = ft.TextField(label="Editar Evento")
    # DatePicker para editar a data do evento
    event_edit_date_picker = ft.DatePicker(
        first_date=datetime.datetime(year=2023, month=10, day=1),
        last_date=datetime.datetime(year=2024, month=10, day=1)
    )
    # Lista para exibir os próximos eventos
    proximos_eventos_list = ft.ListView(controls=[], height=200, spacing=10)

    # Carrega os eventos do banco de dados ao iniciar a visualização
    load_eventos()

    return ft.View(
        "/calendario",
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
                            "Calendário",
                            style=ft.TextThemeStyle.HEADLINE_MEDIUM
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
                        ),
                        selected_date_label,
                        evento_input,
                        ft.ElevatedButton("Adicionar Evento", on_click=add_evento_handler),
                        ft.Text("Eventos do Dia Selecionado"),
                        eventos_list,
                        ft.Text("Próximos Eventos"),
                        proximos_eventos_list
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
