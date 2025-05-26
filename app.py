import streamlit as st
import re
from datetime import datetime

st.title("Gerador de Admissão - Farmácia Clínica Ortopedia")

texto = st.text_area("Cole aqui o texto do prontuário:")

if st.button("Gerar Admissão"):
    hoje = datetime.now().strftime("%d/%m/%Y")

    ses = re.search(r'SES:\s+(\d+)', texto)
    paciente = re.search(r'Paciente:\s+(.*?)\t', texto)
    idade = re.search(r'Idade:\s+(\d+)', texto)

    motivo_match = re.search(r'DIAGN[ÓO]STICOS?:\s*(.*?)\n[-–•]', texto, re.DOTALL | re.IGNORECASE)
    if not motivo_match:
        motivo_match = re.search(r'DIAGN[ÓO]STICOS?:\s*(.*)', texto, re.IGNORECASE)
    motivo = motivo_match.group(1).strip() if motivo_match else "-"

    trauma_match = re.search(r'MECANISMO DO TRAUMA:\s*(.*?)\n', texto, re.IGNORECASE)
    if not trauma_match:
        trauma_match = re.search(r'HDA:\s*(.*?)\n', texto, re.IGNORECASE)
    mecanismo = trauma_match.group(1).strip() if trauma_match else "mecanismo não especificado"

    fratura_match = re.search(r'DATA DA (FRATURA|LES[ÃA]O):\s*(\d{2}/\d{2}/\d{2,4})', texto, re.IGNORECASE)
    data_fratura = fratura_match.group(2) if fratura_match else "-"

    def corrigir_data(data):
        if re.match(r'\d{2}/\d{2}/\d{2}$', data):
            dia, mes, ano = data.split('/')
            ano = '20' + ano if int(ano) < 50 else '19' + ano
            return f"{dia}/{mes}/{ano}"
        return data

    data_fratura = corrigir_data(data_fratura)

    cirurgia_matches = re.findall(r'DATA DA CIRURGIA:\s+(\d{2}/\d{2}/\d{2,4})(?:\s+\((.*?)\))?', texto)
    datas_cirurgia = []
    for data, doutor in cirurgia_matches:
        data_corrigida = corrigir_data(data)
        if doutor:
            datas_cirurgia.append(f"{data_corrigida} ({doutor.strip()})")
        else:
            datas_cirurgia.append(data_corrigida)
    data_cirurgia = "; ".join(datas_cirurgia) if datas_cirurgia else "-"

    analgesia = []
    linhas = texto.splitlines()
    for i in range(len(linhas)-1):
        linha_nome = linhas[i]
        linha_dados = linhas[i+1]

        if any(med in linha_nome.upper() for med in ["DIPIRONA", "TRAMADOL"]):
            nome_match = re.match(r'([A-Za-zçÇãõáéíóúâêôàèìòùäëïöüÁÉÍÓÚÂÊÔÀÈÌÒÙÄËÏÖÜ ]+)', linha_nome.strip())
            if nome_match:
                nome = nome_match.group(1).split()[0].capitalize()
                dose = re.search(r'(\d+)', linha_dados)
                unidade = re.search(r'(Miligrama|Grama|Micrograma)', linha_dados, re.IGNORECASE)
                frequencia = re.search(r'(\d+\s*x\s*\d+\s*h|a crit[ée]rio m[ée]dico|sos)', linha_dados, re.IGNORECASE)
                via = re.search(r'(Endovenosa|Intramuscular|Oral)', linha_dados, re.IGNORECASE)

                unidade_map = {
                    "Miligrama": "mg",
                    "Grama": "g",
                    "Micrograma": "mcg"
                }

                freq_txt = "-"
                if frequencia:
                    f = frequencia.group(1).lower()
                    if "crit" in f:
                        freq_txt = "ACM"
                    elif "sos" in f:
                        freq_txt = "SOS"
                    else:
                        freq_txt = f.replace(" ", "")

                if nome and dose and unidade and via:
                    unidade_abv = unidade_map.get(unidade.group(1).capitalize(), unidade.group(1))
                    via_abv = {"Endovenosa": "EV", "Intramuscular": "IM", "Oral": "VO"}.get(via.group(1), via.group(1))
                    analgesia.append(f"{nome} {dose.group(1)} {unidade_abv}, {freq_txt}, {via_abv}")

    analgesia_str = "; ".join(analgesia) if analgesia else "-"

    output = f"""
FARMÁCIA CLÍNICA 
ADMISSÃO ORTOPEDIA 1 ou 2
----------------------------------------------------------------------------
Paciente: {paciente.group(1) if paciente else '-'}; SES: {ses.group(1) if ses else '-'}; 
Idade: {idade.group(1) if idade else '-'} anos; Peso: ***
Data de admissão: {hoje}
Data da entrevista: {hoje}
----------------------------------------------------------------------------
Motivo da internação:
{motivo}

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
- {analgesia_str}
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

    st.text_area("Admissão Gerada:", output, height=800)
