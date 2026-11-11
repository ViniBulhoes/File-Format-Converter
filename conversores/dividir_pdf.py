import fitz
import os

def processar_divisao(caminho, intervalo=""):
    try:
        doc = fitz.open(caminho)
        total_paginas = len(doc)
        
        if total_paginas <= 1:
            doc.close()
            return False, "O PDF possui apenas 1 página."
            
        pasta_destino = os.path.dirname(caminho)
        nome_sem_ext = os.path.splitext(os.path.basename(caminho))[0]
        
        intervalo = str(intervalo).strip()
        
        # 1. Se NÃO houver intervalo (campo em branco), divide TODAS as páginas (Comportamento antigo)
        if not intervalo:
            pasta_saida = os.path.join(pasta_destino, f"{nome_sem_ext}_Dividido")
            os.makedirs(pasta_saida, exist_ok=True)
            
            for i in range(total_paginas):
                novo_doc = fitz.open()
                novo_doc.insert_pdf(doc, from_page=i, to_page=i)
                caminho_pagina = os.path.join(pasta_saida, f"Pagina_{i+1}.pdf")
                novo_doc.save(caminho_pagina)
                novo_doc.close()
                
            doc.close()
            return True, f"Dividido em {total_paginas} arquivos individuais."
            
        # 2. Se HOUVER intervalo, extrai apenas as páginas solicitadas para UM único arquivo
        else:
            paginas_alvo = set()
            partes = intervalo.split(',')
            for parte in partes:
                parte = parte.strip()
                if '-' in parte:
                    try:
                        inicio_str, fim_str = parte.split('-')
                        # Subtrai 1 porque o PyMuPDF conta as páginas a partir de 0 internamente
                        inicio = max(0, int(inicio_str) - 1)
                        fim = min(total_paginas - 1, int(fim_str) - 1)
                        paginas_alvo.update(range(inicio, fim + 1))
                    except ValueError:
                        pass # Ignora letras ou formatações erradas sem quebrar o programa
                elif parte.isdigit():
                    p = int(parte) - 1
                    if 0 <= p < total_paginas:
                        paginas_alvo.add(p)
            
            if not paginas_alvo:
                doc.close()
                return False, "Nenhuma página válida encontrada no intervalo fornecido."
                
            lista_paginas = sorted(list(paginas_alvo))
            
            # Cria o documento contendo apenas as páginas escolhidas
            novo_doc = fitz.open()
            for p in lista_paginas:
                novo_doc.insert_pdf(doc, from_page=p, to_page=p)
                
            caminho_saida = os.path.join(pasta_destino, f"{nome_sem_ext}_Extraido.pdf")
            
            # Garante que não sobrescreva um arquivo caso extraia duas vezes
            contador = 1
            while os.path.exists(caminho_saida):
                caminho_saida = os.path.join(pasta_destino, f"{nome_sem_ext}_Extraido_({contador}).pdf")
                contador += 1
                
            novo_doc.save(caminho_saida)
            novo_doc.close()
            doc.close()
            
            return True, f"Páginas {intervalo} extraídas com sucesso."
            
    except Exception as e:
        return False, str(e)