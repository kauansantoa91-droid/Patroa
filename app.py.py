import io
import re
import time
import streamlit as st

st.set_page_config(
    page_title="Extrator de Celulares",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilização limpa sem aspas triplas para não quebrar
st.markdown(
    "<style>"
    "@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600;800&display=swap');"
    ".stApp { background: #0b0f14; color: #e6edf3; font-family: 'Inter', sans-serif; }"
    ".header-container { text-align: center; padding: 22px; margin-bottom: 20px; background: rgba(16, 24, 20, 0.7); border: 1px solid #00e676; border-radius: 12px; }"
    ".header-title { font-family: 'JetBrains Mono', monospace; font-size: 1.8rem; font-weight: 800; color: #00e676; margin-bottom: 4px; }"
    ".header-sub { color: #8b949e; font-size: 0.95rem; }"
    ".stat-card { background: #111815; border: 1px solid #1f3326; border-radius: 10px; padding: 14px; text-align: center; margin-bottom: 10px; }"
    ".stat-number { font-family: 'JetBrains Mono', monospace; font-size: 1.5rem; font-weight: 700; color: #00e676; }"
    ".stat-label { font-size: 0.8rem; font-weight: 600; color: #8b949e; text-transform: uppercase; }"
    "div[data-testid='stFileUploadDropzone'] { background: #111815 !important; border: 2px dashed #00e676 !important; border-radius: 10px !important; }"
    ".stButton>button { background: #00e676 !important; color: #000000 !important; font-family: 'JetBrains Mono', monospace !important; font-weight: 800 !important; border-radius: 8px !important; width: 100% !important; padding: 12px !important; border: none !important; }"
    "div[data-testid='stDownloadButton']>button { background: #00e676 !important; color: #000000 !important; font-family: 'JetBrains Mono', monospace !important; font-weight: 800 !important; border-radius: 8px !important; width: 100% !important; padding: 12px !important; border: none !important; }"
    "</style>",
    unsafe_allow_html=True
)

PADRAO_CEL = re.compile(r'(?:CELULAR\s*\d*:\s*|\b)((?:\(?\d{2}\)?\s*)?9\d{8})\b', re.IGNORECASE)

st.markdown(
    "<div class='header-container'>"
    "<div class='header-title'>⚡ EXTRATOR & UNIFICADOR DE CELULARES</div>"
    "<div class='header-sub'>Processamento em alta velocidade com exportação personalizada</div>"
    "</div>",
    unsafe_allow_html=True
)

# Escolha do formato de saída (.csv ou .txt)
formato_saida = st.radio(
    "Formato do arquivo final:",
    options=[".csv (Excel / Equicell)", ".txt (Texto Simples)"],
    index=0,
    horizontal=True
)

arquivos = st.file_uploader(
    "Arraste ou selecione os arquivos com as fichas (.txt, .csv, .log):",
    type=["txt", "csv", "log"],
    accept_multiple_files=True
)

if arquivos:
    st.info(f"📂 Total de arquivos carregados: {len(arquivos)}")

    if st.button("INICIAR EXTRAÇÃO EM LOTE"):
        numeros_unicos = set()
        linhas_totais = 0
        logs = []

        barra_progresso = st.progress(0)
        status_texto = st.empty()

        col1, col2, col3 = st.columns(3)
        with col1:
            m_linhas = st.empty()
        with col2:
            m_unicos = st.empty()
        with col3:
            m_tempo = st.empty()

        terminal_box = st.empty()
        inicio = time.time()
        total_arquivos = len(arquivos)

        for idx, arq in enumerate(arquivos, 1):
            nome_arq = arq.name
            conteudo = io.TextIOWrapper(arq, encoding='utf-8', errors='ignore')

            for linha in conteudo:
                linhas_totais += 1
                encontrados = PADRAO_CEL.findall(linha)

                for item in encontrados:
                    digitos = re.sub(r'\D', '', item)
                    if len(digitos) == 11 and digitos not in numeros_unicos:
                        numeros_unicos.add(digitos)
                        logs.append(f"[+] EXTRAÍDO: {digitos}")
                        if len(logs) > 10:
                            logs.pop(0)

                if linhas_totais % 2000 == 0:
                    pct = int((idx / total_arquivos) * 100)
                    barra_progresso.progress(min(pct, 100))
                    status_texto.text(f"Lendo: {nome_arq}...")

                    m_linhas.markdown(f"<div class='stat-card'><div class='stat-label'>Linhas Lidas</div><div class='stat-number'>{linhas_totais:,}</div></div>", unsafe_allow_html=True)
                    m_unicos.markdown(f"<div class='stat-card'><div class='stat-label'>Celulares Únicos</div><div class='stat-number'>{len(numeros_unicos):,}</div></div>", unsafe_allow_html=True)
                    m_tempo.markdown(f"<div class='stat-card'><div class='stat-label'>Tempo</div><div class='stat-number'>{time.time() - inicio:.1f}s</div></div>", unsafe_allow_html=True)

                    terminal_box.code("\n".join(logs), language="bash")

        tempo_final = time.time() - inicio
        barra_progresso.progress(100)
        status_texto.success("✔ Processamento concluído com sucesso!")

        m_linhas.markdown(f"<div class='stat-card'><div class='stat-label'>Total Linhas</div><div class='stat-number'>{linhas_totais:,}</div></div>", unsafe_allow_html=True)
        m_unicos.markdown(f"<div class='stat-card'><div class='stat-label'>Celulares Únicos</div><div class='stat-number'>{len(numeros_unicos):,}</div></div>", unsafe_allow_html=True)
        m_tempo.markdown(f"<div class='stat-card'><div class='stat-label'>Tempo Total</div><div class='stat-number'>{tempo_final:.2f}s</div></div>", unsafe_allow_html=True)

        terminal_box.code("\n".join(logs), language="bash")

        if "csv" in formato_saida.lower():
            dados_download = "telefone\n" + "\n".join(numeros_unicos) + "\n"
            nome_arquivo_saida = "celulares_unificados.csv"
            tipo_mime = "text/csv"
            rotulo_btn = f"⬇ BAIXAR ARQUIVO .CSV ({len(numeros_unicos):,} NÚMEROS)"
        else:
            dados_download = "\n".join(numeros_unicos) + "\n"
            nome_arquivo_saida = "celulares_unificados.txt"
            tipo_mime = "text/plain"
            rotulo_btn = f"⬇ BAIXAR ARQUIVO .TXT ({len(numeros_unicos):,} NÚMEROS)"

        st.write("---")
        st.download_button(
            label=rotulo_btn,
            data=dados_download,
            file_name=nome_arquivo_saida,
            mime=tipo_mime
        )
