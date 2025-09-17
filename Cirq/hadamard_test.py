
import logging
import cirq
import numpy as np

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

def test_hadamard_with_tolerance():
    logger.info("Praparando circuito")
    qubit = cirq.LineQubit(0)
    circuit = cirq.Circuit(cirq.H(qubit), cirq.measure(qubit, key='m'))
    logger.info("Circuitos:\n%s", circuit)
    logger.info("Rodando No Cirq Simulator")
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1000)
    counts = result.histogram(key='m')
    logger.info("Contagem: %s", counts)

    zero_ratio = counts.get(0, 0) / 1000
    one_ratio = counts.get(1, 0) / 1000

    assert np.isclose(zero_ratio, 0.5, atol=0.05), "probabilidade de 0 próximo a 0.5"
    assert np.isclose(one_ratio, 0.5, atol=0.05), "probabilidade de 1 próximo a 0.5"


if __name__ == "__main__":
    try:
        test_hadamard_with_tolerance()
    except AssertionError as exc:
        logger.error("Testes falharam: %s", exc)
        raise
    else:
        logger.info("Testes passaram: distribuição próxima a 50/50")
