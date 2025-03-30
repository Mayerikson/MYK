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

# Carregar os dados do arquivo Excel
file_path = 'recomendações.xlsx'  # Certifique-se de que o caminho está correto
df = pd.read_excel(file_path)

# Adicionar uma coluna de classificação ao DataFrame
df['Classificação'] = df['% de Confiança'].apply(classificar_confianca)

# Interface do Streamlit
st.title('Lineup de Bandas')

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
