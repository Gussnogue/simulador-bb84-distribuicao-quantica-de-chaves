import requests
import os
from dotenv import load_dotenv

load_dotenv()

LM_URL = os.getenv("LM_STUDIO_URL", "http://localhost:1234/v1/chat/completions")
LM_MODEL = os.getenv("LM_MODEL", "hermes-3-llama-3.2-3b")

def analyze_bb84_results(simulation_results):
    """Gera um relatório explicativo usando Hermes 3."""
    prompt = f"""
Você é um especialista em criptografia quântica. Analise os resultados da simulação do protocolo BB84 abaixo e forneça uma explicação didática em português.

**Parâmetros da simulação:**
- Número de qubits enviados: {simulation_results['num_bits']}
- Taxa de erro natural da linha: {simulation_results['error_rate']:.2%}
- Presença de espião (Eve): {simulation_results['eavesdrop']}

**Resultados:**
- Quantum Bit Error Rate (QBER): {simulation_results['qber']:.2%}
- Espionagem detectada: {simulation_results['eavesdropping_detected']}
- Tamanho da chave final (após sifting): {len(simulation_results['sifted_key'])} bits

Com base nesses dados, responda:
1. O que aconteceu durante a simulação? (processo geral)
2. Explique o valor do QBER e o que ele indica sobre a segurança.
3. Se houve espionagem, explique como ela foi detectada e o que isso significa.
4. Dê uma recomendação prática para garantir a segurança no uso do BB84.
"""
    payload = {
        "model": LM_MODEL,
        "messages": [
            {"role": "system", "content": "Você é um especialista em comunicação quântica e criptografia. Responda de forma clara, concisa e didática."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 600
    }
    try:
        resp = requests.post(LM_URL, json=payload)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Erro ao consultar IA: {e}\nVerifique se o LM Studio está rodando e o modelo está carregado."
    
    