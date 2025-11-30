import streamlit as st
from class_MusicServices import MusicServices
from enum_Valores import ValoresInstrumentos

NOTA_DEFAULT = 'C'
OITAVA_DEFAULT = 0
VOLUME_DEFAULT = 127  # máximo
BPM_DEFAULT = 120
INSTRUMENTO_DEFAULT = 'ACOUSTIC_GRAND_PIANO'
VALOR_INSTRUMENTO_DEFAULT = ValoresInstrumentos.ACOUSTIC_GRAND_PIANO.name

opcoes_oitava = [-5,-4,-3,-2,-1,0,1,2,3,4,5]
opcoes_instrumentos = [inst.name for inst in ValoresInstrumentos]

class UI:
    def __init__(self):
        st.set_page_config(page_title="Gerador de Música", page_icon="🎵")

        if "screen" not in st.session_state:
            st.session_state.screen = "tela_input" 

        st.session_state.setdefault("input_texto", "")
        st.session_state.setdefault("volume", 127)
        st.session_state.setdefault("oitava", 0)
        st.session_state.setdefault("bpm", 120)
        st.session_state.setdefault("instrumento","ACOUSTIC_GRAND_PIANO")

        self.music_services = None
        self.texto_converter = None

        self.inicializaCabecalho()

        if st.session_state.screen == "tela_input":
            self.telaGerador()
        elif st.session_state.screen == "tela_player":
            self.telaPlayer()

    def inicializaCabecalho(self):
        st.markdown(
            "<h1 style='text-align:center;'>Gerador de Música</h1>",
            unsafe_allow_html=True,
        )
        st.write("")

    def mudaTela(self,nome_tela):
        st.session_state.screen = nome_tela
        st.rerun()

    def atualizaTexto(self):
        pass

    def telaGerador(self):
        st.write("Transforma texto em música!")
        st.write("")

        arquivo_texto = st.file_uploader("Carregue um arquivo texto:",type=["txt"])

        if arquivo_texto is not None:
            st.session_state.input_texto = arquivo_texto.read().decode("utf-8")
        else:
            if "texto_digitado" not in st.session_state:
                st.session_state.input_texto = ""

        texto_digitado = st.text_area("Ou insira um texto:", value=st.session_state.input_texto,height=150,on_change=self.atualizaTexto())

        with st.form(key="gerar_musica"):

            self.volume = st.slider("Volume",0,127,127)
            self.oitava = st.selectbox("Oitava:",opcoes_oitava,index=opcoes_oitava.index(OITAVA_DEFAULT))
            self.bpm = st.number_input("Bpm:",10,280,120,10)
            self.instrumento = st.selectbox("Instrumento:",opcoes_instrumentos,index=opcoes_instrumentos.index(VALOR_INSTRUMENTO_DEFAULT))

            botao_gerar = st.form_submit_button(label="Gerar Música")

            if botao_gerar:
                if not texto_digitado.strip():
                    st.warning("Insira um texto OU carregue um arquivo!")
                    return
         
                self.texto_converter = texto_digitado

                self.music_services = MusicServices(texto_digitado,self.instrumento,self.oitava,self.volume,self.bpm)

                #salva a música no buffer de estado
                st.session_state.music_services = self.music_services

                if self.music_services.isMusicaPronta:
                    self.inicializaCabecalho
                    self.mudaTela("tela_player")

    def telaPlayer(self):
        st.write("Música gerada!")

        #busca a música do buffer de estado
        self.music_services = st.session_state.get("music_services", None)

        if self.music_services is None:
            st.warning("Música não encontrada!")
            return
        
        if st.button("Gerar arquivo MIDI"):
            self.music_services.gerarMidi()
            st.toast("Arquivo MIDI 'musica_gerada.mid' gerado com sucesso!")

        col1,col2,col3 = st.columns([1,1,1])

        with col1:
            if st.button("▶️ Play"):        
                self.music_services.play()

        with col2:
            if st.button("⏸️ Pause"):
                pass
                
        with col3:
            if st.button("⏹️ Voltar"):
                self.mudaTela("tela_input")

