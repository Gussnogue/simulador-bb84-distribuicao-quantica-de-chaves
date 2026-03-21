import numpy as np

def simulate_bb84(num_bits, error_rate=0.0, eavesdrop=False):
    """
    Simula o protocolo BB84.

    Parâmetros:
        num_bits: número de bits a serem transmitidos (tamanho da sequência quântica)
        error_rate: taxa de erro na linha (0.0 a 1.0) - ruído natural
        eavesdrop: se True, um espião (Eve) intercepta e reenvia os qubits com base aleatória

    Retorna:
        dicionário com os resultados
    """
    # Gera bits e bases aleatórias para Alice
    alice_bits = np.random.randint(0, 2, num_bits)
    alice_bases = np.random.randint(0, 2, num_bits)

    # Se há espiã, Eve escolhe bases aleatórias
    if eavesdrop:
        eve_bases = np.random.randint(0, 2, num_bits)
    else:
        eve_bases = None

    # Bob escolhe bases aleatórias
    bob_bases = np.random.randint(0, 2, num_bits)

    bob_measures = []
    for i in range(num_bits):
        # Ruído na linha: inverte o bit com probabilidade error_rate
        transmitted_bit = alice_bits[i]
        if np.random.rand() < error_rate:
            transmitted_bit ^= 1

        # Interceptação de Eve (se ativa)
        if eavesdrop:
            # Eve mede o qubit com sua base
            if eve_bases[i] == alice_bases[i]:
                eve_bit = transmitted_bit  # acertou a base, copia corretamente
            else:
                # base errada: o bit medido é aleatório (50% de chance de acertar)
                eve_bit = np.random.randint(0, 2)
            # Eve reenvia o bit que mediu
            transmitted_bit = eve_bit

        # Bob mede com sua base
        if bob_bases[i] == alice_bases[i]:
            # Bases coincidem: Bob obtém o bit transmitido (com eventuais erros)
            bob_measures.append(transmitted_bit)
        else:
            # Bases diferentes: Bob obtém bit aleatório
            bob_measures.append(np.random.randint(0, 2))

    # Sifting: manter apenas posições onde bases coincidem
    sifted_key = []
    for i in range(num_bits):
        if alice_bases[i] == bob_bases[i]:
            # bit final após sifting (se houve erro, bob_measures[i] será diferente de alice_bits[i])
            sifted_key.append(alice_bits[i] if alice_bits[i] == bob_measures[i] else 1 - alice_bits[i])

    # Calcular QBER (sobre os bits sifted)
    if len(sifted_key) > 0:
        errors = sum(1 for i in range(len(sifted_key)) if sifted_key[i] != alice_bits[i])
        qber = errors / len(sifted_key)
    else:
        qber = 1.0

    # Limiar típico: QBER > 11% indica espionagem
    eavesdropping_detected = qber > 0.11

    return {
        'alice_bits': alice_bits,
        'alice_bases': alice_bases,
        'bob_bases': bob_bases,
        'bob_measures': bob_measures,
        'sifted_key': sifted_key,
        'qber': qber,
        'eavesdropping_detected': eavesdropping_detected,
        'num_bits': num_bits,
        'error_rate': error_rate,
        'eavesdrop': eavesdrop
    }

