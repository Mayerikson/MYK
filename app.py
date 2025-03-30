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

# Explicação das classificações
st.write("""
    **Classificações de Confiança:**
    - **Alta:** % de Confiança ≥ 70
    - **Média:** 35 ≤ % de Confiança < 70
    - **Baixa:** % de Confiança < 35

    **Regras de Seleção:**
    - Selecione uma banda de classificação Alta.
    - Selecione até duas bandas de classificação Média ou Baixa.
    - Não é permitido selecionar mais de uma banda de classificação Alta.
""")

# Separar bandas por classificação
bandas_altas = df[df['Classificação'] == 'Alta'][['Antecedent', 'Consequent']].stack().unique()
bandas_medias = df[df['Classificação'] == 'Média'][['Antecedent', 'Consequent']].stack().unique()
bandas_baixas = df[df['Classificação'] == 'Baixa'][['Antecedent', 'Consequent']].stack().unique()

# Seleção de bandas pelo usuário
st.write("Selecione as bandas conforme as regras acima:")
banda_alta = st.selectbox('Selecione uma banda de classificação Alta:', bandas_altas)

# Listas para armazenar as bandas selecionadas
bandas_selecionadas = [banda_alta]

# Seleção de bandas de classificação Média
banda_media1 = st.selectbox('Selecione uma banda de classificação Média (opcional):', bandas_medias, index=None, placeholder="Selecione uma banda de classificação Média...")
if banda_media1:
    bandas_selecionadas.append(banda_media1)
    banda_media2 = st.selectbox('Selecione outra banda de classificação Média (opcional):', bandas_medias, index=None, placeholder="Selecione outra banda de classificação Média...")
    if banda_media2:
        bandas_selecionadas.append(banda_media2)

# Seleção de bandas de classificação Baixa
banda_baixa1 = st.selectbox('Selecione uma banda de classificação Baixa (opcional):', bandas_baixas, index=None, placeholder="Selecione uma banda de classificação Baixa...")
if banda_baixa1:
    bandas_selecionadas.append(banda_baixa1)
    banda_baixa2 = st.selectbox('Selecione outra banda de classificação Baixa (opcional):', bandas_baixas, index=None, placeholder="Selecione outra banda de classificação Baixa...")
    if banda_baixa2:
        bandas_selecionadas.append(banda_baixa2)

# Exibir resultados
if bandas_selecionadas:
    resultados = df[df['Antecedent'].isin(bandas_selecionadas) | df['Consequent'].isin(bandas_selecionadas)]
    st.write('Bandas Selecionadas e suas Classificações de Confiança:')
    # Converter para HTML sem índices
    st.markdown(resultados[['Antecedent', 'Consequent', '% de Confiança', 'Classificação']].to_html(index=False), unsafe_allow_html=True)
else:
    st.write('Por favor, selecione pelo menos uma banda de classificação Alta.')
