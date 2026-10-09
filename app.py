"""Gestão à Vista – NECOC. Painel gerencial com dados agregados de 2026."""
import streamlit as st
import pandas as pd
import plotly.express as px
from modules.indicators import indicators, catalog, MONTHS

st.set_page_config(page_title="Gestão à Vista – NECOC",page_icon="🏥",layout="wide",initial_sidebar_state="expanded")
st.markdown("""
<style>
.block-container{max-width:1660px;padding-top:1.25rem;padding-bottom:2rem}
[data-testid="stAppViewContainer"]{background:#f4f8fb}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0c2d49,#104c67)}
[data-testid="stSidebar"] *{color:#f2f9fd!important}
h1,h2,h3{color:#103a60;letter-spacing:-.025em}
h1{font-size:2.2rem!important}
[data-testid="stMetric"]{background:white;border:1px solid #dce9f0;border-radius:13px;padding:13px}
[data-testid="stVerticalBlockBorderWrapper"]{border-radius:13px;background:#fff}
div.stButton>button{border-radius:10px;min-height:42px;border-color:#d2e4ec;font-weight:650}
div.stButton>button[kind="primary"]{background:#087f89;border-color:#087f89;color:white}
[data-testid="stTabs"] button{font-weight:700}
</style>""",unsafe_allow_html=True)

UNITS=["Maternidade","Clínica Cirúrgica","Centro Cirúrgico","CME"]
ICONS={"Maternidade":"🤱","Clínica Cirúrgica":"🛏️","Centro Cirúrgico":"🏥","CME":"♻️"}
COLORS={"Maternidade":"#e91e72","Clínica Cirúrgica":"#087ad0","Centro Cirúrgico":"#009c80","CME":"#7050c9"}
ALL=indicators().replace({"Unidade":{"Internação Maternidade":"Maternidade"}})
CAT=catalog().replace({"Unidade":{"Internação Maternidade":"Maternidade"}})
if "selected_units" not in st.session_state: st.session_state.selected_units=UNITS.copy()
if "focus" not in st.session_state: st.session_state.focus=None
if "indicator_focus" not in st.session_state: st.session_state.indicator_focus=None

with st.sidebar:
    st.markdown("## 🏥 GESTÃO À VISTA")
    st.markdown("**NECOC**")
    st.caption("Inteligência assistencial • 2026")
    st.divider()
    section=st.radio("NAVEGAÇÃO",["Visão geral","Indicadores comuns","Maternidade","Clínica Cirúrgica","Centro Cirúrgico","CME","Absenteísmo","Quadro dimensionado","Indicadores específicos"],index=0)
    st.divider()
    chart=st.selectbox("Tipo de gráfico",["Linha","Colunas","Barras horizontais","Área","Dispersão","Tabela"])
    show_labels=st.toggle("Mostrar valores nos gráficos",value=True)
    period=st.slider("Período de análise (2026)",1,8,(1,8))
    st.caption("Fontes: apresentações institucionais. Séries sujeitas à conferência.")

st.title("GESTÃO À VISTA – NECOC")
st.caption("CENTRAL DE INTELIGÊNCIA ASSISTENCIAL  /  INDICADORES SETORIAIS 2026")
st.markdown("### Unidades assistenciais")
cols=st.columns(4,gap="medium")
for col,unit in zip(cols,UNITS):
    with col:
        with st.container(border=True):
            st.markdown("#### "+ICONS[unit]+"  "+unit)
            n=CAT[CAT["Unidade"]==unit]["Indicador"].nunique()
            st.caption(f"{n} indicadores catalogados")
            if st.button("Abrir painel →",key="open_"+unit,use_container_width=True):
                st.session_state.focus=unit
                st.session_state.selected_units=[unit]
                st.rerun()
if section in UNITS:
    st.session_state.focus=section
    st.session_state.selected_units=[section]
