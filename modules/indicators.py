"""Dados agregados transcritos de apresentações setoriais de 2026.
Não há dados individuais. Números não verificados são omitidos.
"""
import pandas as pd
MONTHS=["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago"]
SOURCES={
 "CME":"CME INDICADORES AGOSTO 2026(1).pptx",
 "Centro Cirúrgico":"INDICADOR SSECC JUNHO-GEREF 2026 NECOC.pptx",
}
SERIES={
 ("CME","Desinfecção (itens)"):[4085,3287,3716,1812,2720,2828,2609,2699],
 ("CME","Esterilização em autoclave (itens)"):[13391,13886,13646,13985,13891,14713,15878,16599],
 ("CME","Processamento terceirizado (itens)"):[1997,3421,5111,4829,5579,5100,5424,4114],
 ("CME","Absenteísmo de enfermeiros (%)"):[2,1,0,0,0,0,1.39,4.17],
 ("CME","Absenteísmo de técnicos (%)"):[3,1.52,4,4.89,3.76,1.56,3.76,0.86],
 ("Centro Cirúrgico","Cirurgias eletivas (n)"):[60,83,89,69,57,64],
 ("Centro Cirúrgico","Cirurgias urgência/emergência (n)"):[310,286,312,309,358,334],
 ("Centro Cirúrgico","Absenteísmo de enfermeiros (%)"):[1.39,3,0.68,2.1,2,0],
 ("Centro Cirúrgico","Absenteísmo de técnicos (%)"):[2.86,0.82,1.7,4.95,6.28,6],
}
def indicators():
    rows=[]
    for (unit,name),values in SERIES.items():
        for i,value in enumerate(values):
            rows.append({"Unidade":unit,"Indicador":name,"Mês":MONTHS[i],"Ordem":i+1,"Valor":value,"Fonte":SOURCES[unit]})
    return pd.DataFrame(rows)

COVERAGE={
 "Internação Maternidade":"Apresentações mensais de 2026 recebidas. Séries numéricas em conferência.",
 "Clínica Cirúrgica":"Apresentações mensais de 2026 recebidas. Séries numéricas em conferência.",
 "Centro Cirúrgico":"Indicadores consolidados de janeiro a junho de 2026.",
 "CME":"Indicadores consolidados de janeiro a agosto de 2026.",
}
