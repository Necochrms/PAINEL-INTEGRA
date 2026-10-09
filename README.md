# PAINEL INTEGRA — Gestão Integrada Assistencial e Cirúrgica

Protótipo funcional em **Python + Streamlit**, com dados 100% fictícios e filtros de período/setor, gráficos interativos, tabelas e exportação CSV.

## Módulos
1. Visão executiva e indicadores
2. Internação Maternidade — gestantes, puérperas e recém-nascidos internados (**sem Centro Obstétrico**)
3. Clínica Cirúrgica
4. Centro Cirúrgico
5. Central de Material e Esterilização (CME)
6. Gestão de pessoas, escalas, férias e absenteísmo
7. Projetos, pendências e prazos
8. Equipamentos, materiais e riscos
9. Integração dos processos entre setores

## Publicar sem instalar Python
1. Acesse https://share.streamlit.io/ e entre com sua conta GitHub.
2. Clique em **Create app** / **New app**, selecione **Deploy a public app from GitHub**.
3. Repositório: `Necochrms/PAINEL-INTEGRA`; branch: `main`; arquivo principal: `app.py`.
4. Escolha um endereço disponível e clique em **Deploy**.
5. Acompanhe os logs se houver falha de instalação.

O Streamlit instala as dependências listadas em `requirements.txt` automaticamente na nuvem.

## Execução local (opcional)
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Avisos
- Todos os indicadores, nomes de equipamentos e projetos são **fictícios**.
- Sem login, persistência, API hospitalar, banco de dados, auditoria ou controle de acesso nesta versão.
- **Não inserir dados reais de pacientes ou colaboradores. Não usar para decisões assistenciais.**
- Antes de produção: autenticação, autorização por perfil, LGPD, criptografia, logs, backups, testes e homologação institucional.
