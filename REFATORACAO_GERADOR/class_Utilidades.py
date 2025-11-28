MINUTO = 60
DISTANCIA_OITAVA = 12
UNIDADE_BPM = 80

class Utilidades:
    def bpmParaMilisegundos(bpm):
        tempo = 1 / (bpm / MINUTO)
        return tempo
    
    def leArquivoTxt(nome_arquivo):
        try:
            with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
                return arquivo.read()
        except FileNotFoundError:
            print(f"Arquivo ",nome_arquivo," não encontrado!")
            return ""
        except Exception as erro:
            print(f"Erro ao ler arquivo: ",erro)
            return ""