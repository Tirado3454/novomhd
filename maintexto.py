import streamlit as st
import pandas as pd
from fpdf import FPDF

# Inicializar o estado
if "etapas" not in st.session_state:
    st.session_state.etapas = []
if "descricao_etapa" not in st.session_state:
    st.session_state.descricao_etapa = ""
if "topico_selecionado" not in st.session_state:
    st.session_state.topico_selecionado = "Base Teórica"  # Inicialização padrão

# Função para adicionar etapa
def adicionar_etapa():
    if st.session_state.descricao_etapa:
        st.session_state.etapas.append(
            {
                "Tópico": st.session_state.topico_selecionado,
                "Descrição": st.session_state.descricao_etapa,
            }
        )
        st.session_state.descricao_etapa = ""  # Limpar o campo de descrição

# Função para exportar para PDF
def exportar_pdf(etapas):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Relatório do Modelo Hipotético-Dedutivo", ln=True, align='C')
    pdf.ln(10)

    for idx, etapa in enumerate(etapas):
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(200, 10, txt=f"Etapa {idx + 1}: {etapa['Tópico']}", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, etapa["Descrição"])
        pdf.ln(5)
    
    return pdf.output(dest="S").encode("latin1")

# Títulos e introdução
st.markdown(
    """
    <h1>
        <img src='data:image/png;base64,<insira_o_base64_gerado_da_logo_aqui>' style='height:50px; margin-right:10px;'> Modelo Hipot\u00e9tico-Dedutivo no Xadrez
    </h1>
    """,
    unsafe_allow_html=True
)
st.header("Etapas do Modelo Hipotético-Dedutivo")

# Seção de seleção de tópicos
st.subheader("Tópicos do MHD")
topicos_mhd = [
    "Base Teórica",
    "Observação",
    "Formulação de Hipóteses",
    "Dedução",
    "Teste por Experimento",
    "Análise dos Resultados",
    "Conclusão",
]
st.session_state.topico_selecionado = st.selectbox(
    "Selecione um tópico do MHD:", topicos_mhd
)

# Exibir dica com base no tópico selecionado
dicas = {
    "Base Teórica": "Considere o conhecimento já existente que fundamenta sua análise.",
    "Observação": "Observe atentamente e registre os detalhes relevantes.",
    "Formulação de Hipóteses": "Levante hipóteses sobre possíveis padrões ou explicações.",
    "Dedução": "Deduza as consequências lógicas das hipóteses formuladas.",
    "Teste por Experimento": "Teste suas hipóteses de maneira controlada.",
    "Análise dos Resultados": "Analise os dados obtidos para validar ou refutar a hipótese.",
    "Conclusão": "Elabore uma conclusão baseada nas observações e experimentos realizados.",
}
if st.session_state.topico_selecionado in dicas:
    st.info(dicas[st.session_state.topico_selecionado])

# Campo para descrição da etapa
st.subheader("Descreva a etapa")
st.session_state.descricao_etapa = st.text_area(
    "Descrição da etapa:", value=st.session_state.descricao_etapa
)

# Botão para adicionar etapa
if st.button("Adicionar etapa"):
    adicionar_etapa()

# Listar as etapas adicionadas
st.subheader("Etapas Adicionadas")
if st.session_state.etapas:
    for idx, etapa in enumerate(st.session_state.etapas):
        st.write(f"**Etapa {idx + 1}: {etapa['Tópico']}**")
        st.write(etapa["Descrição"])
else:
    st.info("Nenhuma etapa adicionada ainda.")

# Botão para exportar
st.subheader("Exportar Etapas")
col1, col2 = st.columns(2)

# Exportar para PDF
if col1.button("Exportar para PDF"):
    if st.session_state.etapas:
        pdf_bytes = exportar_pdf(st.session_state.etapas)
        st.download_button(
            label="Baixar PDF",
            data=pdf_bytes,
            file_name="etapas_mhd.pdf",
            mime="application/pdf",
        )
    else:
        st.warning("Nenhuma etapa para exportar!")

# Exportar para CSV
if col2.button("Exportar para CSV"):
    if st.session_state.etapas:
        df = pd.DataFrame(st.session_state.etapas)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Baixar CSV",
            data=csv,
            file_name="etapas_mhd.csv",
            mime="text/csv",
        )
    else:
        st.warning("Nenhuma etapa para exportar!")
