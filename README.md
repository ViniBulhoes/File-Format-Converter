# 🔄 File Forge - Conversor de Documentos em Lote

Uma aplicação desktop desenvolvida em Python para facilitar a conversão de múltiplos arquivos e formatos de documentos simultaneamente. O projeto utiliza uma interface gráfica moderna, com tema escuro (Dark Mode), construída com `CustomTkinter`, permitindo que os usuários convertam arquivos entre PDF, DOCX, TXT e Markdown de forma rápida e intuitiva.

## 🚀 Funcionalidades

- **Conversão em Lote (Batch Processing):** Selecione múltiplos arquivos de uma vez para conversão automatizada, otimizando o fluxo de trabalho.
- **Suporte a Múltiplos Formatos:**
  - PDF para DOCX (via `pdf2docx`)
  - DOCX para PDF (via `docx2pdf`)
  - Texto (.txt) e Markdown (.md) para PDF (via `fpdf2` e `Markdown`)
- **Interface Gráfica Moderna:** UI desenvolvida com `CustomTkinter`, incluindo barra de progresso individual, ícones dinâmicos de formato e sistema visual de triagem (arquivos incompatíveis são automaticamente ignorados e marcados em cinza).
- **Processamento Assíncrono:** Uso de *threading* para garantir que a interface não congele durante as conversões pesadas.
- **Processamento Local:** Todas as conversões são feitas localmente na máquina, garantindo privacidade absoluta dos documentos.

## 🏗️ Arquitetura do Projeto

O código foi construído de forma modular para facilitar a manutenção e escalabilidade. A estrutura de pastas está dividida da seguinte forma:

    📦 conversor_arquivos
    ┣ 📂 assets/              # Ícones dinâmicos e imagens da interface (ex: pasta.png, md.png)
    ┣ 📂 conversores/         # Motor lógico central (Core)
    ┃ ┣ 📜 docx_pdf.py        # Módulo de conversão Word > PDF
    ┃ ┣ 📜 pdf_docx.py        # Módulo de conversão PDF > Word
    ┃ ┗ 📜 texto_pdf.py       # Módulo de conversão TXT/MD > PDF
    ┣ 📂 interface/           # Componentes visuais e GUI
    ┃ ┗ 📜 app_gui.py         # Janela principal, botões e roteamento
    ┣ 📜 main.py              # Arquivo principal de execução
    ┗ 📜 requirements.txt     # Dependências do projeto

## 🛠️ Tecnologias Utilizadas

- **[Python 3.x](https://www.python.org/):** Linguagem principal do projeto.
- **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter):** Biblioteca para a interface gráfica moderna.
- **[pdf2docx](https://pypi.org/project/pdf2docx/):** Motor de conversão de PDF para Word.
- **[docx2pdf](https://pypi.org/project/docx2pdf/):** Motor de conversão de Word para PDF.
- **[fpdf2](https://pypi.org/project/fpdf2/) e [Markdown](https://pypi.org/project/Markdown/):** Renderização e conversão de textos e arquivos MD para PDF.
- **[Pillow](https://pypi.org/project/Pillow/):** Manipulação de imagens e renderização dos ícones na interface.
- **[pywin32](https://pypi.org/project/pywin32/):** Integração com o sistema COM do Windows (essencial para *threading* do docx2pdf).

## ⚙️ Pré-requisitos

Certifique-se de ter o Python 3 instalado no seu sistema. O aplicativo foi construído e otimizado para o ambiente **Windows 11**, onde as bibliotecas que dependem do Office (como a `docx2pdf`) funcionam nativamente.

## 📥 Instalação e Execução

1. Clone o repositório para a sua máquina local:
   ```bash
   git clone https://github.com/ViniBulhoes/nome-do-repositorio.git
   cd nome-do-repositorio
   ```

2. Crie e ative um ambiente virtual (recomendado):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Instale todas as dependências necessárias de uma só vez:
   ```bash
   pip install -r requirements.txt
   ```

4. Execute a aplicação:
   ```bash
   python main.py
   ```

*(Nota: Certifique-se de que o Microsoft Word está instalado na máquina caso utilize a conversão de DOCX para PDF, pois a biblioteca requer comunicação com os componentes COM do Office).*

## 📦 Deploy e Distribuição

A arquitetura modular (`main.py` separado da lógica) foi desenhada para ser totalmente compatível com o **PyInstaller**. Futuramente, o projeto pode ser compilado num único arquivo executável `.exe` para distribuição sem necessidade de instalação do Python na máquina de destino.

## 👨‍💻 Desenvolvedor

- **Vinicius Porto (Bulhões)** - [ViniBulhoes](https://github.com/ViniBulhoes)