import os
from pdf2docx import Converter

def processar_pdf(caminho_entrada):
    """
    Converte um arquivo .pdf para .docx.
    Retorna uma tupla: (Sucesso: bool, Mensagem ou Caminho de Saída: str)
    """
    try:
        # Gera o caminho de saída trocando a extensão original por .docx
        base = os.path.splitext(caminho_entrada)[0]
        caminho_saida = f"{base}.docx"
        
        # Inicializa o conversor e processa todas as páginas
        cv = Converter(caminho_entrada)
        cv.convert(caminho_saida)      
        cv.close()
        
        return True, caminho_saida
        
    except Exception as e:
        return False, str(e)