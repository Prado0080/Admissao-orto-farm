import streamlit as st
import re
from datetime import datetime
import unicodedata

def remover_acentos(txt):
    return ''.join(c for c in unicodedata.normalize('NFD', txt)
                   if unicodedata.category(c) != 'Mn')

def extrair_analgesia(texto):
    analgesicos = []

    # Pré-processamento: caixa baixa, sem acento e normalização de espaços
    texto = remover_acentos(texto.lower())
    texto = re.sub(r'[ \t]+', ' ', texto)

    # Expressão para capturar os blocos com Dipirona ou Tramadol
    padrao = r'(dipirona|tramadol).*?(\d+)\s+miligrama.*?(?:(\d+\s*x\s*\d+\s*h)|a criterio medico|sos).*?(endovenosa)'
    resultados = re.findall(padrao, texto, re.DOTALL)

    for nome, dose, frequencia, via in resultados:
        nome_cap = nome.capitalize()
        dose_formatada = f"{dose}mg"

        if not frequencia or frequencia.strip() == '':
            frequencia_formatada = ''
        else:
            frequencia = frequencia.strip().replace(' ', '')
            if "criterio" in frequencia:
                frequencia_formatada = "ACM"
            elif "sos" in frequencia.lower():
                frequencia_formatada = "SOS"
            else:
                frequencia_formatada = frequencia

        via_formatada = "EV" if "endovenosa" in via else via.upper()

        analgesicos.append(f"{nome_cap} {dose_formatada}, {frequencia_formatada}, {via_formatada}")

    return "; ".join(analgesicos) if analgesicos else "-"

def main():
    st.title("Gerador de Relatório - Farmácia Clínica Ortopedia")

    prontuario_input = st.text_area("Cole o texto do prontuário aqui:")

    if st.button("Gerar Relatório"):
        if prontuario_input.strip() == "":
            st.warning("Por favor, cole o texto do prontuário.")
            return

        texto = prontuario_input

        # Datas atuais
        hoje = datetime.today().strftime("%d/%m/%Y")

        # Captura dados básicos
        paciente = re.search(r'Paciente:\s+(.*?)(?:\s{2,}|\t)', texto)
        ses = re.search(r'SES:\s+(\d+)', texto)
        idade = re.search(r'Idade:\s+(\d+)', texto)
        peso = re.search(r'Peso:\s+(\d+)', texto)

        # Diagnóstico (motivo da internação)
        diagnostico = re.search(r'DIAGN[ÓO]STICOS?:\s*[-–]*\s*(.*)', texto, re.IGNORECASE)
        if not diagnostico:
            diagnostico = re.search(r'DIAGN[ÓO]STICO:\s*[-–]*\s*(.*)', texto, re.IGNORECASE)

        motivo = diagnostico.group(1).strip() if diagnostico else "-"

        # Mecanismo do trauma
        mecanismo = re.search(r'(HDA|MECANISMO DO TRAUMA):\s*(.*)', texto, re.IGNORECASE)
        mecanismo = mecanismo.group(2).strip() if mecanismo else "mecanismo não especificado"

        # Data da fratura ou lesão
        fratura = re.search(r'DATA DA (FRATURA|LESAO):\s+(\d{2}/\d{2}/\d{2,4})', texto, re.IGNORECASE)
        data_fratura = "-"
        if fratura:
            data_f = fratura.group(2)
            if len(data_f.split('/')[-1]) == 2:
                data_f = re.sub(r'(\d{2}/\d{2}/)(\d{2})$', r'\g<1>20\2', data_f)
            data_fratura = data_f

        # Datas da cirurgia
        cirurgia_matches = re.findall(r'DATA DA CIRURGIA:\s+(\d{2}/\d{2}/\d{2,4})(?:\s+\((.*?)\))?', texto, re.IGNORECASE)
        datas_cirurgia_formatadas = []
        for data, medico in cirurgia_matches:
            if len(data.split('/')[-1]) == 2:
                data = re.sub(r'(\d{2}/\d{2}/)(\d{2})$', r'\g<1>20\2', data)
            if medico:
                datas_cirurgia_formatadas.append(f"{data} ({medico})")
            else:
                datas_cirurgia_formatadas.append(f"{data}")
        data_cirurgia = "; ".join(datas_cirurgia_formatadas) if datas_cirurgia_formatadas else "-"

        # Analgesia
        analgesia = extrair_analgesia(texto)

        # Resultado final formatado
        resultado = f"""FARMÁCIA CLÍNICA 
ADMISSÃO ORTOPEDIA 1 ou 2
----------------------------------------------------------------------------
Paciente: {paciente.group(1).strip() if paciente else "***"}; SES: {ses.group(1) if ses else "***"}; 
Idade: {idade.group(1) if idade else "***"} anos; Peso: {peso.group(1) if peso else "***"}
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
Profilaxias e protocolos
- TEV/TVP: 
- 
- LAMG: 
-
- Analgesia:
- {analgesia}
----------------------------------------------------------------------------- 
Conduta
- Realizo análise técnica da prescrição quanto à indicação, efetividade, posologia, dose, possíveis interações medicamentosas e disponibilidade na farmácia.
- Realizo visita beira a leito, encontro o paciente dormindo 
- Monitoro exames laboratoriais de **/**/****, controles e evolução clínica.
---
- Acompanho antibioticoterapia e parâmetros infecciosos: Paciente afebril, em uso de (***) D*; Leuco **.
- Paciente avaliado como risco (****), reavaliação programada para o dia: **/**/****
- Segue em acompanhamento pelo Núcleo de Farmácia Clínica.

- Estagiário ***, supervisionado por *********
- Farmacêutico ***
*******************************************************
"""

        st.text_area("Relatório Gerado:", value=resultado, height=1000)

if __name__ == "__main__":
    main()

