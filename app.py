import streamlit as st
import pandas as pd

# Função para classificar a confiança
def classificar_confianca(confianca):
    if confianca >= 70:
        return 'Alta'
    elif confianca >= 35:
        return 'Média'
    else:
        return 'Baixa'

# Interface do Streamlit
st.title('Lineup de Bandas')

# Permitir upload do arquivo Excel
uploaded_file = st.file_uploader("Escolha um arquivo Excel", type=["xlsx"])

if uploaded_file is not None:
    # Carregar os dados do arquivo Excel
    df = pd.read_excel(uploaded_file)

    # Adicionar uma coluna de classificação ao DataFrame
    df['Classificação'] = df['% de Confiança'].apply(classificar_confianca)

    # Seleção de bandas pelo usuário
    bandas_disponiveis = df[['Antecedent', 'Consequent']].stack().unique()
    bandas_selecionadas = st.multiselect('Selecione até 3 bandas:', bandas_disponiveis)

    # Exibir resultados
    if bandas_selecionadas:
        resultados = df[df['Antecedent'].isin(bandas_selecionadas) | df['Consequent'].isin(bandas_selecionadas)]
        st.write('Bandas Selecionadas e suas Classificações de Confiança:')
        st.dataframe(resultados[['Antecedent', 'Consequent', '% de Confiança', 'Classificação']])
    else:
        st.write('Por favor, selecione até 3 bandas.')
else:
    st.write('Por favor, faça upload de um arquivo Excel.')
