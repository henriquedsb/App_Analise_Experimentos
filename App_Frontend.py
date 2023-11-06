import customtkinter as ctk
from App_Backend import Backend
from customtkinter import filedialog
import os

class DataAnalysisApp(ctk.CTk, Backend):
    def __init__(self):
        super().__init__()
        self.configurar_tela()
        self.Velocidades_acelerometro_01 = []
        self.Velocidades_acelerometro_02 = []
        self.Velocidades_acelerometro_03 = []
        self.Velocidades_acelerometro_04 = []
        self.lista_graficos = []
        self.index_lista_graficos = 0
        self.lista_nome_arquivo = []
        self.index_lista_nomes = 0
        self.mainpage()

    def configurar_tela(self):
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('dark-blue')
        self.title('Analise dos Experimentos')
        self.geometry('770x500')
        self.resizable(True, True)

    def mainpage(self):
        self.frame_01 = ctk.CTkFrame(self)
        self.frame_01.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.10)
        
        self.frame_02 = ctk.CTkFrame(self)
        self.frame_02.place(relx=0.02, rely=0.15, relwidth=0.5, relheight=0.82)

        self.frame_03 = ctk.CTkFrame(self)
        self.frame_03.place(relx=0.5, rely=0.15, relwidth=0.48, relheight=0.82)

        self.texto_01 = ctk.CTkLabel(self.frame_01, text='Análise de Dados Experimentais')
        self.texto_01.place(relx=0.4, rely=0.1, relwidth=0.25, relheight=0.30)

        self.selecionar_pasta_button = ctk.CTkButton(self.frame_01, text="Selecionar Pasta", command=self.selecionar_pasta)
        self.selecionar_pasta_button.place(relx=0.425, rely=0.4, relwidth=0.2, relheight=0.45)
        
        self.resultado = ctk.CTkLabel(self.frame_02, text='', justify='left')
        self.resultado.place(relx=0.02, rely=0.02, relwidth=0.7, relheight=0.95)

        self.nome_arquivo_label = ctk.CTkLabel(self.frame_03, text='', justify='left')
        self.nome_arquivo_label.place(relx=0.02, rely=0.03, relwidth=0.3, relheight=0.05)
    
        self.grafico = ctk.CTkLabel(self.frame_03, text='', justify='left')
        self.grafico.place(relx=0.02, rely=0.09, relwidth=0.96, relheight=0.86)

        self.avancar = ctk.CTkButton(self.frame_03, text="Avançar", command=self.botao_avancar)
        self.avancar.place(relx=0.78, rely=0.95, relwidth=0.2, relheight=0.05)

        self.voltar = ctk.CTkButton(self.frame_03, text="Voltar", command=self.botao_voltar)
        self.voltar.place(relx=0.02, rely=0.95, relwidth=0.2, relheight=0.05)

    def selecionar_pasta(self):
        
        self.pasta = filedialog.askdirectory()
        self.processar_dados()
        resultado = (
            self.Inferencia_estatistica()
        )
        self.resultado.configure(text=resultado)
        self.mostrar_grafico()

    def limpar_dados(self):
        self.Velocidades_acelerometro_01 = []
        self.Velocidades_acelerometro_02 = []
        self.Velocidades_acelerometro_03 = []
        self.Velocidades_acelerometro_04 = []
        self.lista_graficos = []
        self.index_lista_graficos = 0
        self.lista_nome_arquivo = []
        self.index_lista_nomes = 0

    def mostrar_grafico(self):
        imagem_atual = self.lista_graficos[self.index_lista_graficos]
        self.grafico.configure(image=imagem_atual)
        self.grafico.image = imagem_atual

        nome_pasta_atual = os.path.basename(self.pasta)
        
        nome_arquivo_atual = self.lista_nome_arquivo[self.index_lista_nomes]
        self.nome_arquivo_label.configure(text=f"Arquivo: {nome_pasta_atual}/{nome_arquivo_atual}")

    def botao_avancar(self):
        self.index_lista_graficos += 1
        self.index_lista_nomes += 1
        if self.index_lista_graficos >= len(self.lista_graficos):
            self.index_lista_graficos = 0
        if self.index_lista_nomes >= len(self.lista_nome_arquivo):
            self.index_lista_nomes = 0

        self.mostrar_grafico()
    
    def botao_voltar(self):
        self.index_lista_graficos -= 1
        self.index_lista_nomes -= 1
        if self.index_lista_graficos < 0:
            self.index_lista_graficos = len(self.lista_graficos) - 1
        if self.index_lista_nomes < 0:
            self.index_lista_nomes = len(self.lista_nome_arquivo) - 1

        self.mostrar_grafico()

if __name__ == "__main__":
    app = DataAnalysisApp()
    app.mainloop()
