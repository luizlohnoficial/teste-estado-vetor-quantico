import logging
from braket.circuits import Circuit
from braket.devices import LocalSimulator

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def test_bell_state_entanglement():
    logger.info("Criando circuito Bell")
    circuit = Circuit().h(0).cnot(0, 1).measure(0).measure(1)
    logger.info("Circuito criado:\n%s", circuit)
    simulator = LocalSimulator()

    result = simulator.run(circuit, shots=1000).result()
    counts = result.measurement_counts
    logger.info("Contagem: %s", counts)

    total = sum(counts.values())
    assert counts.get('00', 0) + counts.get('11', 0) == total, "Resultado deve ser apenas 00 ou 11"

    zero_zero_ratio = counts.get('00', 0) / total
    one_one_ratio = counts.get('11', 0) / total

    assert abs(zero_zero_ratio - 0.5) < 0.05, "probabilidade de 00 próxima a 0.5"
    assert abs(one_one_ratio - 0.5) < 0.05, "probabilidade de 11 próxima a 0.5"


if __name__ == "__main__":
    try:
        test_bell_state_entanglement()
    except AssertionError as exc:
        logger.error("Testes falharam: %s", exc)
        raise
    else:
        logger.info("Testes passaram: estado Bell criado corretamente")
