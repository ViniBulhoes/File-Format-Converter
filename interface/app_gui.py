import customtkinter as ctk
from tkinter import filedialog
import os
import threading
from PIL import Image
from tkinterdnd2 import TkinterDnD, DND_FILES

from conversores.docx_pdf import processar_docx
from conversores.pdf_docx import processar_pdf
from conversores.texto_pdf import processar_texto
from conversores.mesclar_pdf import processar_mesclagem
from conversores.img_pdf import processar_imagem
from conversores.dividir_pdf import processar_divisao
from conversores.comprimir_pdf import processar_compressao

class TkinterDnD_CTk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

class ConversorApp(TkinterDnD_CTk):
    def __init__(self):
        super().__init__()
        
        self.title("File Forge - Studio")
        self.geometry("940x640")
        self.minsize(850, 580)
        
        # --- PALETA NORD / DEEP OCEAN (Confortável e Profissional) ---
        ctk.set_appearance_mode("dark")
        self.bg_root = "#141820"        # Fundo geral
        self.bg_panel = "#1d232f"       # Painéis principais
        self.bg_card = "#262e3d"        # Cards e itens da lista
        self.bg_card_hover = "#303a4d"  # Hover dos cards
        self.border_subtle = "#2e3846"  # Bordas discretas
        
        self.accent = "#38bdf8"         # Azul Celeste vibrante
        self.accent_hover = "#0284c7"   # Azul mais fechado no hover
        self.accent_glow = "#162a3d"    # Fundo suave quando selecionado/arrastando
        
        self.text_primary = "#f1f5f9"   # Branco suave
        self.text_secondary = "#94a3b8" # Cinza azulado
        self.success = "#34d399"        # Verde menta
        self.danger = "#f87171"         # Vermelho suave
        
        self.configure(fg_color=self.bg_root)
        
        self.arquivos_na_fila = []
        self.modo_selecionado = "to_pdf"
        self.botoes_ferramentas = {}
        
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        self.pasta_assets = os.path.join(os.path.dirname(diretorio_atual), "assets")
        
        # Grid Principal (2 Colunas com espaçamento elegante)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0) # Coluna Esquerda (Fixa)
        self.grid_columnconfigure(1, weight=1) # Coluna Direita (Expansível)
        
        # =========================================================
        # COLUNA ESQUERDA: PAINEL DE FERRAMENTAS E AÇÃO
        # =========================================================
        self.left_panel = ctk.CTkFrame(
            self, width=310, fg_color=self.bg_panel, corner_radius=16, 
            border_width=1, border_color=self.border_subtle
        )
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        self.left_panel.grid_propagate(False)
        self.left_panel.grid_rowconfigure(7, weight=1) # Empurra o botão de ação para o rodapé
        self.left_panel.grid_columnconfigure(0, weight=1)
        
        # Header da Marca
        self.brand_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.brand_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(22, 18))
        
        self.lbl_logo = ctk.CTkLabel(
            self.brand_frame, text="⚡ File Forge", 
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"), text_color=self.text_primary
        )
        self.lbl_logo.pack(anchor="w")
        
        self.lbl_sub = ctk.CTkLabel(
            self.brand_frame, text="Selecione a operação desejada", 
            font=ctk.CTkFont(family="Segoe UI", size=12), text_color=self.text_secondary
        )
        self.lbl_sub.pack(anchor="w", pady=(2, 0))
        
        # Lista de Ferramentas (Cards Clicáveis em vez de RadioButtons)
        ferramentas = [
            ("to_pdf", "📄  Converter para PDF", "Word, Imagens, TXT e MD"),
            ("pdf2docx", "📝  PDF para Word", "Extrai texto editável (.docx)"),
            ("merge_pdf", "🔗  Mesclar PDFs", "Une vários PDFs em um só"),
            ("split_pdf", "✂️  Dividir / Extrair PDF", "Separa páginas ou intervalos"),
            ("compress_pdf", "🗜️  Comprimir PDF", "Reduz o tamanho do arquivo")
        ]
        
        for idx, (chave, titulo, desc) in enumerate(ferramentas, start=1):
            btn_card = ctk.CTkButton(
                self.left_panel,
                text=f"{titulo}\n{desc}",
                anchor="w",
                height=54,
                corner_radius=10,
                font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
                fg_color=self.bg_card,
                hover_color=self.bg_card_hover,
                text_color=self.text_primary,
                border_width=2,
                border_color=self.bg_card,
                command=lambda k=chave: self.selecionar_ferramenta(k)
            )
            btn_card.grid(row=idx, column=0, sticky="ew", padx=16, pady=4)
            self.botoes_ferramentas[chave] = btn_card
            
        # Box Condicional: Intervalo de Páginas (Aparece apenas em Dividir PDF)
        self.frame_opcoes_split = ctk.CTkFrame(self.left_panel, fg_color=self.bg_root, corner_radius=10, border_width=1, border_color=self.border_subtle)
        self.frame_opcoes_split.grid(row=6, column=0, sticky="ew", padx=16, pady=(6, 0))
        self.frame_opcoes_split.grid_columnconfigure(0, weight=1)
        
        self.lbl_dica = ctk.CTkLabel(
            self.frame_opcoes_split, text="Intervalo (vazio = todas separadas):", 
            font=ctk.CTkFont(family="Segoe UI", size=11), text_color=self.text_secondary
        )
        self.lbl_dica.grid(row=0, column=0, sticky="w", padx=12, pady=(8, 2))
        
        self.entry_paginas = ctk.CTkEntry(
            self.frame_opcoes_split, placeholder_text="Ex: 1, 3, 5-10", height=32,
            fg_color=self.bg_panel, border_color=self.border_subtle, text_color=self.text_primary
        )
        self.entry_paginas.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 10))
        self.frame_opcoes_split.grid_remove() # Inicia oculto
        
        # Botão Principal de Ação (Ancorado embaixo na esquerda)
        self.btn_converter = ctk.CTkButton(
            self.left_panel, text="Iniciar Processamento", command=self.iniciar_conversao,
            height=48, corner_radius=10, font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            fg_color=self.bg_card, text_color=self.text_secondary, state="disabled"
        )
        self.btn_converter.grid(row=8, column=0, sticky="ew", padx=16, pady=18)

        # =========================================================
        # COLUNA DIREITA: FILA DE ARQUIVOS (CIMA) E DROP ZONE (BAIXO)
        # =========================================================
        self.right_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
        self.right_panel.grid_rowconfigure(1, weight=1) # Fila expande todo o espaço livre
        self.right_panel.grid_columnconfigure(0, weight=1)
        
        # 1. Cabeçalho da Fila
        self.queue_header = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        self.queue_header.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.queue_header.grid_columnconfigure(0, weight=1)
        
        self.lbl_status = ctk.CTkLabel(
            self.queue_header, text="Fila de Processamento", 
            font=ctk.CTkFont(family="Segoe UI", size=17, weight="bold"), text_color=self.text_primary
        )
        self.lbl_status.grid(row=0, column=0, sticky="w")
        
        self.badge_contador = ctk.CTkLabel(
            self.queue_header, text="0 arquivos", fg_color=self.bg_panel, corner_radius=12,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), text_color=self.accent,
            padx=12, pady=4
        )
        self.badge_contador.grid(row=0, column=1, sticky="e", padx=(0, 8))
        
        self.btn_limpar = ctk.CTkButton(
            self.queue_header, text="Limpar", width=70, height=28, corner_radius=8,
            fg_color=self.bg_panel, hover_color="#3f1d28", text_color=self.danger,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            command=self.resetar_interface
        )
        self.btn_limpar.grid(row=0, column=2, sticky="e")
        
        # 2. Área da Fila (Em cima)
        self.container_fila = ctk.CTkFrame(
            self.right_panel, fg_color=self.bg_panel, corner_radius=16, 
            border_width=1, border_color=self.border_subtle
        )
        self.container_fila.grid(row=1, column=0, sticky="nsew", pady=(0, 14))
        self.container_fila.grid_rowconfigure(0, weight=1)
        self.container_fila.grid_columnconfigure(0, weight=1)
        
        self.lbl_fila_vazia = ctk.CTkLabel(
            self.container_fila, text="Nenhum arquivo na fila ainda.\nUse a zona abaixo para adicionar seus documentos.",
            font=ctk.CTkFont(family="Segoe UI", size=14), text_color=self.text_secondary, justify="center"
        )
        self.lbl_fila_vazia.grid(row=0, column=0)
        
        self.scroll_arquivos = ctk.CTkScrollableFrame(
            self.container_fila, fg_color="transparent", corner_radius=12
        )
        
        # 3. Drop Zone / Botão de Adicionar (Ancorado na parte inferior direita)
        self.drop_zone = ctk.CTkFrame(
            self.right_panel, height=110, fg_color=self.bg_panel, corner_radius=16,
            border_width=2, border_color=self.border_subtle
        )
        self.drop_zone.grid(row=2, column=0, sticky="ew")
        self.drop_zone.grid_propagate(False)
        self.drop_zone.grid_rowconfigure(0, weight=1)
        self.drop_zone.grid_columnconfigure(0, weight=1)
        
        self.drop_inner = ctk.CTkFrame(self.drop_zone, fg_color="transparent")
        self.drop_inner.grid(row=0, column=0)
        
        self.lbl_drop_titulo = ctk.CTkLabel(
            self.drop_inner, text="📥  Arraste e solte seus arquivos aqui", 
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"), text_color=self.text_primary
        )
        self.lbl_drop_titulo.pack()
        
        self.lbl_drop_sub = ctk.CTkLabel(
            self.drop_inner, text="ou clique nesta área para procurar no computador (PDF, DOCX, TXT, MD, PNG, JPG)", 
            font=ctk.CTkFont(family="Segoe UI", size=12), text_color=self.text_secondary
        )
        self.lbl_drop_sub.pack(pady=(2, 0))
        
        # Binds de clique na Drop Zone
        for widget in (self.drop_zone, self.drop_inner, self.lbl_drop_titulo, self.lbl_drop_sub):
            widget.bind("<Button-1>", lambda e: self.selecionar_arquivos())
            
        # Registro do Drag & Drop
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<DropEnter>>', self.ao_entrar_drag)
        self.dnd_bind('<<DropLeave>>', self.ao_sair_drag)
        self.dnd_bind('<<Drop>>', self.processar_arquivos_arrastados)
        
        # Ativa visualmente a primeira ferramenta por padrão
        self.selecionar_ferramenta("to_pdf")

    # =========================================================
    # CONTROLE DE ESTADO E INTERAÇÃO VISUAL
    # =========================================================
    def selecionar_ferramenta(self, chave_modo):
        self.modo_selecionado = chave_modo
        
        for chave, botao in self.botoes_ferramentas.items():
            if chave == chave_modo:
                botao.configure(fg_color=self.accent_glow, border_color=self.accent, text_color="#ffffff")
            else:
                botao.configure(fg_color=self.bg_card, border_color=self.bg_card, text_color=self.text_primary)
                
        if chave_modo == "split_pdf":
            self.frame_opcoes_split.grid()
        else:
            self.frame_opcoes_split.grid_remove()
            
        self.atualizar_icones_destino()

    def ao_entrar_drag(self, event):
        self.drop_zone.configure(border_color=self.accent, fg_color=self.accent_glow)
        self.lbl_drop_titulo.configure(text="✨  Solte agora para adicionar à fila!", text_color=self.accent)
        self.lbl_drop_sub.configure(text="Arquivos prontos para importação", text_color=self.text_primary)

    def ao_sair_drag(self, event):
        self.drop_zone.configure(border_color=self.border_subtle, fg_color=self.bg_panel)
        self.lbl_drop_titulo.configure(text="📥  Arraste e solte seus arquivos aqui", text_color=self.text_primary)
        self.lbl_drop_sub.configure(text="ou clique nesta área para procurar no computador (PDF, DOCX, TXT, MD, PNG, JPG)", text_color=self.text_secondary)

    def processar_arquivos_arrastados(self, event):
        self.ao_sair_drag(None)
        arquivos = self.tk.splitlist(event.data)
        extensoes_validas = [".docx", ".pdf", ".md", ".txt", ".jpg", ".jpeg", ".png"]
        
        for caminho in arquivos:
            if os.path.splitext(caminho)[1].lower() in extensoes_validas:
                self.adicionar_linha_arquivo(caminho)

    def selecionar_arquivos(self):
        arquivos = filedialog.askopenfilenames(
            title="Selecione os ficheiros",
            filetypes=[("Ficheiros Suportados", "*.docx *.pdf *.md *.txt *.jpg *.jpeg *.png"), ("Todos", "*.*")]
        )
        for arq in arquivos:
            self.adicionar_linha_arquivo(arq)

    # =========================================================
    # GESTÃO DA FILA DE ARQUIVOS
    # =========================================================
    def adicionar_linha_arquivo(self, caminho_arquivo):
        self.lbl_fila_vazia.grid_remove()
        self.scroll_arquivos.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
        self.btn_converter.configure(state="normal", fg_color=self.accent, text_color="#0f172a", hover_color=self.accent_hover)
        
        nome = os.path.basename(caminho_arquivo)
        extensao = os.path.splitext(nome)[1].lower()
        
        mapa_icones = {".pdf": "pdf.png", ".docx": "docx.png", ".txt": "txt.png", ".md": "md.png", ".jpg": "jpg.png", ".jpeg": "jpg.png", ".png": "png.png"}
        caminho_icone = os.path.join(self.pasta_assets, mapa_icones.get(extensao, "default.png"))
        
        card_item = ctk.CTkFrame(self.scroll_arquivos, fg_color=self.bg_card, corner_radius=10)
        card_item.pack(fill="x", pady=4, padx=4)
        card_item.grid_columnconfigure(1, weight=1)
        
        try:
            icone_img = ctk.CTkImage(light_image=Image.open(caminho_icone), dark_image=Image.open(caminho_icone), size=(26, 26))
            lbl_icone = ctk.CTkLabel(card_item, text="", image=icone_img)
        except Exception:
            lbl_icone = ctk.CTkLabel(card_item, text="📄", font=ctk.CTkFont(size=22))
            
        lbl_icone.grid(row=0, column=0, rowspan=2, padx=(12, 12), pady=10)
        
        lbl_nome = ctk.CTkLabel(
            card_item, text=nome, font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), 
            text_color=self.text_primary, anchor="w"
        )
        lbl_nome.grid(row=0, column=1, sticky="ew", pady=(8, 2))
        
        barra = ctk.CTkProgressBar(card_item, height=5, fg_color=self.bg_root, progress_color=self.accent, corner_radius=4)
        barra.grid(row=1, column=1, sticky="ew", pady=(2, 10))
        barra.set(0)
        
        lbl_pct = ctk.CTkLabel(
            card_item, text="Na fila", font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), 
            text_color=self.text_secondary, width=65, anchor="e"
        )
        lbl_pct.grid(row=0, column=2, rowspan=2, padx=(10, 8))
        
        # Ícone de formato alvo
        extensao_alvo = "docx" if self.modo_selecionado == "pdf2docx" else "pdf"
        caminho_icone_destino = os.path.join(self.pasta_assets, f"{extensao_alvo}.png")
        try:
            img_formato = Image.open(caminho_icone_destino)
            icone_formato = ctk.CTkImage(light_image=img_formato, dark_image=img_formato, size=(22, 22))
            lbl_formato = ctk.CTkLabel(card_item, text="", image=icone_formato)
        except Exception:
            lbl_formato = ctk.CTkLabel(
                card_item, text=extensao_alvo.upper(), font=ctk.CTkFont(size=10, weight="bold"), 
                fg_color=self.bg_panel, text_color=self.accent, corner_radius=6, width=38, height=22
            )
        lbl_formato.grid(row=0, column=3, rowspan=2, padx=(4, 4))
        
        dados_item = {
            "caminho": caminho_arquivo, "extensao": extensao, 
            "barra": barra, "label_pct": lbl_pct, "lbl_formato": lbl_formato
        }
        self.arquivos_na_fila.append(dados_item)
        
        btn_remover = ctk.CTkButton(
            card_item, text="✕", width=28, height=28, corner_radius=8, fg_color="transparent",
            text_color=self.danger, hover_color="#3f1d28", font=ctk.CTkFont(size=14, weight="bold"),
            command=lambda f=card_item, d=dados_item: self.remover_arquivo(f, d)
        )
        btn_remover.grid(row=0, column=4, rowspan=2, padx=(4, 10))
        
        self.atualizar_contador()

    def remover_arquivo(self, frame_linha, dados_item):
        frame_linha.destroy()
        if dados_item in self.arquivos_na_fila:
            self.arquivos_na_fila.remove(dados_item)
            
        if not self.arquivos_na_fila:
            self.resetar_interface()
        else:
            self.atualizar_contador()

    def atualizar_contador(self):
        qtd = len(self.arquivos_na_fila)
        sufixo = "arquivo" if qtd == 1 else "arquivos"
        self.badge_contador.configure(text=f"{qtd} {sufixo}")

    def atualizar_icones_destino(self):
        extensao_alvo = "docx" if self.modo_selecionado == "pdf2docx" else "pdf"
        caminho_icone = os.path.join(self.pasta_assets, f"{extensao_alvo}.png")
        try:
            img_formato = Image.open(caminho_icone)
            icone_formato = ctk.CTkImage(light_image=img_formato, dark_image=img_formato, size=(22, 22))
            for item in self.arquivos_na_fila:
                item["lbl_formato"].configure(image=icone_formato, text="")
        except Exception:
            for item in self.arquivos_na_fila:
                item["lbl_formato"].configure(image=None, text=extensao_alvo.upper())

    # =========================================================
    # EXECUÇÃO DOS MOTORES DE CONVERSÃO
    # =========================================================
    def iniciar_conversao(self):
        if not self.arquivos_na_fila:
            return
            
        self.btn_converter.configure(state="disabled", text="Processando...")
        self.btn_limpar.configure(state="disabled")
        
        for widget in (self.drop_zone, self.drop_inner, self.lbl_drop_titulo, self.lbl_drop_sub):
            widget.unbind("<Button-1>")
            
        for card in self.scroll_arquivos.winfo_children():
            for child in card.winfo_children():
                if isinstance(child, ctk.CTkButton):
                    child.configure(state="disabled")
                    
        threading.Thread(target=self._processar_conversao, daemon=True).start()

    def _processar_conversao(self):
        total = len(self.arquivos_na_fila)
        modo = self.modo_selecionado
        
        if modo == "merge_pdf":
            self.lbl_status.configure(text="Mesclando documentos PDF...")
            caminhos, itens = [], []
            
            for item in self.arquivos_na_fila:
                if item["extensao"] == ".pdf":
                    caminhos.append(item["caminho"])
                    itens.append(item)
                    item["barra"].set(0.5)
                    item["label_pct"].configure(text="50%", text_color=self.accent)
                else:
                    item["barra"].set(1.0)
                    item["barra"].configure(progress_color=self.border_subtle)
                    item["label_pct"].configure(text="Ignorado", text_color=self.text_secondary)
                    
            if caminhos:
                sucesso, _ = processar_mesclagem(caminhos)
                for item in itens:
                    item["barra"].set(1.0)
                    if sucesso:
                        item["barra"].configure(progress_color=self.success)
                        item["label_pct"].configure(text="100%", text_color=self.success)
                    else:
                        item["barra"].configure(progress_color=self.danger)
                        item["label_pct"].configure(text="ERRO", text_color=self.danger)
        else:
            intervalo_digitado = self.entry_paginas.get()
            for index, item in enumerate(self.arquivos_na_fila):
                caminho = item["caminho"]
                extensao = item["extensao"]
                barra = item["barra"]
                label_pct = item["label_pct"]
                
                self.lbl_status.configure(text=f"Processando ({index + 1} de {total})...")
                
                compativel = False
                if modo == "to_pdf" and extensao in [".docx", ".txt", ".md", ".jpg", ".jpeg", ".png"]:
                    compativel = True
                elif modo in ["pdf2docx", "split_pdf", "compress_pdf"] and extensao == ".pdf":
                    compativel = True
                    
                if not compativel:
                    barra.set(1.0)
                    barra.configure(progress_color=self.border_subtle)
                    label_pct.configure(text="Ignorado", text_color=self.text_secondary)
                    continue
                    
                barra.set(0.5)
                label_pct.configure(text="50%", text_color=self.accent)
                
                sucesso = False
                if modo == "to_pdf":
                    if extensao == ".docx":
                        sucesso, _ = processar_docx(caminho)
                    elif extensao in [".txt", ".md"]:
                        sucesso, _ = processar_texto(caminho)
                    elif extensao in [".jpg", ".jpeg", ".png"]:
                        sucesso, _ = processar_imagem(caminho)
                elif modo == "pdf2docx":
                    sucesso, _ = processar_pdf(caminho)
                elif modo == "split_pdf":
                    sucesso, _ = processar_divisao(caminho, intervalo_digitado)
                elif modo == "compress_pdf":
                    sucesso, _ = processar_compressao(caminho)
                    
                barra.set(1.0)
                if sucesso:
                    barra.configure(progress_color=self.success)
                    label_pct.configure(text="100%", text_color=self.success)
                else:
                    barra.configure(progress_color=self.danger)
                    label_pct.configure(text="ERRO", text_color=self.danger)
                    
        self.lbl_status.configure(text="Processamento Concluído!")
        self.btn_limpar.configure(state="normal")
        for widget in (self.drop_zone, self.drop_inner, self.lbl_drop_titulo, self.lbl_drop_sub):
            widget.bind("<Button-1>", lambda e: self.selecionar_arquivos())
            
        self.btn_converter.configure(
            state="normal", text="Nova Conversão (Limpar)", 
            fg_color=self.success, text_color="#0f172a", hover_color="#10b981",
            command=self.resetar_interface
        )
        self.arquivos_na_fila.clear()

    def resetar_interface(self):
        for widget in self.scroll_arquivos.winfo_children():
            widget.destroy()
            
        self.arquivos_na_fila.clear()
        self.atualizar_contador()
        self.lbl_status.configure(text="Fila de Processamento")
        self.btn_converter.configure(
            text="Iniciar Processamento", command=self.iniciar_conversao, 
            state="disabled", fg_color=self.bg_card, text_color=self.text_secondary
        )
        self.scroll_arquivos.grid_remove()
        self.lbl_fila_vazia.grid(row=0, column=0)