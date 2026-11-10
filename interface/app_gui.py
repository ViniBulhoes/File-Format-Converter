import customtkinter as ctk
from tkinter import filedialog
import os
import threading
import time
from PIL import Image
from conversores.docx_pdf import processar_docx
from conversores.pdf_docx import processar_pdf
from conversores.texto_pdf import processar_texto

class ConversorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("File Forge - Conversor")
        self.geometry("800x550")
        ctk.set_appearance_mode("dark")
        
        # O fundo geral da aplicação será um tom muito escuro, semelhante à imagem
        self.configure(fg_color="#0f1115") 
        
        # Lista para guardar referências dos ficheiros e dos seus widgets (barra e percentagem)
        self.arquivos_na_fila = []
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # === SIDEBAR (Esquerda) ===
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#18181b")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1) 
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="File Forge", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 40))
        
        self.lbl_modo = ctk.CTkLabel(self.sidebar_frame, text="Modo de Conversão", font=ctk.CTkFont(size=13, weight="bold"), text_color="#9ca3af")
        self.lbl_modo.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")
        
        self.radio_var = ctk.StringVar(value="docx2pdf")
        
        self.radio_btn1 = ctk.CTkRadioButton(self.sidebar_frame, text="Word para PDF", variable=self.radio_var, value="docx2pdf", hover_color="#2dd4bf")
        self.radio_btn1.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        self.radio_btn2 = ctk.CTkRadioButton(self.sidebar_frame, text="Texto para PDF", variable=self.radio_var, value="txt2pdf", hover_color="#2dd4bf")
        self.radio_btn2.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        
        self.radio_btn3 = ctk.CTkRadioButton(self.sidebar_frame, text="PDF para Word", variable=self.radio_var, value="pdf2docx", hover_color="#2dd4bf")
        self.radio_btn3.grid(row=4, column=0, padx=20, pady=10, sticky="nw")

        # === ÁREA PRINCIPAL (Direita) ===
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)
        
        self.main_frame.grid_rowconfigure(1, weight=1) 
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Cabeçalho da área principal
        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.lbl_status = ctk.CTkLabel(self.header_frame, text="Aguardando ficheiros...", font=ctk.CTkFont(size=18, weight="bold"))
        self.lbl_status.grid(row=0, column=0, sticky="w")

        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        pasta_assets = os.path.join(os.path.dirname(diretorio_atual), "assets")
        
        # ATENÇÃO: Troque "pasta.png" pelo nome exato do arquivo que você baixou
        caminho_icone_pasta = os.path.join(pasta_assets, "folder.png") 
        
        try:
            img_pasta = Image.open(caminho_icone_pasta)
            icone_pasta = ctk.CTkImage(light_image=img_pasta, dark_image=img_pasta, size=(20, 20))
        except FileNotFoundError:
            icone_pasta = None

        self.btn_selecionar = ctk.CTkButton(
            self.header_frame, 
            text=" Adicionar", 
            image=icone_pasta,
            command=self.selecionar_arquivos, 
            width=120,
            fg_color="#374151",
            hover_color="#4b5563"
        )
        self.btn_selecionar.grid(row=0, column=1, sticky="e")
        
        # Lista de Ficheiros (Scrollable Frame estilo "Card" escuro)
        self.scroll_arquivos = ctk.CTkScrollableFrame(self.main_frame, fg_color="#18181b", corner_radius=10)
        self.scroll_arquivos.grid(row=1, column=0, sticky="nsew", pady=(0, 20))
        
        # Rodapé
        self.btn_converter = ctk.CTkButton(
            self.main_frame, 
            text="Iniciar Conversão", 
            command=self.iniciar_conversao, 
            height=45, 
            fg_color="#2dd4bf", # Teal/Ciano da barra
            text_color="#0f1115",
            hover_color="#14b8a6", 
            font=ctk.CTkFont(size=15, weight="bold")
        )
        self.btn_converter.grid(row=2, column=0, sticky="ew")

    def selecionar_arquivos(self):
        arquivos = filedialog.askopenfilenames(
            title="Selecione os ficheiros",
            filetypes=[("Ficheiros Suportados", "*.docx *.pdf *.md *.txt"), ("Todos", "*.*")]
        )
        for arq in arquivos:
            self.adicionar_linha_arquivo(arq)
            
        if self.arquivos_na_fila:
            self.lbl_status.configure(text=f"Enviando {len(self.arquivos_na_fila)} ficheiros")

    def adicionar_linha_arquivo(self, caminho_arquivo):
        nome = os.path.basename(caminho_arquivo)
        extensao = os.path.splitext(nome)[1].lower()
        
        # Mapeia a extensão para o nome do arquivo PNG
        mapa_icones = {
            ".pdf": "pdf.png",
            ".docx": "docx.png",
            ".txt": "txt.png",
            ".md": "md.png"
        }
        
        nome_arquivo_icone = mapa_icones.get(extensao, "default.png")
        
        # Constrói o caminho dinâmico para a pasta assets
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        pasta_assets = os.path.join(os.path.dirname(diretorio_atual), "assets")
        caminho_icone = os.path.join(pasta_assets, nome_arquivo_icone)
        
        linha_frame = ctk.CTkFrame(self.scroll_arquivos, fg_color="transparent")
        linha_frame.pack(fill="x", pady=12, padx=10)
        linha_frame.grid_columnconfigure(1, weight=1) 
        
        # Tenta carregar a imagem. Se você ainda não tiver colocado o PNG na pasta,
        # ele usa um emoji de fallback para o programa não quebrar.
        try:
            icone_img = ctk.CTkImage(
                light_image=Image.open(caminho_icone),
                dark_image=Image.open(caminho_icone),
                size=(28, 28) # Tamanho do ícone
            )
            lbl_icone = ctk.CTkLabel(linha_frame, text="", image=icone_img)
        except FileNotFoundError:
            lbl_icone = ctk.CTkLabel(linha_frame, text="📄", font=ctk.CTkFont(size=28), text_color="#9ca3af")
            
        lbl_icone.grid(row=0, column=0, rowspan=2, sticky="w", padx=(0, 15))
        
        # Nome do Arquivo
        lbl_nome = ctk.CTkLabel(linha_frame, text=nome, font=ctk.CTkFont(size=14, weight="bold"), text_color="#f1f5f9")
        lbl_nome.grid(row=0, column=1, sticky="w", pady=(0, 5))
        
        # Barra de Progresso
        barra = ctk.CTkProgressBar(linha_frame, height=6, fg_color="#1f2937", progress_color="#2dd4bf")
        barra.grid(row=1, column=1, sticky="ew", pady=(0, 0))
        barra.set(0) 
        
        # Percentagem
        lbl_pct = ctk.CTkLabel(linha_frame, text="0%", font=ctk.CTkFont(size=12, family="monospace"), text_color="#9ca3af")
        lbl_pct.grid(row=0, column=2, rowspan=2, sticky="e", padx=(15, 0))
        
        self.arquivos_na_fila.append({
            "caminho": caminho_arquivo,
            "barra": barra,
            "label_pct": lbl_pct
        })

    def iniciar_conversao(self):
        if not self.arquivos_na_fila:
            return
        
        # Desativa os botões para evitar duplo clique
        self.btn_converter.configure(state="disabled", text="A converter...")
        self.btn_selecionar.configure(state="disabled")
        
        # Cria uma thread secundária para não congelar a interface
        thread = threading.Thread(target=self._processar_conversao)
        thread.start()

    def _processar_conversao(self):
        total = len(self.arquivos_na_fila)
        modo_selecionado = self.radio_var.get()
        
        for index, item in enumerate(self.arquivos_na_fila):
            caminho = item["caminho"]
            barra = item["barra"]
            label_pct = item["label_pct"]
            
            self.lbl_status.configure(text=f"A converter... ({index + 1} de {total})")
            
            # Atualiza interface visualmente para "Processando" (50%)
            barra.set(0.5)
            label_pct.configure(text="50%")
            
            sucesso = False
            resultado = "Arquivo incompatível com o modo selecionado."
            
            # Roteamento baseado no modo escolhido no painel esquerdo
            if modo_selecionado == "docx2pdf" and caminho.lower().endswith(".docx"):
                sucesso, resultado = processar_docx(caminho)

            elif modo_selecionado == "pdf2docx" and caminho.lower().endswith(".pdf"):
                sucesso, resultado = processar_pdf(caminho)

            elif modo_selecionado == "txt2pdf" and caminho.lower().endswith((".txt", ".md")):
                sucesso, resultado = processar_texto(caminho)
            
            if sucesso:
                barra.set(1.0)
                label_pct.configure(text="100%", text_color="#2dd4bf") # Fica verde ao concluir
            else:
                barra.set(1.0)
                barra.configure(progress_color="#ef4444") # Fica vermelho se der erro
                label_pct.configure(text="ERRO", text_color="#ef4444")
                print(f"[ERRO] Falha ao converter {caminho}")
                print(f"[DETALHE] {resultado}")
        
        # --- NOVO FINAL DA FUNÇÃO ---
        self.lbl_status.configure(text="Conversão concluída!")
        self.btn_selecionar.configure(state="normal")
        
        # Altera o botão para executar a limpeza visual da tela
        self.btn_converter.configure(
            state="normal", 
            text="Limpar Fila e Nova Conversão", 
            command=self.resetar_interface
        )
        
        self.arquivos_na_fila.clear()

    # --- NOVA FUNÇÃO (Coloque logo abaixo do _processar_conversao) ---
    def resetar_interface(self):
        """ Limpa os arquivos visuais da tela e restaura o botão original """
        for widget in self.scroll_arquivos.winfo_children():
            widget.destroy()
            
        self.lbl_status.configure(text="Aguardando ficheiros...")
        
        self.btn_converter.configure(
            text="Iniciar Conversão", 
            command=self.iniciar_conversao
        )