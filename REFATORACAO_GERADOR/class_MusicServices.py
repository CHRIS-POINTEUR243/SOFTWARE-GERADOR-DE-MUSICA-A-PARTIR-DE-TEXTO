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

        if self.gerador_notas.isMusicaPronta:
            self.isMusicaPronta = True

        if self.isMusicaPronta:
            self.play()
    
    def play(self):
        player = Player(self.musica)
        player.play()