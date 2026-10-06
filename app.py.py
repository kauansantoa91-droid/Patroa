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

# Estilos CSS Dark / Hacker
css_estilo = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600;800&display=swap');

.stApp {
    background: #0b0f14;
    color: #e6edf3;
    font-family: 'Inter', sans-serif;
}

.header-container {
    text-align: center;
    padding: 24px;
    margin-bottom: 20px;
    background: rgba(16, 24, 20, 0.7);
    border: 1px solid #00e676;
    border-radius: 12px;
}

.header-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2rem;
    font-weight: 800;
    color: #00e676;
    margin-bottom: 4px;
}

.header-sub {
    color: #8b949e;
    font-size: 0.95rem;
}

.stat-card {
    background: #111815;
    border: 1px solid #1f3326;
    border-radius: 10px;
    padding: 16px;
    text-align: center;
    margin-bottom: 12px;
}

.stat-number {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.6rem;
    font-weight: 700;
    color: #00e676;
}

.stat-label {
    font-size: 0.8rem;
    font-weight: 600;
    color: #8b949e;
    text-transform: uppercase;
}

div[data-testid="stFileUploadDropzone"] {
    background: #111815 !important;
    border: 2px dashed #00e676 !important;
    border-radius: 10px !important;
}

.stButton>button {
    background: #00e676 !important;
    color: #000000 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 800 !important;
    border-radius: 8px !important;
    width: 100% !important;
    padding: 12px !important;
}

div[data-testid="stDownloadButton"]>button {
    background: #00e676 !important;
    color: #000000 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 800 !important;
    border-radius: 8px !important;
    width: 100% !important;
    padding: 12
