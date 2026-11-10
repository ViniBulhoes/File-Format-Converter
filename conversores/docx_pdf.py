import os
import pythoncom
from docx2pdf import convert

def processar_docx(caminho_entrada):
    """
    Converte um arquivo .docx para .pdf.
    Retorna uma tupla: (Sucesso: bool, Mensagem ou Caminho de Saída: str)
    """
    try:
        # Inicializa o subsistema COM do Windows para a thread atual.
        # Isso é obrigatório sempre que rodamos docx2pdf fora da thread principal da interface.
        pythoncom.CoInitialize() 
        
        # Gera o caminho de saída trocando a extensão original por .pdf
        base = os.path.splitext(caminho_entrada)[0]
        caminho_saida = f"{base}.pdf"
        
        # Realiza a conversão
        convert(caminho_entrada, caminho_saida)
        
        return True, caminho_saida
        
    except Exception as e:
        return False, str(e)