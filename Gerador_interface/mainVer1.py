import pygame
import pygame.midi
import os
import time
import random

pygame.init()
pygame.mixer.init()
pygame.midi.init()

port = pygame.midi.get_default_output_id()
midi_out = pygame.midi.Output(port, 0)

QUANTIDADE_MAXIMA_DE_CARACTERES_FUNCAO = 5
DISTANCIA_OITAVA = 12
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
    def __init__(self, valorMIDI, oitava, bpm, volume, instrumento):
        self.valorMIDI = valorMIDI
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

    def tocar(self):
        midi_out.set_instrument(self.instrumento)
        midi_out.note_on(self.valorMIDI, self.volume)
        time.sleep(bpmToMilliseconds(self.bpm))
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
            'O': self.notaOuTelefone,
            'I': self.notaOuTelefone,
            'U': self.notaOuTelefone,
            '?': self.notaAleatoria,
            '%': self.trocaInstrumento,
            'BPM+': self.aumentaBPM,
            'BPM-': self.diminuiBPM,
            ';': self.silencio,
        }

        self.tabelaNotas = {
            'A': 69,
            'B': 71,
            'C': 60,
            'D': 62,
            'E': 64,
            'F': 65,
            'G': 67,
            'H': 70,
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

    def mapeiaTexto(self, listaDeCaracteres):
        # percorre a lista de tokens já processados
        for idx, comando in enumerate(listaDeCaracteres):
            nota = None

            # vogais O/I/U – regra especial:
            if comando in ('O', 'I', 'U'):
                # se token anterior é nota (A–H), repete nota
                if idx > 0 and listaDeCaracteres[idx - 1] in self.tabelaNotas:
                    self.repeteNota()
                else:
                    # senão, toca telefone
                    self.tocaTelefone()
                continue

            # comandos gerais (espaço, BPM, +, -, %, ;)
            if comando in self.tabelaFuncoes:
                self.obterFuncaoMusical(comando)

            # notas A–H
            elif comando in self.tabelaNotas:
                valorMIDI_mapeado = self.tabelaNotas[comando]
                instrumento_mapeado = self.tabelaInstrumentos[self.instrumento_atual]
                nota = self.setNota(valorMIDI_mapeado, instrumento_mapeado)

            # se criou nota, guarda
            if nota is not None:
                self.lista_notas.append(nota)

    def obterFuncaoMusical(self, ch):
        funcaoMusical = self.tabelaFuncoes.get(ch)
        if funcaoMusical:
            return funcaoMusical()
        return None

    def setNota(self, valorMIDI_mapeado, instrumento_mapeado):
        nota = Nota(
            valorMIDI_mapeado + (DISTANCIA_OITAVA * self.oitava_atual),
            self.oitava_atual,
            self.bpm_atual,
            self.volume_atual,
            instrumento_mapeado,
        )
        return nota

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

    def trocaInstrumento(self):
        iterador = iter(self.tabelaInstrumentos)
        prox_instrumento = self.instrumento_atual
        for chave in iterador:
            if chave == self.instrumento_atual:
                prox_instrumento = next(iterador, self.instrumento_atual)
                break
        self.instrumento_atual = prox_instrumento

    def repeteNota(self):
        if self.lista_notas:
            self.lista_notas.append(self.lista_notas[-1])

    def notaAleatoria(self):
        # escolhe uma letra entre A–H
        letra = random.choice(list(self.tabelaNotas.keys()))
        valorMIDI_mapeado = self.tabelaNotas[letra]
        instrumento_mapeado = self.tabelaInstrumentos[self.instrumento_atual]
        nota = self.setNota(valorMIDI_mapeado, instrumento_mapeado)
        self.lista_notas.append(nota)

    def notaOuTelefone(self):
        # este método não é usado diretamente, deixei pra compatibilidade na tabelaFuncoes
        # a lógica real está em mapeiaTexto (onde temos idx pra ver o anterior)
        pass

    def tocaTelefone(self):
        telefone_instr = self.tabelaInstrumentos['TELEPHONE_RING']
        # escolhi Dó central como nota base do telefone
        valorMIDI_mapeado = self.tabelaNotas['C']
        nota = self.setNota(valorMIDI_mapeado, telefone_instr)
        self.lista_notas.append(nota)

    def aumentaBPM(self):
        self.bpm_atual += UNIDADE_BPM

    def diminuiBPM(self):
        self.bpm_atual -= UNIDADE_BPM

    def silencio(self):
        # não adiciona nota nenhuma = pausa
        pass


# ------------------------------------------------------------------------------------
# CLASS PROCESSA TEXTO
class ProcessaTexto:
    def __init__(self, tabelaCaracteres, tabelaNotas, textoEntrada):
        self.tabela = tabelaCaracteres
        self.tabelaNotas = tabelaNotas
        self.texto = textoEntrada
        self.listaDeCaracteres = []

    # lê o texto e somente com os caracteres q tem na tabela ele cria uma lista
    def processaTextoEmLista(self):
        i = 0
        encontrou = False
        while i < len(self.texto):

            for tamanhoString in range(QUANTIDADE_MAXIMA_DE_CARACTERES_FUNCAO, 0, -1):
                if (i + tamanhoString <= len(self.texto)) and (self.texto[i:i + tamanhoString] in self.tabela):
                    self.listaDeCaracteres.append(self.texto[i:i + tamanhoString])
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


# -----------------------------------------------------------------------------------
# TESTES

if __name__ == "__main__":
    gm = GeradorMusical()

    def roda_teste(texto, descricao):
        proc = ProcessaTexto(gm.tabelaFuncoes, gm.tabelaNotas, texto)
        proc.processaTextoEmLista()
        print(f"\n=== {descricao} ===")
        print("Entrada:", repr(texto))
        print("Tokens:", proc.listaDeCaracteres)

        # resetar estado do gerador
        gm.lista_notas = []
        gm.oitava_atual = OITAVA_DEFAULT
        gm.volume_atual = VOLUME_DEFAULT
        gm.bpm_atual = BPM_DEFAULT
        gm.instrumento_atual = "ACOUSTIC_GRAND_PIANO"

        gm.mapeiaTexto(proc.listaDeCaracteres)

        for n in gm.lista_notas:
            print(
                "notaMIDI:", n.valorMIDI,
                "vol:", n.volume,
                "oit:", n.oitava,
                "inst:", n.instrumento,
                "bpm:", n.bpm,
            )

        #  ouvir son tocar aqui 
        for n in gm.lista_notas:
             n.tocar()


    # testes aqui para acompanhar:
    roda_teste("AB", "Notas simples A e B")
    roda_teste("AO", "O depois de nota (repete A)")
    roda_teste("XO", "O sem nota anterior (telefone)")
    roda_teste("C?C?C?", "? gerando notas aleatórias entre A–H")
    roda_teste("C ; C", "Silêncio com ';' entre duas notas")
