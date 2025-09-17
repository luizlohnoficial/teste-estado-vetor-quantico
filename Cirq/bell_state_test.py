import logging
import cirq
import numpy as np

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def test_bell_state_entanglement():
    logger.info("Preparando circuito Bell")
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='m')
    )
    logger.info("Circuito:\n%s", circuit)

    logger.info("Rodando no Simulador Cirq")
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1000)
    counts = result.histogram(key='m', fold_func=lambda bits: ''.join(str(b) for b in bits))

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
