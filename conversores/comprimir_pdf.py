import fitz
import os

def processar_compressao(caminho):
    try:
        doc = fitz.open(caminho)
        pasta_destino = os.path.dirname(caminho)
        nome_sem_ext, ext = os.path.splitext(os.path.basename(caminho))
        
        caminho_saida = os.path.join(pasta_destino, f"{nome_sem_ext}_Comprimido{ext}")
        
        # O garbage=4 e deflate=True são algoritmos poderosos de compressão nativos do PyMuPDF
        doc.save(caminho_saida, garbage=4, deflate=True)
        doc.close()
        return True, f"Comprimido: {os.path.basename(caminho_saida)}"
    except Exception as e:
        return False, str(e)