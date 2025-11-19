import pygame
import pygame.midi
import os
import time

pygame.init()
pygame.mixer.init()
pygame.midi.init()

port = pygame.midi.get_default_output_id()
midi_out = pygame.midi.Output(port, 0)

QUANTIDADE_MAXIMA_DE_CARACTERES_FUNCAO = 4
DISTANCIA_OITAVA = 12
OITAVA_DEFAULT = 0
VOLUME_DEFAULT = 127 #(máximo)
BPM_DEFAULT = 120
MINUTO = 60
UNIDADE_BPM = 80
#oitava eh +12 ou -12, então 12n onde n pertence aos inteiros

def bpmToMilliseconds(bpm):
      tempo_ms = 1 / (bpm / MINUTO)
      return tempo_ms

class Nota:
    def __init__(self, caractere, oitava, bpm, volume, instrumento):

        self.caractere=caractere
        #esse valor vem da tabela General MIDI (biblioteca pygame.midi)
        #onde o dó central é o C4 = 60
        self.oitava = oitava
        #ex: +1, 0, -1, -2
        self.bpm = bpm
        #delay entre note on note off (bpm da nota)
        self.volume = volume
        #um valor entre 0 e 127, por definição da biblioteca pygame.midi
        self.instrumento = instrumento
        #um dos inseridos na tabela de instrumentos
        self.tabelaNotas = {
            'A': 69 ,
            'B': 71 ,
            'C': 60 ,
            'D': 62 ,
            'E': 64 ,
            'F': 65 ,
            'G': 67 ,
            'H': 70 
        }
        #coloquei aqui pra ja inicializar quando criar uma instancia de niota, ai n precisa chamar nenhuma funcao
        #isso ta certo? n sei se n teria q fazer
        if caractere in self.tabelaNotas:
            self.valorMIDI = self.tabelaNotas[caractere]
        else:
            self.valorMIDI = None  # Ou lançar uma exceção
        
        '''
        isso n eh necessario
    def verificaCaractereEBuscaNota(self):
        if self.caractere in self.tabelaNotas:
            self.valorMIDI = self.tabelaNotas[self.caractere]
                #mapeio aqui instrumento e valorMIDI
                '''
    def tocar(self):
        print (self.valorMIDI,self.oitava,self.bpm,self.volume,self.instrumento)
        
        midi_out.set_instrument(self.instrumento)
        midi_out.note_on(self.valorMIDI, self.volume)
        #volume vai de 0 a 127
        time.sleep(bpmToMilliseconds(self.bpm))
        #time.sleep() ajustar aqui o bpm
        midi_out.note_off(self.valorMIDI, self.volume)
        
        
class GeradorMusical:
    def __init__(self,texto):
        
        self.listaInstrumentos = []
        self.oitava_atual = OITAVA_DEFAULT
        self.volume_atual = VOLUME_DEFAULT
        self.bpm_atual = BPM_DEFAULT
        self.instrumento_atual = "ACOUSTIC_GRAND_PIANO"
        self.tabelaNotas = ['A','B','C','D','E','F','G','H']
        #preciso disso pra minha processa texto
        self.tabelaFuncoes = {
            ' ': self.dobraVolume,
            '+': self.aumentaOitava,
            '-': self.diminuiOitava,
            'O': self.repeteNota,
            'I': self.repeteNota,
            'U': self.repeteNota,
            '?': self.notaAleatoria,
            '%':self.trocaInstrumento,
            'BPM+': self.aumentaBPM,
            'BPM-': self.diminuiBPM,
            ';': self.silencio
        }
        self.tabelaInstrumentos = {
            'ACOUSTIC_GRAND_PIANO' : 0,	
            'BRIGHT_ACOUSTIC_PIANO' : 1,	
            'ELECTRIC_GRAND_PIANO' : 2,
            'HONKY_TONK_PIANO' : 3,
            'RHODES_PIANO' : 4,
            'CHORUSED_PIANO' : 5,
            'HARPSICHORD' : 6,
            'CLAVINET' : 7,	
            'ACOUSTIC_NYLON_GUITAR' : 24,	
            'ACOUSTIC_STEEL_GUITAR' : 25,	
            'ELECTRIC_JAZZ_GUITAR' : 26,	
            'ELECTRIC_CLEAN_GUITAR' : 27,	
            'ELECTRIC_MUTED_GUITAR' : 28,	
            'OVERDRIVEN_GUITAR' : 29,	
            'DISTORTION_GUITAR' : 30,	
            'GUITAR_HARMONICS' : 31,	
            'ACOUSTIC_BASS' : 32,
            'FINGERED_ELECTRIC_BASS' : 33,	
            'PLUCKED_ELECTRIC_BASS' : 34,	
            'FRETLESS_BASS' : 35,	
            'SLAP_BASS_1' : 36,	
            'SLAP_BASS_2' : 37,	
            'SYNTH_BASS_1' : 38,	
            'SYNTH_BASS_2' : 39,	
            'TELEPHONE_RING' : 124
        }

        #chama essa funcao no init pra n precisar chamar na main, ao inicializar ja cria tudo, eh como se fossem metodos privados
        self.listaCaracteres=[]
        self.processaTextoEmLista(texto)

        self.lista_notas=[]
        self.mapeiaTexto()	
        #aqui eh so chamar o metodo na função init, ele mesmp ja preenche a lista notas, n retornando nada

    def novaMusica(self,texto):
        self.processaTextoEmLista(texto)
        self.mapeiaTexto()
       

    def mapeiaTexto(self):
          #assim fica melhor pra tartar caso tenha mais de um caractere, 
    # ai so tem q colocar mais de um caractere na tabela e mudar a constante de quantiadae
        for comando in self.listaCaracteres:
            nota=None
            if  comando in self.tabelaFuncoes:
                    self.obterFuncaoMusical(comando)
