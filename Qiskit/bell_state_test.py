try:
    from qiskit import QuantumCircuit, transpile
    from qiskit_aer import AerSimulator
except ImportError as exc:
    raise ImportError(
        "Qiskit and qiskit-aer are required to run this test. Install with `pip install qiskit qiskit-aer`."
    ) from exc

import logging
import numpy as np

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def test_bell_state_entanglement():
    logger.info("Criando circuito Bell")
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    logger.info("Circuito:\n%s", qc.draw(output='text'))

    logger.info("Rodando no AerSimulator")
    backend = AerSimulator()
    compiled = transpile(qc, backend)
    job = backend.run(compiled, shots=1000)
    counts = job.result().get_counts()

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
