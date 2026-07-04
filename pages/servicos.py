import flet as ft

from database.db import (
    adicionar_servico,
    listar_servicos,
    editar_servico,
    excluir_servico
)

from components.cards import (
    secao_titulo,
    lista_card,
    estado_vazio,
    COR_PRIMARIA,
    COR_ALERTA,
    COR_SUPERFICIE
)


def servicos_page(page):

    lista_servicos_col = ft.Column()
    servico_em_edicao = {"id": None}

    nome = ft.TextField(
        label="Nome do Serviço",
        border_radius=12
    )

    valor = ft.TextField(
        label="Valor (R$)",
        border_radius=12,
        keyboard_type=ft.KeyboardType.NUMBER
    )

    duracao = ft.TextField(
        label="Duração (minutos)",
        border_radius=12,
        keyboard_type=ft.KeyboardType.NUMBER
    )

    mensagem_erro = ft.Text(
        "",
        color=COR_ALERTA,
        size=12,
        visible=False
    )

    botao_salvar = ft.ElevatedButton(
        "Salvar Serviço",
        bgcolor=COR_PRIMARIA,
        color="#FFFFFF",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
    )

    botao_cancelar_edicao = ft.TextButton(
        "Cancelar edição",
        visible=False
    )

    def limpar_formulario():
        servico_em_edicao["id"] = None
        nome.value = ""
        valor.value = ""
        duracao.value = ""
        botao_salvar.text = "Salvar Serviço"
        botao_cancelar_edicao.visible = False
        mensagem_erro.visible = False

    def cancelar_edicao(e):
        limpar_formulario()
        page.update()

    def iniciar_edicao(servico):
        servico_em_edicao["id"] = servico[0]
        nome.value = servico[1]
        valor.value = str(servico[2])
        duracao.value = str(servico[3])
        botao_salvar.text = "Atualizar Serviço"
        botao_cancelar_edicao.visible = True
        mensagem_erro.visible = False
        page.update()

    def confirmar_exclusao(servico_id, nome_servico):
        def excluir_confirmado(e):
            excluir_servico(servico_id)
            page.close(dialogo)
            carregar_servicos()

        def fechar_dialogo(e):
            page.close(dialogo)

        dialogo = ft.AlertDialog(
            title=ft.Text("Excluir serviço"),
            content=ft.Text(f"Tem certeza que deseja excluir {nome_servico}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=fechar_dialogo),
                ft.TextButton(
                    "Excluir",
                    style=ft.ButtonStyle(color=COR_ALERTA),
                    on_click=excluir_confirmado
                )
            ]
        )

        page.open(dialogo)

    def carregar_servicos():

        lista_servicos_col.controls.clear()

        servicos = listar_servicos()

        if not servicos:
            lista_servicos_col.controls.append(
                estado_vazio("Nenhum serviço cadastrado ainda.", ft.Icons.SPA_OUTLINED)
            )
            page.update()
            return

        for servico in servicos:

            linhas = [
                f"R$ {servico[2]:.2f}",
                f"{servico[3]} minutos"
            ]

            acoes = ft.Row(
                spacing=0,
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.EDIT_OUTLINED,
                        icon_size=18,
                        icon_color=COR_PRIMARIA,
                        on_click=lambda e, s=servico: iniciar_edicao(s)
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        icon_size=18,
                        icon_color=COR_ALERTA,
                        on_click=lambda e, sid=servico[0], n=servico[1]:
                            confirmar_exclusao(sid, n)
                    )
                ]
            )

            lista_servicos_col.controls.append(
                lista_card(servico[1], linhas, acao=acoes)
            )

        page.update()

    def validar_numero(texto, tipo):
        if not texto or not texto.strip():
            return None
        texto_normalizado = texto.strip().replace(",", ".")
        try:
            return tipo(texto_normalizado)
        except ValueError:
            return None

    def salvar_servico(e):

        if not nome.value or not nome.value.strip():
            mensagem_erro.value = "Informe o nome do serviço."
            mensagem_erro.visible = True
            page.update()
            return

        valor_numerico = validar_numero(valor.value, float)

        if valor_numerico is None or valor_numerico <= 0:
            mensagem_erro.value = "Informe um valor válido (maior que zero)."
            mensagem_erro.visible = True
            page.update()
            return

        duracao_numerica = validar_numero(duracao.value, int)

        if duracao_numerica is None or duracao_numerica <= 0 or duracao_numerica > 600:
            mensagem_erro.value = "Informe uma duração válida (1 a 600 minutos)."
            mensagem_erro.visible = True
            page.update()
            return

        mensagem_erro.visible = False

        if servico_em_edicao["id"] is not None:
            editar_servico(
                servico_em_edicao["id"],
                nome.value.strip(),
                valor_numerico,
                duracao_numerica
            )
        else:
            adicionar_servico(
                nome.value.strip(),
                valor_numerico,
                duracao_numerica
            )

        limpar_formulario()
        carregar_servicos()

    botao_salvar.on_click = salvar_servico
    botao_cancelar_edicao.on_click = cancelar_edicao

    carregar_servicos()

    return ft.Column(
        scroll=ft.ScrollMode.AUTO,
        spacing=14,
        controls=[

            secao_titulo("Serviços", "Cadastre os serviços que você oferece."),

            ft.Container(
                padding=16,
                border_radius=18,
                bgcolor=COR_SUPERFICIE,
                content=ft.Column(
                    spacing=10,
                    controls=[
                        nome,
                        valor,
                        duracao,
                        mensagem_erro,
                        ft.Row(
                            controls=[
                                botao_salvar,
                                botao_cancelar_edicao
                            ]
                        )
                    ]
                )
            ),

            lista_servicos_col
        ]
    )
