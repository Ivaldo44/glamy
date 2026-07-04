import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "glamy.db"

DIAS_SEMANA = [
    "Segunda",
    "Terça",
    "Quarta",
    "Quinta",
    "Sexta",
    "Sábado",
    "Domingo"
]


def get_connection():
    DATA_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_database():
    conn = get_connection()
    cursor = conn.cursor()

    # CLIENTES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        telefone TEXT,
        instagram TEXT,
        observacoes TEXT
    )
    """)

    # SERVIÇOS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS servicos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        valor REAL NOT NULL,
        duracao_minutos INTEGER NOT NULL
    )
    """)

    # AGENDAMENTOS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agendamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        servico_id INTEGER NOT NULL,
        data TEXT NOT NULL,
        hora_inicio TEXT NOT NULL,
        hora_fim TEXT NOT NULL,
        valor REAL NOT NULL,
        status TEXT DEFAULT 'Agendado',
        observacoes TEXT
    )
    """)

    # EXPEDIENTE (horários de trabalho por dia da semana)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expediente (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dia_semana INTEGER NOT NULL UNIQUE,
        hora_inicio TEXT,
        hora_fim TEXT,
        ativo INTEGER NOT NULL DEFAULT 0
    )
    """)

    # garante uma linha pra cada dia da semana (0=Segunda ... 6=Domingo)
    for indice, _nome_dia in enumerate(DIAS_SEMANA):
        cursor.execute("""
        INSERT INTO expediente (dia_semana, hora_inicio, hora_fim, ativo)
        SELECT ?, '08:00', '18:00', ?
        WHERE NOT EXISTS (
            SELECT 1 FROM expediente WHERE dia_semana = ?
        )
        """, (indice, 1 if indice < 5 else 0, indice))

    conn.commit()
    conn.close()


# ==========================
# CLIENTES
# ==========================

def adicionar_cliente(nome, telefone, instagram, observacoes):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO clientes (
        nome,
        telefone,
        instagram,
        observacoes
    )
    VALUES (?, ?, ?, ?)
    """, (
        nome,
        telefone,
        instagram,
        observacoes
    ))

    conn.commit()
    conn.close()


def editar_cliente(cliente_id, nome, telefone, instagram, observacoes):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE clientes
    SET nome = ?, telefone = ?, instagram = ?, observacoes = ?
    WHERE id = ?
    """, (nome, telefone, instagram, observacoes, cliente_id))

    conn.commit()
    conn.close()


def excluir_cliente(cliente_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))

    conn.commit()
    conn.close()


def listar_clientes():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM clientes
    ORDER BY nome
    """)

    clientes = cursor.fetchall()

    conn.close()

    return clientes


def contar_clientes():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM clientes")
    total = cursor.fetchone()[0]

    conn.close()

    return total


# ==========================
# SERVIÇOS
# ==========================

def adicionar_servico(nome, valor, duracao_minutos):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO servicos (
        nome,
        valor,
        duracao_minutos
    )
    VALUES (?, ?, ?)
    """, (
        nome,
        valor,
        duracao_minutos
    ))

    conn.commit()
    conn.close()


def editar_servico(servico_id, nome, valor, duracao_minutos):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE servicos
    SET nome = ?, valor = ?, duracao_minutos = ?
    WHERE id = ?
    """, (nome, valor, duracao_minutos, servico_id))

    conn.commit()
    conn.close()


def excluir_servico(servico_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM servicos WHERE id = ?", (servico_id,))

    conn.commit()
    conn.close()


def listar_servicos():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM servicos
    ORDER BY nome
    """)

    servicos = cursor.fetchall()

    conn.close()

    return servicos


# ==========================
# AGENDAMENTOS
# ==========================

def adicionar_agendamento(
    cliente_id,
    servico_id,
    data,
    hora_inicio,
    hora_fim,
    valor,
    observacoes=""
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO agendamentos (
        cliente_id,
        servico_id,
        data,
        hora_inicio,
        hora_fim,
        valor,
        observacoes
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        cliente_id,
        servico_id,
        data,
        hora_inicio,
        hora_fim,
        valor,
        observacoes
    ))

    conn.commit()
    conn.close()


def listar_agendamentos():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM agendamentos
    ORDER BY data, hora_inicio
    """)

    dados = cursor.fetchall()

    conn.close()

    return dados


def listar_agendamentos_por_data(data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM agendamentos
    WHERE data = ?
    ORDER BY hora_inicio
    """, (data,))

    dados = cursor.fetchall()

    conn.close()

    return dados


