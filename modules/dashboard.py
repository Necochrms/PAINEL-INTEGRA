import streamlit as st
import pandas as pd
import plotly.express as px

def render_dashboard():
    st.title("Dashboard executivo")
    st.caption("Indicadores ilustrativos para validação visual — não representam dados reais.")
    cols = st.columns(4)
    for col, label, value in zip(cols, ["Cirurgias realizadas", "Taxa de cancelamento", "Ocupação cirúrgica", "Conformidade CME"], ["128", "4,5%", "78%", "96%"]):
        col.metric(label, value)
    st.divider()
    data = pd.DataFrame({"Setor": ["Centro Cirúrgico", "CME", "Qualidade", "Internação"], "Atividades": [128, 215, 42, 174]})
    fig = px.bar(data, x="Setor", y="Atividades", title="Atividades por setor (dados fictícios)", color="Setor")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    st.info("Próxima etapa: conectar fontes de dados validadas e definir os indicadores institucionais.")
