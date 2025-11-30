from enum_Valores import ValoresNotas,Tokens,MAX_LEN_TOKEN

class Parser:
    def __init__(self,texto):
        self.texto = texto.upper()
        self.lista_tokens=[]
        self.lista_tokens = self.textoParaTokens()
    
    def textoParaTokens(self):
        i = 0
        #encontrou=False
        tamanhoTexto=len(self.texto)
        while i < tamanhoTexto:
            encontrou = False
            #for tamanhoString in range(tamanhoTexto,0,-1)
            for tamanhoString in range(min(MAX_LEN_TOKEN,tamanhoTexto-i),0,-1):
                if (i + tamanhoString <= len(self.texto)):
                    token = self.texto[i:i+tamanhoString]
                    try:
                        comando = Tokens(token)
                        self.lista_tokens.append(token)
                        i += tamanhoString
                        encontrou = True
                        break
                    except ValueError:
                        pass
                    if token in ValoresNotas.__members__:
                        self.lista_tokens.append(token)
                        i += tamanhoString
                        encontrou = True
                        break     
            if encontrou:
                encontrou = False
                continue
            else:
                i += 1

        print(self.lista_tokens)
        return self.lista_tokens