elif section=="Visão geral" and st.session_state.focus:
    st.info("Painel da unidade: "+st.session_state.focus+" — use Visão geral / comparação para retornar.")
if st.session_state.focus:
    if st.button("← Visão geral / comparação"):
        st.session_state.focus=None
        st.session_state.selected_units=UNITS.copy()
        st.rerun()
selected=st.multiselect("Comparar unidades (permite múltipla seleção)",UNITS,key="selected_units")
if not selected:
    st.info("Selecione ao menos uma unidade para visualizar os indicadores.")
    st.stop()
subcat=CAT[CAT["Unidade"].isin(selected)]
data=ALL[ALL["Unidade"].isin(selected)&ALL["Ordem"].between(*period)].copy()

def draw_chart(frame,name,key):
    if frame.empty:
        st.caption("Série mensal ainda não disponível para este indicador.")
        return
    opts=dict(data_frame=frame.sort_values("Ordem"),x="Mês",y="Valor",color="Unidade",
              color_discrete_map=COLORS,category_orders={"Mês":MONTHS})
    if chart=="Linha": fig=px.line(**opts,markers=True,text="Valor" if show_labels else None)
    elif chart=="Colunas": fig=px.bar(**opts,barmode="group",text="Valor" if show_labels else None)
    elif chart=="Barras horizontais":
        opts["x"],opts["y"]="Valor","Mês"
        fig=px.bar(**opts,orientation="h",barmode="group",text="Valor" if show_labels else None)
    elif chart=="Área": fig=px.area(**opts)
    elif chart=="Dispersão": fig=px.scatter(**opts,text="Valor" if show_labels else None)
    else:
        st.dataframe(frame[["Unidade","Mês","Valor"]],hide_index=True,use_container_width=True)
        return
    fig.update_layout(height=330,margin=dict(l=5,r=5,t=22,b=0),legend_title_text="",
                      paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)")
    if show_labels and chart in ["Linha","Colunas","Barras horizontais","Dispersão"]:
        fig.update_traces(texttemplate="%{text:.2f}",textposition="top center" if chart in ["Linha","Dispersão"] else "outside",cliponaxis=False)
    st.plotly_chart(fig,use_container_width=True,key=key)

st.markdown("### Principais indicadores")
available=data.sort_values("Ordem").groupby(["Unidade","Indicador"],sort=False).tail(1)
metric_names=["Absenteísmo de enfermeiros (%)","Absenteísmo de técnicos (%)","Taxa de ocupação (%)","Média de permanência — ALCON (dias)"]
metrics=st.columns(4)
for col,name in zip(metrics,metric_names):
    rows=available[available["Indicador"]==name]
    with col:
        with st.container(border=True):
            st.caption(name)
            if rows.empty: st.metric("Último registro","—")
            else:
                last=rows.sort_values("Ordem").iloc[-1]
                st.metric("Último valor",f"{last['Valor']:,.2f}"+("%" if "(%)" in name else ""))
                st.caption(last["Unidade"]+" • "+last["Mês"]+"/2026")
st.caption("Os cards exibem o último valor cadastrado, que pode ser de meses diferentes. Não são médias consolidadas.")

