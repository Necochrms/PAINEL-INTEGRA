import streamlit as st

DESCRIPTIONS = {
    "Centro Cirúrgico": "Produção cirúrgica, cancelamentos, atrasos e utilização de salas.",
    "CME": "Rastreabilidade, processamento, esterilização e produtividade.",
    "Qualidade": "Indicadores, notificações e não conformidades.",
    "Equipes": "Dimensionamento, escalas e produtividade.",
    "Financeiro": "Custos, consumo, orçamento e análises.",
    "Administração": "Configurações, usuários e perfis de acesso.",
}

def render_module(name: str):
    st.title(name)
    st.write(DESCRIPTIONS[name])
    st.info("Módulo em desenvolvimento. Nenhum dado real é coletado ou armazenado nesta versão.")
