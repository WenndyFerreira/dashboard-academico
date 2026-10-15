import streamlit as st
import pandas as pd
import plotly.express as px
from banco_supabase import login, conectar, carregar, carregar_publico, inserir, atualizar, excluir, COLUNAS
st.set_page_config(page_title='Dashboard Acadêmico',page_icon='🎓',layout='wide')
VERMELHO='#E53945'
st.markdown('''<style>
:root {color-scheme: dark;}
.stApp, [data-testid="stAppViewContainer"] {background:#0B0C0F; color:#F5F5F7;}
[data-testid="stSidebar"] {background:#15161B; border-right:1px solid #303139;}
[data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {color:#FAFAFC;}
[data-testid="stHeader"] {background:rgba(11,12,15,.9);}
h1,h2,h3 {letter-spacing:-.02em;}
h1 {font-size:2.4rem!important;}
[data-testid="stMetric"] {background:#181A20; border:1px solid #2D2F38; border-radius:14px; padding:18px;}
[data-testid="stMetricValue"] {color:#FAFAFC;}
div.stButton > button[kind="primary"] {background:#C92534; color:white; border:0; font-weight:700;}
div.stButton > button[kind="primary"]:hover {background:#E53945; color:white;}
div.stButton > button {border-radius:9px;}
[data-testid="stVerticalBlockBorderWrapper"] {border-color:#2D2F38;}
hr {border-color:#303139;}
.hero {background:#16171C; border:1px solid #303139; border-left:4px solid #E53945; padding:23px 28px; border-radius:14px; margin-bottom:22px;}
.hero h1 {margin:0 0 8px 0; color:white;}
.hero p {color:#B7BAC4; margin:0;}
.small-muted {color:#A6A8B1; font-size:.87rem;}
</style>''', unsafe_allow_html=True)

def abreviar_materia(nome):
    nomes = {
        'Projeto de Software': 'Projeto de<br>Software',
        'Fundamentos da Inteligência Artificial Aplicada': 'Fundamentos<br>de IA',
        'Redes de Computadores': 'Redes de<br>Computadores',
        'Arquitetura e Organização de Computadores': 'Arquitetura e<br>Organização',
        'Segurança e Auditoria de Sistemas': 'Segurança e<br>Auditoria',
        'Interface e Usabilidade': 'Interface e<br>Usabilidade',
        'Engenharia de Software': 'Engenharia de<br>Software',}
    return nomes.get(nome, nome)

def avaliacao_valida(parte):
    for categoria in ('Recuperação', 'Segunda Chamada', 'Prova'):
        notas = parte.loc[parte['categoria'] == categoria, 'nota_obtida']
        if not notas.empty:
            return float(notas.max())
    return 0.0

def tabela_resumo(df):
    linhas = []
    for materia, parte in df.groupby('disciplina', sort=False):
        comuns = parte.loc[~parte['categoria'].isin(['Prova', 'Recuperação', 'Segunda Chamada']), 'nota_obtida'].sum()
        linhas.append({'Matéria': materia, 'Nota Final': float(comuns + avaliacao_valida(parte)), 'Nota da Prova': avaliacao_valida(parte),
            'Presença/Progresso': float(parte.loc[parte['categoria'].isin(['Progresso em Aula','Presença online']), 'nota_obtida'].sum()),
            'Exercícios': float(parte.loc[parte['categoria'].isin(['Exercício','Exercício de unidade']), 'nota_obtida'].sum()),
            'Trabalhos': float(parte.loc[parte['categoria'] == 'Trabalho', 'nota_obtida'].sum())})
    return pd.DataFrame(linhas, columns=['Matéria','Nota Final','Nota da Prova','Presença/Progresso','Exercícios','Trabalhos'])

def tema_grafico(fig, altura=470, esquerda=50):
    fig.update_layout(
        template='plotly_dark', paper_bgcolor='#17191F', plot_bgcolor='#17191F',
        font=dict(color='#EDEEF2', family='Arial', size=12),
        title=dict(font=dict(size=19, color='#FFFFFF'), x=0.02, xanchor='left'),
        margin=dict(l=esquerda, r=35, t=80, b=65), height=altura,
        legend=dict(bgcolor='rgba(0,0,0,0)', orientation='h', y=1.12, x=0),
        hoverlabel=dict(bgcolor='#252831', font_color='white'))
    fig.update_xaxes(gridcolor='#292B33', zerolinecolor='#292B33')
    fig.update_yaxes(gridcolor='#292B33', zerolinecolor='#292B33')
    return fig


