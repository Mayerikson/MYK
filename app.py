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
    - Selecione **uma banda de classificação Alta**.
    - Selecione **até duas bandas de classificação Média ou Baixa**.
    - O total de bandas selecionadas não pode exceder **4**.
""")

# Separar bandas por classificação
bandas_altas = df[df['Classificação'] == 'Alta'][['Antecedent', 'Consequent']].stack().unique()
bandas_medias = df[df['Classificação'] == 'Média'][['Antecedent', 'Consequent']].stack().unique()
bandas_baixas = df[df['Classificação'] == 'Baixa'][['Antecedent', 'Consequent']].stack().unique()

# Seleção de bandas pelo usuário
st.write("Selecione as bandas conforme as regras acima:")

# Banda de classificação Alta (obrigatória)
banda_alta = st.selectbox('Selecione uma banda de classificação Alta:', bandas_altas)

# Listas para armazenar as bandas selecionadas
bandas_selecionadas = [banda_alta] if banda_alta else []

# Contador para limitar o número de bandas adicionais
max_bandas_adicionais = 2  # Máximo de 2 bandas adicionais (Média ou Baixa)

if len(bandas_selecionadas) > 0:  # Apenas se uma banda Alta foi selecionada
    st.write(f"Você pode selecionar até {max_bandas_adicionais} bandas de classificação Média ou Baixa:")
    
    # Combinação de bandas Médias e Baixas
    todas_bandas_medias_baixas = list(set(bandas_medias).union(set(bandas_baixas)))
    
    for i in range(max_bandas_adicionais):
        placeholder_text = f"Selecione uma banda adicional ({i+1}/{max_bandas_adicionais}):"
        banda_adicional = st.selectbox(placeholder_text, todas_bandas_medias_baixas, index=None, key=f"banda_{i}")
        
        if banda_adicional:
            bandas_selecionadas.append(banda_adicional)
        else:
            break  # Para de solicitar seleções se o usuário não escolher mais bandas

# Exibir resultados
if bandas_selecionadas:
    resultados = df[df['Antecedent'].isin(bandas_selecionadas) | df['Consequent'].isin(bandas_selecionadas)]
    st.write('Bandas Selecionadas e suas Classificações de Confiança:')
    # Converter para HTML sem índices
    st.markdown(resultados[['Antecedent', 'Consequent', '% de Confiança', 'Classificação']].to_html(index=False), unsafe_allow_html=True)
else:
    st.write('Por favor, selecione pelo menos uma banda de classificação Alta.')
