QUANTIDADE_MAXIMA_DE_CARACTERES_FUNCAO = 4

class Nota:
    def __init__(self, nome, oitava=4, duracao=1, volume=80, instrumento="Piano"):
        self.nome = nome
        self.oitava = oitava
        self.duracao = duracao
        self.volume = volume
        self.instrumento = instrumento

    def tocar(self):
        i=0
        



class GeradorMusical:
    def __init__(self):
        self.listaNotas = []
        self.listaInstrumentos = []
        self.oitavaAtual = 4
        self.volumeAtual = 80
        self.instrumentoAtual = "Piano"
        self.tabelaFuncoes = {
            ' ': self.aumentarVolume,
            '+': self.aumentarOitava,
            '-': self.diminuirOitava,
            'O': self.repetirNota,
            'I': self.repetirNota,
            'U': self.repetirNota,
            '?': self.notaAleatoria,
            '\n':self.trocaInstrumento,
            'BPM+': self.aumentarBPM,
            'BPM-': self.diminuirBMP,
            ';': self.silencio
        }
        self.notas = {
            'A': "Lá",
            'B': "Si",
            'C': "Dó",
            'D': "Ré",
            'E': "Mi",
            'F': "Fá",
            'G': "Sol",
            'H': "Si Bemol"
        }



    
    def mapeiaTexto(self, texto):
          #assim fica melhor pra tartar caso tenha mais de um caractere, 
    # ai so tem q colocar mais de um caractere na tabela e mudar a constante de quantiadae
        i = 0
        texto=texto.upper()
        while i < len(texto):
            nota = None
            comando_encontrado = False
            
            # Verifica da quantidade maxima ate a minima 1 
            for tamanho in range(QUANTIDADE_MAXIMA_DE_CARACTERES_FUNCAO, 0, -1):
                #se ja acabou o texto ou esta na tabela de funcoes
                if (i + (tamanho - 1) < len(texto)) and (texto[i:i+tamanho] in self.tabela):
                    comando = texto[i:i+tamanho]
                    self.obterFuncao(comando)
                    i += tamanho
                    comando_encontrado = True
                    break  #sai do for quando encontrar um comando na tabela
            
            if comando_encontrado:
                continue  #ja achou o comando na tabela vai pro proxio caractere
            #n encontrou o comando ve se eh nota
            elif texto[i] in self.notas:
                nota = Nota(self.notas[texto[i]], self.oitava_atual, 1, self.volume_atual, self.instrumento_atual)
                i += 1
    
            #pra n dar problema com caracteres desconhecidos
            else:
                i += 1
            # pra n dar problema caso n crie nota
            if nota is not None:
                self.listaNotas.append(nota)

    def obterFuncao(self, ch):
        funcao = self.tabela.get(ch)
        if funcao:
            return funcao()
        return None


    def executar(self):
        i=0

    def aumentaVolume(self):
        self.volumeAtual*2

    def trocaInstrumento():
        i=0
    
    def notaAleatoria():
        
       



#-----------------------------------------------------------------------------

