import streamlit as st
import re
from datetime import datetime
import unicodedata

def remover_acentos(txt):
    return ''.join(c for c in unicodedata.normalize('NFD', txt)
                   if unicodedata.category(c) != 'Mn')

def extrair_info(texto):
    texto_sem_acentos = remover_acentos(texto.lower())

    nome = re.search(r'paciente:\s*(.+?)\t', texto, re.IGNORECASE)
    ses = re.search(r'ses:\s*(\d+)', texto, re.IGNORECASE)
    idade = re.search(r'idade:\s*(\d+)', texto, re.IGNORECASE)
    peso = re.search(r'peso[:\s]*([\d,\.]+)', texto, re.IGNORECASE)
    motivo = re.search(r'diagn[oó]sticos?:\s*(.*?)\n', texto, re.IGNORECASE | re.DOTALL)
    mecanismo = re.search(r'(hda:|mecanismo do trauma:)\s*(.*?)(?:\n|$)', texto, re.IGNORECASE)

    fratura = re.search(r'data da (fratura|lesao):\s*(\d{2}/\d{2}/\d{2,4})', texto, re.IGNORECASE)
    cirurgia_matches = re.findall(r'data da cirurgia:\s+(\d{2}/\d{2}/\d{2,4})(?:\s+\((.*?)\))?', texto, re.IGNORECASE)

    data_hoje = datetime.now().strftime('%d/%m/%Y')

    if cirurgia_matches:
        cirurgias = []
        for data, medico in cirurgia_matches:
            data_fmt = formatar_data(data)
            if medico:
                medico_fmt = medico.strip().capitalize()
                cirurgias.append(f"{data_fmt} ({medico_fmt})")
            else:
                cirurgias.append(f"{data_fmt}")
        cirurgia_str = "; ".join(cirurgias)
    else:
        cirurgia_str = "-"

    return {
        "paciente": nome.group(1).strip() if nome else "***",
        "ses": ses.group(1) if ses else "***",
        "idade": idade.group(1) if idade else "***",
        "peso": peso.group(1) if peso else "***",
        "data_admissao": data_hoje,
        "data_entrevista": data_hoje,
        "motivo": motivo.group(1).strip().replace('\n', ' ') if motivo else "***",
        "mecanismo": mecanismo.group(2).strip() if mecanismo else "mecanismo não especificado",
        "fratura": formatar_data(fratura.group(2)) if fratura else "-",
        "cirurgia": cirurgia_str
    }

def formatar_data(data):
    partes = data.strip().split('/')
    if len(partes[2]) == 2:
        partes[2] = '20' + partes[2]
    return '/'.join(partes)

def extrair_analgesia(texto):
    analgesicos = []
    texto = remover_acentos(texto.lower())

    padrao = r'(dipirona|tramadol)[^\n]*?\n?(\d+)\s+miligrama.*?(\d+\s*x\s*\d+\s*h|a criterio medico|sos).*?(endovenosa|subcutanea)'
    matches = re.findall(padrao, texto, re.IGNORECASE)

    for nome, dose, freq, via in matches:
        freq = freq.lower()
        if "criterio" in freq:
            freq_fmt = "ACM"
        elif "sos" in freq:
            freq_fmt = "SOS"
        else:
            freq_fmt = re.sub(r'\s+', '', freq)
        via_fmt = "EV" if "endovenosa" in via else "SC"
        analgesicos.append(f"{nome.capitalize()} {dose}mg, {freq_fmt}, {via_fmt}")

    return "; ".join(analgesicos) if analgesicos else "-"

def extrair_tev_tvp(texto):
    texto = remover_acentos(texto.lower())
    texto = re.sub(r'[ \t]+', ' ', texto)

    padrao = r'enoxaparina.*?(\d+)\s+mg.*?(1\s+vez\s+ao\s+dia|1x/dia|1\s*x\s*/\s*dia).*?(subcutanea)'
    resultados = re.findall(padrao, texto, re.DOTALL)

    protocolos = []
    for dose, freq, via in resultados:
        dose_fmt = f"{dose}mg"
        freq_fmt = "1x/dia"
        via_fmt = "SC" if "subcutanea" in via else via.upper()
        protocolos.append(f"Enoxaparina {dose_fmt}, {freq_fmt}, {via_fmt}")

    return "; ".join(protocolos) if protocolos else "-"

# Interface do Streamlit
st.title("Gerador de Admissão - Farmácia Clínica Ortopedia")

texto_input = st.text_area("Cole aqui o texto do prontuário:")

if st.button("Gerar Formatação"):
    if texto_input:
        info = extrair_info(texto_input)
        analgesia = extrair_analgesia(texto_input)
        tev_tvp = extrair_tev_tvp(texto_input)

        resultado = f"""
FARMÁCIA CLÍNICA 
ADMISSÃO ORTOPEDIA 1 ou 2
----------------------------------------------------------------------------
Paciente: {info["paciente"]}; SES: {info["ses"]}; 
Idade: {info["idade"]} anos; Peso: {info["peso"]}
Data de admissão: {info["data_admissao"]}
Data da entrevista: {info["data_entrevista"]}
----------------------------------------------------------------------------
Motivo da internação:
{info["motivo"]}
Mecanismo do trauma:
{info["mecanismo"]}
Data da fratura: {info["fratura"]}
Data da cirurgia: {info["cirurgia"]}
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
- TEV/TVP: {tev_tvp}
- 
- LAMG: 
-
- Analgesia:
- {analgesia}
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
        st.text_area("Resultado Formatado:", resultado, height=900)
    else:
        st.warning("Por favor, cole o texto do prontuário.")
