import flet as ft

from database.db import resumo_financeiro, historico_financeiro_mensal

from components.cards import (
    stat_card,
    secao_titulo,
    estado_vazio,
    COR_PRIMARIA,
    COR_SUCESSO,
    COR_TEXTO_TITULO,
    COR_TEXTO_CORPO,
    COR_SUPERFICIE
)


def financeiro_page():

    resumo = resumo_financeiro()
    historico = historico_financeiro_mensal(meses=6)

    maior_valor = max([valor for _mes, valor in historico], default=0) or 1

    barras_historico = []

    for mes_ano, valor in reversed(historico):
        mes, _ano = mes_ano.split("/")
        altura = max(6, int((valor / maior_valor) * 90))

        barras_historico.append(
            ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
                controls=[
                    ft.Container(
                        width=28,
                        height=altura,
                        border_radius=6,
                        bgcolor=COR_PRIMARIA if valor > 0 else "#E5E7EB",
                    ),
                    ft.Text(mes, size=11, color=COR_TEXTO_CORPO)
                ]
            )
        )

    grafico_historico = ft.Container(
        padding=16,
        border_radius=18,
        bgcolor=COR_SUPERFICIE,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.END,
            controls=barras_historico
        )
    ) if any(v > 0 for _m, v in historico) else estado_vazio(
        "Sem histórico financeiro ainda.",
        icone=ft.Icons.BAR_CHART_OUTLINED
    )

    return ft.Column(
        scroll=ft.ScrollMode.AUTO,
        spacing=18,
        controls=[
            secao_titulo(
                "Financeiro",
                "Acompanhe seus ganhos e atendimentos."
            ),

            ft.Row(
                controls=[
                    stat_card(
                        "Hoje",
                        f"R$ {resumo['ganhos_dia']:.2f}",
                        icone=ft.Icons.TODAY_OUTLINED,
                        cor_destaque=COR_SUCESSO
                    ),
                    stat_card(
                        "Semana",
                        f"R$ {resumo['ganhos_semana']:.2f}",
                        icone=ft.Icons.DATE_RANGE_OUTLINED,
                        cor_destaque=COR_SUCESSO
                    )
                ]
            ),

            ft.Row(
                controls=[
                    stat_card(
                        "Mês",
                        f"R$ {resumo['ganhos_mes']:.2f}",
                        icone=ft.Icons.CALENDAR_MONTH_OUTLINED,
                        cor_destaque=COR_SUCESSO
                    ),
                    stat_card(
                        "Ticket médio",
                        f"R$ {resumo['ticket_medio']:.2f}",
                        icone=ft.Icons.PERCENT_OUTLINED
                    )
                ]
            ),

            stat_card(
                "Atendimentos no mês",
                str(resumo["atendimentos_mes"]),
                icone=ft.Icons.EVENT_AVAILABLE_OUTLINED,
                expand=True
            ),

            secao_titulo("Histórico (últimos 6 meses)"),
            grafico_historico,

            ft.Container(height=10)
        ]
    )
