"""PAINEL INTEGRA — demonstração com dados 100% sintéticos."""
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, timedelta

st.set_page_config(page_title="PAINEL INTEGRA", page_icon="🏥", layout="wide")
NAV = ["Visão executiva", "Internação Maternidade", "Clínica Cirúrgica", "Centro Cirúrgico", "CME", "Gestão de pessoas", "Projetos e prazos", "Equipamentos e riscos", "Integração de processos"]
SECTORS = NAV[1:6] + NAV[6:]
COLORS = ["#087e8b", "#173c5b", "#36a58b", "#e9aa47", "#cf6d67"]
st.markdown("""<style>
[data-testid="stSidebar"]{background:#12344d}
[data-testid="stSidebar"] *{color:#f1f7fa!important}
.block-container{padding-top:1.5rem}
h1,h2,h3{color:#12344d}
div[data-testid="stMetric"]{background:#eaf3f6;padding:14px;border-radius:12px;border:1px solid #d7e8ee}
</style>""", unsafe_allow_html=True)

@st.cache_data
def demo():
    dates = pd.date_range("2026-07-01", periods=92, freq="D")
    records = []
    for i, day in enumerate(dates):
        for j, sector in enumerate(SECTORS):
            records.append({"Data": day, "Setor": sector, "Atendimentos": 8 + (i * 7 + j * 11) % 27,
                            "Pendências": (i + j * 3) % 8, "Conformidade": 85 + (i + j * 5) % 15})
    return pd.DataFrame(records)

df = demo()
with st.sidebar:
    st.title("🏥 PAINEL INTEGRA")
    st.caption("Gestão Integrada Assistencial e Cirúrgica")
    page = st.radio("Módulos", NAV)
    st.divider()
    st.caption("DEMONSTRAÇÃO • dados fictícios")
    st.caption("Sem dados pessoais ou persistência")

st.title(page)
st.caption("PAINEL INTEGRA • Ambiente demonstrativo • Indicadores sintéticos, não assistenciais")
with st.container(border=True):
    a, b, c = st.columns([1.2, 1.2, 1.6])
    start = a.date_input("Data inicial", value=date(2026, 9, 1), min_value=date(2026, 7, 1), max_value=date(2026, 9, 30))
    end = b.date_input("Data final", value=date(2026, 9, 30), min_value=date(2026, 7, 1), max_value=date(2026, 9, 30))
    options = SECTORS if page == "Visão executiva" else [page]
    selected = c.multiselect("Setores", options, default=options)
if start > end:
    st.error("A data inicial não pode ser posterior à final.")
    st.stop()
filtered = df[(df["Data"].dt.date >= start) & (df["Data"].dt.date <= end) & df["Setor"].isin(selected)]
if filtered.empty:
    st.warning("Nenhum registro fictício para os filtros escolhidos.")
    st.stop()

def chart(data, x, y, title, color=None):
    fig = px.bar(data, x=x, y=y, color=color, title=title, color_discrete_sequence=COLORS)
    fig.update_layout(margin=dict(l=10,r=10,t=55,b=10), legend_title_text="")
    st.plotly_chart(fig, use_container_width=True)

total = int(filtered["Atendimentos"].sum())
pending = int(filtered["Pendências"].sum())
quality = float(filtered["Conformidade"].mean())
m1,m2,m3,m4 = st.columns(4)
m1.metric("Atividades simuladas", f"{total:,}".replace(",", "."))
m2.metric("Pendências simuladas", pending)
m3.metric("Conformidade média", f"{quality:.1f}%".replace(".", ","))
m4.metric("Setores selecionados", filtered["Setor"].nunique())
st.divider()

if page == "Visão executiva":
    left,right = st.columns(2)
    with left:
        chart(filtered.groupby("Setor",as_index=False)["Atendimentos"].sum(),"Setor","Atendimentos","Volume por setor")
    with right:
        trend = filtered.groupby("Data",as_index=False)["Atendimentos"].sum()
        st.plotly_chart(px.line(trend,x="Data",y="Atendimentos",title="Evolução diária",markers=True,color_discrete_sequence=COLORS),use_container_width=True)
