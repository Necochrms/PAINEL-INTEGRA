# PAINEL INTEGRA

Protótipo inicial de sistema modular de gestão hospitalar, desenvolvido em **Python + Streamlit**.

## Executar localmente

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

## Módulos

- Dashboard executivo (indicadores demonstrativos)
- Centro Cirúrgico
- CME
- Qualidade
- Equipes
- Financeiro
- Administração

## Segurança e privacidade

**Versão demonstrativa, sem autenticação e sem persistência de dados.** Não utilizar em produção nem inserir dados pessoais ou dados de pacientes. Antes de uso institucional: implementar autenticação, autorização por perfil, auditoria, banco de dados seguro, política de backup e avaliação de conformidade com a LGPD.

## Publicação

O código está preparado para execução via Streamlit. A implantação pública deve ocorrer apenas após revisão de segurança e decisão sobre hospedagem e acesso restrito.
