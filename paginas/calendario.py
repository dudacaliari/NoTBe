import datetime
import flet as ft
from database import add_evento, get_eventos_by_data, get_all_eventos, delete_evento, update_evento

def CalendarioView(page: ft.Page):
    # Função para atualizar a lista de próximos eventos
    def update_proximos_eventos():
        proximos_eventos_list.controls.clear()  # Limpa a lista de eventos
        for date, eventos_data in sorted(eventos.items(), reverse=True):
            for evento in eventos_data:
                proximos_eventos_list.controls.append(create_event_row(date, evento))  # Adiciona evento à lista
        page.update()  # Atualiza a página

    # Função para criar uma linha de evento
    def create_event_row(date, event):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(f"{date}: {event}", color="#45287a", weight=ft.FontWeight.NORMAL),
                    ft.Row(
                        controls=[
                            ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e: edit_event(date, event), icon_color="#c29dd1"),
                            ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e: confirm_delete_event(date, event), icon_color="#c29dd1")
                        ],
                        alignment=ft.MainAxisAlignment.END
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=8,
            bgcolor="#F9F9F9",
            border=ft.Border(
                left=ft.BorderSide(color="#D7BDE2", width=1),
                right=ft.BorderSide(color="#D7BDE2", width=1),
                top=ft.BorderSide(color="#D7BDE2", width=1),
                bottom=ft.BorderSide(color="#D7BDE2", width=1)
            ),
            border_radius=6
        )

    # Função para confirmar a exclusão de um evento
    def confirm_delete_event(date, event):
        def delete_event(e):
            evento_id = next((id for id, desc in get_eventos_by_data(date) if desc == event), None)
            if evento_id:
                delete_evento(evento_id)  # Exclui o evento do banco de dados
                eventos[date].remove(event)  # Remove o evento da lista local
                if not eventos[date]:
                    del eventos[date]  # Remove a data se não houver mais eventos
                update_proximos_eventos()  # Atualiza a lista de eventos
            page.dialog.open = False
            page.update()

        def close_dialog():
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

    # Função para editar um evento
    def edit_event(date, event):
        event_edit_input.value = event
        event_edit_date_picker.value = datetime.datetime.strptime(date, '%Y-%m-%d').date()
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

    # Função para salvar um evento editado
    def save_event(old_date, old_event):
        new_event = event_edit_input.value
        new_date = event_edit_date_picker.value.strftime('%Y-%m-%d')
        evento_id = next((id for id, desc in get_eventos_by_data(old_date) if desc == old_event), None)
        if evento_id:
            update_evento(evento_id, new_date, new_event)  # Atualiza o evento no banco de dados
            if new_date != old_date:
                eventos[old_date].remove(old_event)  # Remove o evento da data antiga
                if not eventos[old_date]:
                    del eventos[old_date]  # Remove a data se não houver mais eventos
                if new_date not in eventos:
                    eventos[new_date] = []
                eventos[new_date].append(new_event)  # Adiciona o evento à nova data
            else:
                index = eventos[old_date].index(old_event)
                eventos[old_date][index] = new_event  # Atualiza o evento na mesma data
            update_proximos_eventos()  # Atualiza a lista de eventos
            close_dialog()

    # Função para fechar o diálogo
    def close_dialog():
        page.dialog.open = False
        page.update()

    # Função para lidar com a mudança de data no DatePicker
    def handle_change(e):
        nonlocal selected_date
        selected_date = e.control.value.strftime('%Y-%m-%d')
        selected_date_label.value = f"Data Selecionada: {selected_date}"
        update_proximos_eventos()  # Atualiza a lista de eventos para a nova data selecionada
        page.update()

    # Função para lidar com o fechamento do DatePicker
    def handle_dismissal(e):
        page.add(ft.Text("DatePicker dismissed"))

    # Campos de entrada e widgets
    evento_input = ft.TextField(
        label="Adicionar Evento",
        bgcolor="#FFFFFF",
        border_color=ft.colors.TRANSPARENT, 
        border_radius=40,
        label_style=ft.TextStyle(color="#8F8F8F"),
        color="#8F8F8F"
    )
    proximos_eventos_list = ft.ListView(controls=[], spacing=10, expand=True)
    eventos = {}  # Dicionário para armazenar eventos por data
    selected_date = None
    event_edit_input = ft.TextField(
        label="Editar Evento",
        bgcolor="#FFFFFF"
    )
    event_edit_date_picker = ft.DatePicker(
        first_date=datetime.datetime(year=2023, month=10, day=1).date(),
        last_date=datetime.datetime(year=2024, month=10, day=1).date()
    )
    selected_date_label = ft.Text("", color="#FFFFFF", weight=ft.FontWeight.BOLD)

    # Função para adicionar um novo evento
    def add_evento_handler(e):
        if not selected_date:
            page.add(ft.Text("Por favor, selecione uma data."))
            return
        evento = evento_input.value
        if evento:
            add_evento(selected_date, evento)  # Adiciona o evento ao banco de dados
            if selected_date not in eventos:
                eventos[selected_date] = []
            eventos[selected_date].append(evento)  # Adiciona o evento à lista local
            update_proximos_eventos()  # Atualiza a lista de eventos
            evento_input.value = ""
            page.update()

    # Função para carregar eventos existentes do banco de dados
    def load_eventos():
        for data, descricao in get_all_eventos():
            if data not in eventos:
                eventos[data] = []
            eventos[data].append(descricao)  # Adiciona evento à lista
        update_proximos_eventos()  # Atualiza a lista de eventos

    load_eventos()  # Carrega os eventos ao iniciar a visualização

    return ft.View(
        "/calendario",
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
                                                    "Calendário",
                                                    style=ft.TextStyle(
                                                        size=30,
                                                        weight=ft.FontWeight.W_300,
                                                        color=ft.colors.WHITE
                                                    )
                                                ),
                                                ft.Row(
                                                    controls=[
                                                        ft.IconButton(
                                                            icon=ft.icons.CALENDAR_MONTH,
                                                            icon_color="#906BAB",
                                                            icon_size=20,
                                                            bgcolor="#F5F5F5",
                                                            on_click=lambda e: page.open(
                                                                ft.DatePicker(
                                                                    first_date=datetime.datetime(year=2023, month=10, day=1).date(),
                                                                    last_date=datetime.datetime(year=2024, month=10, day=1).date(),
                                                                    on_change=handle_change,
                                                                    on_dismiss=handle_dismissal
                                                                )
                                                            )
                                                        ),
                                                        selected_date_label
                                                    ],
                                                    alignment=ft.MainAxisAlignment.CENTER,
                                                    spacing=10
                                                ),
                                                ft.Row(
                                                    controls=[
                                                        evento_input,
                                                        ft.IconButton(
                                                            icon=ft.icons.ADD,
                                                            icon_color="#906BAB",
                                                            icon_size=20,
                                                            bgcolor="#F5F5F5",
                                                            on_click=add_evento_handler
                                                        )
                                                    ],
                                                    alignment=ft.MainAxisAlignment.CENTER,
                                                    spacing=10
                                                ),
                                                ft.Container(
                                                    content=ft.Column(
                                                        controls=[
                                                            ft.Text(
                                                                "Próximos Eventos:",
                                                                style=ft.TextStyle(
                                                                    size=15,
                                                                    weight=ft.FontWeight.W_500,
                                                                    color="#c29dd1"
                                                                )
                                                            ),
                                                            proximos_eventos_list
                                                        ]
                                                    ),
                                                    padding=20,
                                                    width=page.window.width * 0.9,
                                                    height=page.window.height * 0.4,
                                                    border=ft.Border(
                                                        left=ft.BorderSide(color="#D7BDE2", width=2),
                                                        right=ft.BorderSide(color="#D7BDE2", width=2),
                                                        top=ft.BorderSide(color="#D7BDE2", width=2),
                                                        bottom=ft.BorderSide(color="#D7BDE2", width=2)
                                                    ),
                                                    border_radius=15,
                                                    margin=20
                                                )
                                            ],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            spacing=20
                                        ),
                                        padding=20,
                                        width=page.window.width,
                                        height=page.window.height * 0.6,
                                        expand=True
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=20
                            )
                        )
                    ]
                )
            ),
            ft.BottomAppBar(
                content=ft.Row(
                    controls=[
                        ft.IconButton(icon=ft.icons.ALARM, icon_color="#785494", on_click=lambda _: page.go("/faltas")),
                        ft.IconButton(icon=ft.icons.HOME, icon_color="#785494", on_click=lambda _: page.go("/home")),
                        ft.IconButton(icon=ft.icons.EVENT, icon_color="#5e4e69", bgcolor="#c5a4de", on_click=lambda _: page.go("/calendario"))
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND
                ),
                bgcolor="#dec5f0",
                padding=10,
            )
        ]
    )