st.markdown("### Indicadores por categoria")
if section=="Quadro dimensionado": active_tab="Quadro dimensionado"
elif section=="Absenteísmo": active_tab="Absenteísmo"
elif section=="Indicadores específicos": active_tab="Específicos"
elif section=="Indicadores comuns": active_tab="Comuns"
else: active_tab="Todos"
tabnames=["Todos","Comuns","Específicos","Absenteísmo","Quadro dimensionado"]
tabs=st.tabs(tabnames)
for tab,kind in zip(tabs,tabnames):
    with tab:
        if kind=="Quadro dimensionado":
            st.caption("GAP = quadro atual equivalente menos quadro dimensionado. Dados conferidos de agosto/2026 para a Clínica Cirúrgica.")
            gap_data=[
                {"Unidade":"Clínica Cirúrgica","Categoria":"Enfermeiros","Colaboradores":13,"Atual equivalente":13.11,"Dimensionado":12.75,"GAP":0.36},
                {"Unidade":"Clínica Cirúrgica","Categoria":"Técnicos","Colaboradores":54,"Atual equivalente":54.44,"Dimensionado":55.72,"GAP":-1.27},
            ]
            gdf=pd.DataFrame(gap_data)
            for unit in selected:
                with st.container(border=True):
                    st.markdown("#### "+ICONS[unit]+" "+unit)
                    gg=gdf[gdf["Unidade"]==unit]
                    if gg.empty:
                        st.info("Quadro dimensionado, quantitativo de colaboradores e GAP: aguardando conferência documental.")
                    else:
                        cc=st.columns(2)
                        for c,(_,row) in zip(cc,gg.iterrows()):
                            with c:
                                status="Superávit" if row["GAP"]>0 else "Déficit" if row["GAP"]<0 else "Equilíbrio"
                                st.metric(row["Categoria"]+" — colaboradores",int(row["Colaboradores"]),delta=f"GAP {row['GAP']:+.2f}",delta_color="off")
                                st.caption(f"Dimensionado: {row['Dimensionado']:.2f} • Atual equivalente: {row['Atual equivalente']:.2f} • {status}")
            continue
        rows=subcat.copy()
        if kind=="Comuns": rows=rows[rows["Classificação"]=="comum"]
        if kind=="Específicos": rows=rows[rows["Classificação"]=="específico"]
        if kind=="Absenteísmo": rows=rows[rows["Indicador"].str.contains("Absenteísmo",case=False)]
        if st.session_state.focus and kind=="Todos": rows=rows[rows["Unidade"]==st.session_state.focus]
        if rows.empty: st.info("Nenhum indicador catalogado neste filtro.");continue
        grouped=rows.groupby("Indicador",sort=False)
        entries=list(grouped)
        cards=st.columns(4)
        for i,(name,group) in enumerate(entries):
            with cards[i%4]:
                with st.container(border=True):
                    st.markdown("**"+name+"**")
                    st.caption(" • ".join(group["Unidade"].tolist()))
                    count=(group["Situação"]=="Série disponível").sum()
                    st.caption(f"{count}/{len(group)} unidade(s) com valores")
                    if st.button("Ver gráfico →",key="card_"+kind+"_"+str(i)):
                        st.session_state.indicator_focus=name
                        st.rerun()

if st.session_state.indicator_focus:
    st.markdown("### Indicador selecionado")
    target=st.session_state.indicator_focus
    st.markdown("**"+target+"**")
    draw_chart(data[data["Indicador"]==target],target,"focused_chart")
    if st.button("Fechar indicador"):
        st.session_state.indicator_focus=None
        st.rerun()

st.markdown("### Evolução mensal e comparativos")
choices=sorted(data["Indicador"].unique())
default=[x for x in ["Absenteísmo de enfermeiros (%)","Absenteísmo de técnicos (%)"] if x in choices]
if not default: default=choices[:2]
chosen=st.multiselect("Indicadores para comparar",choices,default=default)
for i,name in enumerate(chosen):
    with st.container(border=True):
        st.markdown("#### "+name)
        draw_chart(data[data["Indicador"]==name],name,"trend_"+str(i))
with st.expander("Dados, fontes e exportação"):
    st.dataframe(data[["Unidade","Indicador","Mês","Valor","Fonte"]],hide_index=True,use_container_width=True)
    st.download_button("Baixar CSV",data.to_csv(index=False).encode("utf-8-sig"),"gestao_a_vista_necoc_2026.csv","text/csv")
st.warning("Dados agregados extraídos de apresentações, ainda sujeitos à homologação. Indicadores sem série não são zero. Não utilizar para decisões assistenciais; esta versão não possui autenticação.")
