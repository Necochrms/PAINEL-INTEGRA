"""Gestão à Vista – NECOC | dashboard executivo de indicadores agregados."""
import html
import streamlit as st
import pandas as pd
import plotly.express as px
from modules.indicators import indicators, catalog, MONTHS

st.set_page_config(page_title="Gestão à Vista – NECOC",page_icon="🏥",layout="wide",initial_sidebar_state="expanded")
st.markdown("""
<style>
.block-container{max-width:1750px;padding:1rem 1.6rem 2rem}
[data-testid="stAppViewContainer"]{background:#f5f9fd}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#052e4f,#07426b 55%,#052b49)}
[data-testid="stSidebar"] *{color:#f3faff!important}
[data-testid="stSidebar"] hr{border-color:#3b617c}
h1,h2,h3{color:#103d69;letter-spacing:-.03em}
h1{font-size:2.05rem!important;margin-bottom:0}
h3{font-size:1.14rem!important}
[data-testid="stVerticalBlockBorderWrapper"]{background:white;border-radius:13px;border-color:#dce9f4;box-shadow:0 2px 10px #0c45600a}
[data-testid="stMetric"]{background:white;border:1px solid #e1eaf2;border-radius:12px;padding:12px}
[data-testid="stMetricValue"]{color:#1264a1;font-weight:750}
div.stButton>button{border-radius:9px;min-height:36px;font-weight:650;border-color:#cfe0ef}
div.stButton>button[kind="primary"]{background:#007e89;border-color:#007e89;color:white}
[data-testid="stTabs"] button{font-weight:650}
.hero-sub{color:#597b9a;font-size:.84rem;letter-spacing:.04em;margin-bottom:13px}
.unit-card{border:1.5px solid var(--accent);background:var(--tint);border-radius:12px;padding:15px 16px 12px;min-height:118px}
.unit-card .uc-icon{font-size:31px;float:left;margin-right:13px}
.unit-card .uc-name{font-size:1.1rem;font-weight:800;color:#103d69}
.unit-card .uc-sub{color:#54728c;font-size:.82rem;margin-top:4px}
.unit-card .uc-check{font-size:.76rem;color:#087f79;margin-top:8px;font-weight:650}
.kpi-card{border:1px solid #dce8f2;border-radius:12px;background:white;padding:14px 14px 12px;min-height:125px;box-shadow:0 2px 10px #0d3d6409}
.kpi-label{color:#294862;font-size:.79rem;font-weight:750;min-height:34px}
.kpi-val{font-size:1.7rem;font-weight:850;line-height:1.3}
.kpi-sub{font-size:.77rem;color:#597a96;margin-top:4px}
.ind-card{border:1px solid #dce8f2;background:#fff;border-radius:10px;padding:12px 13px;min-height:95px}
.ind-card .ind-title{font-size:.84rem;font-weight:760;color:#143e63}
.ind-card .ind-sub{font-size:.73rem;color:#6c879d;margin-top:5px}
.section-heading{font-size:1.15rem;font-weight:800;color:#103d69;margin:14px 0 9px}
.note{font-size:.78rem;color:#5d7b92}
</style>
""",unsafe_allow_html=True)

UNITS=["Maternidade","Clínica Cirúrgica","Centro Cirúrgico","CME"]
ICONS={"Maternidade":"🤱","Clínica Cirúrgica":"🛏️","Centro Cirúrgico":"🩺","CME":"♻️"}
PALETTE={
"Maternidade":("#ed2680","#fff0f7"),
"Clínica Cirúrgica":("#2196f3","#eef8ff"),
"Centro Cirúrgico":("#10ae87","#edfcf7"),
"CME":("#9867f5","#f5f0ff")}
COLORS={u:PALETTE[u][0] for u in UNITS}
ALL=indicators().replace({"Unidade":{"Internação Maternidade":"Maternidade"}})
CAT=catalog().replace({"Unidade":{"Internação Maternidade":"Maternidade"}})
if "units_selected" not in st.session_state: st.session_state.units_selected=UNITS.copy()
if "unit_focus" not in st.session_state: st.session_state.unit_focus=None
if "indicator_focus" not in st.session_state: st.session_state.indicator_focus=None

with st.sidebar:
    st.markdown("## 🏥 GESTÃO À VISTA")
    st.markdown("**NECOC · Indicadores 2026**")
    st.divider()
    section=st.radio("NAVEGAÇÃO",["Visão geral","Indicadores comuns","Maternidade","Clínica Cirúrgica","Centro Cirúrgico","CME","Absenteísmo","Quadro dimensionado","Indicadores específicos"],key="nav_section")
    st.divider()
    chart=st.selectbox("Tipo de gráfico",["Linha","Colunas","Barras horizontais","Área","Dispersão","Tabela"])
    show_labels=st.toggle("Exibir valores mensais",value=True)
    period=st.slider("Período (2026)",1,8,(1,8))
    st.caption("Fontes institucionais • dados em conferência")

if section in UNITS and st.session_state.unit_focus!=section:
    st.session_state.unit_focus=section
    st.session_state.units_selected=[section]
