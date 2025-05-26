import streamlit as st
import re
from datetime import datetime

st.title("Gerador de Formatação de Admissão - Farmácia Clínica Ortopedia 2.0")

texto = st.text_area("Cole aqui os dados do prontuário:")

if st.button("Gerar Formatação"):
    hoje = datetime.now().strftime("%d/%m/%Y")

    # Extrair informações com expressões regulares
    paciente = re.search(r'Paciente:\s+(.*?)(?:\t|  )', texto)
    ses = re.search(r'SES:\s+(\d+)', texto)
    idade = re.search(r'Idade:\s+(\d+)', texto)
    peso = re.search(r'Peso[: ]+(\d+)', texto, re.IGNORECASE)
    
    # Diagnóstico
    motivo = re.search(r'DIAGNÓSTICOS?:\s*(?:-)?\s*(.*?)(?:\n|$)', texto, re.IGNORECASE | re.DOTALL)

    # Mecanismo do trauma
    mecanismo = re.search(r'MECANISMO DO TRAUMA:\s*(.*)', texto, re.IGNORECASE)
    if not mecanismo:
        mecanismo = re.search(r'HDA:\s*(.*)', texto, re.IGNORECASE)
    mecanismo = mecanismo.group(1).strip() if mecanismo else "mecanismo não especificado"

    # Datas
    def corrigir_data(data):
        partes = data.split('/')
        if len(partes[-1]) == 2:
            partes[-1] = '20' + partes[-1]
        return '/'.join(partes)

    data_fratura = re.search(r'DATA DA (?:FRATURA|LESAO):\s*(\d{2}/\d{2}/\d{2,4})', texto, re.IGNORECASE)
    data_fratura = corrigir_data(data_fratura.group(1)) if data_fratura else "-"

    cirurgia_matches = re.findall(r'DATA DA CIRURGIA:\s+(\d{2}/\d{2}/\d{2,4})(?:\s+\((.*?)\))?', texto, re.IGNORECASE)
    datas_cirurgia = []
    for data, medico in cirurgia_matches:
        data_corrigida = corrigir_data(data)
        if medico:
            datas_cirurgia.append(f"{data_corrigida} ({medico.strip().title()})")
        else:
            datas_cirurgia.append(f"{data_corrigida}")
    data_cirurgia = "\n".join(datas_cirurgia) if datas_cirurgia else "-"

    # Montar texto formatado
    output = f"""FARMÁCIA CLÍNICA 
ADMISSÃO ORTOPEDIA 1 ou 2
----------------------------------------------------------------------------
Paciente: {paciente.group(1) if paciente else '***'}; SES: {ses.group(1) if ses else '***'}; 
Idade: {idade.group(1) if idade else '***'} anos; Peso: {peso.group(1) if peso else '***'}
Data de admissão: {hoje}
Data da entrevista: {hoje}
----------------------------------------------------------------------------
Motivo da internação:
{motivo.group(1).strip() if motivo else '***'}
Mecanismo do trauma:
{mecanismo}
Data da fratura: {data_fratura}
Data da cirurgia: {data_cirurgia}
----------------------------------------------------------------------------
Antecedentes: 
----------------------------------------------------------------------------
Alergias: 
----------------------------------------------------------------------------
Conciliação medicamentosa:
- Histórico obtido através de: 
- Medicamentos de uso domiciliar: 
----------------------------------------------------------------------------
Antimicrobianos:
Em uso:
- 
Uso prévio:
- 
-----------------------------------------------------------------------------
Culturas e Sorologias:
-----------------------------------------------------------------------------
Profilaxias e protocolos
- TEV/TVP: 
- 
- LAMG: 
-
- Analgesia:
- 
----------------------------------------------------------------------------- 
Conduta
- Realizo análise técnica da prescrição quanto à indicação, efetividade, posologia, dose, possíveis interações medicamentosas e disponibilidade na farmácia.
- Realizo visita beira a leito, encontro o paciente dormindo 
- Monitoro exames laboratoriais de **/**/****, controles e evolução clínica.
---
- Acompanho antibioticoterapia e parâmetros infecciosos: Paciente afebril, em uso de (***) D*; Leuco **.
- Paciente avaliado como risco (****), reavaliação programada para o dia: **/**/****
- Segue em acompanhamento pelo Núcleo de Farmácia Clínica.

- Estagiário ***, supervisionado por *********
- Farmacêutico ***
*******************************************************
"""

    st.text_area("Formatação gerada:", value=output, height=900)
