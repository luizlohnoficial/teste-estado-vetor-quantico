
import logging
from braket.circuits import Circuit
from braket.devices import LocalSimulator

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

def test_double_hadamard_returns_initial_state():
    logger.info("Criando circuito")
    circuit = Circuit().h(0).h(0).measure(0)
    logger.info("Circuito criado:\n%s", circuit)
    logger.info("Rodando simulador local")
    simulator = LocalSimulator()

    result = simulator.run(circuit, shots=100).result()
    counts = result.measurement_counts
    logger.info("Contagem: %s", counts)

    assert counts.get('0', 0) == 100, "double hadamard deve retornar |0>"

if __name__ == "__main__":
    try:
        test_double_hadamard_returns_initial_state()
    except AssertionError as exc:
        logger.error("Testes falharam: %s", exc)
        raise
    else:
        logger.info("Os testes passaram: distribução próximo a 50/50")
