import flet as ft

from database.db import (
    adicionar_cliente,
    listar_clientes,
    editar_cliente,
    excluir_cliente
)

from components.cards import (
    secao_titulo,
    lista_card,
    estado_vazio,
    COR_PRIMARIA,
    COR_ALERTA,
    COR_SUPERFICIE,
    COR_TEXTO_TITULO,
    cor_opacidade
)


def clientes_page(page):

    lista_clientes_col = ft.Column()
    cliente_em_edicao = {"id": None}

    nome = ft.TextField(
        label="Nome",
        border_radius=12
    )

    telefone = ft.TextField(
        label="Telefone",
        border_radius=12
    )

    instagram = ft.TextField(
        label="Instagram",
        border_radius=12
    )

    observacoes = ft.TextField(
        label="Observações",
        border_radius=12,
        multiline=True,
        min_lines=2,
        max_lines=4
    )

    mensagem_erro = ft.Text(
        "",
        color=COR_ALERTA,
        size=12,
        visible=False
    )

    botao_salvar = ft.ElevatedButton(
        "Salvar Cliente",
        bgcolor=COR_PRIMARIA,
        color="#FFFFFF",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
    )

    botao_cancelar_edicao = ft.TextButton(
        "Cancelar edição",
        visible=False
    )

    def limpar_formulario():
        cliente_em_edicao["id"] = None
        nome.value = ""
        telefone.value = ""
        instagram.value = ""
        observacoes.value = ""
        botao_salvar.text = "Salvar Cliente"
        botao_cancelar_edicao.visible = False
        mensagem_erro.visible = False

    def cancelar_edicao(e):
        limpar_formulario()
        page.update()

    def iniciar_edicao(cliente):
        cliente_em_edicao["id"] = cliente[0]
        nome.value = cliente[1]
        telefone.value = cliente[2] or ""
        instagram.value = cliente[3] or ""
        observacoes.value = cliente[4] or ""
        botao_salvar.text = "Atualizar Cliente"
        botao_cancelar_edicao.visible = True
        mensagem_erro.visible = False
        page.update()

    def confirmar_exclusao(cliente_id, nome_cliente):
        def excluir_confirmado(e):
            excluir_cliente(cliente_id)
            page.close(dialogo)
            carregar_clientes()

        def fechar_dialogo(e):
            page.close(dialogo)

        dialogo = ft.AlertDialog(
            title=ft.Text("Excluir cliente"),
            content=ft.Text(f"Tem certeza que deseja excluir {nome_cliente}?"),
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

    def carregar_clientes():

        lista_clientes_col.controls.clear()

        clientes = listar_clientes()

        if not clientes:
            lista_clientes_col.controls.append(
                estado_vazio("Nenhum cliente cadastrado ainda.", ft.Icons.PEOPLE_OUTLINE)
            )
            page.update()
            return

        for cliente in clientes:

            linhas = []

            if cliente[2]:
                linhas.append(f"📞 {cliente[2]}")
            if cliente[3]:
                linhas.append(f"📷 {cliente[3]}")
            if cliente[4]:
                linhas.append(cliente[4])

            acoes = ft.Row(
                spacing=0,
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.EDIT_OUTLINED,
                        icon_size=18,
                        icon_color=COR_PRIMARIA,
                        on_click=lambda e, c=cliente: iniciar_edicao(c)
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        icon_size=18,
                        icon_color=COR_ALERTA,
                        on_click=lambda e, cid=cliente[0], n=cliente[1]:
                            confirmar_exclusao(cid, n)
                    )
                ]
            )

            lista_clientes_col.controls.append(
                lista_card(cliente[1], linhas, acao=acoes)
            )

        page.update()

    def salvar_cliente(e):

        if not nome.value or not nome.value.strip():
            mensagem_erro.value = "Informe o nome do cliente."
            mensagem_erro.visible = True
            page.update()
            return

        mensagem_erro.visible = False

        if cliente_em_edicao["id"] is not None:
            editar_cliente(
                cliente_em_edicao["id"],
                nome.value.strip(),
                telefone.value.strip(),
                instagram.value.strip(),
                observacoes.value.strip()
            )
        else:
            adicionar_cliente(
                nome.value.strip(),
                telefone.value.strip(),
                instagram.value.strip(),
                observacoes.value.strip()
            )

        limpar_formulario()
        carregar_clientes()

    botao_salvar.on_click = salvar_cliente
    botao_cancelar_edicao.on_click = cancelar_edicao

    carregar_clientes()

    return ft.Column(
        scroll=ft.ScrollMode.AUTO,
        spacing=14,
        controls=[

            secao_titulo("Clientes", "Cadastre e gerencie seus clientes."),

            ft.Container(
                padding=16,
                border_radius=18,
                bgcolor=COR_SUPERFICIE,
                content=ft.Column(
                    spacing=10,
                    controls=[
                        nome,
                        telefone,
                        instagram,
                        observacoes,
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

            ft.Divider(color=cor_opacidade(0.0, "#000000"), height=4),

            lista_clientes_col
        ]
    )
