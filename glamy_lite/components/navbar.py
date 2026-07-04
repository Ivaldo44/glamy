import flet as ft

from components.cards import COR_PRIMARIA, COR_TEXTO_SUTIL, cor_opacidade


def build_navbar(on_change):
    return ft.NavigationBar(
        bgcolor="#FFFFFF",
        indicator_color=cor_opacidade(0.15, COR_PRIMARIA),
        selected_index=0,
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.HOME_OUTLINED,
                selected_icon=ft.Icons.HOME,
                label="Home"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.CALENDAR_MONTH_OUTLINED,
                selected_icon=ft.Icons.CALENDAR_MONTH,
                label="Agenda"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.PEOPLE_OUTLINE,
                selected_icon=ft.Icons.PEOPLE,
                label="Clientes"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.SPA_OUTLINED,
                selected_icon=ft.Icons.SPA,
                label="Serviços"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.ATTACH_MONEY,
                selected_icon=ft.Icons.ATTACH_MONEY,
                label="Financeiro"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.SETTINGS_OUTLINED,
                selected_icon=ft.Icons.SETTINGS,
                label="Config"
            ),
        ],
        on_change=on_change
    )
