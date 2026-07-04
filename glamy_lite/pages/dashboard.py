import flet as ft
from datetime import datetime

from database.db import (
    contar_clientes,
    resumo_financeiro,
    agendamentos_de_hoje,
    agendamentos_de_amanha,
    buscar_cliente_por_id,
    buscar_servico_por_id,
    horarios_disponiveis_do_dia
)

from components.cards import (
    stat_card,
    secao_titulo,
    estado_vazio,
    COR_PRIMARIA,
    COR_SUCESSO,
    COR_TEXTO_TITULO,
    COR_TEXTO_CORPO,
    COR_TEXTO_SUTIL,
    COR_SUPERFICIE,
    cor_opacidade
)

DIAS_PT = [
    "Segunda-feira", "Terça-feira", "Quarta-feira",
    "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"
]

MESES_PT = [
    "janeiro", "fevereiro", "março", "abril", "maio", "junho",
    "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
]


def _data_extenso():
    hoje = datetime.now()
    dia_semana = DIAS_PT[hoje.weekday()]
    mes = MESES_PT[hoje.month - 1]
    return f"{dia_semana}, {hoje.day} de {mes}"


def dashboard_page():

    resumo = resumo_financeiro()
    total_clientes = contar_clientes()
    hoje = agendamentos_de_hoje()
    amanha = agendamentos_de_amanha()

    # ------------------------------------------------------------
    # Lista de atendimentos de hoje
    # ------------------------------------------------------------
    itens_hoje = []

    for ag in sorted(hoje, key=lambda a: a[4]):
        cliente = buscar_cliente_por_id(ag[1])
        servico = buscar_servico_por_id(ag[2])

        nome_cliente = cliente[0] if cliente else "Cliente removido"
        nome_servico = servico[0] if servico else "Serviço removido"

        itens_hoje.append(
            ft.Container(
                padding=ft.Padding(left=14, right=14, top=10, bottom=10),
                border_radius=14,
                bgcolor=COR_SUPERFICIE,
                margin=ft.Margin(left=0, right=0, top=0, bottom=8),
                content=ft.Row(
                    controls=[
                        ft.Container(
                            width=54,
                            content=ft.Text(
                                ag[4],
                                weight=ft.FontWeight.BOLD,
                                color=COR_PRIMARIA,
                                size=14
                            )
                        ),
                        ft.Column(
                            spacing=0,
                            expand=True,
                            controls=[
                                ft.Text(
                                    nome_cliente,
                                    weight=ft.FontWeight.W_600,
                                    size=14,
                                    color=COR_TEXTO_TITULO
                                ),
                                ft.Text(
                                    nome_servico,
                                    size=12,
                                    color=COR_TEXTO_CORPO
                                )
                            ]
                        ),
                        ft.Text(
                            f"R$ {ag[6]:.2f}",
                            size=13,
                            weight=ft.FontWeight.W_600,
                            color=COR_TEXTO_TITULO
                        )
                    ]
                )
            )
        )

    bloco_hoje = ft.Column(
        spacing=0,
        controls=itens_hoje
    ) if itens_hoje else estado_vazio("Nenhum atendimento marcado para hoje.")

    # ------------------------------------------------------------
    # Lembretes de amanhã
    # ------------------------------------------------------------
    if amanha:
        texto_lembrete = f"Você tem {len(amanha)} atendimento(s) marcado(s) para amanhã."
    else:
        texto_lembrete = "Nenhum atendimento marcado para amanhã."

    bloco_lembrete = ft.Container(
        padding=14,
        border_radius=16,
        bgcolor=cor_opacidade(0.10, COR_PRIMARIA),
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.NOTIFICATIONS_ACTIVE_OUTLINED, color=COR_PRIMARIA),
                ft.Container(width=8),
                ft.Text(
                    texto_lembrete,
                    size=13,
                    color=COR_TEXTO_TITULO,
                    expand=True
                )
            ]
        )
    )

    # ------------------------------------------------------------
    # Horários disponíveis hoje (considerando o 1º serviço cadastrado
    # apenas como referência de duração mínima de 30 min)
    # ------------------------------------------------------------
    hoje_str = datetime.now().strftime("%d/%m/%Y")
    horarios_livres = horarios_disponiveis_do_dia(hoje_str, duracao_minutos=30)

    if horarios_livres:
        chips_horarios = ft.Row(
            wrap=True,
            spacing=6,
            run_spacing=6,
            controls=[
                ft.Container(
                    padding=ft.Padding(left=10, right=10, top=6, bottom=6),
                    border_radius=10,
                    bgcolor=cor_opacidade(0.10, COR_SUCESSO),
                    content=ft.Text(
                        h, size=12, color=COR_SUCESSO, weight=ft.FontWeight.W_600
                    )
                )
                for h in horarios_livres[:10]
            ]
        )
    else:
        chips_horarios = ft.Text(
            "Sem expediente ou sem horários livres hoje.",
            size=12,
            color=COR_TEXTO_SUTIL
        )

    # ------------------------------------------------------------
    # Layout final
    # ------------------------------------------------------------
    return ft.Column(
        scroll=ft.ScrollMode.AUTO,
        spacing=18,
        controls=[
            ft.Column(
                spacing=2,
                controls=[
                    ft.Text(
                        "Glamy",
                        size=26,
                        weight=ft.FontWeight.BOLD,
                        color=COR_TEXTO_TITULO
                    ),
                    ft.Text(
                        _data_extenso(),
                        size=14,
                        color=COR_TEXTO_CORPO
                    )
                ]
            ),

            ft.Row(
                controls=[
                    stat_card(
                        "Ganhos hoje",
                        f"R$ {resumo['ganhos_dia']:.2f}",
                        icone=ft.Icons.PAID_OUTLINED,
                        cor_destaque=COR_SUCESSO
                    ),
                    stat_card(
                        "Clientes",
                        str(total_clientes),
                        icone=ft.Icons.PEOPLE_OUTLINE
                    )
                ]
            ),

            ft.Row(
                controls=[
                    stat_card(
                        "Atendimentos hoje",
                        str(resumo["atendimentos_dia"]),
                        icone=ft.Icons.EVENT_AVAILABLE_OUTLINED
                    ),
                    stat_card(
                        "Ganhos na semana",
                        f"R$ {resumo['ganhos_semana']:.2f}",
                        icone=ft.Icons.TRENDING_UP,
                        cor_destaque=COR_SUCESSO
                    )
                ]
            ),

            bloco_lembrete,

            secao_titulo("Atendimentos de hoje"),
            bloco_hoje,

            secao_titulo("Horários livres hoje"),
            chips_horarios,

            ft.Container(height=10)
        ]
    )
