# ⚡ File Forge - Conversor e Manipulador de Documentos

Uma aplicação desktop moderna e de alta performance desenvolvida em Python para conversão, manipulação e gerenciamento de múltiplos documentos simultaneamente. O projeto conta com uma interface gráfica profissional inspirada em design de estúdios modernos (paleta *Nord / Deep Ocean*), suporte a *Drag & Drop* avançado, motores assíncronos e processamento 100% local.

## 🚀 Funcionalidades Principais

- **Conversão em Lote (Batch Processing):** Processe vários arquivos simultaneamente com acompanhamento de progresso individual.
- **Suporte a Múltiplos Formatos:**
  - **Conversão para PDF:** De Word (`.docx`), Texto (`.txt`), Markdown (`.md`) e Imagens (`.jpg`, `.jpeg`, `.png`).
  - **PDF para Word (`pdf2docx`):** Extração de texto e layout para documentos editáveis do Word.
  - **Mesclagem de PDFs (`PyMuPDF`):** Agrupe múltiplos arquivos PDF em um único documento sequencial em segundos.
  - **Divisão / Extração de Páginas:** Extraia páginas específicas ou intervalos customizados (ex: `1, 3, 5-10`) ou divida todas as páginas do PDF.
  - **Compressão de PDF:** Reduza o tamanho de PDFs pesados de forma inteligente.
- **Interface Studio (Nord / Deep Ocean):** Layout dividido em duas colunas com cards de ferramentas interativos, fila em tempo real com indicador de quantidade, botão de remoção individual e zona de arraste (*Drop Zone*) dinâmica na base.
- **Execução Silenciosa (`iniciar.bat`):** Inicialização otimizada para Windows sem janelas de terminal abertas.

## 🏗️ Arquitetura do Projeto

```text
📁 conversor_arquivos
┣ 📂 assets/              # Ícones dinâmicos da interface (pdf.png, docx.png, etc.)
┣ 📂 conversores/         # Motores lógicos isolados (Core)
┃ ┣ 📜 docx_pdf.py        # Conversão Word > PDF
┃ ┣ 📜 pdf_docx.py        # Conversão PDF > Word
┃ ┣ 📜 texto_pdf.py       # Conversão TXT/MD > PDF
┃ ┣ 📜 mesclar_pdf.py     # Junção de múltiplos PDFs
┃ ┣ 📜 img_pdf.py         # Conversão de Imagens > PDF
┃ ┣ 📜 dividir_pdf.py     # Divisão e extração de páginas em PDFs
┃ ┗ 📜 comprimir_pdf.py   # Compressão e otimização de PDFs
┣ 📂 interface/           # Componentes visuais e layouts
┃ ┣ 📜 app_gui.py         # Layout clássico original
┃ ┗ 📜 app_gui_novo.py    # Novo layout Studio (Nord / Deep Ocean)
┣ 📜 iniciar.bat          # Script de inicialização automática e silenciosa (Pythonw)
┣ 📜 main.py              # Ponto de entrada principal da aplicação
┗ 📜 requirements.txt     # Dependências e bibliotecas do projeto
```

## 🛠️ Tecnologias Utilizadas

- **[Python 3.x](https://www.python.org/):** Linguagem base.
- **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter):** Framework moderno para interface gráfica.
- **[tkinterdnd2](https://github.com/pminkov/tkinterdnd2):** Suporte nativo a *Drag & Drop* no Windows.
- **[PyMuPDF (fitz)](https://pypi.org/project/PyMuPDF/):** Motor de altíssima performance para manipulação, mesclagem, divisão e compressão de PDFs.
- **[pdf2docx](https://pypi.org/project/pdf2docx/) & [docx2pdf](https://pypi.org/project/docx2pdf/):** Conversão bidirecional de documentos Word e PDF.
- **[fpdf2](https://pypi.org/project/fpdf2/) & [Markdown](https://pypi.org/project/Markdown/):** Renderização de textos e arquivos `.md` em PDF formatado.
- **[Pillow (PIL)](https://pypi.org/project/Pillow/):** Manipulação e conversão de imagens.
- **[pywin32](https://pypi.org/project/pywin32/):** Integração com o sistema COM do Windows.

## 📥 Instalação e Execução

1. Clone ou baixe o repositório para sua máquina local.
2. **Modo Automático (Recomendado para Windows):**
   Dê um duplo clique no arquivo **`iniciar.bat`**. Ele verificará ou criará o ambiente virtual (`.venv`), instalará as dependências automaticamente e abrirá o aplicativo de forma limpa e silenciosa.

3. **Modo Manual via Terminal:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   python main.py
   ```

## 👨‍💻 Desenvolvedor

Desenvolvido por **Vinicius Porto (Bulhões)** - [ViniBulhoes](https://github.com/ViniBulhoes)