# 🔄 Conversor de Documentos em Lote

Uma aplicação desktop desenvolvida em Python para facilitar a conversão de múltiplos arquivos e formatos de documentos simultaneamente. O projeto utiliza uma interface gráfica moderna e amigável construída com `CustomTkinter`, permitindo que usuários convertam arquivos entre PDF, DOCX e Markdown de forma rápida e intuitiva.

## 🚀 Funcionalidades

- **Conversão em Lote:** Selecione múltiplos arquivos de uma vez para conversão automatizada, otimizando o fluxo de trabalho.
- **Suporte a Múltiplos Formatos:**
  - PDF para DOCX (via `pdf2docx`)
  - DOCX para PDF (via `docx2pdf`)
  - Suporte a formatação e conversão de arquivos Markdown
- **Interface Gráfica Moderna:** UI desenvolvida com `CustomTkinter`, oferecendo um visual limpo, responsivo e suporte a temas (claro/escuro).
- **Processamento Local:** Todas as conversões são feitas localmente na máquina, garantindo privacidade e segurança dos documentos.

## 🛠️ Tecnologias Utilizadas

- **[Python 3.x](https://www.python.org/):** Linguagem principal do projeto.
- **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter):** Biblioteca para a interface gráfica moderna.
- **[pdf2docx](https://pypi.org/project/pdf2docx/):** Motor de conversão de PDF para Word.
- **[docx2pdf](https://pypi.org/project/docx2pdf/):** Motor de conversão de Word para PDF.

## ⚙️ Pré-requisitos

Certifique-se de ter o Python 3 instalado no seu sistema. O aplicativo foi testado em ambiente Windows, onde bibliotecas que dependem do Office (como a `docx2pdf`) funcionam nativamente.

Você também precisará instalar as dependências do projeto. Recomenda-se o uso de um ambiente virtual (venv).

## 📥 Instalação e Execução

1. Clone o repositório para a sua máquina local:
   ```bash
   git clone https://github.com/ViniBulhoes/nome-do-repositorio.git
   cd nome-do-repositorio
   ```

2. Crie e ative um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   
   # No Windows:
   venv\Scripts\activate
   
   # No Linux/Mac:
   source venv/bin/activate
   ```

3. Instale as dependências necessárias:
   ```bash
   pip install customtkinter pdf2docx docx2pdf
   ```

4. Execute a aplicação:
   ```bash
   python main.py
   ```

*(Nota: Certifique-se de que o Microsoft Word está instalado na máquina caso utilize a conversão de DOCX para PDF via `docx2pdf`, pois a biblioteca requer a comunicação com os componentes do Office).*

## 👨‍💻 Desenvolvedor

- **Vinicius Bulhões** - [ViniBulhoes](https://github.com/ViniBulhoes)