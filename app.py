import streamlit as st
import re
from datetime import datetime

st.set_page_config(page_title="Admissão Ortopedia", layout="centered")
st.title("Gerador de Admissão - Farmácia Clínica Ortopedia")

prontuario_texto = st.text_area("Cole abaixo o texto do prontuário:", height=300)

def formatar_data(data_str):
    """Aceita datas com 2 ou 4 dígitos no ano e padroniza para dd/mm/yyyy."""
    try:
        if re.match(r'\d{2}/\d{2}/\d{2}$', data_str):
            return datetime.strptime(data_str, "%d/%m/%y").strftime("%d/%m/%Y")
        elif re.match(r'\d{2}/\d{2}/\d{4}$', data_str):
            return datetime.strptime(data_str, "%d/%m/%Y").strftime("%d/%m/%Y")
    except:
        return data_str
    return data_str

def extrair_info(texto):
    paciente = re.search(r'Paciente:\s+(.*?)\t', texto)
    ses = re.search(r'SES:\s+(\d+)', texto)
    idade = re.search(r'Idade:\s+(\d+)', texto)
    peso = re.search(r'Peso:\s+(\d+)', texto)

    # Diagnóstico
    diagnostico_match = re.search(r'DIAGN[ÓO]STICOS?:\s*\n((?:- .*\n?)+)', texto, re.IGNORECASE)
    if diagnostico_match:
        linhas_diagnostico = diagnostico_match.group(1).strip().splitlines()
        diagnostico_formatado = " / ".join([linha.strip("- ").strip() for linha in linhas_diagnostico])
    else:
        diagnostico_formatado = "Diagnóstico não especificado"

    # Mecanismo do trauma
    mecanismo = re.search(r'MECANISMO DO TRAUMA:\s*(.*)', texto)
    if not mecanismo:
        mecanismo = re.search(r'HDA:\s*(.*)', texto)
    mecanismo_texto = mecanismo.group(1).strip() if mecanismo else "mecanismo não especificado"

    # Data da fratura
    data_fratura_match = re.search(r'DATA DA FRATURA:\s+(\d{2}/\d{2}/\d{2,4})', texto)
    data_fratura = formatar_data(data_fratura_match.group(1)) if data_fratura_match else "-"

    # Datas da cirurgia
    cirurgia_matches = re.findall(r'DATA DA CIRURGIA:\s+(\d{2}/\d{2}/\d{2,4})(?:\s+\((.*?)\))?', texto)
    if cirurgia_matches:
        datas_cirurgia_texto = []
        for data, medico in cirurgia_matches:
            data_formatada = formatar_data(data)
            if medico:
                medico_formatado = re.sub(r'(?i)^dr[.]?\s*', '', medico.strip())
                medico_formatado = "Dr. " + medico_formatado.title()
                datas_cirurgia_texto.append(f"{data_formatada} ({medico_formatado})")
            else:
                datas_cirurgia_texto.append(data_formatada)
        datas_cirurgia_texto = ", ".join(datas_cirurgia_texto)
    else:
        datas_cirurgia_texto = "-"

    # Data atual formatada para admissão e entrevista
    hoje = datetime.today().strftime('%d/%m/%Y')

    return {
        "paciente": paciente.group(1) if paciente else "",
        "ses": ses.group(1) if ses else "",
        "idade": idade.group(1) if idade else "",
        "peso": peso.group(1) if peso else "—",
        "data_admissao": hoje,
        "data_entrevista": hoje,
        "motivo": diagnostico_formatado,
        "mecanismo": mecanismo_texto,
        "data_fratura": data_fratura,
        "datas_cirurgia": datas_cirurgia_texto
    }

if prontuario_texto:
    dados = extrair_info(prontuario_texto)

    resultado = f"""
FARMÁCIA CLÍNICA 
ADMISSÃO ORTOPEDIA 1 ou 2
----------------------------------------------------------------------------
Paciente: {dados['paciente']}; SES: {dados['ses']}; 
Idade: {dados['idade']} anos; Peso: {dados['peso']}
Data de admissão: {dados['data_admissao']}
Data da entrevista: {dados['data_entrevista']}
----------------------------------------------------------------------------
Motivo da internação: {dados['motivo']}

Mecanismo do trauma: {dados['mecanismo']}
Data da fratura: {dados['data_fratura']}.
Data da cirurgia: {dados['datas_cirurgia']}.
    """.strip()

    st.text_area("Resultado formatado:", value=resultado, height=300)
