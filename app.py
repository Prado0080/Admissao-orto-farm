import streamlit as st
import re
from datetime import datetime

st.title("Gerador de Admissão Farmácia Clínica")

# Seletor de tipo de formatação
formato = st.radio("Selecione o tipo de formatação:", ["Ortopedia", "Clínica médica"])

texto = st.text_area("Cole aqui os dados do prontuário:", height=600)

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

def normalizar_data(data):
    if re.match(r'\d{2}/\d{2}/\d{2}$', data):
        return re.sub(r'/((\d{2}))$', lambda m: '/20' + m.group(1), data)
    return data

def extrair_comum(texto):
    ses = re.search(r'SES:\s+(\d+)', texto)
    paciente = re.search(r'Paciente:\s+([^\t\n]+)', texto)
    idade = re.search(r'Idade:\s+(\d+)', texto)

    tev_texto = "\n".join([f"- {med}" for med in selecionados_tev]) if selecionados_tev else "- Não prescrito"
    lamg_texto = "\n".join([f"- {med}" for med in selecionados_lamg]) if selecionados_lamg else "- Não prescrito"
    analgesia_texto = "\n".join([f"- {med}" for med in selecionados_analgesia]) if selecionados_analgesia else "- Não prescrito"

    nome_paciente = paciente.group(1).strip().replace(" ", "_") if paciente else "paciente"

    return ses, paciente, idade, tev_texto, lamg_texto, analgesia_texto, nome_paciente

# As funções extrair_info_ortopedia e extrair_info_clinica permanecem iguais
# (mantidas como estavam no seu código original por questão de espaço)
# ...

if texto:
    if formato == "Ortopedia":
        resultado = extrair_info_ortopedia(texto)
    else:
        resultado = extrair_info_clinica(texto)

    paciente = re.search(r'Paciente:\s+([^\t\n]+)', texto)
    nome_paciente = paciente.group(1).strip().replace(" ", "_") if paciente else "paciente"

    st.text_area("Resultado Formatado:", resultado, height=1000, key="resultado_formatado")

    st.markdown("""
        <style>
            .copiar-botao {
                background-color: #07693d;
                border: none;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                border-radius: 10px;
                margin-top: 10px;
                cursor: pointer;
            }
        </style>

        <button class="copiar-botao" onclick="copiarTexto()">📋 Clique aqui para copiar</button>
        <p id="aviso-copiado" style="color:green; font-weight:bold; display:none;">
            Texto copiado para a área de transferência!
        </p>

        <script>
        function copiarTexto() {
            const texto = document.getElementById("resultado_formatado").value;
            navigator.clipboard.writeText(texto).then(function() {
                const aviso = document.getElementById("aviso-copiado");
                aviso.style.display = "block";
                setTimeout(() => aviso.style.display = "none", 3000);
            });
        }
        </script>
    """, unsafe_allow_html=True)

    st.download_button("\U0001F5D5️ Baixar como .txt", resultado, file_name=f"{nome_paciente}_admissao.txt")
