import streamlit as st
import re
from datetime import datetime

st.title("Gerador de Admissão Farmácia Clínica")

texto = st.text_area("Cole aqui os dados do prontuário:", height=600)

# --- Seleção TEV/TVP ---
opcoes_tev = [
    "Enoxaparina 20mg 1x/dia SC",
    "Enoxaparina 20mg 12/12h SC",
    "Enoxaparina 40mg 1x/dia SC",
    "Enoxaparina 40mg 12/12h SC",
    "Enoxaparina 60mg 1x/dia SC",
    "Enoxaparina 60mg 12/12h SC",
    "Enoxaparina 80mg 1x/dia SC",
    "Enoxaparina 80mg 12/12h SC",
    "Enoxaparina 100mg 1x/dia SC",
    "Enoxaparina 100mg 12/12h SC",
    "HNF 5.000UI 12/12h SC",
    "HNF 5.000UI 8/8h SC"
]

selecionados_tev = st.multiselect(
    "Profilaxia TEV/TVP (Selecione até 3 opções):",
    options=opcoes_tev,
    max_selections=3
)

# --- Seleção LAMG ---
opcoes_lamg = [
    "Omeprazol 20mg 1x/dia VO",
    "Omeprazol 20mg 12/12h VO",
    "Omeprazol 40mg 1x/dia EV",
    "Omeprazol 40mg 12/12h EV",
    "Omeprazol 80mg 1x/dia EV",
    "Omeprazol 80mg 12/12h EV",
    "Pantoprazol 40mg 1x/dia EV",
    "Pantoprazol 40mg 12/12h EV",
    "Pantoprazol 80mg 1x/dia EV",
    "Pantoprazol 80mg 12/12h EV"
]

selecionados_lamg = st.multiselect(
    "Profilaxia LAMG (Selecione até 3 opções):",
    options=opcoes_lamg,
    max_selections=3
)

def extrair_info(texto):
    hoje = datetime.today().strftime('%d/%m/%Y')

    def normalizar_data(data):
        if re.match(r'\d{2}/\d{2}/\d{2}$', data):
            return re.sub(r'/(\d{2})$', lambda m: '/20' + m.group(1), data)
        return data

    ses = re.search(r'SES:\s+(\d+)', texto)
    paciente = re.search(r'Paciente:\s+([^\t\n]+)', texto)
    idade = re.search(r'Idade:\s+(\d+)', texto)

    diagnostico = ""
    padroes_diagnostico = [
        r'DIAGNÓSTICOS?:\s*((?:- .+\n?)+)',
        r'DIAGNÓSTICO:\s*((?:- .+\n?)+)',
        r'DIAGNÓSTICO:\s+([^\n]+)'
    ]
    for padrao in padroes_diagnostico:
        match = re.search(padrao, texto, re.IGNORECASE)
        if match:
            diagnostico = match.group(1).strip().replace('\n', ' ')
            break

    mecanismo = re.search(r'MECANISMO DO TRAUMA:\s*(.+)', texto, re.IGNORECASE)
    hda = re.search(r'HDA:\s*(.+)', texto, re.IGNORECASE)
    mecanismo_trauma = "mecanismo não especificado"
    if mecanismo:
        mecanismo_trauma = mecanismo.group(1).strip()
    elif hda:
        mecanismo_trauma = hda.group(1).strip()

    data_fratura = re.search(r'DATA DA (?:FRATURA|LES[AÃ]O):\s+(\d{2}/\d{2}/\d{2,4})', texto, re.IGNORECASE)
    data_fratura_formatada = normalizar_data(data_fratura.group(1)) if data_fratura else "-"

    cirurgia_matches = re.findall(r'DATA DA CIRURGIA:\s+(\d{2}/\d{2}/\d{2,4})(?:\s+\((.*?)\))?', texto)
    datas_cirurgia = []
    for data, medico in cirurgia_matches:
        data_formatada = normalizar_data(data)
        if medico:
            medico = medico.strip()
            medico = re.sub(r'(?i)^Dr\.?\s*', '', medico)
            datas_cirurgia.append(f"{data_formatada} (Dr. {medico.capitalize()})")
        else:
            datas_cirurgia.append(data_formatada)
    cirurgia_str = "; ".join(datas_cirurgia) if datas_cirurgia else "-"

    tev_texto = "\n".join([f"- {med}" for med in selecionados_tev]) if selecionados_tev else "- Não prescrito"
    lamg_texto = "\n".join([f"- {med}" for med in selecionados_lamg]) if selecionados_lamg else "- Não prescrito"

    resultado = f"""FARMÁCIA CLÍNICA 
ADMISSÃO ORTOPEDIA 1
----------------------------------------------------------------------------
Paciente: {paciente.group(1) if paciente else '-'}; SES: {ses.group(1) if ses else '-'}; 
Idade: {idade.group(1) if idade else '-'} anos; Peso: -
Data de admissão: {hoje}
Data da entrevista: {hoje}
----------------------------------------------------------------------------
Motivo da internação:
{diagnostico}
Mecanismo do trauma:
{mecanismo_trauma}
Data da fratura: {data_fratura_formatada}
Data da cirurgia: {cirurgia_str}
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
{tev_texto}
- LAMG:
{lamg_texto}
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
*******************************************************"""
    return resultado

if texto:
    resultado = extrair_info(texto)
    st.text_area("Resultado Formatado:", resultado, height=1000)
    st.download_button("📥 Baixar como .txt", resultado, file_name="formatação_farmacia.txt")
