import flet as ft
from paginas.splash import SplashView
from paginas.home import HomeView
from paginas.materias import MateriasView
from paginas.faltas import FaltasView
from paginas.calendario import CalendarioView

def main(page: ft.Page):
    page.title = "NoTBe"
    page.vertical_alignment = ft.MainAxisAlignment.START

    def route_change(e: ft.RouteChangeEvent):
        page.views.clear()  # Limpa as views antes de adicionar uma nova
        if e.route == "/":
            page.views.append(SplashView(page))  # Tela de splash
        elif e.route == "/home":
            page.views.append(HomeView(page))  # Tela Home
        elif e.route == "/materias":
            page.views.append(MateriasView(page))  # Tela de adição de matérias
        elif e.route == "/faltas":
            page.views.append(FaltasView(page))  # Tela de registro de faltas
        elif e.route == "/calendario":
            page.views.append(CalendarioView(page))  # Tela de calendário
        page.update()

    page.on_route_change = route_change
    page.go("/")  # Inicia na tela de splash

ft.app(target=main)