with st.sidebar:
    st.markdown('## 🎓 Painel acadêmico')
    c, uid = conectar()
    admin_id = st.secrets.get('ADMIN_USER_ID', '').strip()
    administrador = c is not None and uid == admin_id and bool(admin_id)
    if c is not None and not administrador:
        st.warning('Esta conta não possui acesso de administração.')
        if st.button('Sair da conta'):
            st.session_state.pop('auth', None)
            st.rerun()
    elif administrador:
        st.success('Modo administrador')
        if st.button('Sair da conta'):
            st.session_state.pop('auth', None)
            st.rerun()
    else:
        st.caption('Modo visitante · somente leitura')
        with st.expander('🔐 Entrar como administrador'):
            with st.form('login'):
                email = st.text_input('E-mail')
                senha = st.text_input('Senha', type='password')
                entrar = st.form_submit_button('Entrar', type='primary')
            if entrar:
                try:
                    login(email, senha)
                    st.rerun()
                except Exception:
                    st.error('Não foi possível entrar. Verifique suas credenciais.')
try:
    dados = carregar(c) if administrador else carregar_publico()
except Exception as erro:
    st.error('Não foi possível carregar os dados do Supabase.')
    st.exception(erro)  # Diagnóstico temporário: remova antes da publicação pública.
    st.stop()
if administrador:
    with st.sidebar:
        st.divider();st.markdown('### Cadastrar matéria')
        st.caption('Informe somente as notas máximas. Notas obtidas começam em zero.')
        with st.form('cadastro',clear_on_submit=True):
            materia=st.text_input('Nome da matéria')
            presenca=st.number_input('Presença / Progresso — nota máxima',min_value=0.,max_value=100.,step=1.)
            exercicios=st.number_input('Exercícios — nota máxima',min_value=0.,max_value=100.,step=1.)
            trabalho=st.number_input('Trabalho — nota máxima',min_value=0.,max_value=100.,step=1.)
            prova=st.number_input('Prova — nota máxima',min_value=0.,max_value=100.,step=1.)
            cadastrar=st.form_submit_button('Cadastrar matéria',type='primary',use_container_width=True)
        if cadastrar:
            nome=materia.strip()
            valores=[('Progresso em Aula',presenca),('Exercício',exercicios),('Trabalho',trabalho),('Prova',prova)]
            if not nome: st.error('Informe o nome da matéria.')
            elif nome.casefold() in dados['disciplina'].astype(str).str.casefold().tolist(): st.error('Essa matéria já existe.')
            elif not any(v>0 for _,v in valores): st.error('Informe pelo menos uma nota máxima.')
            else:
                linhas=[{'disciplina':nome,'categoria':cat,'atividade':cat,'nota_obtida':0.,'nota_maxima':float(maxima)} for cat,maxima in valores if maxima>0]
                try: inserir(c,uid,linhas); st.session_state['mensagem']='Matéria salva no Supabase!';st.rerun()
                except Exception as e: st.error(f'Erro ao salvar: {e}')
        st.divider();st.markdown('### Atualizar nota obtida')
        if not dados.empty:
            with st.form('atualizar'):
                nome=st.selectbox('Matéria',dados['disciplina'].unique().tolist())
                parte=dados[dados['disciplina']==nome]
                opcoes={f"{r['categoria']} — {r['atividade']} (ID {r['id']}; máximo {r['nota_maxima']:g})":int(r['id']) for _,r in parte.iterrows()}
                escolha=st.selectbox('Atividade',list(opcoes));id=opcoes[escolha]
                registro=dados.loc[dados['id']==id].iloc[0];maxima=float(registro['nota_maxima'])
                nota=st.number_input('Nota obtida',min_value=0.,max_value=maxima,value=min(float(registro['nota_obtida']),maxima),step=1.)
                gravar=st.form_submit_button('Salvar nota obtida',use_container_width=True)
            if gravar:
                try: atualizar(c,id,nota);st.session_state['mensagem']='Nota atualizada!';st.rerun()
                except Exception as e: st.error(f'Erro ao atualizar: {e}')
        st.divider();st.markdown('### Excluir matéria')
        if not dados.empty:
            apagar=st.selectbox('Matéria para excluir',dados['disciplina'].unique().tolist())
            confirma=st.checkbox('Confirmo a exclusão definitiva desta matéria')
            if st.button('🗑️ Excluir matéria',disabled=not confirma,use_container_width=True):
                try: excluir(c,apagar);st.session_state['mensagem']='Matéria excluída!';st.rerun()
                except Exception as e: st.error(f'Erro ao excluir: {e}')
        st.divider()
        with st.expander('Importar CSV antigo'):
            arquivo=st.file_uploader('Selecione notas_academicas.csv',type='csv')
            if arquivo is not None:
                try:
                    antigo=pd.read_csv(arquivo,encoding='utf-8-sig')
                    if any(k not in antigo.columns for k in COLUNAS): st.error('O CSV precisa ter as cinco colunas originais.')
                    else:
                        antigo=antigo[COLUNAS].copy()
                        for k in ('nota_obtida','nota_maxima'): antigo[k]=pd.to_numeric(antigo[k],errors='raise')
                        valido=(antigo[COLUNAS[:3]].notna().all().all() and (antigo['nota_maxima']>0).all() and (antigo['nota_obtida']>=0).all() and (antigo['nota_obtida']<=antigo['nota_maxima']).all())
                        if not valido: st.error('CSV contém campos vazios ou notas inválidas.')
                        elif st.button('Importar (atenção: pode duplicar registros)'):
                            inserir(c,uid,antigo.to_dict(orient='records'));st.session_state['mensagem']='CSV importado!';st.rerun()
                except Exception as e: st.error(f'Erro na importação: {e}')
