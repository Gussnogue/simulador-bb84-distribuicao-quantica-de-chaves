import streamlit as st
import numpy as np
import plotly.graph_objects as go
from bb84 import simulate_bb84
from ai_analyzer import analyze_bb84_results

st.set_page_config(page_title="BB84 QKD Simulator", layout="wide")
st.title("🔐 Simulador BB84 - Distribuição Quântica de Chaves")
st.markdown("Simulação do protocolo BB84 com detecção de espionagem e análise por IA local (Hermes 3)")

st.sidebar.header("Parâmetros da Simulação")
num_bits = st.sidebar.slider("Número de qubits enviados", 100, 2000, 500, step=50)
error_rate = st.sidebar.slider("Taxa de erro natural da linha", 0.0, 0.2, 0.02, step=0.01, format="%.2f")
eavesdrop = st.sidebar.checkbox("Ativar espião (Eve)", value=False)

if st.sidebar.button("Simular", type="primary"):
    with st.spinner("Simulando protocolo BB84..."):
        results = simulate_bb84(num_bits, error_rate, eavesdrop)

    col1, col2, col3 = st.columns(3)
    col1.metric("QBER (taxa de erro)", f"{results['qber']:.2%}")
    col2.metric("Espionagem detectada?", "✅ Sim" if results['eavesdropping_detected'] else "❌ Não")
    col3.metric("Tamanho da chave final", f"{len(results['sifted_key'])} bits")

    # Gráfico comparativo QBER vs limiar
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["QBER Medido", "Limiar (11%)"],
        y=[results['qber'], 0.11],
        marker_color=["#FF4B4B" if results['qber'] > 0.11 else "#00CC96", "#636EFA"],
        text=[f"{results['qber']:.2%}", "11%"],
        textposition="auto"
    ))
    fig.update_layout(
        title="Comparação QBER vs. Limiar de Segurança",
        yaxis_title="Taxa de erro",
        yaxis_tickformat=".0%",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🤖 Análise da IA (Hermes 3)")
    with st.spinner("Consultando IA local..."):
        analysis = analyze_bb84_results(results)
    st.markdown(analysis)

    with st.expander("📊 Ver detalhes técnicos da simulação"):
        st.write(f"**Bits enviados:** {num_bits}")
        st.write(f"**Bits sifted (bases coincidentes):** {len(results['sifted_key'])}")
        st.write(f"**Taxa de erro natural:** {error_rate:.2%}")
        st.write(f"**Espião ativo:** {eavesdrop}")
        if results['eavesdropping_detected']:
            st.warning("⚠️ Espionagem detectada! A chave deve ser descartada.")
        else:
            st.success("✅ Nenhuma espionagem detectada. A chave pode ser usada com segurança.")
else:
    st.info("Ajuste os parâmetros na barra lateral e clique em 'Simular' para iniciar.")


    