import logging
import textwrap
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from banco_supabase import (
    login,
    conectar,
    carregar,
    carregar_publico,
    inserir,
    atualizar,
    excluir,
    COLUNAS,
)

st.set_page_config(
    page_title="Dashboard Acadêmico",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Paleta executiva sobria
COR_PRIMARIA = "#6366F1"
COR_SECUNDARIA = "#38BDF8"
COR_ROXO = "#A855F7"
COR_SUCESSO = "#10B981"
COR_ALERTA = "#F59E0B"
COR_PERIGO = "#F43F5E"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.markdown(
    """<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

:root {
    color-scheme: dark;
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}

.stApp, [data-testid="stAppViewContainer"] {
    background-color: #080C14;
    background-image: 
        radial-gradient(at 15% 0%, rgba(99, 102, 241, 0.12) 0px, transparent 45%),
        radial-gradient(at 85% 5%, rgba(56, 189, 248, 0.08) 0px, transparent 45%);
    color: #F1F5F9;
}

[data-testid="stHeader"] {
    background: rgba(8, 12, 20, 0.75);
    backdrop-filter: blur(12px);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1360px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D1322 0%, #090D18 100%);
    border-right: 1px solid rgba(148, 163, 184, 0.12);
}

[data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: #F8FAFC;
    font-weight: 700;
    letter-spacing: -0.02em;
}

/* Inputs & Selectboxes */
div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div {
    background-color: rgba(15, 23, 42, 0.75) !important;
    border-color: rgba(148, 163, 184, 0.18) !important;
    border-radius: 10px !important;
    transition: all 0.2s ease;
}

div[data-baseweb="input"] > div:focus-within,
div[data-baseweb="select"] > div:focus-within {
    border-color: #6366F1 !important;
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.25) !important;
}

/* Botões */
div.stButton > button, div.stFormSubmitButton > button {
    border-radius: 10px;
    font-weight: 600;
    padding: 0.55rem 1rem;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    border: 1px solid rgba(148, 163, 184, 0.18);
    background: rgba(30, 41, 59, 0.7);
    color: #F1F5F9;
}

div.stButton > button:hover, div.stFormSubmitButton > button:hover {
    border-color: rgba(99, 102, 241, 0.5);
    background: rgba(51, 65, 85, 0.8);
    transform: translateY(-1px);
}

div.stButton > button[kind="primary"],
div.stFormSubmitButton > button[kind="primary"] {
    background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);
    color: #FFFFFF;
    border: none;
    box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35);
}

div.stButton > button[kind="primary"]:hover,
div.stFormSubmitButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #818CF8 0%, #6366F1 100%);
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5);
    color: #FFFFFF;
}

/* Expanders */
[data-testid="stExpander"] {
    background: rgba(17, 24, 39, 0.65);
    border: 1px solid rgba(148, 163, 184, 0.12) !important;
    border-radius: 12px !important;
    overflow: hidden;
}

/* Tabs */
button[data-baseweb="tab"] {
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    color: #94A3B8 !important;
    letter-spacing: 0.01em;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #F8FAFC !important;
}

/* Hero Banner */
.hero-card {
    background: linear-gradient(135deg, rgba(19, 28, 46, 0.92) 0%, rgba(15, 23, 42, 0.78) 100%);
    border: 1px solid rgba(148, 163, 184, 0.14);
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 12px 32px -8px rgba(0, 0, 0, 0.45);
}

.hero-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #6366F1, #38BDF8, #A855F7);
}

.hero-top-row {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 10px;
    margin-bottom: 14px;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    background: rgba(99, 102, 241, 0.12);
    border: 1px solid rgba(99, 102, 241, 0.28);
    color: #A5B4FC;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 6px;
}

.hero-mode-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 6px;
}

.hero-title {
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    margin: 0 0 12px 0;
    color: #F8FAFC;
}

.hero-meta-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 10px 16px;
    margin-bottom: 12px;
    color: #E2E8F0;
    font-size: 0.88rem;
}

.hero-meta-item {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(30, 41, 59, 0.55);
    border: 1px solid rgba(148, 163, 184, 0.14);
    padding: 6px 14px;
    border-radius: 8px;
}

.hero-meta-label {
    color: #94A3B8;
    font-weight: 500;
}

.hero-subtitle {
    color: #94A3B8;
    font-size: 0.92rem;
    margin: 0;
}

/* KPI Cards Executivos */
.kpi-card {
    background: linear-gradient(180deg, rgba(19, 28, 46, 0.85) 0%, rgba(13, 19, 33, 0.9) 100%);
    border: 1px solid rgba(148, 163, 184, 0.12);
    border-radius: 14px;
    padding: 20px 22px;
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    height: 100%;
    position: relative;
    overflow: hidden;
}

.kpi-card:hover {
    transform: translateY(-2px);
    border-color: rgba(99, 102, 241, 0.35);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.35);
}

.kpi-accent {
    width: 28px;
    height: 3px;
    border-radius: 99px;
    margin-bottom: 12px;
}

.kpi-label {
    color: #94A3B8;
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 8px;
}

.kpi-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.85rem;
    font-weight: 700;
    color: #F8FAFC;
    line-height: 1.15;
    margin-bottom: 8px;
}

.kpi-sub {
    font-size: 0.78rem;
    font-weight: 500;
    color: #64748B;
}

/* Subject Cards (Boletim Visual) */
.subject-card {
    background: rgba(17, 24, 39, 0.75);
    border: 1px solid rgba(148, 163, 184, 0.12);
    border-radius: 12px;
    padding: 16px 18px;
    margin-bottom: 12px;
}

.subject-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.subject-name {
    font-weight: 700;
    font-size: 0.95rem;
    color: #F1F5F9;
}

.status-pill {
    font-size: 0.7rem;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 6px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

.progress-track {
    width: 100%;
    height: 7px;
    background: rgba(30, 41, 59, 0.9);
    border-radius: 999px;
    overflow: hidden;
    margin-bottom: 10px;
}

.progress-fill {
    height: 100%;
    border-radius: 999px;
    transition: width 0.4s ease;
}

.subject-meta {
    display: flex;
    justify-content: space-between;
    font-size: 0.76rem;
    color: #94A3B8;
}

/* Sidebar Status Card */
.sidebar-status {
    background: rgba(30, 41, 59, 0.55);
    border: 1px solid rgba(148, 163, 184, 0.14);
    border-radius: 10px;
    padding: 12px 14px;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
}
</style>""",
    unsafe_allow_html=True,
)


# FUNÇÕES AUXILIARES
def abreviar_materia(nome):
    nomes = {
        "Projeto de Software": "Projeto de<br>Software",
        "Fundamentos da Inteligência Artificial Aplicada": "Fundamentos<br>de IA",
        "Redes de Computadores": "Redes de<br>Computadores",
        "Arquitetura e Organização de Computadores": "Arquitetura e<br>Organização",
        "Segurança e Auditoria de Sistemas": "Segurança e<br>Auditoria",
        "Interface e Usabilidade": "Interface e<br>Usabilidade",
        "Engenharia de Software": "Engenharia de<br>Software",
    }
    if nome in nomes:
        return nomes[nome]
    if len(nome) > 18:
        linhas = textwrap.wrap(nome, width=16)
        return "<br>".join(linhas[:2])
    return nome


def formatar_nota(valor):
    numero = float(valor)
    texto = f"{numero:.10f}".rstrip("0").rstrip(".")
    if texto == "-0":
        texto = "0"
    return texto.replace(".", ",")


def avaliacao_valida(parte):
    categorias_avaliacao = ["Prova", "Recuperação", "Segunda Chamada"]
    avaliacoes = parte.loc[
        parte["categoria"].isin(categorias_avaliacao),
        "nota_obtida",
    ]
    if avaliacoes.empty:
        return 0.0
    return float(avaliacoes.max())


def tabela_resumo(df):
    colunas_resumo = [
        "Matéria",
        "Nota Final",
        "Nota da Prova",
        "Presença/Progresso",
        "Exercícios",
        "Trabalhos",
    ]

    if df.empty:
        return pd.DataFrame(columns=colunas_resumo)

    base = df.copy()
    base["disciplina"] = base["disciplina"].astype(str).str.strip()
    base["categoria"] = base["categoria"].astype(str).str.strip()
    base["nota_obtida"] = pd.to_numeric(
        base["nota_obtida"],
        errors="coerce",
    ).fillna(0.0)

    categorias_avaliacao = ["Prova", "Recuperação", "Segunda Chamada"]
    linhas = []

    for materia, parte in base.groupby("disciplina", sort=False):
        atividades_comuns = parte.loc[
            ~parte["categoria"].isin(categorias_avaliacao),
            "nota_obtida",
        ].sum()
        nota_avaliacao = avaliacao_valida(parte)
        nota_final = float(atividades_comuns + nota_avaliacao)

        presenca = float(
            parte.loc[
                parte["categoria"].isin(["Progresso em Aula", "Presença online"]),
                "nota_obtida",
            ].sum()
        )
        exercicios = float(
            parte.loc[
                parte["categoria"].isin(["Exercício", "Exercício de unidade"]),
                "nota_obtida",
            ].sum()
        )
        trabalhos = float(
            parte.loc[
                parte["categoria"] == "Trabalho",
                "nota_obtida",
            ].sum()
        )

        linhas.append(
            {
                "Matéria": materia,
                "Nota Final": nota_final,
                "Nota da Prova": nota_avaliacao,
                "Presença/Progresso": presenca,
                "Exercícios": exercicios,
                "Trabalhos": trabalhos,
            }
        )

    return pd.DataFrame(linhas, columns=colunas_resumo)


def tema_grafico(fig, altura=470, esquerda=50):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(
            color="#E2E8F0",
            family="Plus Jakarta Sans, sans-serif",
            size=12,
        ),
        title=dict(
            font=dict(
                size=18,
                color="#F8FAFC",
                family="Plus Jakarta Sans, sans-serif",
            ),
            x=0.02,
            xanchor="left",
        ),
        margin=dict(l=esquerda, r=35, t=80, b=60),
        height=altura,
        legend=dict(
            bgcolor="rgba(15, 23, 42, 0.6)",
            bordercolor="rgba(148, 163, 184, 0.15)",
            borderwidth=1,
            orientation="h",
            y=1.12,
            x=0,
        ),
        hoverlabel=dict(
            bgcolor="#1E293B",
            bordercolor="#475569",
            font=dict(
                color="#F8FAFC",
                family="Plus Jakarta Sans, sans-serif",
                size=13,
            ),
        ),
    )
    try:
        fig.update_layout(barcornerradius=6)
    except Exception:
        pass
    fig.update_xaxes(
        gridcolor="rgba(148, 163, 184, 0.08)",
        zerolinecolor="rgba(148, 163, 184, 0.15)",
    )
    fig.update_yaxes(
        gridcolor="rgba(148, 163, 184, 0.08)",
        zerolinecolor="rgba(148, 163, 184, 0.15)",
    )
    return fig


