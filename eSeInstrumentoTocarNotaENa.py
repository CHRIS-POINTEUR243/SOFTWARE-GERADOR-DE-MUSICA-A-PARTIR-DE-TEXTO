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


DISTANCIA_OITAVA = 12
NOTA_DEFAULT = 'C'
OITAVA_DEFAULT = 0
VOLUME_DEFAULT = 127  # máximo
BPM_DEFAULT = 120
MINUTO = 60
UNIDADE_BPM = 80
# oitava eh +12 ou -12, então 12n onde n pertence aos inteiros



class Bpm:
    def __init__(self,bpm):
        self.bpm=bpm
    def getMilliseconds(self):
        tempo = 1 / (self.bpm / MINUTO)
        return tempo
class Nota:
    tabelaNotas = {
            'A': 69 ,
            'B': 71 ,
            'C': 60 ,
            'D': 62 ,
            'E': 64 ,
            'F': 65 ,
            'G': 67 ,
            'H': 70 
    }
    def __init__(self, caractere):
    
        if caractere in Nota.tabelaNotas:
            self.valorMIDI = Nota.tabelaNotas[caractere]
        else:
            self.valorMIDI = None 
  


class Instrumento:
    tabelaInstrumentos = {
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
        'TELEPHONE_RING': 124, 
    }
    def __init__(self, caractere, oitava, bpm, volume, instrumento):
        #pode colocar no init os volumes, oitavas instrumento inicial
        self.nota = Nota(caractere)
        # esse valor vem da tabela General MIDI (pygame.midi)
        # onde o dó central é o C4 = 60
        self.oitava = oitava
        # ex: +1, 0, -1, -2
        self.bpm = bpm
        # delay entre note on / note off (bpm da nota)
        self.volume = volume
        # 0 a 127
        self.instrumento = instrumento
    '''
    
    def tocar(self):
        if self.valorMIDI is not None:
            notaMIDI = self.valorMIDI + (DISTANCIA_OITAVA * self.oitava)
            instrumento_numero = Instrumento.tabelaInstrumentos.get(self.instrumento, 0)
            midi_out.set_instrument(instrumento_numero) 
            midi_out.note_on(notaMIDI, self.volume)
            time.sleep(Bpm(self.bmp).getMilliseconds())
            #time.sleep(bpmToMilliseconds(self.bpm))
            midi_out.note_off(notaMIDI, self.volume)
        else:
            pass
            '''
    def tocar(self):
        
        if self.nota.valorMIDI is not None:
            notaMIDI = self.nota.valorMIDI + (DISTANCIA_OITAVA * self.oitava)
            instrumento_numero = Instrumento.tabelaInstrumentos.get(self.instrumento, 0)
            midi_out.set_instrument(instrumento_numero)
            midi_out.note_on(notaMIDI, self.volume)
            time.sleep(Bpm(self.bpm).getMilliseconds())  
            midi_out.note_off(notaMIDI, self.volume)




