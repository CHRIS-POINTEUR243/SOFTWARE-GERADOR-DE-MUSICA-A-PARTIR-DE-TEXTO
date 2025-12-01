#Aciona Parser, GeradorNotas e Player de acordo com demanda de UI

from class_Parser import Parser
from class_GeradorNotas import GeradorNotas
from class_Player import Player

class MusicServices:
    def __init__(self,texto,instrumento,oitava,volume,bpm):
        self.musica = []
        self.isMusicaPronta = False

        self.parser = Parser(texto)
        self.gerador_notas = GeradorNotas(self.parser.lista_tokens,instrumento,oitava,volume,bpm)
        self.musica = self.gerador_notas.lista_notas
        self.player = None
        #Imediatamente ao ser acionado, instancia e executa parser e gerador de notas
        #Player estático 

        if self.gerador_notas.isMusicaPronta:
            self.isMusicaPronta = True
    
    def play(self):
        self.player = Player(self.musica)
        self.player.play()

    def gerarMidi(self):
        sucesso = self.gerador_notas.gerarMidi()
        if sucesso:
            return True
        else:
            return False
    #Aciona GeradorNotas