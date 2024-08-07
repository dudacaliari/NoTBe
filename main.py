import flet as ft
import time

from paginas.home import HomeView
from paginas.materias import MateriasView
from paginas.faltas import FaltasView
from paginas.calendario import CalendarioView
from database import create_tables

def splashScreen(page: ft.Page):  
    page.title = "NoTBe"
    page.update()

    # Adicionar a imagem GIF
    gif_image = ft.Image(
        src="assets/LogoNB.gif",
        width=400,
        height=400
    )

    splash_content = ft.Container(
        width=page.window.width,
        height=page.window.height,
        gradient=ft.LinearGradient(
            colors=["#885D9A", "#4B83A7"],
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1)
        ),
        content=ft.ResponsiveRow(
            controls=[
                ft.Column(
                    controls=[
                        ft.Container(
                            content=gif_image,
                            alignment=ft.alignment.center
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    col={"xs": 12, "sm": 10, "md": 8, "lg": 6, "xl": 4},
                    spacing=20
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    page.add(splash_content)

    # Simulação de carregamento
    time.sleep(3)

    page.go("/home")

def main(page: ft.Page):
    # Criar as tabelas no banco de dados
    create_tables()

    page.title = "NoTBe"
    page.vertical_alignment = ft.MainAxisAlignment.START

    def route_change(e: ft.RouteChangeEvent):
        page.views.clear()  # Limpa as views antes de adicionar uma nova
        if e.route == "/home":
            page.views.append(HomeView(page))  # Tela Home
        elif e.route.startswith("/materias"):
            parts = e.route.split("/")
            materia_id = int(parts[2]) if len(parts) > 2 else None
            page.views.append(MateriasView(page, materia_id))  # Tela de adição/edição de matérias
        elif e.route == "/faltas":
            page.views.append(FaltasView(page))  # Tela de registro de faltas
        elif e.route == "/calendario":
            page.views.append(CalendarioView(page))  # Tela de calendário
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # Inicia na tela de splash
    splashScreen(page)

ft.app(target=main, assets_dir="assets")