if section=="Visão geral" and st.session_state.unit_focus and st.session_state.get("last_nav")!=section:
    st.session_state.unit_focus=None
    st.session_state.units_selected=UNITS.copy()
st.session_state.last_nav=section

st.title("GESTÃO À VISTA – NECOC")
st.markdown('<div class="hero-sub">CENTRAL DE INTELIGÊNCIA ASSISTENCIAL / INDICADORES SETORIAIS 2026</div>',unsafe_allow_html=True)
st.markdown('<div class="section-heading">Unidades assistenciais</div>',unsafe_allow_html=True)
cols=st.columns(4,gap="small")
for col,unit in zip(cols,UNITS):
    accent,tint=PALETTE[unit]
    count=CAT.loc[CAT["Unidade"]==unit,"Indicador"].nunique()
    with col:
        st.markdown(f'<div class="unit-card" style="--accent:{accent};--tint:{tint}"><span class="uc-icon">{ICONS[unit]}</span><div class="uc-name">{unit}</div><div class="uc-sub">{count} indicadores disponíveis</div><div class="uc-check">{"☑ Unidade selecionada" if unit in st.session_state.units_selected else "☐ Não selecionada"}</div></div>',unsafe_allow_html=True)
        if st.button("Abrir "+unit+" →",key="unit_"+unit,use_container_width=True):
            st.session_state.unit_focus=unit
            st.session_state.units_selected=[unit]
            st.rerun()

if st.session_state.unit_focus:
    st.caption("Painel setorial: "+st.session_state.unit_focus)
    if st.button("← Voltar à comparação geral",key="back"):
        st.session_state.unit_focus=None
        st.session_state.units_selected=UNITS.copy()
        st.rerun()
selected=st.multiselect("Unidades para comparação",UNITS,key="units_selected")
if not selected:
    st.info("Selecione uma ou mais unidades.")
    st.stop()
df=ALL[ALL["Unidade"].isin(selected)&ALL["Ordem"].between(*period)].copy()
cat=CAT[CAT["Unidade"].isin(selected)].copy()

def chart_panel(name,frame,key):
    if frame.empty:
        st.info("Sem série mensal validada para o indicador selecionado.")
        return
    opts=dict(data_frame=frame.sort_values("Ordem"),x="Mês",y="Valor",color="Unidade",color_discrete_map=COLORS,category_orders={"Mês":MONTHS})
    if chart=="Linha": fig=px.line(**opts,markers=True,text="Valor" if show_labels else None)
    elif chart=="Colunas": fig=px.bar(**opts,barmode="group",text="Valor" if show_labels else None)
    elif chart=="Barras horizontais":
        opts.update(x="Valor",y="Mês")
        fig=px.bar(**opts,orientation="h",barmode="group",text="Valor" if show_labels else None)
    elif chart=="Área": fig=px.area(**opts)
    elif chart=="Dispersão": fig=px.scatter(**opts,text="Valor" if show_labels else None)
    else:
        st.dataframe(frame[["Unidade","Mês","Valor"]],hide_index=True,use_container_width=True)
        return
    fig.update_layout(height=295,margin=dict(l=2,r=5,t=20,b=5),legend_title_text="",legend=dict(orientation="h",y=-.2,x=.02),
                      paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font=dict(color="#426782"))
    fig.update_yaxes(gridcolor="#e6eef5",title_text=None)
    fig.update_xaxes(title_text=None)
    if show_labels and chart in ["Linha","Colunas","Barras horizontais","Dispersão"]:
        fig.update_traces(texttemplate="%{text:.2f}",textposition="top center" if chart in ["Linha","Dispersão"] else "outside",cliponaxis=False)
    st.plotly_chart(fig,use_container_width=True,key=key)

st.markdown('<div class="section-heading">Principais indicadores</div>',unsafe_allow_html=True)
kpis=[
("Absenteísmo – Enfermeiros","Absenteísmo de enfermeiros (%)","#ec1975"),
("Absenteísmo – Técnicos","Absenteísmo de técnicos (%)","#009b78"),
("Taxa de ocupação","Taxa de ocupação (%)","#1686dd"),
("Média de permanência","Média de permanência — ALCON (dias)","#7346c8"),
("Cirurgias eletivas","Cirurgias eletivas (n)","#008b91")]
cols=st.columns(5,gap="small")
for col,(label,indicator,color) in zip(cols,kpis):
    rows=df[df["Indicador"]==indicator].sort_values("Ordem")
    if not rows.empty:
        last=rows.iloc[-1]
        suffix="%" if "(%)" in indicator else " dias" if "(dias)" in indicator else ""
        value=f"{last['Valor']:,.2f}{suffix}"
        origin=last["Unidade"]+" · "+last["Mês"]+"/2026"
    else: value="—";origin="Sem valor no período"
    with col:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">{html.escape(label)}</div><div class="kpi-val" style="color:{color}">{value}</div><div class="kpi-sub">{html.escape(origin)}</div></div>',unsafe_allow_html=True)
st.caption("Cada destaque corresponde ao último registro disponível de uma unidade identificada, não a um consolidado institucional.")

