import streamlit as st
import re
from datetime import datetime

st.title("Gerador de Admissão Farmácia Clínica")
texto = st.text_area("Cole aqui os dados do prontuário:", height=600)

formato = st.radio("Escolha o tipo de formatação:", ["Ortopedia", "Clínica médica"])

# --- Seleções TEV/TVP ---
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
selecionados_tev = st.multiselect("Profilaxia TEV/TVP (Selecione até 3 opções):", options=opcoes_tev, max_selections=3)

# --- Seleções LAMG ---
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
selecionados_lamg = st.multiselect("Profilaxia LAMG (Selecione até 3 opções):", options=opcoes_lamg, max_selections=3)

# --- Seleções ANALGESIA ---
opcoes_analgesia = [
    "Dipirona 1g 6/6h EV",
    "Dipirona 1g SOS EV",
    "Tramadol 100mg 12/12h EV",
    "Tramadol 100mg 8/8h EV",
    "Tramadol 100mg 6/6h EV",
    "Tramadol 100mg SOS EV",
    "Tramadol 50mg 12/12h EV",
    "Tramadol 50mg 8/8h EV",
    "Tramadol 50mg 6/6h EV",
    "Tramadol 50mg SOS EV",
    "Tenoxicam 20mg 1x/dia EV",
    "Tenoxicam 20mg 12/12h EV",
    "Tenoxicam 40mg 1x/dia EV",
    "Tenoxicam 40mg 12/12h EV",
    "Naproxeno",
    "Diclofenaco"
]
selecionados_analgesia = st.multiselect("Analgesia (Selecione até 3 opções):", options=opcoes_analgesia, max_selections=3)

def gerar_formatacao_ortopedia(paciente, ses, idade, hoje, diagnostico, mecanismo_trauma, data_fratura_formatada, cirurgia_str, tev_texto, lamg_texto, analgesia_texto):
    return f"""FARMÁCIA CLÍNICA 
ADMISSÃO ORTOPEDIA 1
----------------------------------------------------------------------------
Paciente: {paciente}; SES: {ses}; 
Idade: {idade} anos; Peso: -
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
{analgesia_texto}
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

def gerar_formatacao_clinica(paciente, ses, idade, hoje, tev_texto, lamg_texto, analgesia_texto):
    return f"""ADMISSÃO FARMACÊUTICA | ANEXO CLÍNICA MÉDICA
----------------------------------------------------------------------------
Paciente: {paciente}; SES: {ses}; 
Idade: {idade} anos; Peso: -
Data de admissão: {hoje}
Data da entrevista: {hoje}
----------------------------------------------------------------------------
Motivo da internação:
-
----------------------------------------------------------------------------
Antecedentes:
- XXX
- Nega comorbidades
- Sem relato de tabagismo e etilismo
- Nega tabagismo e etilismo
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
----------------------------------------------------------------------------
Culturas e Sorologias: 
----------------------------------------------------------------------------
Profilaxias e protocolos
- TEV/TVP:
{tev_texto}
- LAMG: 
{lamg_texto}
- Analgesia:
{analgesia_texto}
----------------------------------------------------------------------------
Conduta
- Realizo a avaliação farmacoterapêutica e a análise da prescrição quanto à necessidade, efetividade e segurança, incluindo avaliação de dose, posologia, via de administração, possíveis interações medicamentosas e disponibilidade em estoque.
- Sem exames laboratoriais recentes. Acompanho evolução clínica.
- Avalio exames laboratoriais de **/**/****, controles e acompanho evolução clínica.
---
- Vigilância infecciosa.
- Programo entrevista farmacêutica.
- Realizo entrevista farmacêutica: XXX
- Paciente avaliado como risco BAIXO. Reavaliação programada para o dia: 06/06/25
- Paciente avaliado como risco MÉDIO. Reavaliação programada para o dia: 03/06/25
- Paciente avaliado como risco ALTO. Reavaliação programada para o dia: 01/06/25
.
Segue em acompanhamento pelo Núcleo de Farmácia Clínica.
************************************************************"""

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
        r'DIAGN[ÓO]STICOS?:\s*((?:- .+\n?)+)',
        r'DIAGN[ÓO]STICO:\s+([^\n]+)'
    ]
    for padrao in padroes_diagnostico:
        match = re.search(padrao, texto, re.IGNORECASE)
        if match:
            diagnostico = match.group(1).strip().replace('\n', ' ')
            break

    mecanismo = re.search(r'MECANISMO DO TRAUMA:\s*(.+)', texto, re.IGNORECASE)
    hda = re.search(r'HDA:\s*(.+)', texto, re.IGNORECASE)
    mecanismo_trauma = mecanismo.group(1).strip() if mecanismo else (hda.group(1).strip() if hda else "mecanismo não especificado")

    data_fratura = re.search(r'DATA DA (?:FRATURA|LES[ÃA]O):\s+(\d{2}/\d{2}/\d{2,4})', texto, re.IGNORECASE)
    data_fratura_formatada = normalizar_data(data_fratura.group(1)) if data_fratura else "-"

    cirurgia_matches = re.findall(r'DATA DA CIRURGIA:\s+(\d{2}/\d{2}/\d{2,4})(?:\s+\((.*?)\))?', texto)
    datas_cirurgia = []
    for data, medico in cirurgia_matches:
        data_formatada = normalizar_data(data)
        if medico:
            medico = re.sub(r'(?i)^Dr\.?\s*', '', medico.strip())
            datas_cirurgia.append(f"{data_formatada} (Dr. {medico.capitalize()})")
        else:
            datas_cirurgia.append(data_formatada)
    cirurgia_str = "; ".join(datas_cirurgia) if datas_cirurgia else "-"

    tev_texto = "\n".join([f"- {med}" for med in selecionados_tev]) if selecionados_tev else "- Não prescrito"
    lamg_texto = "\n".join([f"- {med}" for med in selecionados_lamg]) if selecionados_lamg else "- Não prescrito"
    analgesia_texto = "\n".join([f"- {med}" for med in selecionados_analgesia]) if selecionados_analgesia else "- Não prescrito"

    nome = paciente.group(1).strip() if paciente else "paciente"
    nome_paciente = nome.replace(" ", "_")

    resultado = gerar_formatacao_ortopedia(paciente.group(1) if paciente else "-", ses.group(1) if ses else "-", idade.group(1) if idade else "-", hoje, diagnostico, mecanismo_trauma, data_fratura_formatada, cirurgia_str, tev_texto, lamg_texto, analgesia_texto) if formato == "Ortopedia" else gerar_formatacao_clinica(paciente.group(1) if paciente else "-", ses.group(1) if ses else "-", idade.group(1) if idade else "-", hoje, tev_texto, lamg_texto, analgesia_texto)

    return resultado, nome_paciente

if texto:
    resultado, nome_paciente = extrair_info(texto)
    st.text_area("Resultado Formatado:", resultado, height=1000, key="resultado_formatado")

    st.markdown(f"""
        <button onclick=\"navigator.clipboard.writeText(document.getElementById('resultado_formatado').value)\" 
                style=\"background-color:#4CAF50;border:none;color:#07693d;padding:10px 20px;
                       text-align:center;text-decoration:none;display:inline-block;
                       font-size:16px;border-radius:10px;margin-top:10px;cursor:pointer;\">
            📋 Clique aqui para copiar
        </button>
    """, unsafe_allow_html=True)

    st.download_button("📅 Baixar como .txt", resultado, file_name=f"{nome_paciente}_admissao.txt")
