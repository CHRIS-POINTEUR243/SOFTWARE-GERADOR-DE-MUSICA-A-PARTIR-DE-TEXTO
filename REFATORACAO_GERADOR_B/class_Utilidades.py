MINUTO = 60
DISTANCIA_OITAVA = 12
UNIDADE_BPM = 80

class Utilidades:
     
    def bpmParaMilisegundos(bpm):
        tempo = 1 / (bpm / MINUTO)
        return tempo
    #usado em player e em geradornotas
        
    # Adicinei: função para SALVAR texto em um arquivo .txt
    def salvaArquivoTxt(nome_arquivo, conteudo):
        """
        Salva o conteúdo de texto em um arquivo .txt.
        Retorna True se deu certo, False se deu erro.
        """
        try:
            with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
                arquivo.write(conteudo)
            print(f"Arquivo '{nome_arquivo}' salvo com sucesso.")
            return True
        except Exception as erro:
            print(f"Erro ao salvar arquivo '{nome_arquivo}': ", erro)
            return False
