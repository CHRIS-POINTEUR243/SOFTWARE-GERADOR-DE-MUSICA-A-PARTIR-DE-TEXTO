#Interface de usuário
#Aciona music services de acordo com input do usuário

import streamlit as st
from class_MusicServices import MusicServices
from enum_Valores import ValoresInstrumentos
import base64  
import os 

OITAVA_DEFAULT = 0
VOLUME_DEFAULT = 127  
BPM_DEFAULT = 120
INSTRUMENTO_DEFAULT = ValoresInstrumentos.ACOUSTIC_GRAND_PIANO.name
#Valores padrões para os parâmetros que o usuário pode escolher na interface

opcoes_oitava = [-5,-4,-3,-2,-1,0,1,2,3,4,5]
#Tomando dó central = C4 como oitava 0
opcoes_instrumentos = [inst.name for inst in ValoresInstrumentos]
#Alterável em ValoresInstrumentos

class UI:
    def __init__(self):
        self.music_services = None
        self.texto_converter = None

        st.set_page_config(page_title="Gerador de Música", page_icon="🎵")
        #Nome na aba da interface

        self.inicializaImagem()
        self.inicializaCabecalho()

    def inicializaImagem(self):
        path_imagem = "foto.jpg"
        if not os.path.exists(path_imagem):
            st.error(f"Arquivo não encontrado: {path_imagem}")
            return
        with open("foto.jpg", "rb") as image:  
            encoded = base64.b64encode(image.read()).decode()

        css = f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
        #Tratamento da imagem no fundo da interface

    def inicializaCabecalho(self):
        st.markdown(
            "<h1 style='text-align:center;'>Gerador de Música</h1>",
            unsafe_allow_html=True,
        )
        st.write("")

        if "screen" not in st.session_state:
            st.session_state.screen = "tela_input" 
        if st.session_state.screen == "tela_input":
            self.telaGerador()
        elif st.session_state.screen == "tela_player":
            self.telaPlayer()

    def mudaTela(self,nome_tela):
        if nome_tela == "tela_input":
            st.session_state.tela_player_carregada = False
            st.session_state.midi_try = False
            st.session_state.midi_sucesso = None
            st.session_state.texto_digitado = self.texto_converter
            #Reseta lógica de download do arquivo MIDI e mantém o texto previamente inserido
        st.session_state.screen = nome_tela
        st.rerun()

    def atualizaTexto(self):
        pass

    def telaGerador(self):
        st.write("Transforma texto em música!")
        st.write("")

        arquivo_texto = st.file_uploader("Carregue um arquivo texto:",type=["txt"])
        conteudo_arquivo = None

        if arquivo_texto is not None:
            conteudo_arquivo = arquivo_texto.read().decode("utf-8")
            st.session_state.input_texto = conteudo_arquivo
            st.session_state.nome_arquivo_texto = arquivo_texto.name
        else:
            if "texto_digitado" not in st.session_state:
                st.session_state.input_texto = ""

        texto_digitado = st.text_area("Ou insira um texto:", value=st.session_state.input_texto,height=150,on_change=self.atualizaTexto())
        st.session_state.input_texto = texto_digitado

        #Recebe o texto via arquivo ou digitado no campo texto
        #Arquivo tem prioridade, se houver texto já digitado no momento em que um arquivo for carregado, será sobrescrito.

        st.write("")  
        if st.button("Salvar texto em arquivo",icon=":material/file_save:"):
            if texto_digitado is not None:
                st.toast(f"Arquivo texto salvo com sucesso!",icon=":material/thumb_up:")

                st.download_button(label="Download TXT",data=texto_digitado,file_name="novo_texto.txt",on_click="ignore",type="primary",icon=":material/download:")
            else: 
                st.toast("Digite alguma coisa!",icon="🚨")

        with st.form(key="gerar_musica"):
            self.volume = st.slider("Volume",0,127,127)
            self.oitava = st.selectbox("Oitava:",opcoes_oitava,index=opcoes_oitava.index(OITAVA_DEFAULT))
            self.bpm = st.number_input("Bpm:",10,280,120,10)
            self.instrumento = st.selectbox("Instrumento:",opcoes_instrumentos,index=opcoes_instrumentos.index(INSTRUMENTO_DEFAULT))
            #Guarda os parametros deinidos 

            botao_gerar = st.form_submit_button(label="Gerar Música")

            if botao_gerar:
                if not texto_digitado.strip():
                    st.toast("Insira um texto ou carregue um arquivo!",icon="🚨")
                    return
         
                self.texto_converter = texto_digitado
                self.music_services = MusicServices(texto_digitado,self.instrumento,self.oitava,self.volume,self.bpm)
                st.session_state.music_services = self.music_services
                #Aciona music services para gerar a música a partir do texto e salva no buffer de estado

                if self.music_services.isMusicaPronta:
                    self.inicializaCabecalho
                    self.mudaTela("tela_player")
                #Troca para tela de player

    def telaPlayer(self):
        st.write("Música gerada!")

        self.music_services = st.session_state.get("music_services", None)
        if self.music_services is None:
            st.warning("Música não encontrada!")
            return
        #Busca a música do buffer de estado
        
        if "tela_player_carregada" not in st.session_state or not st.session_state.tela_player_carregada:
            st.session_state.midi_try = False
            st.session_state.midi_sucesso = None
            st.session_state.tela_player_carregada = True

        if st.button("Gerar arquivo MIDI"):
            st.session_state.midi_try = True
            st.session_state.midi_sucesso = self.music_services.gerarMidi()

        if st.session_state.midi_try:    
            if st.session_state.midi_sucesso:
                st.toast("Arquivo MIDI gerado com sucesso!",icon=":material/thumb_up:")
                with open("musica_gerada.mid", "rb") as f:
                    st.download_button(label="Download MIDI",data=f,file_name="musica_gerada.mid",mime="audio/midi",on_click="ignore",type="primary",icon=":material/download:",)
            else:
                st.error("Não foi possível gerar o arquivo.")
        #Se o botão de gerar midi foi acionado, permite o download do arquivo
        
        col1,col2 = st.columns([1,1])
        with col1:
            if st.button("Play",icon=":material/play_circle:"):        
                self.music_services.play()
        with col2:
            if st.button("Voltar",icon=":material/logout:"):
                self.mudaTela("tela_input")
        #Botões de play e voltar 
