# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 22:49:42 2023

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
ds = xr.open_dataset("C:/Users/gabri/datasets/divergence.nc")

# Definir as variáveis
d = ds['d']

# Conversão de unidades
d = d*1e4

for index, row in df.iterrows():
    # Extrair informações específicas. Por exemplo, para obter a velocidade vertical em uma localização e hora específicas:
    latitude = row['Lat']  # Latitude
    longitude = row['Lon']  # Longitude
    time_index = pd.to_datetime(row['Date'] + ' ' + row['Time'])  # Escolha o dia e horário
    d_specific = d.sel(latitude=latitude, longitude=longitude, time=time_index, method='nearest')
    
    # Plot do gráfico do perfil vertical da atmosfera para as variáveis. (Gráfico de dispersão)
    fig, axs = plt.subplots(1, figsize=(10,13)) # Tamanho da figura
    
    # Elementos do gráfico
    axs.semilogy(d_specific, d_specific['level'], linestyle='--', marker='o', label='line with marker', color='b')
    axs.grid(True)
    axs.axvline(0, color='r')
    
    # Títulos e legendas
    axs.set_title(f'Divergência em ({latitude}, {longitude}) - {time_index}', fontsize='16')
    axs.set_ylabel('Níveis de pressão (hPa)', fontsize='16')
    axs.set_xlabel('Divergência (Pa/s)', fontsize='16')

    # Trocar a formatação log para semilog
    axs.yaxis.set_major_formatter(ScalarFormatter())
    axs.yaxis.set_minor_formatter(NullFormatter())
    axs.set_yticks(np.linspace(100, 1000, 10))
    axs.tick_params(axis='both', which='major', labelsize=15)
    axs.set_xticks(np.linspace(-3.0, 3.0, 9))
    axs.set_ylim(1000, 100)
    axs.set_xlim(-3, 3)
    axs.xaxis.set_major_locator(MultipleLocator(1)) # Ajusta o localizador do eixo x para mostrar a escala
    
    plt.show()