def excluir_agendamento(agendamento_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM agendamentos
    WHERE id = ?
    """, (agendamento_id,))

    conn.commit()
    conn.close()


def atualizar_status_agendamento(agendamento_id, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE agendamentos
    SET status = ?
    WHERE id = ?
    """, (status, agendamento_id))

    conn.commit()
    conn.close()


def buscar_cliente_por_id(cliente_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT nome
    FROM clientes
    WHERE id = ?
    """, (cliente_id,))

    dado = cursor.fetchone()

    conn.close()

    return dado


def buscar_servico_por_id(servico_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT nome, valor, duracao_minutos
    FROM servicos
    WHERE id = ?
    """, (servico_id,))

    dado = cursor.fetchone()

    conn.close()

    return dado


def buscar_clientes_dropdown():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, nome
    FROM clientes
    ORDER BY nome
    """)

    dados = cursor.fetchall()

    conn.close()

    return dados


def buscar_servicos_dropdown():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, nome, valor, duracao_minutos
    FROM servicos
    ORDER BY nome
    """)

    dados = cursor.fetchall()

    conn.close()

    return dados


# ==========================
# EXPEDIENTE (horários de trabalho)
# ==========================

def listar_expediente():
    """Retorna lista ordenada por dia da semana (0=Segunda ... 6=Domingo)."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, dia_semana, hora_inicio, hora_fim, ativo
    FROM expediente
    ORDER BY dia_semana
    """)

    dados = cursor.fetchall()

    conn.close()

    return dados


def atualizar_expediente(dia_semana, hora_inicio, hora_fim, ativo):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE expediente
    SET hora_inicio = ?, hora_fim = ?, ativo = ?
    WHERE dia_semana = ?
    """, (hora_inicio, hora_fim, int(ativo), dia_semana))

    conn.commit()
    conn.close()


def buscar_expediente_do_dia(dia_semana):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT dia_semana, hora_inicio, hora_fim, ativo
    FROM expediente
    WHERE dia_semana = ?
    """, (dia_semana,))

    dado = cursor.fetchone()

    conn.close()

    return dado


# ==========================
# DISPONIBILIDADE DE HORÁRIOS
# ==========================

def _gerar_grade_horarios(hora_inicio, hora_fim, intervalo_minutos=30):
    """Gera lista de horários 'HH:MM' entre início e fim, no intervalo dado."""
    inicio = datetime.strptime(hora_inicio, "%H:%M")
    fim = datetime.strptime(hora_fim, "%H:%M")

    horarios = []
    atual = inicio

    while atual < fim:
        horarios.append(atual.strftime("%H:%M"))
        atual += timedelta(minutes=intervalo_minutos)

    return horarios


def _intervalos_conflitam(inicio_a, fim_a, inicio_b, fim_b):
    return inicio_a < fim_b and inicio_b < fim_a


def horario_disponivel(data_str, hora_inicio_str, duracao_minutos):
    """
    Verifica se um horário está livre (sem sobreposição com outros
    agendamentos) para uma data e duração específicas.
    data_str no formato dd/mm/aaaa, hora_inicio_str no formato HH:MM.
    """
    inicio_novo = datetime.strptime(hora_inicio_str, "%H:%M")
    fim_novo = inicio_novo + timedelta(minutes=duracao_minutos)

    agendamentos = listar_agendamentos_por_data(data_str)

    for ag in agendamentos:
        if ag[7] == "Cancelado":
            continue

        inicio_existente = datetime.strptime(ag[4], "%H:%M")
        fim_existente = datetime.strptime(ag[5], "%H:%M")

        if _intervalos_conflitam(
            inicio_novo, fim_novo,
            inicio_existente, fim_existente
        ):
            return False

    return True


def horario_ocupado(data, hora_inicio):
    """Mantido por compatibilidade: checagem simples de horário exato."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM agendamentos
    WHERE data = ?
    AND hora_inicio = ?
    AND status != 'Cancelado'
    """, (data, hora_inicio))

    resultado = cursor.fetchone()[0]

    conn.close()

    return resultado > 0


