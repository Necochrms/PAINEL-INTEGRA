import streamlit as st
from modules.dashboard import render_dashboard
from modules.pages import render_module

st.set_page_config(page_title="PAINEL INTEGRA", page_icon="🏥", layout="wide", initial_sidebar_state="expanded")

st.markdown("""<style>
[data-testid="stSidebar"] {background: #102d46;}
[data-testid="stSidebar"] * {color: #f0f7fa !important;}
.block-container {padding-top: 2rem;}
</style>""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🏥 PAINEL INTEGRA")
    st.caption("Gestão hospitalar integrada • v1.0")
    st.divider()
    page = st.radio("Navegação", ["Visão geral", "Centro Cirúrgico", "CME", "Qualidade", "Equipes", "Financeiro", "Administração"])
    st.divider()
    st.caption("Ambiente demonstrativo — sem dados de pacientes")

if page == "Visão geral":
    render_dashboard()
else:
    render_module(page)