st.markdown('<div class="section-heading">Indicadores comuns e específicos</div>',unsafe_allow_html=True)
tabs=st.tabs(["Indicadores comuns","Indicadores específicos / setoriais","Todos os indicadores"])
for tab,kind in zip(tabs,["comum","específico","todos"]):
    with tab:
        filtered=cat if kind=="todos" else cat[cat["Classificação"]==kind]
        if section=="Absenteísmo": filtered=filtered[filtered["Indicador"].str.contains("Absenteísmo",case=False)]
        if filtered.empty: st.info("Nenhum indicador neste filtro.");continue
        entries=list(filtered.groupby("Indicador",sort=False))
        grid=st.columns(4,gap="small")
        for i,(name,rows) in enumerate(entries):
            color=COLORS[rows.iloc[0]["Unidade"]]
            with grid[i%4]:
                st.markdown(f'<div class="ind-card" style="border-top:3px solid {color}"><div class="ind-title">{html.escape(name)}</div><div class="ind-sub">{html.escape(" • ".join(rows["Unidade"].tolist()))}</div><div class="ind-sub">{(rows["Situação"]=="Série disponível").sum()} unidade(s) com série</div></div>',unsafe_allow_html=True)
                if st.button("Ver evolução →",key="indicator_"+kind+"_"+str(i),use_container_width=True):
                    st.session_state.indicator_focus=name
                    st.rerun()

if st.session_state.indicator_focus:
    name=st.session_state.indicator_focus
    st.markdown("### Indicador selecionado: "+name)
    with st.container(border=True):
        chart_panel(name,df[df["Indicador"]==name],"focus_chart")
    if st.button("Fechar detalhe",key="close_detail"):
        st.session_state.indicator_focus=None
        st.rerun()

st.markdown('<div class="section-heading">Evolução mensal dos indicadores</div>',unsafe_allow_html=True)
choices=sorted(df["Indicador"].unique())
defaults=[x for x in ["Absenteísmo de enfermeiros (%)","Absenteísmo de técnicos (%)"] if x in choices]
if not defaults: defaults=choices[:2]
chosen=st.multiselect("Indicadores exibidos nos gráficos",choices,default=defaults)
for offset in range(0,len(chosen),2):
    cols=st.columns(2,gap="small")
    for col,name in zip(cols,chosen[offset:offset+2]):
        with col:
            with st.container(border=True):
                st.markdown("#### "+name)
                chart_panel(name,df[df["Indicador"]==name],"trend_"+str(offset)+"_"+name)

st.markdown('<div class="section-heading">Quadro dimensionado e GAP de enfermagem</div>',unsafe_allow_html=True)
st.caption("Dados quantitativos confirmados: Clínica Cirúrgica, agosto/2026. GAP = quadro atual equivalente − quadro dimensionado.")
GAP=[
{"Unidade":"Clínica Cirúrgica","Categoria":"Enfermeiros","Colaboradores":13,"Atual":13.11,"Dimensionado":12.75,"GAP":0.36},
{"Unidade":"Clínica Cirúrgica","Categoria":"Técnicos","Colaboradores":54,"Atual":54.44,"Dimensionado":55.72,"GAP":-1.27}]
gaps=pd.DataFrame(GAP)
cols=st.columns(4,gap="small")
for col,unit in zip(cols,UNITS):
    accent,tint=PALETTE[unit]
    with col:
        st.markdown(f'<div class="unit-card" style="--accent:{accent};--tint:{tint};min-height:55px;padding:10px"><b>{ICONS[unit]} {unit}</b></div>',unsafe_allow_html=True)
        with st.container(border=True):
            if unit not in selected: st.caption("Unidade não selecionada")
            elif unit not in gaps["Unidade"].values: st.caption("Quantitativos e GAP aguardando conferência nos documentos.")
            else:
                for _,r in gaps[gaps["Unidade"]==unit].iterrows():
                    status="Superávit" if r["GAP"]>0 else "Déficit" if r["GAP"]<0 else "Equilíbrio"
                    color="#078c65" if r["GAP"]>0 else "#cb304c" if r["GAP"]<0 else "#4d708d"
                    st.markdown(f'**{r["Categoria"]}** · {int(r["Colaboradores"])} colaboradores')
                    st.caption(f'Dimensionado {r["Dimensionado"]:.2f} · Atual equivalente {r["Atual"]:.2f}')
                    st.markdown(f'<span style="color:{color};font-weight:800">GAP {r["GAP"]:+.2f} · {status}</span>',unsafe_allow_html=True)
                    st.divider()
with st.expander("Tabela de dados, fontes e exportação"):
    st.dataframe(df[["Unidade","Indicador","Mês","Valor","Fonte"]],hide_index=True,use_container_width=True)
    st.download_button("Exportar CSV",df.to_csv(index=False).encode("utf-8-sig"),"gestao_a_vista_necoc_2026.csv","text/csv")
st.caption("⚠️ Séries em processo de conferência; não confundir ausência de dado com zero. Não publicar informações pessoais ou usar este protótipo para decisões assistenciais.")
