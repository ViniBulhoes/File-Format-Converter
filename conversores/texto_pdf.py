import os
import markdown
from fpdf import FPDF, HTMLMixin

# Criamos uma classe personalizada que herda do FPDF e do HTMLMixin 
# para permitir a renderização de tags HTML geradas a partir do Markdown.
class PDF(FPDF, HTMLMixin):
    pass

def processar_texto(caminho_entrada):
    """
    Converte arquivos .txt ou .md para .pdf.
    Retorna uma tupla: (Sucesso: bool, Mensagem ou Caminho de Saída: str)
    """
    try:
        base, ext = os.path.splitext(caminho_entrada)
        caminho_saida = f"{base}.pdf"
        extensao = ext.lower()

        # Lê o conteúdo do arquivo
        with open(caminho_entrada, 'r', encoding='utf-8') as f:
            conteudo = f.read()

        pdf = PDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Helvetica", size=12)

        if extensao == ".md":
            # Converte as marcações do Markdown para HTML
            html_conteudo = markdown.markdown(conteudo)
            # Escreve o HTML interpretado no PDF
            pdf.write_html(html_conteudo)
        else:
            # Para .txt, escreve o texto diretamente linha a linha
            pdf.write(txt=conteudo)

        pdf.output(caminho_saida)
        return True, caminho_saida

    except Exception as e:
        return False, str(e)