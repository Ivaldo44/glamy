import flet as ft

from database.db import listar_expediente, atualizar_expediente, DIAS_SEMANA

from components.cards import (
    secao_titulo,
    COR_PRIMARIA,
    COR_TEXTO_TITULO,
    COR_TEXTO_CORPO,
    COR_SUPERFICIE
)


def configuracoes_page(page):

    linhas_expediente = listar_expediente()

    linha_widgets = []

    def criar_linha_dia(dado_dia):
        dia_semana, hora_inicio, hora_fim, ativo = (
            dado_dia[1], dado_dia[2], dado_dia[3], dado_dia[4]
        )

        nome_dia = DIAS_SEMANA[dia_semana]

        campo_inicio = ft.TextField(
            label="Início",
            value=hora_inicio or "08:00",
            width=90,
            text_size=13,
            dense=True,
            disabled=not ativo
        )

        campo_fim = ft.TextField(
            label="Fim",
            value=hora_fim or "18:00",
            width=90,
            text_size=13,
            dense=True,
            disabled=not ativo
        )

        def alternar_ativo(e, d=dia_semana, ci=None, cf=None):
            novo_estado = e.control.value
            campo_inicio.disabled = not novo_estado
            campo_fim.disabled = not novo_estado

            atualizar_expediente(
                d,
                campo_inicio.value,
                campo_fim.value,
                novo_estado
            )

            page.update()

        def salvar_horario(e, d=dia_semana):
            atualizar_expediente(
                d,
                campo_inicio.value,
                campo_fim.value,
                switch_ativo.value
            )

        switch_ativo = ft.Switch(
            value=bool(ativo),
            active_color=COR_PRIMARIA,
            on_change=alternar_ativo
        )

        campo_inicio.on_blur = salvar_horario
        campo_fim.on_blur = salvar_horario

        return ft.Container(
            padding=12,
            border_radius=14,
            bgcolor=COR_SUPERFICIE,
            margin=ft.Margin(left=0, right=0, top=0, bottom=8),
            content=ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        width=80,
                        content=ft.Text(
                            nome_dia,
                            weight=ft.FontWeight.W_600,
                            size=13,
                            color=COR_TEXTO_TITULO
                        )
                    ),
                    switch_ativo,
                    ft.Container(width=4),
                    campo_inicio,
                    ft.Text("–", color=COR_TEXTO_CORPO),
                    campo_fim,
                ]
            )
        )

    for dado_dia in linhas_expediente:
        linha_widgets.append(criar_linha_dia(dado_dia))

    return ft.Column(
        scroll=ft.ScrollMode.AUTO,
        spacing=18,
        controls=[
            secao_titulo(
                "Configurações",
                "Defina seu expediente de atendimento."
            ),

            ft.Text(
                "Horários de trabalho",
                size=16,
                weight=ft.FontWeight.BOLD,
                color=COR_TEXTO_TITULO
            ),

            ft.Text(
                "Ative os dias em que você atende e defina o horário "
                "de início e fim. Isso define quais horários aparecem "
                "disponíveis na Agenda.",
                size=12,
                color=COR_TEXTO_CORPO
            ),

            ft.Column(controls=linha_widgets),

            ft.Container(height=10)
        ]
    )
