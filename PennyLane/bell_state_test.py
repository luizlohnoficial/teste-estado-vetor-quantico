import logging
import pennylane as qml
from pennylane import numpy as np

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

dev = qml.device("default.qubit", wires=2, shots=1000)

@qml.qnode(dev)
def circuit():
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])
    return qml.sample(qml.PauliZ(0)), qml.sample(qml.PauliZ(1))

def test_bell_state_entanglement():
    logger.info("Rodando circuito PennyLane Bell")
    logger.info("Circuito:\n%s", qml.draw(circuit)())
    samples0, samples1 = circuit()
    bits0 = (1 - samples0) / 2
    bits1 = (1 - samples1) / 2
    counts = {}
    for b0, b1 in zip(bits0, bits1):
        key = f"{int(b0)}{int(b1)}"
        counts[key] = counts.get(key, 0) + 1

    logger.info("Contagem: %s", counts)
    total = sum(counts.values())
    assert counts.get('00', 0) + counts.get('11', 0) == total, "Resultado deve ser apenas 00 ou 11"

    zero_zero_ratio = counts.get('00', 0) / total
    one_one_ratio = counts.get('11', 0) / total

    assert np.isclose(zero_zero_ratio, 0.5, atol=0.05), "probabilidade de 00 próxima a 0.5"
    assert np.isclose(one_one_ratio, 0.5, atol=0.05), "probabilidade de 11 próxima a 0.5"


if __name__ == "__main__":
    try:
        test_bell_state_entanglement()
    except AssertionError as exc:
        logger.error("Testes falharam: %s", exc)
        raise
    else:
        logger.info("Testes passaram: estado Bell criado corretamente")
