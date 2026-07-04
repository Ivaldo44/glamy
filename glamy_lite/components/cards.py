import flet as ft

# Paleta central do app — usada por todos os componentes
COR_PRIMARIA = "#7C3AED"
COR_PRIMARIA_CLARA = "#A78BFA"
COR_FUNDO = "#F5F3FF"
COR_SUPERFICIE = "#FFFFFF"
COR_TEXTO_TITULO = "#111827"
COR_TEXTO_CORPO = "#4B5563"
COR_TEXTO_SUTIL = "#9CA3AF"
COR_SUCESSO = "#16A34A"
COR_ALERTA = "#DC2626"


def cor_opacidade(opacidade, cor_hex):
    """
    Gera uma cor em formato #AARRGGBB a partir de um hex '#RRGGBB' e uma
    opacidade de 0 a 1. Evita depender de ft.Colors.with_opacity, cuja
    disponibilidade varia entre versões do Flet.
    """
    cor_hex = cor_hex.lstrip("#")
    alpha = max(0, min(255, round(opacidade * 255)))
    return f"#{alpha:02X}{cor_hex.upper()}"


def stat_card(titulo, valor, icone=None, cor_destaque=COR_PRIMARIA, largura=170, expand=False):
    """Card de estatística usado no Dashboard e no Financeiro.

    Use expand=True (em vez de uma largura grande) para ocupar todo
    o espaço disponível dentro de um Row/Column.
    """

    cabecalho = [
        ft.Text(
            titulo,
            color=COR_TEXTO_CORPO,
            size=13,
            weight=ft.FontWeight.W_500
        )
    ]

    if icone:
        cabecalho.insert(
            0,
            ft.Container(
                width=30,
                height=30,
                border_radius=10,
                bgcolor=cor_opacidade(0.12, cor_destaque),
                alignment=ft.Alignment(0, 0),
                content=ft.Icon(icone, color=cor_destaque, size=16)
            )
        )

    return ft.Container(
        width=None if expand else largura,
        expand=expand,
        padding=16,
        border_radius=18,
        bgcolor=COR_SUPERFICIE,
        shadow=ft.BoxShadow(
            blur_radius=12,
            spread_radius=0,
            color=cor_opacidade(0.06, "#000000"),
            offset=ft.Offset(0, 4)
        ),
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Row(spacing=8, controls=cabecalho),
                ft.Text(
                    valor,
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color=COR_TEXTO_TITULO
                )
            ]
        )
    )


def lista_card(titulo_principal, linhas, cor_lateral=COR_PRIMARIA, acao=None):
    """
    Card padrão para itens de lista (cliente, serviço, agendamento).
    `linhas` é uma lista de strings exibidas abaixo do título.
    `acao` é um controle opcional (ex: botão excluir) no canto.
    """

    conteudo_textos = [
        ft.Text(
            titulo_principal,
            weight=ft.FontWeight.BOLD,
            size=15,
            color=COR_TEXTO_TITULO
        )
    ]

    for linha in linhas:
        conteudo_textos.append(
            ft.Text(linha, size=13, color=COR_TEXTO_CORPO)
        )

    coluna = ft.Column(
        spacing=2,
        controls=conteudo_textos,
        expand=True
    )

    linha_topo = ft.Row(
        vertical_alignment=ft.CrossAxisAlignment.START,
        controls=[coluna] + ([acao] if acao else [])
    )

    return ft.Container(
        padding=14,
        border_radius=16,
        bgcolor=COR_SUPERFICIE,
        margin=ft.Margin(left=0, right=0, top=0, bottom=10),
        content=ft.Row(
            controls=[
                ft.Container(
                    width=4,
                    border_radius=4,
                    bgcolor=cor_lateral,
                ),
                ft.Container(width=10),
                ft.Container(content=linha_topo, expand=True)
            ]
        )
    )


def secao_titulo(texto, subtitulo=None):
    controles = [
        ft.Text(
            texto,
            size=24,
            weight=ft.FontWeight.BOLD,
            color=COR_TEXTO_TITULO
        )
    ]

    if subtitulo:
        controles.append(
            ft.Text(subtitulo, size=14, color=COR_TEXTO_CORPO)
        )

    return ft.Column(spacing=2, controls=controles)


def estado_vazio(mensagem, icone=ft.Icons.INBOX_OUTLINED):
    return ft.Container(
        padding=30,
        alignment=ft.Alignment(0, 0),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
            controls=[
                ft.Icon(icone, color=COR_TEXTO_SUTIL, size=36),
                ft.Text(
                    mensagem,
                    color=COR_TEXTO_SUTIL,
                    size=13,
                    text_align=ft.TextAlign.CENTER
                )
            ]
        )
    )
