import flet as ft
from datetime import datetime, timedelta

from database.db import (
    buscar_clientes_dropdown,
    buscar_servicos_dropdown,
    adicionar_agendamento,
    listar_agendamentos,
    excluir_agendamento,
    buscar_cliente_por_id,
    buscar_servico_por_id,
    horarios_disponiveis_do_dia,
    atualizar_status_agendamento
)

from components.cards import (
    secao_titulo,
    estado_vazio,
    COR_PRIMARIA,
    COR_ALERTA,
    COR_SUCESSO,
    COR_TEXTO_TITULO,
    COR_TEXTO_CORPO,
    COR_TEXTO_SUTIL,
    COR_SUPERFICIE,
    cor_opacidade
)

STATUS_CORES = {
    "Agendado": COR_PRIMARIA,
    "Concluído": COR_SUCESSO,
    "Cancelado": COR_ALERTA
}


def agenda_page(page):

    lista_agendamentos_col = ft.Column()

    def recarregar_dropdowns():
        clientes = buscar_clientes_dropdown()
        servicos = buscar_servicos_dropdown()

        cliente_dropdown.options = [
            ft.dropdown.Option(key=str(c[0]), text=c[1]) for c in clientes
        ]

        servico_dropdown.options = [
            ft.dropdown.Option(key=str(s[0]), text=s[1]) for s in servicos
        ]

    cliente_dropdown = ft.Dropdown(
        label="Cliente",
        border_radius=12,
        options=[]
    )

    servico_dropdown = ft.Dropdown(
        label="Serviço",
        border_radius=12,
        options=[]
    )

    data = ft.TextField(
        label="Data (dd/mm/aaaa)",
        value=datetime.now().strftime("%d/%m/%Y"),
        border_radius=12
    )

    hora = ft.Dropdown(
        label="Horário disponível",
        border_radius=12,
        options=[],
        hint_text="Escolha cliente, serviço e data primeiro"
    )

    mensagem_erro = ft.Text("", color=COR_ALERTA, size=12, visible=False)

    def data_valida(texto):
        try:
            datetime.strptime(texto, "%d/%m/%Y")
            return True
        except (ValueError, TypeError):
            return False

    def atualizar_horarios_disponiveis(e=None):
        hora.options = []
        hora.value = None

        if not servico_dropdown.value or not data_valida(data.value):
            hora.hint_text = "Escolha cliente, serviço e data primeiro"
            page.update()
            return

        servico = buscar_servico_por_id(int(servico_dropdown.value))

        if not servico:
            page.update()
            return

        duracao = servico[2]

        disponiveis = horarios_disponiveis_do_dia(data.value, duracao)

        if not disponiveis:
            hora.hint_text = "Sem horários livres nesse dia"
        else:
            hora.options = [ft.dropdown.Option(h) for h in disponiveis]
            hora.hint_text = "Selecione"

        page.update()

    servico_dropdown.on_change = atualizar_horarios_disponiveis
    data.on_change = atualizar_horarios_disponiveis
    data.on_blur = atualizar_horarios_disponiveis

    def badge_status(status):
        cor = STATUS_CORES.get(status, COR_TEXTO_SUTIL)
        return ft.Container(
            padding=ft.Padding(left=10, right=10, top=4, bottom=4),
            border_radius=10,
            bgcolor=cor_opacidade(0.12, cor),
            content=ft.Text(status, size=11, weight=ft.FontWeight.W_600, color=cor)
        )

    def carregar_agendamentos():

        lista_agendamentos_col.controls.clear()

        agendamentos = listar_agendamentos()

        if not agendamentos:
            lista_agendamentos_col.controls.append(
                estado_vazio("Nenhum agendamento ainda.", ft.Icons.CALENDAR_MONTH_OUTLINED)
            )
            page.update()
            return

        for agendamento in agendamentos:

            cliente = buscar_cliente_por_id(agendamento[1])
            servico = buscar_servico_por_id(agendamento[2])

            nome_cliente = cliente[0] if cliente else "Cliente removido"
            nome_servico = servico[0] if servico else "Serviço removido"
            status_atual = agendamento[7] if len(agendamento) > 7 else "Agendado"

            menu_status = ft.PopupMenuButton(
                icon=ft.Icons.MORE_VERT,
                items=[
                    ft.PopupMenuItem(
                        content=ft.Text("Marcar como Concluído"),
                        on_click=lambda e, id_ag=agendamento[0]:
                            mudar_status(id_ag, "Concluído")
                    ),
                    ft.PopupMenuItem(
                        content=ft.Text("Cancelar"),
                        on_click=lambda e, id_ag=agendamento[0]:
                            mudar_status(id_ag, "Cancelado")
                    ),
                    ft.PopupMenuItem(
                        content=ft.Text("Excluir"),
                        on_click=lambda e, id_ag=agendamento[0]:
                            remover_agendamento(id_ag)
                    )
                ]
            )

            lista_agendamentos_col.controls.append(
                ft.Container(
                    padding=14,
                    border_radius=16,
                    bgcolor=COR_SUPERFICIE,
                    margin=ft.Margin(left=0, right=0, top=0, bottom=10),
                    content=ft.Column(
                        spacing=6,
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text(
                                        nome_cliente,
                                        weight=ft.FontWeight.BOLD,
                                        size=15,
                                        color=COR_TEXTO_TITULO
                                    ),
                                    menu_status
                                ]
                            ),
                            ft.Text(nome_servico, size=13, color=COR_TEXTO_CORPO),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text(
                                        f"{agendamento[3]} · {agendamento[4]} - {agendamento[5]}",
                                        size=12,
                                        color=COR_TEXTO_SUTIL
                                    ),
                                    ft.Text(
                                        f"R$ {agendamento[6]:.2f}",
                                        size=13,
                                        weight=ft.FontWeight.W_600,
                                        color=COR_TEXTO_TITULO
                                    )
                                ]
                            ),
                            badge_status(status_atual)
                        ]
                    )
                )
            )

        page.update()

    def mudar_status(id_ag, novo_status):
        atualizar_status_agendamento(id_ag, novo_status)
        carregar_agendamentos()

    def remover_agendamento(id_ag):
        excluir_agendamento(id_ag)
        carregar_agendamentos()

    def salvar_agendamento(e):

        if not cliente_dropdown.value:
            mensagem_erro.value = "Selecione um cliente."
            mensagem_erro.visible = True
            page.update()
            return

        if not servico_dropdown.value:
            mensagem_erro.value = "Selecione um serviço."
            mensagem_erro.visible = True
            page.update()
            return

        if not data_valida(data.value):
            mensagem_erro.value = "Informe uma data válida (dd/mm/aaaa)."
            mensagem_erro.visible = True
            page.update()
            return

        if not hora.value:
            mensagem_erro.value = "Selecione um horário disponível."
            mensagem_erro.visible = True
            page.update()
            return

        mensagem_erro.visible = False

        servico = buscar_servico_por_id(int(servico_dropdown.value))

        valor = servico[1]
        duracao = servico[2]

        hora_inicio = datetime.strptime(hora.value, "%H:%M")
        hora_fim = hora_inicio + timedelta(minutes=duracao)

        adicionar_agendamento(
            int(cliente_dropdown.value),
            int(servico_dropdown.value),
            data.value,
            hora.value,
            hora_fim.strftime("%H:%M"),
            valor
        )

        cliente_dropdown.value = None
        servico_dropdown.value = None
        data.value = datetime.now().strftime("%d/%m/%Y")
        hora.options = []
        hora.value = None

        carregar_agendamentos()
        page.update()

    recarregar_dropdowns()
    carregar_agendamentos()

    return ft.Column(
        scroll=ft.ScrollMode.AUTO,
        spacing=14,
        controls=[

            secao_titulo("Agenda", "Crie e acompanhe seus agendamentos."),

            ft.Container(
                padding=16,
                border_radius=18,
                bgcolor=COR_SUPERFICIE,
                content=ft.Column(
                    spacing=10,
                    controls=[
                        cliente_dropdown,
                        servico_dropdown,
                        data,
                        hora,
                        mensagem_erro,
                        ft.ElevatedButton(
                            "Agendar",
                            bgcolor=COR_PRIMARIA,
                            color="#FFFFFF",
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=12)
                            ),
                            on_click=salvar_agendamento
                        )
                    ]
                )
            ),

            lista_agendamentos_col
        ]
    )
