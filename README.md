# PAINEL INTEGRA — Gestão Integrada Assistencial e Cirúrgica

Dashboard Streamlit baseado em **indicadores agregados de apresentações setoriais de 2026**. Não contém dados pessoais, identificadores ou apresentações originais.

## O que funciona
- Menu com nove áreas; visão executiva, Centro Cirúrgico, CME e absenteísmo possuem séries mensais transcritas.
- Filtros de unidade, indicador e mês; gráficos Plotly, tabelas e exportação CSV.
- Maternidade (somente internação) e Clínica Cirúrgica aparecem como **em conferência**, sem números inventados.
- Projetos, equipamentos e integração são demonstrações explicitamente fictícias.
- Dados e fontes em `modules/indicators.py`.

## Fontes e qualidade
- `CME INDICADORES AGOSTO 2026(1).pptx` — desinfecção, autoclave, terceirização e absenteísmo, janeiro–agosto.
- `INDICADOR SSECC JUNHO-GEREF 2026 NECOC.pptx` — cirurgias eletivas, urgência/emergência e absenteísmo, janeiro–junho.
- Demais apresentações de Maternidade e Clínica Cirúrgica recebidas; extração numérica ainda pendente.
- Os dados foram transcritos de gráficos/tabelas e **não foram homologados**; conferir divergências entre versões e definições antes de uso institucional.
- Não há metas presumidas, dados individuais ou decisões clínicas.

## Publicação sem instalar Python
Acesse https://share.streamlit.io/ e crie um app a partir de GitHub:
- Repositório: `Necochrms/PAINEL-INTEGRA`
- Branch: `main`
- Main file path: `app.py`

## Execução opcional
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Pendente
Conferência de indicadores de Maternidade e Clínica Cirúrgica, homologação de fórmulas e metas, testes em Cloud, autenticação, perfis, banco de dados, auditoria, integração entre setores e avaliação LGPD. **Não usar como prontuário ou ferramenta de decisão assistencial.**
