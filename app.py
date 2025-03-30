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

# Separar bandas por classificação
bandas_altas = df[df['Classificação'] == 'Alta'][['Antecedent', 'Consequent']].stack().unique()
bandas_medias = df[df['Classificação'] == 'Média'][['Antecedent', 'Consequent']].stack().unique()
bandas_baixas = df[df['Classificação'] == 'Baixa'][['Antecedent', 'Consequent']].stack().unique()

# Seleção de bandas pelo usuário
st.write("Selecione uma banda de cada classificação:")
banda_alta = st.selectbox('Selecione uma banda de classificação Alta:', bandas_altas)
banda_media = st.selectbox('Selecione uma banda de classificação Média:', bandas_medias)
banda_baixa = st.selectbox('Selecione uma banda de classificação Baixa:', bandas_baixas)
banda_extra = st.selectbox('Selecione uma banda adicional (opcional):', df[['Antecedent', 'Consequent']].stack().unique(), index=None, placeholder="Selecione uma banda adicional...")

# Lista de bandas selecionadas
bandas_selecionadas = [banda_alta, banda_media, banda_baixa]
if banda_extra:
    bandas_selecionadas.append(banda_extra)

# Exibir resultados
if bandas_selecionadas:
    resultados = df[df['Antecedent'].isin(bandas_selecionadas) | df['Consequent'].isin(bandas_selecionadas)]
    st.write('Bandas Selecionadas e suas Classificações de Confiança:')
    # Converter para HTML sem índices
    st.markdown(resultados[['Antecedent', 'Consequent', '% de Confiança', 'Classificação']].to_html(index=False), unsafe_allow_html=True)
else:
    st.write('Por favor, selecione pelo menos uma banda de cada classificação.')
