import streamlit as st
import re
from datetime import datetime

st.title("Gerador de Admissão Farmácia Clínica")

texto = st.text_area("Cole aqui os dados do prontuário:", height=600)

def extrair_info(texto):
    hoje = datetime.today().strftime('%d/%m/%Y')

    # Função para normalizar datas
    def normalizar_data(data):
        if re.match(r'\d{2}/\d{2}/\d{2}$', data):
            return re.sub(r'/(\d{2})$', lambda m: '/20' + m.group(1), data)
        return data

    # SES e paciente
    ses = re.search(r'SES:\s+(\d+)', texto)
    paciente = re.search(r'Paciente:\s+([^\t\n]+)', texto)
    idade = re.search(r'Idade:\s+(\d+)', texto)
    
    # Diagnóstico
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

    # Mecanismo do trauma
    mecanismo = re.search(r'MECANISMO DO TRAUMA:\s*(.+)', texto, re.IGNORECASE)
    hda = re.search(r'HDA:\s*(.+)', texto, re.IGNORECASE)
    mecanismo_trauma = "mecanismo não especificado"
    if mecanismo:
        mecanismo_trauma = mecanismo.group(1).strip()
    elif hda:
        mecanismo_trauma = hda.group(1).strip()

    # Data da fratura ou lesão
    data_fratura = re.search(r'DATA DA (?:FRATURA|LES[AÃ]O):\s+(\d{2}/\d{2}/\d{2,4})', texto, re.IGNORECASE)
    data_fratura_formatada = normalizar_data(data_fratura.group(1)) if data_fratura else "-"

    # Datas de cirurgia e médicos
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

    # Analgesia (dipirona e tramadol)
    analgesicos = []
    analgesia_padrao = re.compile(
        r'(DIPI?RONA|TRAMADOL)[^\n]*?\n(\d+)\s+Mili(?:grama|gramas).*?\n(.+?)\s+(Endovenosa)',
        re.IGNORECASE
    )
    for match in analgesia_padrao.findall(texto):
        nome = match[0].capitalize()
        dose = match[1]
        freq_raw = match[2].lower()
        via = "EV"
        if "crit" in freq_raw:
            freq = "ACM"
        elif "sos" in freq_raw:
            freq = "SOS"
        else:
            freq = re.sub(r'[^0-9x/]', '', freq_raw).replace('x', 'x')
            if not freq:
                freq = freq_raw
        analgesicos.append(f"{nome} {dose}mg, {freq}, {via}")
    analgesia_str = "; ".join(analgesicos) if analgesicos else "-"

    # TEV/TVP com Enoxaparina
    tev_tvp = "-"
    enoxa_match = re.search(
        r'ENOXAPARINA[^\n]*?\n(\d+)\s+UM.*?\n(.+?)\s+(Subcutanea)',
        texto, re.IGNORECASE
    )
    if enoxa_match:
        dose = enoxa_match.group(1)
        freq_raw = enoxa_match.group(2).lower()
        via = "SC"
        if "crit" in freq_raw:
            freq = "ACM"
        elif "sos" in freq_raw:
            freq = "SOS"
        else:
            freq = re.sub(r'[^0-9x/]', '', freq_raw).replace('x', 'x')
            if not freq:
                freq = freq_raw
        tev_tvp = f"Enoxaparina {dose}mg, {freq}, {via}"

    # Formatação final
    resultado = f"""FARMÁCIA CLÍNICA 
ADMISSÃO ORTOPEDIA 1
----------------------------------------------------------------------------
Paciente: {paciente.group(1) if paciente else '-'}; SES: {ses.group(1) if ses else '-'}; 
Idade: {idade.group(1) if idade else '-'} anos; Peso: -
Data de admissão: {hoje}
Data da entrevista: {hoje}
----------------------------------------------------------------------------
Motivo da intern