def horarios_disponiveis_do_dia(data_str, duracao_minutos, intervalo_minutos=30):
    """
    Retorna a lista de horários (HH:MM) livres em um dia, considerando:
    - O expediente cadastrado para o dia da semana correspondente.
    - A duração do serviço selecionado (não pode sobrepor outro agendamento
      nem passar do fim do expediente).
    """
    try:
        data_obj = datetime.strptime(data_str, "%d/%m/%Y")
    except ValueError:
        return []

    dia_semana = data_obj.weekday()  # 0 = Segunda ... 6 = Domingo

    expediente = buscar_expediente_do_dia(dia_semana)

    if not expediente or not expediente[3]:
        return []

    _, hora_inicio_exp, hora_fim_exp, _ativo = expediente

    if not hora_inicio_exp or not hora_fim_exp:
        return []

    grade = _gerar_grade_horarios(
        hora_inicio_exp,
        hora_fim_exp,
        intervalo_minutos
    )

    fim_expediente = datetime.strptime(hora_fim_exp, "%H:%M")

    disponiveis = []

    for horario in grade:
        inicio_candidato = datetime.strptime(horario, "%H:%M")
        fim_candidato = inicio_candidato + timedelta(minutes=duracao_minutos)

        if fim_candidato > fim_expediente:
            continue

        if horario_disponivel(data_str, horario, duracao_minutos):
            disponiveis.append(horario)

    return disponiveis


# ==========================
# FINANCEIRO / DASHBOARD
# ==========================

def _data_str(date_obj):
    return date_obj.strftime("%d/%m/%Y")


def _agendamentos_validos(agendamentos):
    return [ag for ag in agendamentos if ag[7] != "Cancelado"]


def resumo_financeiro(referencia=None):
    """
    Calcula ganhos e métricas de hoje, da semana (seg-dom) e do mês corrente,
    com base na data de referência (default: hoje).
    """
    if referencia is None:
        referencia = datetime.now()

    inicio_semana = referencia - timedelta(days=referencia.weekday())
    dias_semana = [
        _data_str(inicio_semana + timedelta(days=i)) for i in range(7)
    ]

    todos = listar_agendamentos()
    validos = _agendamentos_validos(todos)

    hoje_str = _data_str(referencia)
    mes_str = referencia.strftime("%m/%Y")

    ganhos_dia = 0.0
    ganhos_semana = 0.0
    ganhos_mes = 0.0
    atendimentos_dia = 0
    atendimentos_mes = 0

    for ag in validos:
        data_ag = ag[3]
        valor_ag = ag[6]

        if data_ag == hoje_str:
            ganhos_dia += valor_ag
            atendimentos_dia += 1

        if data_ag in dias_semana:
            ganhos_semana += valor_ag

        try:
            data_ag_obj = datetime.strptime(data_ag, "%d/%m/%Y")
        except ValueError:
            continue

        if data_ag_obj.strftime("%m/%Y") == mes_str:
            ganhos_mes += valor_ag
            atendimentos_mes += 1

    ticket_medio = (ganhos_mes / atendimentos_mes) if atendimentos_mes else 0.0

    return {
        "ganhos_dia": ganhos_dia,
        "ganhos_semana": ganhos_semana,
        "ganhos_mes": ganhos_mes,
        "atendimentos_dia": atendimentos_dia,
        "atendimentos_mes": atendimentos_mes,
        "ticket_medio": ticket_medio
    }


def historico_financeiro_mensal(meses=6):
    """Retorna lista de tuplas (mes/ano, total) dos últimos N meses, mais recente primeiro."""
    todos = _agendamentos_validos(listar_agendamentos())

    totais = {}

    for ag in todos:
        try:
            data_obj = datetime.strptime(ag[3], "%d/%m/%Y")
        except ValueError:
            continue

        chave = data_obj.strftime("%m/%Y")
        totais[chave] = totais.get(chave, 0.0) + ag[6]

    referencia = datetime.now()
    resultado = []

    for i in range(meses):
        mes_ref = referencia.month - i
        ano_ref = referencia.year

        while mes_ref <= 0:
            mes_ref += 12
            ano_ref -= 1

        chave = f"{mes_ref:02d}/{ano_ref}"
        resultado.append((chave, totais.get(chave, 0.0)))

    return resultado


def agendamentos_de_hoje():
    return _agendamentos_validos(
        listar_agendamentos_por_data(_data_str(datetime.now()))
    )


def agendamentos_de_amanha():
    amanha = datetime.now() + timedelta(days=1)
    return _agendamentos_validos(
        listar_agendamentos_por_data(_data_str(amanha))
    )
