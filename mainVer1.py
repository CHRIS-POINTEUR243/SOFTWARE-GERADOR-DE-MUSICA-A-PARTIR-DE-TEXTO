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
    def __init__(self, valorMIDI, oitava, bpm, volume, instrumento):
        self.valorMIDI = valorMIDI
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

    def tocar(self):
        midi_out.set_instrument(self.instrumento)
        midi_out.note_on(self.valorMIDI, self.volume)
        #volume vai de 0 a 127
        time.sleep(bpmToMilliseconds(self.bpm))
        #time.sleep() ajustar aqui o bpm
        midi_out.note_off(self.valorMIDI, self.volume)
        
class GeradorMusical:
    def __init__(self):
        self.lista_notas = []
        self.listaInstrumentos = []
        self.oitava_atual = OITAVA_DEFAULT
        self.volume_atual = VOLUME_DEFAULT
        self.bpm_atual = BPM_DEFAULT
        self.instrumento_atual = "ACOUSTIC_GRAND_PIANO"
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

    def mapeiaTexto(self, texto):
          #assim fica melhor pra tartar caso tenha mais de um caractere, 
    # ai so tem q colocar mais de um caractere na tabela e mudar a constante de quantiadae
        i = 0
        texto=texto.upper()
        nota = None
        comando_encontrado = False
        while i < len(texto):
            
            # Verifica da quantidade maxima ate a minima 1 
            for tamanhoString in range(QUANTIDADE_MAXIMA_DE_CARACTERES_FUNCAO, 0, -1):
                #se ja acabou o texto ou esta na tabela de funcoes
                if (i + (tamanhoString - 1) < len(texto)) and (texto[i:i+tamanhoString] in self.tabelaFuncoes):
                    comando = texto[i:i+tamanhoString]
                    self.obterFuncaoMusical(comando)
                    i += tamanhoString
                    comando_encontrado = True
                    break  #sai do for quando encontrar um comando na tabela
            
            if comando_encontrado:
                comando_encontrado = False
                continue  
                #ja achou o comando na tabela vai pro proximo caractere

            #n encontrou o comando ve se eh nota
            elif texto[i] in self.tabelaNotas:
                valorMIDI_mapeado = self.tabelaNotas[texto[i]]
                instrumento_mapeado = self.tabelaInstrumentos[self.instrumento_atual]
                #mapeio aqui instrumento e valorMIDI
                nota = self.setNota(valorMIDI_mapeado, instrumento_mapeado)
                i += 1
    
            #pra n dar problema com caracteres desconhecidos
            else:
                i += 1 
            # pra n dar problema caso n crie nota
            if nota is not None:
                self.lista_notas.append(nota)

    def obterFuncaoMusical(self, ch):
        funcaoMusical = self.tabelaFuncoes.get(ch)
        if funcaoMusical:
            return funcaoMusical()
        return None

    def setNota(self, valorMIDI_mapeado, instrumento_mapeado):
        nota = Nota(valorMIDI_mapeado + (DISTANCIA_OITAVA * self.oitava_atual), 
                    self.oitava_atual, 
                    self.bpm_atual, 
                    self.volume_atual, 
                    instrumento_mapeado)
        return nota

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
#----------------------------------------------------------------------------------------------CLASS PROCESSA TEXTO
class ProcessaTexto:
    def __init__(self, tabelaCaracteres,tabelaNotas,textoEntrada):
        self.tabela=tabelaCaracteres
        self.tabelaNotas=tabelaNotas
        self.texto=textoEntrada
        self.listaDeCaracteres=[]
      #le o texto e somente com os caracteres q tem na tabela ele cria uma lista
    def processaTextoEmLista(self):
        i = 0
        encontrou=False
        while i < len(self.texto):
        
            for tamanhoString in range(QUANTIDADE_MAXIMA_DE_CARACTERES_FUNCAO, 0, -1):
                if (i + tamanhoString <= len(self.texto)) and (self.texto[i:i+tamanhoString] in self.tabela):
                    self.listaDeCaracteres.append(self.texto[i:i+tamanhoString])
                    i += tamanhoString
                    encontrou = True
                    break
            
            if encontrou:
                encontrou = False
                continue
            elif self.texto[i] in self.tabelaNotas:
                self.listaDeCaracteres.append(self.texto[i]) 
                i += 1
            else:
                i += 1
        
        return self.listaDeCaracteres
    
#-----------------------------------------------------------------------------------MAIN

GeradorTeste = GeradorMusical()
texto = ProcessaTexto(GeradorTeste.tabelaFuncoes,GeradorTeste.tabelaNotas,"ABABABPM+'++==0AEE,EE")
texto.processaTextoEmLista()
print (texto.listaDeCaracteres)

listaNotas = []
GeradorTeste.mapeiaTexto(texto.listaDeCaracteres)
listaNotas = GeradorTeste.lista_notas

for nota in listaNotas:
    #nota.tocar()
    print(nota.valorMIDI,nota.volume, nota.oitava,nota.instrumento,nota.bpm)


