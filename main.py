import flet as ft
from paginas.splash import SplashView
from paginas.home import HomeView
from paginas.materias import MateriasView
from paginas.calendario import CalendarioView
from database import create_tables

def main(page: ft.Page):
    create_tables()
    page.title = "NoTBe"
    page.vertical_alignment = ft.MainAxisAlignment.START

    def route_change(e: ft.RouteChangeEvent):
        page.views.clear()  # Limpa as views antes de adicionar uma nova
        if e.route == "/":
            page.views.append(SplashView(page))  # Tela de splash
        elif e.route == "/home":
            page.views.append(HomeView(page))  # Tela Home
        elif e.route.startswith("/materias"):
            parts = e.route.split("/")
            materia_id = int(parts[2]) if len(parts) > 2 else None
            page.views.append(MateriasView(page, materia_id))  # Tela de adição/edição de matérias
        elif e.route == "/calendario":
            page.views.append(CalendarioView(page))  # Tela de calendário
        page.update()

    page.on_route_change = route_change
    page.go("/")  # Inicia na tela de splash

ft.app(target=main)