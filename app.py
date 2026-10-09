"""PAINEL INTEGRA — painel executivo hospitalar com dados agregados."""
import streamlit as st
import pandas as pd
import plotly.express as px
from modules.indicators import indicators, catalog, COVERAGE, MONTHS

st.set_page_config(page_title="PAINEL INTEGRA",page_icon="🏥",layout="wide",initial_sidebar_state="expanded")
st.markdown("""<style>
:root{--navy:#12354c;--teal:#087f87}
.block-container{max-width:1600px;padding-top:1.1rem;padding-bottom:2rem}
h1,h2,h3{color:#14384e;letter-spacing:-.02em}
h1{font-size:2.05rem!important}
[data-testid="stSidebar"]{background:#102f46}
[data-testid="stSidebar"] *{color:#f5fbfc!important}
[data-testid="stMetric"]{border:1px solid #d7e8eb;background:#f5fafb;border-radius:14px;padding:15px}
div.stButton>button{border-radius:11px;border:1px solid #c8dfe2;min-height:44px;font-weight:600}
div.stButton>button[kind="primary"]{background:#087f87;border-color:#087f87;color:white}
[data-testid="stVerticalBlockBorderWrapper"]{border-radius:16px}
[data-testid="stTabs"] button{font-weight:650}
</style>""",unsafe_allow_html=True)

UNITS=list(COVERAGE)
ALL=indicators()
CAT=catalog()
if "units" not in st.session_state: st.session_state.units=UNITS.copy()
if "view" not in st.session_state: st.session_state.view="Indicadores assistenciais"
if "chart_type" not in st.session_state: st.session_state.chart_type="Linha"
if "period" not in st.session_state: st.session_state.period=(1,8)
if "focus_unit" not in st.session_state: st.session_state.focus_unit=None

with st.sidebar:
    st.markdown("## 🏥 PAINEL INTEGRA")
    st.caption("Gestão integrada • Indicadores 2026")
    st.divider()
    st.radio("Área de análise",["Indicadores assistenciais","Gestão de pessoas","Projetos e prazos","Equipamentos e riscos","Integração de processos"],key="view")
    st.divider()
    st.caption("Os valores são agregados e exigem conferência institucional.")
    if st.button("Visão geral / comparação",use_container_width=True):
        st.session_state.focus_unit=None
        st.rerun()

st.markdown("# PAINEL INTEGRA")
st.caption("CENTRAL DE INTELIGÊNCIA ASSISTENCIAL  /  INDICADORES SETORIAIS 2026")
st.markdown("#### Unidades assistenciais")
cols=st.columns(4,gap="medium")
for col,unit,emoji in zip(cols,UNITS,["🤱","🛏️","🏥","♻️"]):
    n=CAT.loc[CAT["Unidade"]==unit,"Indicador"].nunique()
    selected=unit in st.session_state.units
    with col:
        with st.container(border=True):
            st.markdown(f"### {emoji} {unit}")
            st.caption(f"{n} indicadores cadastrados")
            if st.button("Abrir painel →",key="unit_"+unit,
                         type="primary" if selected else "secondary",use_container_width=True):
                st.session_state.focus_unit=unit
                st.session_state.units=[unit]
                st.rerun()

c1,c2,c3=st.columns([2,1,1])
with c1:
    units=st.multiselect("Comparar unidades (seleção múltipla)",UNITS,key="units")
with c2:
    chart=st.selectbox("Tipo de gráfico",["Linha","Barras","Colunas","Área","Dispersão","Tabela"],key="chart_type",label_visibility="visible")
with c3:
    period=st.slider("Período (jan–ago)",1,8,key="period")
st.divider()
if st.session_state.focus_unit and st.session_state.focus_unit in units and len(units)==1:
    st.markdown("## "+st.session_state.focus_unit+" — painel da unidade")
    current=CAT[CAT["Unidade"]==st.session_state.focus_unit]
    for group,group_df in current.groupby("Grupo",sort=False):
        with st.expander(group+" • "+str(len(group_df))+" indicadores",expanded=True):
            st.dataframe(group_df[["Indicador","Classificação","Situação","Meses disponíveis"]],
                         hide_index=True,use_container_width=True)
elif units:
    st.markdown("## Indicadores comuns e específicos")
    selected_catalog=CAT[CAT["Unidade"].isin(units)]
    common=selected_catalog[selected_catalog["Classificação"]=="comum"]
    specific=selected_catalog[selected_catalog["Classificação"]=="específico"]
    t1,t2=st.tabs(["Indicadores comuns","Indicadores exclusivos / setoriais"])
    with t1:
        st.caption("Indicadores comparáveis por tema. As definições e denominadores devem ser homologados antes da comparação entre setores.")
        st.dataframe(common[["Unidade","Indicador","Situação"]],hide_index=True,use_container_width=True)
    with t2:
        st.dataframe(specific[["Unidade","Indicador","Situação"]],hide_index=True,use_container_width=True)
