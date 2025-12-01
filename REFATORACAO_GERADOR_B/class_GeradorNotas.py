#RECEBE LISTA DE TOKENS vinda de Parser e RETORNA LISTA DE NOTAS

import random
from midiutil import MIDIFile

from class_Nota import Nota,NOTA_DEFAULT
from enum_Valores import Tokens,ValoresNotas,ValoresInstrumentos
from class_Utilidades import Utilidades,DISTANCIA_OITAVA,UNIDADE_BPM

class GeradorNotas:
    def __init__(self,lista_tokens,instrumento,oitava,volume,bpm):
        self.lista_tokens = lista_tokens
        self.lista_notas = []
        self.oitava_atual = oitava
        self.volume_atual = volume
        self.bpm_atual = bpm
        self.instrumento_atual = instrumento
        self.idxChar = 0    
        self.isMusicaPronta = False

        self.TokensParaComandos = {
            Tokens.ESPACO: self.dobraVolume,
            Tokens.MAIS: self.aumentaOitava,
            Tokens.MENOS: self.diminuiOitava,
            Tokens.LETRA_O: self.notaOuTelefone,
            Tokens.LETRA_I: self.notaOuTelefone,
            Tokens.LETRA_U: self.notaOuTelefone,
            Tokens.INTERROGACAO: self.notaAleatoria,
            Tokens.BPM_MAIS: self.aumentaBPM,
            Tokens.BPM_MENOS: self.diminuiBPM,
            Tokens.PONTO_VIRGULA: self.silencio,
            Tokens.NOVA_LINHA: self.trocaInstrumentoAleatoriamente,  
        }
        #Define o mapeamento de tokens para métodos de gerador

        self.tokensParaNotas()	

    def tokensParaNotas(self):
        self.idxChar = 0   
        for token in self.lista_tokens:
            nota = None
            comando = None

            try:
                comando = Tokens(token)
            except ValueError:
                pass

            if comando is not None and comando in self.TokensParaComandos:
                funcao_musical = self.TokensParaComandos[comando]
                if funcao_musical:
                    funcao_musical()

            elif (token in ValoresNotas.__members__):
                nota=Nota(token,
                    self.oitava_atual,
                    self.bpm_atual,
                    self.volume_atual,
                    self.instrumento_atual)
                
            if nota is not None:
                self.lista_notas.append(nota)

            self.idxChar += 1

        self.gerarMidi()
        self.isMusicaPronta = True
    #Percorre a lista de tokens já processados por Parser
        
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

    def trocaInstrumentoAleatoriamente(self):
        novo_instrumento = random.choice(list(ValoresInstrumentos))
        while novo_instrumento == self.instrumento_atual:
            novo_instrumento = random.choice(list(ValoresInstrumentos))
        self.instrumento_atual = novo_instrumento.name

    def notaAleatoria(self):
        letra = random.choice(list(ValoresNotas))
        nota = Nota(letra.name,
                  self.oitava_atual,
                  self.bpm_atual,
                  self.volume_atual,
                  self.instrumento_atual)
        if nota is not None:
                self.lista_notas.append(nota)

    def repeteNota(self,ant):
        nota = Nota(ant,
                    self.oitava_atual,
                    self.bpm_atual,
                    self.volume_atual,
                    self.instrumento_atual)
        return nota

    def tocaTelefone(self):
        som_telefone = 'TELEPHONE_RING'
        nota = Nota(NOTA_DEFAULT,
                    self.oitava_atual,
                    self.bpm_atual,
                    self.volume_atual,
                    som_telefone)
        return nota
    
    def notaOuTelefone(self):
        idx = self.idxChar
        if idx == 0:
            self.lista_notas.append(self.tocaTelefone())
            return

        ant = self.lista_tokens[idx - 1]  

        if ant in ValoresNotas.__members__:
            nota_repetida = self.repeteNota(ant)
            if nota_repetida:
                self.lista_notas.append(nota_repetida)
        else:
            self.lista_notas.append(self.tocaTelefone())

    def aumentaBPM(self):
        self.bpm_atual += UNIDADE_BPM

    def diminuiBPM(self):
        novo_bpm = self.bpm_atual + UNIDADE_BPM
        if novo_bpm > 0:
            self.bpm_atual -= UNIDADE_BPM
        else:
            pass
        #Deixa igual caso contrário

    def silencio(self):
        volume_zerado = 0
        nota = Nota(NOTA_DEFAULT,
                    self.oitava_atual,
                    self.bpm_atual,
                    volume_zerado,
                    self.instrumento_atual)
        if nota is not None:
            self.lista_notas.append(nota)
            
    def gerarMidi(self, nome_arquivo="musica_gerada.mid"):
        midi = MIDIFile(1)
        midi.addTrackName(0, 0, "Música Gerada")
        midi.addTempo(0, 0, self.bpm_atual)     
        tempoAtual = 0
            
        for nota in self.lista_notas:
            if nota.valorMIDI is not None:
                if isinstance(nota.instrumento, str):
                    instrumento_midi = ValoresInstrumentos[nota.instrumento].value
                else:
                    instrumento_midi = nota.instrumento
                #Converte instrumento
                
                midi.addProgramChange(0, 0, tempoAtual, instrumento_midi)
                frequencia = nota.valorMIDI + (nota.oitava * DISTANCIA_OITAVA)
                
                duracao_segundos = Utilidades.bpmParaMilisegundos(nota.bpm)
                duracao_beats = duracao_segundos * (self.bpm_atual / 60.0)
                #Converte duração de segundos para batidas
                
                midi.addNote(0, 0, frequencia, tempoAtual, duracao_beats, nota.volume)
                tempoAtual += duracao_beats
        try:    
            with open(nome_arquivo, "wb") as f:
                midi.writeFile(f)
            print(f"Arquivo MIDI '{nome_arquivo}' gerado com sucesso.")
            return True
        except Exception as erro:
            print(f"Erro ao gerar arquivo '{nome_arquivo}': ", erro)
            return False
        #Retorna True se o arquivo foi gerado com sucesso
            
