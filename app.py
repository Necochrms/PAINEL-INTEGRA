"""PAINEL INTEGRA | gestão integrada assistencial e cirúrgica."""
import streamlit as st
import pandas as pd
import plotly.express as px
from modules.indicators import indicators, COVERAGE, MONTHS

st.set_page_config(page_title="PAINEL INTEGRA",page_icon="🏥",layout="wide")
st.markdown("""<style>
[data-testid="stSidebar"]{background:#102f46}
[data-testid="stSidebar"] *{color:#f4fbfc!important}
.block-container{padding-top:1.5rem}
h1,h2,h3{color:#15364c}
[data-testid="stMetric"]{background:#edf6f8;border:1px solid #d6e7ec;border-radius:12px;padding:14px}
</style>""",unsafe_allow_html=True)
NAV=["Visão executiva","Internação Maternidade","Clínica Cirúrgica","Centro Cirúrgico","CME","Gestão de pessoas","Projetos e prazos","Equipamentos e riscos","Integração de processos"]
with st.sidebar:
    st.title("🏥 PAINEL INTEGRA")
    st.caption("Gestão Integrada Assistencial e Cirúrgica")
    page=st.radio("Navegação",NAV)
    st.divider()
    st.caption("Base: relatórios setoriais 2026")
    st.caption("Somente dados agregados • sem identificação pessoal")
if "selected_page" not in st.session_state: st.session_state.selected_page="Visão executiva"
st.title(page)
if page=="Visão executiva":
    st.subheader("Unidades assistenciais")
    c1,c2,c3,c4=st.columns(4)
    for col,unit in zip([c1,c2,c3,c4],["Internação Maternidade","Clínica Cirúrgica","Centro Cirúrgico","CME"]):
        with col:
            st.markdown("### "+unit)
            count=indicators().query("Unidade == @unit")["Indicador"].nunique()
            st.metric("Indicadores disponíveis",count)
            if st.button("Abrir painel →",key="open_"+unit,use_container_width=True):
                st.session_state.selected_page=unit
                st.rerun()
if st.session_state.selected_page!="Visão executiva" and page=="Visão executiva":
    page=st.session_state.selected_page
    st.title("Painel: "+page)
    if st.button("← Voltar à visão executiva"):
        st.session_state.selected_page="Visão executiva"
        st.rerun()
elif page!="Visão executiva":
    st.session_state.selected_page="Visão executiva"
st.caption("Painel demonstrativo baseado em relatórios setoriais recebidos • 2026")
df=indicators()
units=list(COVERAGE) if page=="Visão executiva" else ([page] if page in COVERAGE else [])
if page=="Gestão de pessoas": units=["CME","Centro Cirúrgico"]
if units:
    selected=st.multiselect("Unidades",units,default=units)
    data=df[df["Unidade"].isin(selected)]
    if page=="Gestão de pessoas": data=data[data["Indicador"].str.contains("Absenteísmo")]
    elif page!="Visão executiva": data=data[~data["Indicador"].str.contains("Absenteísmo")]
    indicators_available=sorted(data["Indicador"].unique())
    names=st.multiselect("Indicadores",indicators_available,default=indicators_available[:3])
    months=st.slider("Período de referência (meses de 2026)",1,8,(1,8))
    data=data[data["Indicador"].isin(names)&data["Ordem"].between(*months)]
    if data.empty:
        st.warning("Não há valores transcritos para esta combinação de filtros.")
    else:
        k1,k2,k3=st.columns(3)
        k1.metric("Indicadores exibidos",data["Indicador"].nunique())
        k2.metric("Unidades com dados",data["Unidade"].nunique())
        k3.metric("Registros mensais",len(data))
        for indicator in names:
            sub=data[data["Indicador"]==indicator].sort_values("Ordem")
            if sub.empty: continue
            st.subheader(indicator)
            fig=px.line(sub,x="Mês",y="Valor",color="Unidade",markers=True,category_orders={"Mês":MONTHS},
                        color_discrete_sequence=["#078c93","#174567"])
            fig.update_layout(legend_title_text="",margin=dict(l=5,r=5,t=12,b=5))
            st.plotly_chart(fig,use_container_width=True)
        st.subheader("Dados e rastreabilidade")
        st.dataframe(data[["Unidade","Indicador","Mês","Valor","Fonte"]],hide_index=True,use_container_width=True)
        st.download_button("Exportar tabela agregada CSV",data.to_csv(index=False).encode("utf-8-sig"),
                           "indicadores_agregados_2026.csv","text/csv")
elif page in COVERAGE:
    st.info(COVERAGE[page])
    if page=="Internação Maternidade":
        st.markdown("**Escopo:** gestantes, puérperas e recém-nascidos internados. **Centro Obstétrico não incluído.**")
    st.warning("Os valores de indicadores desta unidade ainda precisam de extração e conferência. Não serão inventados.")
elif page=="Projetos e prazos":
    st.info("Modelo demonstrativo. Os itens abaixo são exemplos e não registros institucionais.")
    st.dataframe(pd.DataFrame({"Projeto fictício":["Rastreabilidade de materiais","Fluxo de alta","Checklist de transferência"],
    "Unidade":["CME","Clínica Cirúrgica","Internação Maternidade"],"Status":["Planejado","Em andamento","Planejado"]}),hide_index=True,use_container_width=True)
elif page=="Equipamentos e riscos":
    st.info("Matriz ilustrativa, sem patrimônio ou eventos reais.")
    st.dataframe(pd.DataFrame({"Item fictício":["Autoclave A","Cama B","Monitor C"],"Unidade":["CME","Internação Maternidade","Centro Cirúrgico"],
    "Risco ilustrativo":["Alto","Médio","Baixo"]}),hide_index=True,use_container_width=True)
elif page=="Integração de processos":
    st.write("Representação conceitual de interfaces assistenciais, sem movimentações reais.")
    st.graphviz_chart('digraph {rankdir=LR; node [shape=box style=rounded]; "Internação" -> "Centro Cirúrgico"; "Centro Cirúrgico" -> "Clínica Cirúrgica"; "CME" -> "Centro Cirúrgico"; "Gestão de pessoas" -> "CME";}')
st.divider()
with st.expander("Cobertura e limitações das fontes"):
    for unit,description in COVERAGE.items():
        st.markdown("**"+unit+"** — "+description)
    st.caption("Os relatórios são cumulativos e podem conter divergências entre versões. Valores extraídos exigem homologação antes de uso gerencial.")
st.warning("Não inserir dados identificáveis de pacientes ou colaboradores. Esta versão não possui login nem banco de dados e não deve ser usada para decisões assistenciais.")