if 'mensagem' in st.session_state: st.success(st.session_state.pop('mensagem'))
st.markdown('<div class="hero"><h1>🎓 DASHBOARD ACADÊMICO</h1><p>Visão geral das notas e avaliações por disciplina</p></div>',unsafe_allow_html=True)
st.caption('Desenvolvido por Wenndy Ferreira dos Santos • Supabase • ' + ('Administração' if administrador else 'Visualização pública'))
resumo=tabela_resumo(dados)
if resumo.empty: st.info('Cadastre uma matéria ou importe o CSV antigo.');st.stop()
c1,c2,c3,c4=st.columns(4)
c1.metric('Disciplinas',len(resumo));c2.metric('Média das notas finais',f"{resumo['Nota Final'].mean():.1f} / 100")
c3.metric('Aprovadas (≥ 60)',int((resumo['Nota Final']>=60).sum()));c4.metric('Maior nota',f"{resumo['Nota Final'].max():g}")
st.caption('Notas ainda não lançadas contam como zero.');st.divider()
resumo['Nome Gráfico']=resumo['Matéria'].apply(abreviar_materia)
fig1=px.line(resumo,x='Nome Gráfico',y='Nota Final',markers=True,text='Nota Final',title='Nota final por matéria',color_discrete_sequence=[VERMELHO],hover_data={'Matéria':True,'Nome Gráfico':False})
fig1.update_traces(textposition='top center',line=dict(width=3),marker=dict(size=10));fig1.update_xaxes(title=None,tickangle=0,tickfont=dict(size=10))
fig1.update_yaxes(title='Nota final',range=[0,max(105,resumo['Nota Final'].max()*1.12)])
fig1.add_hline(y=60,line_dash='dash',line_color='#FFFFFF',opacity=.6,annotation_text='Aprovação: 60',annotation_position='top left')
st.plotly_chart(tema_grafico(fig1,altura=490),use_container_width=True)
fig2=px.bar(resumo,x='Nota da Prova',y='Matéria',orientation='h',text='Nota da Prova',title='Notas das provas por matéria',color_discrete_sequence=[VERMELHO])
fig2.update_traces(textposition='outside',cliponaxis=False);fig2.update_xaxes(title='Nota da avaliação',range=[0,max(55,resumo['Nota da Prova'].max()*1.13)])
fig2.update_yaxes(title=None,automargin=True,categoryorder='array',categoryarray=resumo['Matéria'].tolist()[::-1])
st.plotly_chart(tema_grafico(fig2,altura=max(440,65*len(resumo)),esquerda=250),use_container_width=True)
fig3=px.bar(resumo,x='Nome Gráfico',y=['Presença/Progresso','Exercícios','Trabalhos'],barmode='group',title='Comparação de notas por matéria',color_discrete_map={'Presença/Progresso':'#E53945','Exercícios':'#FFFFFF','Trabalhos':'#A7ABB5'},labels={'value':'Nota','variable':'Categoria'})
fig3.update_traces(texttemplate='%{y:g}',textposition='outside',cliponaxis=False);fig3.update_xaxes(title=None,tickangle=0,tickfont=dict(size=10))
fig3.update_yaxes(title='Pontos',range=[0,max(35,resumo[['Presença/Progresso','Exercícios','Trabalhos']].max().max()*1.18)])
st.plotly_chart(tema_grafico(fig3,altura=500),use_container_width=True)
with st.expander('Ver resumo das notas'): st.dataframe(resumo.drop(columns=['Nome Gráfico']),use_container_width=True,hide_index=True)
with st.expander('Ver registros acadêmicos'): st.dataframe(dados[COLUNAS],use_container_width=True,hide_index=True)
st.caption('Dashboard Acadêmico • Python · Streamlit · Pandas · Plotly · Supabase')
