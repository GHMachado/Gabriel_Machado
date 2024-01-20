# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 18:53:09 2023

@author: Gabriel Machado
"""

import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import ScalarFormatter, NullFormatter, MultipleLocator

# Abrir CSV com o rastreador (tracker)
df = pd.read_csv('C:/Users/gabri/datasets/tracker_ophelia2.csv', sep=';')

# Carregar o arquivo NetCDF
ds1 = xr.open_dataset("C:/Users/gabri/datasets/verticalV.nc")
ds2 = xr.open_dataset("C:/Users/gabri/datasets/divergence.nc")

# Definir as variáveis
w = ds1['w']
d = ds2['d']

# Conversão de unidades
d = d*1e4

for index, row in df.iterrows():
    # Extrair informações específicas. Por exemplo, para obter a velocidade vertical em uma localização e hora específicas:
    latitude = row['Lat']  # Latitude
    longitude = row['Lon']  # Longitude
    time_index = pd.to_datetime(row['Date'] + ' ' + row['Time'])  # Escolha o dia e horário
    w_specific = w.sel(latitude=latitude, longitude=longitude, time=time_index, method='nearest') # Variável 1  
    d_specific = d.sel(latitude=latitude, longitude=longitude, time=time_index, method='nearest') # Variável 2  

    # Plot do gráfico do perfil vertical da atmosfera para as variáveis. (Gráfico de dispersão)
    fig, axs = plt.subplots(1, 2, figsize=(16, 13)) # Tamanho da figura
    
    # Gráfico para a primeira variável
    
    # Elementos do gráfico
    axs[0].semilogy(w_specific, w_specific['level'], linestyle='--', marker='o', label='line with marker', color='b')
    axs[0].grid(True)
    axs[0].axvline(0, color='r')
    
    # Títulos e legendas
    axs[0].set_title(f'Ômega em ({latitude}, {longitude}) - {time_index}', fontsize='16')
    axs[0].set_ylabel('Níveis de pressão (hPa)', fontsize='16')
    axs[0].set_xlabel('Ômega (Pa/s)', fontsize='16')

    # Trocar a formatação log para semilog
    axs[0].yaxis.set_major_formatter(ScalarFormatter())
    axs[0].yaxis.set_minor_formatter(NullFormatter())
    axs[0].set_yticks(np.linspace(100, 1000, 10))
    axs[0].tick_params(axis='both', which='major', labelsize=15)
    axs[0].set_xticks(np.linspace(-3.0, 3.0, 9))
    axs[0].set_ylim(1000, 100)
    axs[0].set_xlim(-3, 3)
    axs[0].xaxis.set_major_locator(MultipleLocator(1)) # Ajusta o localizador do eixo x para mostrar a escala
    
    # Gráfico para a segunda variável
    
    # Elementos do gráfico
    axs[1].semilogy(d_specific, d_specific['level'], linestyle='--', marker='o', label='line with marker', color='b')
    axs[1].grid(True)
    axs[1].axvline(0, color='r')
    
    # Títulos e legendas
    axs[1].set_title(f'Divergência em ({latitude}, {longitude}) - {time_index}',fontsize='16')
    axs[1].set_xlabel('Divergência (s-1) * 10^4', fontsize='16')
    axs[1].set_ylabel('Níveis de pressão (hPa)', fontsize='16')
    
    # Trocar a formatação log para semilog
    axs[1].yaxis.set_major_formatter(ScalarFormatter())
    axs[1].yaxis.set_minor_formatter(NullFormatter())
    axs[1].set_yticks(np.linspace(100, 1000, 10))
    axs[1].set_xticks(np.linspace(-3.0, 3.0, 9))
    axs[1].tick_params(axis='both', which='major', labelsize=15)
    axs[1].set_ylim(1000, 100)
    axs[1].set_xlim(-3, 3)
    axs[1].xaxis.set_major_locator(MultipleLocator(1)) # Ajusta o localizador do eixo x para mostrar a escala

    plt.show()
    