elif page == "Internação Maternidade":
    st.info("Escopo: gestantes, puérperas e recém-nascidos internados. Centro Obstétrico excluído.")
    a,b,c=st.columns(3)
    a.metric("Gestantes internadas (simulação)", 12)
    b.metric("Puérperas internadas (simulação)", 18)
    c.metric("Recém-nascidos internados (simulação)", 15)
elif page == "Clínica Cirúrgica":
    st.info("Acompanhamento demonstrativo de pré-operatório, pós-operatório, altas e pendências assistenciais.")
elif page == "Centro Cirúrgico":
    st.info("Painel demonstrativo de produção cirúrgica, utilização de salas, cancelamentos e atrasos.")
elif page == "CME":
    st.info("Painel demonstrativo de processamento, esterilização, rastreabilidade e não conformidades.")
elif page == "Gestão de pessoas":
    st.info("Escalas, férias e absenteísmo: indicadores sintéticos, sem identificação de colaboradores.")
    a,b,c=st.columns(3)
    a.metric("Plantões previstos (fictícios)", 96)
    b.metric("Férias programadas (fictícias)", 7)
    c.metric("Absenteísmo simulado", "2,8%")
elif page == "Projetos e prazos":
    st.info("Controle demonstrativo de projetos, responsáveis por função, prazos e status.")
    projects=pd.DataFrame({"Projeto":["Fluxo de internação","Rastreabilidade CME","Checklist cirúrgico"],
      "Setor":["Internação Maternidade","CME","Centro Cirúrgico"],
      "Prazo":["2026-10-15","2026-10-25","2026-11-05"],"Status":["Em andamento","Planejado","Em andamento"]})
    st.dataframe(projects,hide_index=True,use_container_width=True)
elif page == "Equipamentos e riscos":
    st.info("Inventário e matriz de riscos ilustrativos, sem patrimônio real.")
    risk=pd.DataFrame({"Item":["Autoclave fictícia A","Monitor fictício B","Bomba fictícia C"],
      "Setor":["CME","Centro Cirúrgico","Clínica Cirúrgica"],"Risco":["Alto","Médio","Baixo"],
      "Situação":["Revisão programada","Operacional","Operacional"]})
    st.dataframe(risk,hide_index=True,use_container_width=True)
elif page == "Integração de processos":
    st.info("Mapa ilustrativo de interfaces: internação → centro cirúrgico → recuperação → clínica cirúrgica; CME fornece materiais processados.")
    st.graphviz_chart("""digraph {rankdir=LR; node [shape=box style=rounded]; "Internação" -> "Centro Cirúrgico"; "Centro Cirúrgico" -> "Clínica Cirúrgica"; "CME" -> "Centro Cirúrgico"; "Gestão de pessoas" -> "Centro Cirúrgico"; "Equipamentos" -> "CME";}""")
if page not in ["Visão executiva"]:
    trend=filtered.groupby("Data",as_index=False)["Atendimentos"].sum()
    st.plotly_chart(px.line(trend,x="Data",y="Atendimentos",title="Atividades por dia (fictícias)",markers=True,color_discrete_sequence=COLORS),use_container_width=True)
st.subheader("Detalhamento sintético")
summary=filtered.groupby("Setor",as_index=False).agg(Atividades=("Atendimentos","sum"),Pendências=("Pendências","sum"),Conformidade_media=("Conformidade","mean"))
summary["Conformidade_media"]=summary["Conformidade_media"].round(1)
st.dataframe(summary,hide_index=True,use_container_width=True)
st.download_button("Exportar resumo fictício (CSV)",summary.to_csv(index=False).encode("utf-8-sig"),"painel_integra_demo.csv","text/csv")
st.caption("Versão 1.1 demonstrativa • Não usar para decisões assistenciais ou registros institucionais.")