#musdar aqui
            else:
                nota=Nota(comando,self.oitava_atual,self.bpm_atual,self.volume_atual,self.instrumento_atual)
                
            # pra n dar problema caso n crie nota
            if nota is not None:
                self.lista_notas.append(nota)

    def obterFuncaoMusical(self, ch):
        funcaoMusical = self.tabelaFuncoes.get(ch)
        if funcaoMusical:
            return funcaoMusical()
        return None
    
    def processaTextoEmLista(self,texto):
        i = 0
        encontrou=False
        while i < len(texto):
        
            for tamanhoString in range(QUANTIDADE_MAXIMA_DE_CARACTERES_FUNCAO, 0, -1):
                if (i + tamanhoString <= len(texto)) and (texto[i:i+tamanhoString] in self.tabelaFuncoes):
                    self.listaCaracteres.append(texto[i:i+tamanhoString])
                    i += tamanhoString
                    encontrou = True
                    break
            
            if encontrou:
                encontrou = False
                continue
            elif texto[i] in self.tabelaNotas:
                self.listaCaracteres.append(texto[i]) 
                i += 1
            else:
                i += 1
        

    def dobraVolume(self):
        volume_dobrado = self.volume_atual * 2
        if (volume_dobrado <= 127):
            self.volume_atual = volume_dobrado
        else:
            self.volume_atual = 127
    
    def aumentaOitava(self):
        self.oitava_atual += 1
        
    def diminuiOitava(self):
        self.oitava_atual -= 1

    def trocaInstrumento(self):
        iterador = iter(self.tabelaInstrumentos)
        for chave in iterador:
            if chave == self.instrumento_atual:
                prox_instrumento = next(iterador,None)
                break
        self.instrumento_atual = prox_instrumento
#POSSIVELMENTE FAZER ALGO DESSE JEITO SE FOR PASSAR TABELA DE INSTRUMENTOS PRA DENTRO DE GERADORMUSICAL 
#AO INVÉS DE DENTRO DE NOTAMUSICAL

    def repeteNota(self):
        self.lista_notas.append(self.lista_notas[len(self.lista_notas) - 1])

    def notaAleatoria():
        i=0
    
    #time.sleep(segundos), vamos definir um bpm padrão = 120 bpm
    #assim temos 2 batidas por segundo, ou seja, 
    #time.sleep(0.5) por padrão
    #aumentar em 80 unidades seria -> 120 + 80 = 200
    #portanto, time.sleep(200 / 60)
    def aumentaBPM(self):
        self.bpm_atual += UNIDADE_BPM
    
    def diminuiBPM(self):
        self.bpm_atual -= UNIDADE_BPM
    #não está nas especificações do programa, mas deve poder diminuir na interface

    def silencio(self):
        i=0
    
    #def notaAleatoria():

      
            
#main super pequena, facil de um usuario usar, n precisa saber como eh a implementacao
#gerador continua dependente de nota, eu iria q eh tipo uma relacao de agregacao
#mas nota pode ser usado separado
#gerador realmente tem mts funcoes, mas ele so tem um objetivo; criar uma lista de notas baseado num texto de entrada
#talvez seria legal colocar a tabela como argumento a tabela, ou colocar metodos de alterar, como set('A',lá)
#criar metodo altera texto, nova string, set sting, pq assim ele so toca uma sring --> por isso tem o novaMusica
geradorTeste = GeradorMusical("ABABABPM+'++==0AEE,EE")

for nota in geradorTeste.lista_notas:
    #nota.tocar()
    print(nota.valorMIDI,nota.volume, nota.oitava,nota.instrumento,nota.bpm)
  
print ("vai trocar a musica")

geradorTeste.novaMusica('HDUGDUEGNKSNK,,OIO')

for nota in geradorTeste.lista_notas:
    #nota.tocar()
    print(nota.valorMIDI,nota.volume, nota.oitava,nota.instrumento,nota.bpm)