class Musica:
    def __init__(self,texto,instrumento="ACOUSTIC_GRAND_PIANO",oitava=OITAVA_DEFAULT,volume=VOLUME_DEFAULT,bpm=BPM_DEFAULT):
        self.lista_instrumentos = []
        self.listaInstrumentos = []
        self.oitava_atual = oitava
        self.volume_atual = volume
        self.bpm_atual = bpm
        self.instrumento_atual = instrumento
       # self.notaAtual

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
    

        self.listaCaracteres=[]
        self.idxChar = 0    
        #self.processaTextoEmLista(texto)
        self.juncaoDasTabelas = {**Nota.tabelaNotas, **self.tabelaFuncoes}
        if texto:
            self.novaMusica(texto)

     


    def novaMusica(self,texto):
        parser =Parcer(self.juncaoDasTabelas,texto)
        self.listaCaracteres=parser.geraTokens()
        self.TokensParaListaDeNotas()


    def TokensParaListaDeNotas(self):
        self.idxChar = 0
        self.lista_instrumentos = [] 
        
        for comando in self.listaCaracteres:
           
            if comando in self.tabelaFuncoes:
                self.obterFuncaoMusical(comando)
            else:
                
                instrumento = Instrumento(comando, self.oitava_atual, self.bpm_atual, 
                                        self.volume_atual, self.instrumento_atual)
                self.lista_instrumentos.append(instrumento)
            
            self.idxChar += 1

    def obterFuncaoMusical(self, ch):
        funcaoMusical = self.tabelaFuncoes.get(ch)
        if funcaoMusical:
            return funcaoMusical()
        return None


        
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

    def trocaInstrumentoAleatorio(self):
        novo_instrumento = random.choice(list(Instrumento.tabelaInstrumentos.keys()))
        while novo_instrumento == self.instrumento_atual:
            novo_instrumento = random.choice(list(Instrumento.tabelaInstrumentos.keys()))
        self.instrumento_atual = novo_instrumento

    def notaAleatoria(self):
        letra = random.choice(list(Nota.tabelaNotas.keys()))
        instrumento = Instrumento(letra,
                  self.oitava_atual,
                  self.bpm_atual,
                  self.volume_atual,
                  self.instrumento_atual)
        if instrumento  is not None:
                self.lista_instrumentos.append(instrumento)

    def repeteNota(self):
        instrumento =  Instrumento (self.listaCaracteres[-2],
                  self.oitava_atual,
                  self.bpm_atual,
                  self.volume_atual,
                  self.instrumento_atual)
        return instrumento 

    def tocaTelefone(self):
        som_telefone = 'TELEPHONE_RING'
        instrumento = Instrumento (NOTA_DEFAULT,
                    self.oitava_atual,
                    self.bpm_atual,
                    self.volume_atual,
                    som_telefone)
        return instrumento 
    
    def notaOuTelefone(self):
        idx = self.idxChar
        if idx == 0:
            self.lista_instrumentos.append(self.tocaTelefone())
            return

        ant = self.listaCaracteres[idx - 1]  
        
        if ant in Nota.tabelaNotas:
            nota_repetida = self.repeteNota()
            if nota_repetida:
                self.lista_instrumentos.append(nota_repetida)
        else:
            self.lista_instrumentos.append(self.tocaTelefone())

    def aumentaBPM(self):
        self.bpm_atual += UNIDADE_BPM

    def diminuiBPM(self):
        self.bpm_atual -= UNIDADE_BPM

    def silencio(self):
        volume_zerado = 0
        instrumento  = Instrumento (NOTA_DEFAULT,
                    self.oitava_atual,
                    self.bpm_atual,
                    volume_zerado,
                    self.instrumento_atual)
        if instrumento  is not None:
            self.lista_instrumentos.append(instrumento)
            
    def salvarParaMidi(self, nome_arquivo="musica_gerada.mid"):
        midi = MIDIFile(1)
        midi.addTrackName(0, 0, "Música Gerada")
        midi.addTempo(0, 0, self.bpm_atual)
            
        tempoAtual = 0
            
        for instrumento  in self.lista_instrumentos:
            if instrumento.nota.valorMIDI is not None:
                # Converter instrumento
                if isinstance(instrumento.instrumento, str):
                    instrumento_midi = Instrumento.tabelaInstrumentos[instrumento.instrumento]
                else:
                    instrumento_midi = instrumento.instrumento
                
                midi.addProgramChange(0, 0, tempoAtual, instrumento_midi)
                frequencia = instrumento .valorMIDI + (instrumento.oitava * DISTANCIA_OITAVA)
                
                # Converter duração de segundos para beats
                duracao_segundos = Bpm(instrumento.bpm).getMilliseconds
                duracao_beats = duracao_segundos * (self.bpm_atual / 60.0)
                
                midi.addNote(0, 0, frequencia, tempoAtual, duracao_beats, instrumento.volume)
                tempoAtual += duracao_beats
            
        with open(nome_arquivo, "wb") as f:
            midi.writeFile(f)
            
        print("Música foi salva como", nome_arquivo)
# -----------------------------------------------------------------------------------
# TESTES

class Parcer:
    def __init__(self, tabela=None, texto=None):
        self.tabela = tabela or {}
        self.texto = texto or ""
        self.listaCaracteres = []
    
    def setTexto(self, novoTexto):
        self.texto = novoTexto
    
    def setTabela(self, novaTabela):
        self.tabela = novaTabela

    def geraTokens(self):
        i = 0
        while i < len(self.texto):
            encontrou = False
            
            # Procura tokens multi-caractere
            for tamanhoString in range(min(4, len(self.texto) - i), 0, -1):
                candidato = self.texto[i:i+tamanhoString]
                if candidato in self.tabela:
                    self.listaCaracteres.append(candidato)
                    i += tamanhoString
                    encontrou = True
                    break
            
            if not encontrou:
                i += 1  # Ignora caracteres desconhecidos
                
        return self.listaCaracteres
    
class Arquivos:
    def leArquivoTxt(self, nome_arquivo):
        try:
            with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
                return arquivo.read()
        except FileNotFoundError:
            print(f"Arquivo ",nome_arquivo," não encontrado!")
            return ""
        except Exception as erro:
            print(f"Erro ao ler arquivo: ",erro)
            return ""
        
   

if __name__ == "__main__":
    
    def roda_teste(texto, descricao):
        print (descricao)
        gm = Musica(texto)
        # resetar estado do gerador

        for n in gm.lista_instrumentos:
            print(
                "notaMIDI:", n.nota.valorMIDI,
                "vol:", n.volume,
                "oit:", n.oitava,
                "inst:", n.instrumento,
                "bpm:", n.bpm,
            )

        for n in gm.lista_instrumentos:
            n.tocar()
        gm.salvarParaMidi(descricao)

#Testes
    roda_teste("BAAAAAAA", "Notajhasdjs.mid")




