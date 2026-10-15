
import streamlit as st
import pandas as pd
from supabase import create_client

# Colunas utilizadas pelo Dashboard Acadêmico
COLUNAS = [
    "disciplina",
    "categoria",
    "atividade",
    "nota_obtida",
    "nota_maxima"]

# CONEXÃO COM O SUPABASE
def cliente():
    """Cria uma conexão com o Supabase."""
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_ANON_KEY"])

# LOGIN DO ADMINISTRADOR
def login(email, senha):
    """Autentica o usuário no Supabase."""
    c = cliente()

    resposta = c.auth.sign_in_with_password({
        "email": email,
        "password": senha})

    if resposta.session is None:
        raise ValueError("Não foi possível iniciar a sessão.")

    st.session_state["auth"] = {
        "access": resposta.session.access_token,
        "refresh": resposta.session.refresh_token,
        "email": email}


def conectar():
    """Restaura a sessão autenticada do usuário."""
    sessao = st.session_state.get("auth")

    if not sessao:
        return None, None

    c = cliente()

    try:
        resposta = c.auth.set_session(
            sessao["access"],
            sessao["refresh"])

        if resposta.session is None or resposta.user is None:
            raise ValueError("Sessão inválida.")

        sessao["access"] = resposta.session.access_token
        sessao["refresh"] = resposta.session.refresh_token

        return c, resposta.user.id

    except Exception:
        st.session_state.pop("auth", None)
        return None, None

# CONSULTA PÚBLICA — VISITANTES
def carregar_publico():
    """
    Carrega as notas da VIEW pública.
    Não exige login e não modifica o banco.
    """
    c = cliente()

    registros = []
    inicio = 0
    tamanho_pagina = 1000

    while True:
        resposta = (
            c.table("notas_publicas")
            .select("*")
            .range(inicio, inicio + tamanho_pagina - 1)
            .execute())

        pagina = resposta.data or []
        registros.extend(pagina)

        if len(pagina) < tamanho_pagina:
            break

        inicio += tamanho_pagina

    df = pd.DataFrame(registros)

    if df.empty:
        return pd.DataFrame(columns=COLUNAS)

    for coluna in ["nota_obtida", "nota_maxima"]:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

    return df[COLUNAS]

# CONSULTA PRIVADA — ADMINISTRADOR
def carregar(c):
    """Carrega os registros acessíveis ao usuário autenticado."""
    registros = []
    inicio = 0
    tamanho_pagina = 1000

    while True:
        resposta = (
            c.table("notas_academicas")
            .select("*")
            .order("id")
            .range(inicio, inicio + tamanho_pagina - 1)
            .execute())

        pagina = resposta.data or []
        registros.extend(pagina)

        if len(pagina) < tamanho_pagina:
            break

        inicio += tamanho_pagina

    df = pd.DataFrame(registros)

    if df.empty:
        return pd.DataFrame(columns=["id", *COLUNAS])

    for coluna in ["nota_obtida", "nota_maxima"]:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

    return df

# CADASTRAR NOTAS — ADMINISTRADOR
def inserir(c, uid, linhas):
    """Insere registros vinculados ao usuário autenticado."""
    if not linhas:
        return

    dados = [
        {**linha, "user_id": uid}
        for linha in linhas]

    return (
        c.table("notas_academicas")
        .insert(dados)
        .execute())

# ATUALIZAR NOTA — ADMINISTRADOR
def atualizar(c, id, nota):
    """Atualiza a nota obtida de um registro."""
    return (
        c.table("notas_academicas")
        .update({"nota_obtida": float(nota)})
        .eq("id", int(id))
        .execute())

# EXCLUIR MATÉRIA — ADMINISTRADOR
def excluir(c, materia):
    """Exclui os registros de uma disciplina."""
    return (
        c.table("notas_academicas")
        .delete()
        .eq("disciplina", materia)
        .execute())
