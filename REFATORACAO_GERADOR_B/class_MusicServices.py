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

        if self.gerador_notas.isMusicaPronta:
            self.isMusicaPronta = True
    
    def play(self):
        self.player = Player(self.musica)
        self.player.play()
        
    def pause(self):
        pass

    def gerarMidi(self):
        self.gerador_notas.gerarMidi()