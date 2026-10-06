import io
import re
import time
import streamlit as st

# Configuração da página e layout
st.set_page_config(
    page_title="2B // Extrator de Celulares",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilização CSS completa (Dark Cyberpunk / Glassmorphism)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@300;400;600;800&display=swap');

    /* Fundo da aplicação */
    .stApp {
        background: radial-gradient(circle at 15% 15%, #0d1f14 0%, #08090c 70%, #030406 100%);
        color: #e6edf3;
        font-family: 'Inter', sans-serif;
    }

    /* Cabeçalho estilizado */
    .header-container {
        text-align: center;
        padding: 30px 10px 20px 10px;
        margin-bottom: 25px;
        background: rgba(13, 20, 16, 0.6);
        border: 1px solid rgba(0, 230, 118, 0.2);
        border-radius: 16px;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
    }
    .header-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2.3rem;
        font-weight: 800;
        letter-spacing: -1px;
        background: linear-gradient(90deg, #00e676, #00b0ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
    }
    .header-sub {
        color: #8b949e;
        font-size: 0.95rem;
    }

    /* Cartões de estatísticas */
    .stat-card {
        background: rgba(18, 26, 22, 0.7);
        border: 1px solid rgba(0, 230, 118, 0.25);
        border