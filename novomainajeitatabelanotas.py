import pygame
import pygame.midi
import os
import time
import random
from midiutil import MIDIFile

pygame.init()
pygame.mixer.init()
pygame.midi.init()

port = pygame.midi.get_default_output_id()
midi_out = pygame.midi.Output(port, 0)

QUANTIDADE_MAXIMA_DE_CARACTERES_FUNCAO = 4
DISTANCIA_OITAVA = 12
NOTA_DEFAULT = 'C'
OITAVA_DEFAULT = 0
VOLUME_DEFAULT = 127  # máximo
BPM_DEFAULT = 120
MINUTO = 60
UNIDADE_BPM = 80
# oitava eh +12 ou -12, então 12n onde n pertence aos inteiros

def bpmToMilliseconds(bpm):
    tempo = 1 / (bpm / MINUTO)
    return tempo

class Nota:
    def __init__(self, caractere, oitava, bpm, volume, instrumento):
        self.caractere = caractere
        # esse valor vem da tabela General MIDI (pygame.midi)
        # onde o dó central é o C4 = 60
        self.oitava = oitava
        # ex: +1, 0, -1, -2
        self.bpm = bpm
        # delay entre note on / note off (bpm da nota)
        self.volume = volume
        # 0 a 127
        self.instrumento = instrumento
        # um dos inseridos na tabela de instrumentos
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
            self.valorMIDI = None 

    def tocar(self):
        if self.valorMIDI is not None:
            notaMIDI = self.valorMIDI + (DISTANCIA_OITAVA * self.oitava)
            midi_out.set_instrument(self.instrumento)
            midi_out.note_on(notaMIDI, self.volume)
            time.sleep(bpmToMilliseconds(self.bpm))
            midi_out.note_off(notaMIDI, self.volume)
        else:
            pass

