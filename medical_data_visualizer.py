import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Importando dados
df = pd.read_csv('medical_examination.csv')

# Adicionando coluna 'overweight' (sobrepeso)
df['overweight'] = (df['weight'] / ((df['height'] / 100) ** 2) > 25).astype(int)

# Normalizando colunas 'gluc' e 'cholesterol'
df[['gluc', 'cholesterol']] = (df[['gluc', 'cholesterol']] > 1).astype(int)

# Função para gerar gráfico categórico
def draw_cat_plot():
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'])
    fig = sns.catplot(data=df_cat, kind='count', x='variable', hue='value', col='cardio').set(ylabel='total').fig
    fig.savefig('catplot.png')
    return fig

# Função para gerar mapa de calor
def draw_heat_map():
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]
    
    corr = df_heat.corr()
    mask = np.triu(corr)

    fig, ax = plt.subplots()
    sns.heatmap(corr, mask=mask, annot=True, fmt='0.1f', square=True, ax=ax)
    
    fig.savefig('heatmap.png')
    return fig
