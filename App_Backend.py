from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import tkinter as tk
import pandas as pd
import numpy as np
import os
import io

class Backend():
    def processar_dados(self, n=10.0, limite_derivada=100):
        for arquivo in os.listdir(self.pasta):
            caminho_completo = os.path.join(self.pasta, arquivo)
            self.lista_nome_arquivo.append(arquivo)
            if arquivo.lower().endswith('.csv'):
                dataframe = pd.read_csv(caminho_completo)
                self.dados = dataframe.values
            elif arquivo.lower().endswith('.txt'):
                dataframe = pd.read_fwf(caminho_completo)
                self.dados = dataframe.values
            elif arquivo.lower().endswith(('.xlsx')):
                dataframe = pd.read_excel(caminho_completo)
                self.dados = dataframe.values
            else:
                raise ValueError('Selecione uma pasta com arquivos suportados.')
            
            self.tempo_acelerometro_01 = []
            self.tempo_acelerometro_02 = []
            self.tempo_acelerometro_03 = []
            self.tempo_acelerometro_04 = []
            self.sinal_acelerometro_01 = []
            self.sinal_acelerometro_02 = []
            self.sinal_acelerometro_03 = []
            self.sinal_acelerometro_04 = []

            for i in range(len(self.dados)):
                if self.dados[i][1]:
                    self.sinal_acelerometro_01.append(self.dados[i][1])
                    self.tempo_acelerometro_01.append(self.dados[i][0])
                if self.dados[i][2]:
                    self.sinal_acelerometro_02.append(self.dados[i][2])
                    self.tempo_acelerometro_02.append(self.dados[i][0])
                if self.dados[i][3]:
                    self.sinal_acelerometro_03.append(self.dados[i][3])
                    self.tempo_acelerometro_03.append(self.dados[i][0])
                if self.dados[i][4]:
                    self.sinal_acelerometro_04.append(self.dados[i][4])
                    self.tempo_acelerometro_04.append(self.dados[i][0])

            pico_acelerometro_01 = max(self.sinal_acelerometro_01)
            pico_acelerometro_02 = max(self.sinal_acelerometro_02)
            pico_acelerometro_03 = max(self.sinal_acelerometro_03)
            pico_acelerometro_04 = max(self.sinal_acelerometro_04)

            self.tempo_tratado_acelerometro_01 = []
            self.tempo_tratado_acelerometro_02 = []
            self.tempo_tratado_acelerometro_03 = []
            self.tempo_tratado_acelerometro_04 = []
            self.sinal_tratado_acelerometro_01 = []
            self.sinal_tratado_acelerometro_02 = []
            self.sinal_tratado_acelerometro_03 = []
            self.sinal_tratado_acelerometro_04 = []

            for i in range(1, len(self.dados)):
                if self.sinal_acelerometro_01[i] > n and abs(self.sinal_acelerometro_01[i] - self.sinal_acelerometro_01[i-1]) > limite_derivada:
                    self.sinal_tratado_acelerometro_01.append(self.sinal_acelerometro_01[i])
                    self.tempo_tratado_acelerometro_01.append(self.tempo_acelerometro_01[i])
                    if pico_acelerometro_01 in self.sinal_tratado_acelerometro_01:
                        break

                if self.sinal_acelerometro_02[i] > n and abs(self.sinal_acelerometro_02[i] - self.sinal_acelerometro_02[i-1]) > limite_derivada:
                    self.sinal_tratado_acelerometro_02.append(self.sinal_acelerometro_02[i])
                    self.tempo_tratado_acelerometro_02.append(self.tempo_acelerometro_02[i])
                    if pico_acelerometro_02 in self.sinal_tratado_acelerometro_02:
                        break

                if self.sinal_acelerometro_03[i] > n and abs(self.sinal_acelerometro_03[i] - self.sinal_acelerometro_03[i-1]) > limite_derivada:
                    self.sinal_tratado_acelerometro_03.append(self.sinal_acelerometro_03[i])
                    self.tempo_tratado_acelerometro_03.append(self.tempo_acelerometro_03[i])
                    if pico_acelerometro_03 in self.sinal_tratado_acelerometro_03:
                        break

                if self.sinal_acelerometro_04[i] > n and abs(self.sinal_acelerometro_04[i] - self.sinal_acelerometro_04[i-1]) > limite_derivada:
                    self.sinal_tratado_acelerometro_04.append(self.sinal_acelerometro_04[i])
                    self.tempo_tratado_acelerometro_04.append(self.tempo_acelerometro_04[i])
                    if pico_acelerometro_04 in self.sinal_tratado_acelerometro_04:
                        break

            integral_01 = np.trapz(self.sinal_tratado_acelerometro_01, self.tempo_tratado_acelerometro_01)
            self.Velocidades_acelerometro_01.append(integral_01)
            
            integral_02 = np.trapz(self.sinal_tratado_acelerometro_02, self.tempo_tratado_acelerometro_02)
            self.Velocidades_acelerometro_02.append(integral_02)
            
            integral_03 = np.trapz(self.sinal_tratado_acelerometro_03, self.tempo_tratado_acelerometro_03)
            self.Velocidades_acelerometro_03.append(integral_03)
            
            integral_04 = np.trapz(self.sinal_tratado_acelerometro_04, self.tempo_tratado_acelerometro_04)
            self.Velocidades_acelerometro_04.append(integral_04)

            self.plotar_graficos()
        
    def plotar_graficos(self):
        fig = plt.figure(figsize=(6, 9), facecolor='#BEBEBE', frameon=False, clear=True)
        # Criação da figura e eixos
        fig, (ax1, ax2) = plt.subplots(2, 1)
        #ax1.set_facecolor('#BEBEBE')
        ax1.plot(self.tempo_acelerometro_01, self.sinal_acelerometro_01, label='Acelerômetro 1')
        ax1.plot(self.tempo_acelerometro_02, self.sinal_acelerometro_02, label='Acelerômetro 2')
        ax1.plot(self.tempo_acelerometro_03, self.sinal_acelerometro_03, label='Acelerômetro 3')
        ax1.plot(self.tempo_acelerometro_04, self.sinal_acelerometro_04, label='Acelerômetro 4')
        ax1.set_title("Dados sem Análise")
        ax1.legend(fontsize='small')
        ax1.set_xlabel('Tempo')
        ax1.set_ylabel('Sinal do Acelerômetro')

        #ax2.set_facecolor('#BEBEBE')
        ax2.plot(self.tempo_tratado_acelerometro_01, self.sinal_tratado_acelerometro_01, label='Acelerômetro 1')
        ax2.plot(self.tempo_tratado_acelerometro_02, self.sinal_tratado_acelerometro_02, label='Acelerômetro 2')
        ax2.plot(self.tempo_tratado_acelerometro_03, self.sinal_tratado_acelerometro_03, label='Acelerômetro 3')
        ax2.plot(self.tempo_tratado_acelerometro_04, self.sinal_tratado_acelerometro_04, label='Acelerômetro 4')
        ax2.set_title("Dados com Análise")
        ax2.legend(fontsize='small')
        ax2.set_xlabel('Tempo')
        ax2.set_ylabel('Sinal do Acelerômetro')

        plt.tight_layout()  # Ajusta o layout para evitar sobreposição

        # Converte a figura para uma imagem
        imagem = self.figura_para_imagem(fig)
        self.lista_graficos.append(imagem)

    def figura_para_imagem(self, figura):
        buffer = io.BytesIO()
        figura.savefig(buffer, format="png")
        buffer.seek(0)
        imagem = tk.PhotoImage(data=buffer.getvalue())
        return imagem

    def Inferencia_estatistica(self):
        resultados = []

        for i, velocidades in enumerate([
            self.Velocidades_acelerometro_01,
            self.Velocidades_acelerometro_02,
            self.Velocidades_acelerometro_03,
            self.Velocidades_acelerometro_04
        ], start=1):
            resultado = f"Inferência Estatística para o Acelerômetro {i}\n"
            resultado += f'Velocidades: {", ".join(f"{v:.4f}" for v in velocidades)}\n'
            resultado += f"Média: {np.mean(velocidades):.3f}\n"
            resultado += f"Mediana: {np.median(velocidades):.3f}\n"
            resultado += f"Variância: {np.var(velocidades):.3f}\n"
            resultado += f"Desvio Padrão: {np.std(velocidades):.3f}\n"
            resultado += f"Valor Máximo: {np.amax(velocidades):.3f}\n"
            resultado += f"Valor Mínimo: {np.amin(velocidades):.3f}\n\n"
            resultados.append(resultado)

        return "\n".join(resultados)