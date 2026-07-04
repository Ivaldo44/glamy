import flet as ft

from database.db import init_database

from pages.dashboard import dashboard_page
from pages.agenda import agenda_page
from pages.clientes import clientes_page
from pages.financeiro import financeiro_page
from pages.configuracoes import configuracoes_page
from pages.servicos import servicos_page

from components.navbar import build_navbar
from components.cards import COR_FUNDO


def main(page: ft.Page):

    init_database()

    page.title = "Glamy Lite"
    page.bgcolor = COR_FUNDO

    page.window.width = 430
    page.window.height = 900

    page.padding = ft.Padding(left=20, right=20, top=24, bottom=10)

    page.theme = ft.Theme(
        color_scheme_seed="#7C3AED"
    )

    page.theme_mode = ft.ThemeMode.LIGHT

    content = ft.Container(expand=True)

    def change_page(index):

        if index == 0:
            content.content = dashboard_page()

        elif index == 1:
            content.content = agenda_page(page)

        elif index == 2:
            content.content = clientes_page(page)

        elif index == 3:
            content.content = servicos_page(page)

        elif index == 4:
            content.content = financeiro_page()

        elif index == 5:
            content.content = configuracoes_page(page)

        page.update()

    navigation = build_navbar(
        on_change=lambda e: change_page(e.control.selected_index)
    )

    page.navigation_bar = navigation

    content.content = dashboard_page()

    page.add(content)


ft.run(main)