if st.session_state.view in ["Indicadores assistenciais","Gestão de pessoas"]:
    if not units:
        st.info("Selecione uma ou mais unidades nos cards ou no filtro para visualizar os indicadores.")
    else:
        data=ALL[ALL["Unidade"].isin(units)].copy()
        if st.session_state.view=="Gestão de pessoas":
            data=data[data["Indicador"].str.contains("Absenteísmo",case=False)]
        else:
            data=data[~data["Indicador"].str.contains("Absenteísmo",case=False)]
        data=data[data["Ordem"].between(*period)]
        names=sorted(data["Indicador"].unique())
        if not names:
            st.warning("Não há indicadores transcritos para este recorte.")
        else:
            st.markdown("### Resumo gerencial")
            a,b,c,d=st.columns(4)
            a.metric("Unidades selecionadas",len(units))
            b.metric("Indicadores disponíveis",len(names))
            c.metric("Registros mensais",len(data))
            d.metric("Meses no filtro",period[1]-period[0]+1)
            st.caption("A quantidade de registros não representa volume de pacientes ou procedimentos.")
            st.markdown("### Indicadores e evolução")
            chosen=st.multiselect("Selecione um ou vários indicadores",names,default=names[:min(4,len(names))])
            if not chosen:
                st.info("Escolha ao menos um indicador para exibir os gráficos.")
            for name in chosen:
                sub=data[data["Indicador"]==name].sort_values("Ordem")
                if sub.empty: continue
                with st.container(border=True):
                    st.markdown("#### "+name)
                    latest=sub.sort_values("Ordem").groupby("Unidade").tail(1)
                    st.caption("Último valor disponível por unidade: "+ "  •  ".join(
                        f"{r['Unidade']}: {r['Valor']:,.2f} ({r['Mês']})" for _,r in latest.iterrows()))
                    opts=dict(data_frame=sub,x="Mês",y="Valor",color="Unidade",
                              category_orders={"Mês":MONTHS},
                              color_discrete_sequence=["#087f87","#174b74","#d58b38","#6b5aa8"])
                    if chart=="Linha": fig=px.line(**opts,markers=True)
                    elif chart=="Barras": fig=px.bar(**opts,orientation="v",barmode="group");fig.update_layout(xaxis_title="")
                    elif chart=="Colunas": fig=px.bar(**opts,barmode="group")
                    elif chart=="Área": fig=px.area(**opts)
                    elif chart=="Dispersão": fig=px.scatter(**opts)
                    else: fig=None
                    if fig is not None:
                        fig.update_layout(margin=dict(l=0,r=0,t=10,b=0),legend_title_text="",height=335,
                                          paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)")
                        fig.update_xaxes(categoryorder="array",categoryarray=MONTHS)
                        st.plotly_chart(fig,use_container_width=True)
                    else:
                        st.dataframe(sub[["Unidade","Mês","Valor"]],hide_index=True,use_container_width=True)
            with st.expander("Base consolidada e fontes dos indicadores",expanded=False):
                table=data[data["Indicador"].isin(chosen)]
                st.dataframe(table[["Unidade","Indicador","Mês","Valor","Fonte"]],hide_index=True,use_container_width=True)
                st.download_button("Exportar dados agregados (CSV)",table.to_csv(index=False).encode("utf-8-sig"),
                                   "painel_integra_indicadores_2026.csv","text/csv")
elif st.session_state.view=="Projetos e prazos":
    st.info("Módulo demonstrativo: projetos fictícios, não representam dados institucionais.")
    st.dataframe(pd.DataFrame({"Projeto fictício":["Rastreabilidade","Fluxo de alta","Transferência segura"],"Unidade":["CME","Clínica Cirúrgica","Internação Maternidade"],"Situação":["Planejado","Em andamento","Planejado"]}),hide_index=True,use_container_width=True)
elif st.session_state.view=="Equipamentos e riscos":
    st.info("Módulo demonstrativo: itens e riscos fictícios.")
    st.dataframe(pd.DataFrame({"Item fictício":["Autoclave A","Cama B","Monitor C"],"Unidade":["CME","Internação Maternidade","Centro Cirúrgico"],"Risco ilustrativo":["Alto","Médio","Baixo"]}),hide_index=True,use_container_width=True)
else:
    st.info("Fluxo conceitual entre setores, sem movimentações reais.")
    st.graphviz_chart('digraph {rankdir=LR; node [shape=box style=rounded]; "Internação Maternidade" -> "Centro Cirúrgico" [style=dashed]; "Centro Cirúrgico" -> "Clínica Cirúrgica"; "CME" -> "Centro Cirúrgico";}')

with st.expander("Fontes, cobertura e limites"):
    for unit,desc in COVERAGE.items(): st.markdown(f"**{unit}** — {desc}")
    st.caption("Os relatórios de origem são cumulativos. Séries extraídas de apresentações exigem homologação e conferência de divergências antes do uso institucional.")
st.caption("⚠️ Ambiente sem autenticação e sem banco de dados. Não inserir informações identificáveis de pacientes ou colaboradores.")
