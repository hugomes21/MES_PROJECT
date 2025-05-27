from Lang import *
from evaluate import *
from contextlib import redirect_stdout

# Test suites para programa1 a programa3 (como exigido pelo enunciado para runTestSuite)
testSuite1 = [
    ([("x", 3)], 1),  # Soma: 3+2+1 = 6 → y == 6 → result = 1
    ([("x", 2)], 0),  # Soma: 2+1 = 3 → y != 6
    ([("x", 0)], 0),  # While não executa → y = 0
    ([("x", 4)], 0),  # Soma: 4+3+2+1 = 10 → y != 6
    ([("x", 6)], 0),  # Soma: 6+5+4+3+2+1 = 21
]
testSuite2 = [
    ([], 6),  # Soma 1+2+3 = 6
    ([("sum", 99)], 6),  # Variável externa ignorada → soma reinicia a 0
    ([("i", 0)], 6),  # "i" externo ignorado, loop interno define-o
    ([("sum", 0), ("i", 2)], 6),  # Mesmo com vars externas → resultado fixo
]
testSuite3 = [
    ([("a", 2), ("b", 3)], 5),   # Passa → a > 0 ∧ b > 0 → r = a + b = 5
    ([("a", 0), ("b", 3)], 0),   # Falha → a == 0 → ramo else
    ([("a", 2), ("b", 0)], 0),   # Falha → b == 0
    ([("a", -1), ("b", 1)], 0),  # Falha → a < 0
    ([("a", 1), ("b", 1)], 2),   # Passa → 1 + 1
    ([("a", -1), ("b", -1)], 0), # Falha total
    ([("a", 10), ("b", 0)], 0),  # Falha parcial → b ≤ 0
]


# Programas de teste
runTestSuitePrograma1 = runTestSuite(programa1, testSuite1)
runTestSuitePrograma2 = runTestSuite(programa2, testSuite2)
runTestSuitePrograma3 = runTestSuite(programa3, testSuite3)

# Aplicar mutação aleatória ao programa1
def testar_mutacoes():
    programas = [
        ("programa1", programa1, testSuite1),
        ("programa2", programa2, testSuite2),
        ("programa3", programa3, testSuite3)
    ]

    for nome, prog, suite in programas:
        mutado = mutate(prog)
        print(f"\nMutando {nome}...")
        print(mutado)
        passou = runTestSuite(mutado, suite)
        print(f"{nome} mutado → passou tests? {passou}")

        # Executar SBFL sobre o programa mutado
        print(f"\n[SBFL] Spectrum-Based Fault Localization para {nome}_mut")
        scores = spectrum_based_fault_localization(mutado, suite)
        for instr_id, score in scores:
            print(f"Instrução {instr_id}: score = {score:.4f}")



def test_all_with_evaluate():    
    test_suites = {
        1: testSuite1,
        2: testSuite2,
        3: testSuite3
    }

    for i in range(1, 4):
        prog = globals().get(f"programa{i}")
        suite = test_suites.get(i)
        if not prog or not suite:
            continue

        for j, (inputs, expected) in enumerate(suite, 1):
            try:
                result = evaluate(prog, inputs)
                status = "✓" if result == expected else "✗"
                print(f"Programa {i} - Teste {j}: resultado = {result} (esperado = {expected}) {status}")
            except Exception as e:
                print(f"Programa {i} - Teste {j}: erro → {e}")


def test_all_with_runTest():    
    test_suites = {
        1: testSuite1,
        2: testSuite2,
        3: testSuite3
    }

    for i in range(1, 4):
        prog = globals().get(f"programa{i}")
        suite = test_suites.get(i)
        if not prog or not suite:
            continue

        for j, test_case in enumerate(suite, 1):
            try:
                ok = runTest(prog, test_case)
                status = "✓" if ok else "✗"
                print(f"Programa {i} - Teste {j}: passou = {ok} {status}")
            except Exception as e:
                print(f"Programa {i} - Teste {j}: erro → {e}")


def test_instrumentation_manual():
    instr = instrumentation(programa1)
    print("Programa 1 instrumentado:")
    print(instr)


def main():
    with open("resultado_evaluate.txt", "w", encoding="utf-8") as f:
        with redirect_stdout(f):
            print("======================== Testar evaluate() ========================")
            test_all_with_evaluate()
            
            print("\n========================  Testar runTest() ========================")
            test_all_with_runTest()

            print("\n========================  Testar runTestSuite() para os 3 programas escolhidos ========================")
            print("Programa 1:", runTestSuitePrograma1)
            print("Programa 2:", runTestSuitePrograma2)
            print("Programa 3:", runTestSuitePrograma3)

            print("\n========================  Testar mutações aleatoriamente ========================")
            testar_mutacoes()

            print("\n========================  Testar instrumentation manualmente ========================")
            test_instrumentation_manual()

            print("\n========================  Testar instrumentedTestSuite ========================")
            result = instrumentedTestSuite(programa1, testSuite1)
            print("instrumentedTestSuite para programa1:", result)
            result = instrumentedTestSuite(programa2, testSuite2)
            print("instrumentedTestSuite para programa2:", result)
            result = instrumentedTestSuite(programa3, testSuite3)
            print("instrumentedTestSuite para programa3:", result)


if __name__ == "__main__":
    main()

