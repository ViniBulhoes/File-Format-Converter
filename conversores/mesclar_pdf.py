import fitz
import os

def processar_mesclagem(lista_caminhos):
    """
    Recebe uma lista de caminhos de arquivos PDF e os mescla em um único arquivo.
    Salva o resultado na mesma pasta do primeiro arquivo da lista.
    """
    if not lista_caminhos:
        return False, "Nenhum arquivo PDF válido para mesclar."
    
    try:
        # Cria um novo documento PDF vazio
        doc_final = fitz.open()
        
        for caminho in lista_caminhos:
            # Abre cada PDF da lista e insere no documento final
            doc_atual = fitz.open(caminho)
            doc_final.insert_pdf(doc_atual)
            doc_atual.close()
            
        # Define o caminho de saída baseado na pasta do primeiro arquivo
        pasta_destino = os.path.dirname(lista_caminhos[0])
        caminho_saida = os.path.join(pasta_destino, "PDF_Mesclado.pdf")
        
        # Lógica para não sobrescrever se o arquivo já existir
        contador = 1
        while os.path.exists(caminho_saida):
            caminho_saida = os.path.join(pasta_destino, f"PDF_Mesclado_{contador}.pdf")
            contador += 1
            
        # Salva o arquivo final no disco
        doc_final.save(caminho_saida)
        doc_final.close()
        
        return True, f"Arquivo gerado: {os.path.basename(caminho_saida)}"
        
    except Exception as e:
        return False, str(e)