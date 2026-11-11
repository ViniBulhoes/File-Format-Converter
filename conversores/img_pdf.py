from PIL import Image
import os

def processar_imagem(caminho):
    try:
        img = Image.open(caminho)
        # Se a imagem tiver transparência (PNG), converte para RGB para o PDF aceitar
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
            
        pasta_destino = os.path.dirname(caminho)
        nome_sem_ext = os.path.splitext(os.path.basename(caminho))[0]
        caminho_saida = os.path.join(pasta_destino, f"{nome_sem_ext}.pdf")
        
        img.save(caminho_saida, "PDF", resolution=100.0)
        return True, f"Imagem convertida: {os.path.basename(caminho_saida)}"
    except Exception as e:
        return False, str(e)