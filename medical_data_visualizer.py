import pandas as pd # Importa a biblioteca Pandas para manipulação de dados
import seaborn as sns # Importa a biblioteca Seaborn para visualização de dados
import matplotlib.pyplot as plt # Importa Matplotlib para gerar gráficos
import numpy as np # Importa NumPy para operações matemáticas

# Importando dados do arquivo CSV para um dataframe do Pandas
df = pd.read_csv('medical_examination.csv')

# Adicionando coluna 'overweight' (sobrepeso)
df['overweight'] = (df['weight'] / ((df['height'] / 100) ** 2) > 25).astype(int)

# Normalizando colunas 'gluc' e 'cholesterol'
df[['gluc', 'cholesterol']] = (df[['gluc', 'cholesterol']] > 1).astype(int)

# Função para gerar gráfico categórico
def draw_cat_plot():
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke']) # Reorganiza os dados em um formato adequado
    fig = sns.catplot(data=df_cat, kind='count', x='variable', hue='value', col='cardio').set(ylabel='total').fig   # Cria um gráfico categórico mostrando a contagem de cada variável
    fig.savefig('catplot.png') # Salva o gráfico categórico em um arquivo PNG
    return fig

# Função para gerar mapa de calor
def draw_heat_map():
    df_heat = df[
        # Filtra os dados para remover outliers
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]
    
    corr = df_heat.corr() # Calcula a matriz de correlação dos dados filtrados
    mask = np.triu(corr) # Cria uma máscara para a matriz triangular superior para não mostrar valores duplicados no mapa de calor

    fig, ax = plt.subplots() # Cria uma figura para o mapa de calor
    sns.heatmap(corr, mask=mask, annot=True, fmt='0.1f', square=True, ax=ax) # Gera o mapa de calor usando a matriz de correlação e aplica a máscara para a metade superior
    
    fig.savefig('heatmap.png') # Salva o mapa de calor em um arquivo PNG
    return fig