class GeradorMusical:
    def __init__(self,texto):
        self.lista_notas = []
        self.listaInstrumentos = []
        self.oitava_atual = OITAVA_DEFAULT
        self.volume_atual = VOLUME_DEFAULT
        self.bpm_atual = BPM_DEFAULT
        self.instrumento_atual = "ACOUSTIC_GRAND_PIANO"
        self.tabelaNotas = ['A','B','C','D','E','F','G','H']

        self.tabelaFuncoes = {
            ' ': self.dobraVolume,
            '+': self.aumentaOitava,
            '-': self.diminuiOitava,
            'O': self.notaOuTelefone,
            'I': self.notaOuTelefone,
            'U': self.notaOuTelefone,
            '?': self.notaAleatoria,
            '%': self.trocaInstrumentoAleatorio,
            'BPM+': self.aumentaBPM,
            'BPM-': self.diminuiBPM,
            ';': self.silencio,
        }

        self.tabelaInstrumentos = {
            'ACOUSTIC_GRAND_PIANO': 0,
            'BRIGHT_ACOUSTIC_PIANO': 1,
            'ELECTRIC_GRAND_PIANO': 2,
            'HONKY_TONK_PIANO': 3,
            'RHODES_PIANO': 4,
            'CHORUSED_PIANO': 5,
            'HARPSICHORD': 6,
            'CLAVINET': 7,
            'ACOUSTIC_NYLON_GUITAR': 24,
            'ACOUSTIC_STEEL_GUITAR': 25,
            'ELECTRIC_JAZZ_GUITAR': 26,
            'ELECTRIC_CLEAN_GUITAR': 27,
            'ELECTRIC_MUTED_GUITAR': 28,
            'OVERDRIVEN_GUITAR': 29,
            'DISTORTION_GUITAR': 30,
            'GUITAR_HARMONICS': 31,
            'ACOUSTIC_BASS': 32,
            'FINGERED_ELECTRIC_BASS': 33,
            'PLUCKED_ELECTRIC_BASS': 34,
            'FRETLESS_BASS': 35,
            'SLAP_BASS_1': 36,
            'SLAP_BASS_2': 37,
            'SYNTH_BASS_1': 38,
            'SYNTH_BASS_2': 39,
            'TELEPHONE_RING': 124,  # telefone tocando
        }
        self.listaCaracteres=[]
        self.idxChar = 0    
        self.processaTextoEmLista(texto)

        self.lista_notas=[]
        self.mapeiaTexto()	
        #aqui eh so chamar o metodo na função init, ele mesmp ja preenche a lista notas, n retornando nada

    def novaMusica(self,texto):
        self.processaTextoEmLista(texto)
        self.mapeiaTexto()
       

    def mapeiaTexto(self):
        # percorre a lista de tokens já processados
        self.idxChar = 0   
        for comando in self.listaCaracteres:
            nota = None

            ## vogais O/I/U – regra especial:
            #if comando in ('O', 'I', 'U'):
            #    # se token anterior é nota (A–H), repete nota
            #    if idx > 0 and self.listaCaracteres[idx - 1] in self.tabelaNotas:
            #        self.repeteNota()
            #    else:
            #        # senão, toca telefone
            #        self.tocaTelefone()
            #    continue

            if comando in self.tabelaFuncoes:
                self.obterFuncaoMusical(comando)
            else:
                nota=Nota(comando,self.oitava_atual,self.bpm_atual,self.volume_atual,self.tabelaInstrumentos.get(self.instrumento_atual))
                
            if nota is not None:
                self.lista_notas.append(nota)

            self.idxChar += 1

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
        if volume_dobrado <= 127:
            self.volume_atual = volume_dobrado
        else:
            self.volume_atual = 127

    def aumentaOitava(self):
        self.oitava_atual += 1

    def diminuiOitava(self):
        self.oitava_atual -= 1

    #def trocaInstrumento(self):
    #    iterador = iter(self.tabelaInstrumentos)
    #    prox_instrumento = self.instrumento_atual
    #    for chave in iterador:
    #        if chave == self.instrumento_atual:
    #            prox_instrumento = next(iterador, self.instrumento_atual)
    #            break
    #    self.instrumento_atual = prox_instrumento

    def trocaInstrumentoAleatorio(self):
        novo_instrumento = random.choice(list(self.tabelaInstrumentos.keys()))
        while novo_instrumento == self.instrumento_atual:
            novo_instrumento = random.choice(list(self.tabelaInstrumentos.keys()))
        self.instrumento_atual = novo_instrumento

    def notaAleatoria(self):
        letra = random.choice(self.tabelaNotas)
        nota=Nota(letra,self.oitava_atual,self.bpm_atual,self.volume_atual,self.tabelaInstrumentos.get(self.instrumento_atual))
        if nota is not None:
                self.lista_notas.append(nota)

    def repeteNota(self):
        #return self.lista_notas[-1]
        print(self.listaCaracteres)
        print(self.listaCaracteres[-2])
        nota=Nota(self.listaCaracteres[-2],
                  self.oitava_atual,
                  self.bpm_atual,
                  self.volume_atual,
                  self.tabelaInstrumentos.get(self.instrumento_atual))
        return nota

    def tocaTelefone(self):
        som_telefone = 'TELEPHONE_RING'
        letra = NOTA_DEFAULT
        nota=Nota(letra,self.oitava_atual,self.bpm_atual,self.volume_atual,self.tabelaInstrumentos.get(som_telefone))
        return nota
    
    def notaOuTelefone(self):
        idx = self.idxChar
        if idx == 0:
            self.lista_notas.append(self.tocaTelefone())
            return

        ant = self.listaCaracteres[idx - 1]  
        nota = self.repeteNota()
        
        if ant in nota.tabelaNotas:
            self.lista_notas.append(nota)
        else:
            nota = Nota
            self.lista_notas.append(self.tocaTelefone())

    def aumentaBPM(self):
        self.bpm_atual += UNIDADE_BPM

    def diminuiBPM(self):
        self.bpm_atual -= UNIDADE_BPM

    def silencio(self):
        volume_zerado = 0
        nota=Nota('C',self.oitava_atual,self.bpm_atual,volume_zerado,self.tabelaInstrumentos.get(self.instrumento_atual))
        if nota is not None:
            self.lista_notas.append(nota)
        
    def salvarParaMidi(self, nome_arquivo="musica_gerada.mid"):
        midi = MIDIFile(1)
        midi.addTrackName(0, 0, "Música Gerada")
        midi.addTempo(0, 0, BPM_DEFAULT)
            
        tempoAtual = 0
            
        for nota in self.lista_notas:
            if nota.valorMIDI is not None:
                if nota.volume > 0:
            
                    instrumento_midi = nota.instrumento
                    midi.addProgramChange(0, 0, tempoAtual, instrumento_midi)
                    frequencia = nota.valorMIDI + (nota.oitava * DISTANCIA_OITAVA)

                    duracao = bpmToMilliseconds(nota.bpm)

                    midi.addNote(0, 0, frequencia, tempoAtual, duracao, nota.volume)
                    tempoAtual += duracao
                else:
                    #nota com volume 0 = silencio
                    duracao = bpmToMilliseconds(nota.bpm)
                    tempoAtual += duracao
#
# -----------------------------------------------------------------------------------
# TESTES
if __name__ == "__main__":
    
    def roda_teste(texto, descricao):
        print (descricao)
        gm= GeradorMusical(texto)
        # resetar estado do gerador

        for n in gm.lista_notas:
            print(
                "notaMIDI:", n.valorMIDI,
                "vol:", n.volume,
                "oit:", n.oitava,
                "inst:", n.instrumento,
                "bpm:", n.bpm,
            )

        #  ouvir som tocar aqui 
        for n in gm.lista_notas:
             n.tocar()
        gm.salvarParaMidi(descricao)

    # testes aqui para acompanhar:
    roda_teste("AABB", "Notas simples A e B")
    roda_teste("AO", "O depois de nota (repete A)")
    roda_teste("C+O", "O sem nota anterior (telefone)")
    roda_teste("C???", "? gerando notas aleatórias entre A–H")
    roda_teste("C;;C", "Silêncio com ';' entre duas notas")
    roda_teste("CBPM+CCCBPM-CC++CC---CC", "Aumento/diminuição do bpm + oitavas")
    roda_teste("CC%CC%CC%CC%CC", "Troca instrumentos aleatoriamente")
    roda_teste("CCBPM+CC++CC", "Troca instrumentos aleatoriamente")
    roda_teste("AOOAO", "Troca instrumentos aleatoriamente")