def render_kpi(titulo, valor, subtitulo, cor_hex):
    return f"""
    <div class="kpi-card">
        <div class="kpi-accent" style="background: {cor_hex};"></div>
        <div class="kpi-label">{titulo}</div>
        <div class="kpi-value">{valor}</div>
        <div class="kpi-sub">{subtitulo}</div>
    </div>
    """


# CONEXÃO E AUTENTICAÇÃO
with st.sidebar:
    st.markdown("## Painel Acadêmico")

    c, uid = conectar()
    admin_id = str(st.secrets.get("ADMIN_USER_ID", "")).strip()

    administrador = c is not None and bool(admin_id) and uid == admin_id

    if c is not None and not administrador:
        st.warning("Esta conta não possui acesso de administração.")
        if st.button("Sair da conta", use_container_width=True):
            st.session_state.pop("auth", None)
            st.rerun()

    elif administrador:
        st.markdown(
            """
            <div class="sidebar-status" style="border-color: rgba(16, 185, 129, 0.35); background: rgba(16, 185, 129, 0.08);">
                <span class="status-dot" style="background: #10B981;"></span>
                <div>
                    <div style="font-weight: 700; font-size: 0.84rem; color: #34D399;">Modo Administrador</div>
                    <div style="font-size: 0.74rem; color: #94A3B8;">Edição habilitada</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Sair da conta", use_container_width=True):
            st.session_state.pop("auth", None)
            st.rerun()

    else:
        st.markdown(
            """
            <div class="sidebar-status">
                <span class="status-dot" style="background: #38BDF8;"></span>
                <div>
                    <div style="font-weight: 700; font-size: 0.84rem; color: #E2E8F0;">Modo Visitante</div>
                    <div style="font-size: 0.74rem; color: #94A3B8;">Somente leitura</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.expander("Entrar como administrador"):
            with st.form("login"):
                email = st.text_input("E-mail")
                senha = st.text_input("Senha", type="password")
                entrar = st.form_submit_button(
                    "Entrar",
                    type="primary",
                    use_container_width=True,
                )

            if entrar:
                try:
                    login(email, senha)
                    st.rerun()
                except Exception:
                    logger.exception("Falha na autenticação")
                    st.error("Não foi possível entrar. Verifique suas credenciais.")

# CARREGAMENTO DOS DADOS
try:
    if administrador:
        dados = carregar(c)
    else:
        dados = carregar_publico()
except Exception:
    logger.exception("Falha ao carregar dados do Supabase")
    st.error("Não foi possível carregar os dados do Supabase. Tente novamente mais tarde.")
    st.stop()

# ÁREA ADMINISTRATIVA
if administrador:
    with st.sidebar:
        st.divider()
        st.markdown("### Gerenciamento")

        with st.expander("Cadastrar matéria", expanded=dados.empty):
            st.caption(
                "Informe as notas de cada atividade. "
                "A nota obtida será preenchida automaticamente com o mesmo valor da nota máxima."
            )
            with st.form("cadastro", clear_on_submit=True):
                materia = st.text_input("Nome da matéria")
                c_p, c_e = st.columns(2)
                presenca = c_p.number_input(
                    "Presença (máx)",
                    min_value=0.0,
                    max_value=100.0,
                    step=1.0,
                )
                exercicios = c_e.number_input(
                    "Exercícios (máx)",
                    min_value=0.0,
                    max_value=100.0,
                    step=1.0,
                )
                c_t, c_pr = st.columns(2)
                trabalho = c_t.number_input(
                    "Trabalho (máx)",
                    min_value=0.0,
                    max_value=100.0,
                    step=1.0,
                )
                prova = c_pr.number_input(
                    "Prova (máx)",
                    min_value=0.0,
                    max_value=100.0,
                    step=1.0,
                )
                cadastrar = st.form_submit_button(
                    "Cadastrar matéria",
                    type="primary",
                    use_container_width=True,
                )

            if cadastrar:
                nome = materia.strip()
                valores = [
                    ("Progresso em Aula", presenca),
                    ("Exercício", exercicios),
                    ("Trabalho", trabalho),
                    ("Prova", prova),
                ]
                existentes = (
                    dados["disciplina"]
                    .astype(str)
                    .str.strip()
                    .str.casefold()
                    .tolist()
                )

                if not nome:
                    st.error("Informe o nome da matéria.")
                elif nome.casefold() in existentes:
                    st.error("Essa matéria já existe.")
                elif not any(valor > 0 for _, valor in valores):
                    st.error("Informe pelo menos uma nota máxima.")
                else:
                    linhas = [
                        {
                            "disciplina": nome,
                            "categoria": categoria,
                            "atividade": categoria,
                            "nota_obtida": float(maxima),
                            "nota_maxima": float(maxima),
                        }
                        for categoria, maxima in valores
                        if maxima > 0
                    ]
                    try:
                        inserir(c, uid, linhas)
                        st.session_state["mensagem"] = "Matéria salva no Supabase!"
                        st.rerun()
                    except Exception:
                        logger.exception("Erro ao cadastrar matéria")
                        st.error("Não foi possível salvar a matéria.")

        # ATUALIZAR NOTA
        if not dados.empty:
            with st.expander("Atualizar nota obtida", expanded=True):
                nome = st.selectbox(
                    "Matéria",
                    dados["disciplina"].unique().tolist(),
                    key="sel_materia_att",
                )
                parte = dados[dados["disciplina"] == nome]
                opcoes = {
                    (
                        f"{r['categoria']} - {r['atividade']} "
                        f"(ID {r['id']}; máximo {r['nota_maxima']:g})"
                    ): int(r["id"])
                    for _, r in parte.iterrows()
                }
                escolha = st.selectbox("Atividade", list(opcoes), key="sel_ativ_att")
                registro_id = opcoes[escolha]
                registro = dados.loc[dados["id"] == registro_id].iloc[0]
                maxima = float(registro["nota_maxima"])

                with st.form("atualizar"):
                    nota = st.number_input(
                        f"Nota obtida (0 a {maxima:g})",
                        min_value=0.0,
                        max_value=maxima,
                        value=min(float(registro["nota_obtida"]), maxima),
                        step=1.0,
                    )
                    gravar = st.form_submit_button(
                        "Salvar nota obtida",
                        type="primary",
                        use_container_width=True,
                    )

                if gravar:
                    try:
                        atualizar(c, registro_id, nota)
                        st.session_state["mensagem"] = "Nota atualizada!"
                        st.rerun()
                    except Exception:
                        logger.exception("Erro ao atualizar nota")
                        st.error("Não foi possível atualizar a nota.")

            # EXCLUIR MATÉRIA
            with st.expander("Excluir matéria"):
                apagar = st.selectbox(
                    "Matéria para excluir",
                    dados["disciplina"].unique().tolist(),
                )
                confirma = st.checkbox("Confirmo a exclusão definitiva desta matéria")
                if st.button(
                    "Excluir matéria",
                    disabled=not confirma,
                    use_container_width=True,
                ):
                    try:
                        excluir(c, apagar)
                        st.session_state["mensagem"] = "Matéria excluída!"
                        st.rerun()
                    except Exception:
                        logger.exception("Erro ao excluir matéria")
                        st.error("Não foi possível excluir a matéria.")

        # IMPORTAÇÃO DE CSV
        with st.expander("Importar CSV antigo"):
            arquivo = st.file_uploader("Selecione notas_academicas.csv", type="csv")
            if arquivo is not None:
                try:
                    antigo = pd.read_csv(arquivo, encoding="utf-8-sig")
                    if any(coluna not in antigo.columns for coluna in COLUNAS):
                        st.error("O CSV precisa ter as cinco colunas originais.")
                    else:
                        antigo = antigo[COLUNAS].copy()
                        for coluna in ("nota_obtida", "nota_maxima"):
                            antigo[coluna] = pd.to_numeric(
                                antigo[coluna],
                                errors="raise",
                            )
                        valido = (
                            antigo[COLUNAS[:3]].notna().all().all()
                            and (antigo["nota_maxima"] > 0).all()
                            and (antigo["nota_obtida"] >= 0).all()
                            and (antigo["nota_obtida"] <= antigo["nota_maxima"]).all()
                        )
                        if not valido:
                            st.error("CSV contém campos vazios ou notas inválidas.")
                        elif st.button(
                            "Importar (atenção: pode duplicar registros)",
                            type="primary",
                            use_container_width=True,
                        ):
                            inserir(c, uid, antigo.to_dict(orient="records"))
                            st.session_state["mensagem"] = "CSV importado!"
                            st.rerun()
                except Exception:
                    logger.exception("Erro na importação do CSV")
                    st.error("Não foi possível importar o CSV.")

# MENSAGENS E CABEÇALHO
if "mensagem" in st.session_state:
    st.success(st.session_state.pop("mensagem"))

modo_cor = "#10B981" if administrador else "#38BDF8"
modo_bg = "rgba(16, 185, 129, 0.12)" if administrador else "rgba(56, 189, 248, 0.12)"
modo_txt = "Administração" if administrador else "Visualização Pública"

st.markdown(
    f"""
    <div class="hero-card">
        <div class="hero-top-row">
            <span class="hero-badge">Portfólio Acadêmico</span>
            <span class="hero-mode-pill" style="color: {modo_cor}; background: {modo_bg}; border: 1px solid {modo_cor}44;">
                {modo_txt}
            </span>
        </div>
        <h1 class="hero-title">DASHBOARD ACADÊMICO</h1>
        <div class="hero-meta-grid">
            <span class="hero-meta-item"><span class="hero-meta-label">Discente:</span> <b>Wenndy Ferreira dos Santos</b></span>
            <span class="hero-meta-item"><span class="hero-meta-label">Curso:</span> <b>Análise e Desenvolvimento de Sistemas (ADS)</b></span>
            <span class="hero-meta-item"><span class="hero-meta-label">Instituição:</span> <b>Anhanguera</b></span>
        </div>
        <p class="hero-subtitle">Acompanhamento de notas, avaliações e desempenho acadêmico por disciplina.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# RESUMO ACADÊMICO
resumo = tabela_resumo(dados)

if resumo.empty:
    st.info("Nenhuma matéria cadastrada no momento.")
    st.stop()

total_disc = len(resumo)
media_final = resumo["Nota Final"].mean()
aprovadas = int((resumo["Nota Final"] >= 60).sum())
taxa_aprov = (aprovadas / total_disc * 100) if total_disc > 0 else 0
maior_nota = resumo["Nota Final"].max()
melhor_materia = resumo.loc[resumo["Nota Final"].idxmax(), "Matéria"]

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(
        render_kpi(
            "Disciplinas",
            f"{total_disc}",
            "Matérias registradas no histórico",
            COR_PRIMARIA,
        ),
        unsafe_allow_html=True,
    )

with c2:
    cor_media = COR_SUCESSO if media_final >= 60 else COR_ALERTA
    st.markdown(
        render_kpi(
            "Média das notas finais",
            f'{formatar_nota(round(media_final, 1))} <span style="font-size:1rem;color:#64748B;">/ 100</span>',
            "Meta de aprovação: 60 pontos",
            cor_media,
        ),
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        render_kpi(
            "Aprovadas (≥ 60)",
            f'{aprovadas} <span style="font-size:1rem;color:#64748B;">de {total_disc}</span>',
            f"{taxa_aprov:.0f}% de aproveitamento",
            COR_SUCESSO,
        ),
        unsafe_allow_html=True,
    )

with c4:
    melhor_curto = (
        melhor_materia
        if len(melhor_materia) <= 24
        else melhor_materia[:22] + "…"
    )
    st.markdown(
        render_kpi(
            "Maior nota",
            f'{formatar_nota(maior_nota)} <span style="font-size:1rem;color:#64748B;">pts</span>',
            f"Destaque: {melhor_curto}",
            COR_SECUNDARIA,
        ),
        unsafe_allow_html=True,
    )

st.markdown('<div style="height: 8px;"></div>', unsafe_allow_html=True)
st.caption("Notas ainda não lançadas contam como zero.")

resumo["Nome Gráfico"] = resumo["Matéria"].apply(abreviar_materia)
resumo["Nota Final Formatada"] = resumo["Nota Final"].apply(formatar_nota)
resumo["Nota Prova Formatada"] = resumo["Nota da Prova"].apply(formatar_nota)

aba_visao, aba_boletim, aba_dados = st.tabs(
    [
        "Visão Gráfica",
        "Progresso por Matéria",
        "Tabelas e Registros",
    ]
)

with aba_visao:
    # GRÁFICO 1 - NOTA FINAL POR MATÉRIA (LARGURA TOTAL)
    cores_marcadores = [
        COR_SUCESSO if v >= 60 else COR_PERIGO
        for v in resumo["Nota Final"]
    ]
    fig1 = go.Figure()
    fig1.add_trace(
        go.Scatter(
            x=resumo["Nome Gráfico"],
            y=resumo["Nota Final"],
            mode="lines+markers+text",
            text=resumo["Nota Final Formatada"].tolist(),
            textposition="top center",
            textfont=dict(
                size=12,
                color="#F8FAFC",
                family="JetBrains Mono, monospace",
            ),
            line=dict(
                color=COR_PRIMARIA,
                width=3.5,
                shape="spline",
                smoothing=0.8,
            ),
            fill="tozeroy",
            fillcolor="rgba(99, 102, 241, 0.12)",
            marker=dict(
                size=11,
                color=cores_marcadores,
                line=dict(width=2.5, color="#0F172A"),
            ),
            customdata=resumo[["Matéria", "Nota Final Formatada"]],
            hovertemplate="<b>%{customdata[0]}</b><br>Nota final: <b>%{customdata[1]} pts</b><extra></extra>",
        )
    )
    fig1.add_hline(
        y=60,
        line_dash="dash",
        line_color=COR_SUCESSO,
        opacity=0.75,
        annotation_text="Aprovação: 60",
        annotation_position="top left",
        annotation_font=dict(color=COR_SUCESSO, size=11),
    )
    fig1.update_layout(title="Nota final por matéria")
    fig1.update_xaxes(title=None, tickangle=0, tickfont=dict(size=11))
    fig1.update_yaxes(
        title="Nota final",
        range=[0, max(108, float(resumo["Nota Final"].max()) * 1.15)],
    )
    st.plotly_chart(
        tema_grafico(fig1, altura=480),
        use_container_width=True,
    )

    # GRÁFICO 2 - NOTAS DAS PROVAS (ABAIXO DO GRÁFICO 1, LARGURA TOTAL)
    fig2 = px.bar(
        resumo,
        x="Nota da Prova",
        y="Matéria",
        orientation="h",
        title="Notas das provas por matéria",
        color="Nota da Prova",
        color_continuous_scale=["#4F46E5", "#38BDF8", "#10B981"],
    )
    fig2.update_traces(
        text=resumo["Nota Prova Formatada"].tolist(),
        textposition="outside",
        cliponaxis=False,
        hovertemplate="<b>%{y}</b><br>Nota da prova: <b>%{text} pts</b><extra></extra>",
    )
    fig2.update_coloraxes(showscale=False)
    fig2.update_xaxes(
        title="Nota da avaliação",
        range=[0, max(55, float(resumo["Nota da Prova"].max()) * 1.15)],
    )
    fig2.update_yaxes(
        title=None,
        automargin=True,
        categoryorder="array",
        categoryarray=resumo["Matéria"].tolist()[::-1],
    )
    st.plotly_chart(
        tema_grafico(
            fig2,
            altura=max(440, 62 * len(resumo)),
            esquerda=240,
        ),
        use_container_width=True,
    )

    # GRÁFICO 3 - COMPARAÇÃO DE NOTAS (ABAIXO DO GRÁFICO 2, LARGURA TOTAL)
    categorias_comparacao = ["Presença/Progresso", "Exercícios", "Trabalhos"]
    fig3 = px.bar(
        resumo,
        x="Nome Gráfico",
        y=categorias_comparacao,
        barmode="group",
        title="Comparação de notas por matéria",
        color_discrete_map={
            "Presença/Progresso": COR_PRIMARIA,
            "Exercícios": COR_SECUNDARIA,
            "Trabalhos": COR_ROXO,
        },
        labels={"value": "Nota", "variable": "Categoria"},
    )

    for trace in fig3.data:
        valores = [float(valor) for valor in trace.y]
        rotulos = [formatar_nota(valor) for valor in valores]
        trace.update(
            text=rotulos,
            texttemplate="%{text}",
            textposition="outside",
            cliponaxis=False,
            hovertemplate="%{x}<br>" + trace.name + ": <b>%{text}</b><extra></extra>",
        )

    fig3.update_xaxes(title=None, tickangle=0, tickfont=dict(size=11))
    fig3.update_yaxes(
        title="Pontos",
        range=[
            0,
            max(
                35,
                float(resumo[categorias_comparacao].max().max()) * 1.2,
            ),
        ],
    )
    st.plotly_chart(
        tema_grafico(fig3, altura=490),
        use_container_width=True,
    )

with aba_boletim:
    st.markdown("#### Acompanhamento Individual por Disciplina")
    st.caption(
        "Barras de progresso rumo aos 100 pontos. A marca de 60 pontos define a aprovação na matéria."
    )

    col_b1, col_b2 = st.columns(2, gap="medium")
    for idx, linha in resumo.iterrows():
        nota_f = float(linha["Nota Final"])
        pct = min(max(nota_f, 0.0), 100.0)
        aprovado = nota_f >= 60
        cor_barra = (
            "linear-gradient(90deg, #10B981, #34D399)"
            if aprovado
            else "linear-gradient(90deg, #6366F1, #38BDF8)"
        )
        cor_status = "#10B981" if aprovado else "#F59E0B"
        bg_status = (
            "rgba(16, 185, 129, 0.12)"
            if aprovado
            else "rgba(245, 158, 11, 0.12)"
        )
        txt_status = (
            "Aprovado"
            if aprovado
            else f"Faltam {formatar_nota(max(0, 60 - nota_f))} pts"
        )

        card_html = f"""
        <div class="subject-card">
            <div class="subject-header">
                <span class="subject-name">{linha['Matéria']}</span>
                <span class="status-pill" style="color: {cor_status}; background: {bg_status}; border: 1px solid {cor_status}44;">
                    {txt_status} • {formatar_nota(nota_f)}/100
                </span>
            </div>
            <div class="progress-track">
                <div class="progress-fill" style="width: {pct}%; background: {cor_barra};"></div>
            </div>
            <div class="subject-meta">
                <span>Prova: <b>{formatar_nota(linha['Nota da Prova'])}</b></span>
                <span>Trabalhos: <b>{formatar_nota(linha['Trabalhos'])}</b></span>
                <span>Exercícios: <b>{formatar_nota(linha['Exercícios'])}</b></span>
                <span>Presença: <b>{formatar_nota(linha['Presença/Progresso'])}</b></span>
            </div>
        </div>
        """
        if idx % 2 == 0:
            col_b1.markdown(card_html, unsafe_allow_html=True)
        else:
            col_b2.markdown(card_html, unsafe_allow_html=True)

with aba_dados:
    colunas_auxiliares = [
        "Nome Gráfico",
        "Nota Final Formatada",
        "Nota Prova Formatada",
    ]
    st.markdown("#### Resumo das Notas")
    st.dataframe(
        resumo.drop(columns=colunas_auxiliares, errors="ignore"),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Nota Final": st.column_config.ProgressColumn(
                "Nota Final (0–100)",
                format="%.1f pts",
                min_value=0,
                max_value=100,
            ),
        },
    )

    st.markdown("#### Registros Acadêmicos")
    st.dataframe(dados[COLUNAS], use_container_width=True, hide_index=True)

st.divider()
st.caption(
    "Dashboard Acadêmico • Desenvolvido por Wenndy Ferreira dos Santos • "
    "Python · Streamlit · Pandas · Plotly · Supabase • "
    + ("Administração" if administrador else "Visualização pública")
)
