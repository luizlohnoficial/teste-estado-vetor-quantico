
import logging
import pennylane as qml
from pennylane import numpy as np

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

dev = qml.device("default.qubit", wires=1, shots=1000)

@qml.qnode(dev)
def circuit():
    qml.Hadamard(wires=0)
    return qml.sample(qml.PauliZ(0))

def test_hadamard_distribution():
    logger.info("Rodando Circuito PennyLane")
    logger.info("Circuito:\n%s", qml.draw(circuit)())
    samples = circuit()
    zero_count = np.sum(samples == 1)
    one_count = np.sum(samples == -1)

    logger.info("Contagem de Zero: %s, Contagem de Um: %s", zero_count, one_count)

    zero_ratio = zero_count / 1000
    one_ratio = one_count / 1000

    assert np.isclose(zero_ratio, 0.5, atol=0.05), "probabilidade de 0 próximo a 0.5"
    assert np.isclose(one_ratio, 0.5, atol=0.05), "probabilidade de 1 próximo a 0.5"


if __name__ == "__main__":
    try:
        test_hadamard_distribution()
    except AssertionError as exc:
        logger.error("Testes falharam: %s", exc)
        raise
    else:
        logger.info("Testes passaram: distribuição próxima a 50/50")
