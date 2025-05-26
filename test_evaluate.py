from Lang import *
from evaluate import *
from contextlib import redirect_stdout

# Test suites para programa1 a programa3 (como exigido pelo enunciado para runTestSuite)
testSuite1 = [
    ([("x", 3)], 1),             # x = 3 → soma = 6 → result = 1
    ([("x", 2)], 0),             # soma = 2 + 1 = 3 → result = 0
    ([("x", 0)], 0),             # while nunca executa
    ([("x", 1)], 0),             # soma = 1 → result = 0
    ([("x", 4)], 0)              # soma = 4+3+2+1 = 10 → result = 0
]
testSuite2 = [
    ([], 6),                          # soma 1+2+3
    ([("i", 0)], 6),                  # ignora "i" se não usada
    ([("sum", 5)], 6),               # ignora "sum" externo
]
testSuite3 = [
    ([("a", 2), ("b", 3)], 5),   # passa → soma
    ([("a", 0), ("b", 1)], 0),   # falha → a ≤ 0
    ([("a", 2), ("b", -1)], 0),  # falha → b ≤ 0
    ([("a", 1), ("b", 1)], 2),   # passa
    ([("a", 1), ("b", 0)], 0),   # falha
    ([("a", -1), ("b", -1)], 0)  # falha total
]

# Programas de teste
runTestSuitePrograma1 = runTestSuite(programa1, testSuite1)
runTestSuitePrograma2 = runTestSuite(programa2, testSuite2)
runTestSuitePrograma3 = runTestSuite(programa3, testSuite3)


testPrintSuite = [ ([], 42) ]

# Programas mutados
programa1_mut = Program([
    Assign("y", IntLit(0)),
    While(
        condition=BinOp(">", Var("x"), IntLit(0)),
        body=[
            Assign("y", BinOp("+", Var("y"), Var("x"))),
            Assign("x", BinOp("-", Var("x"), IntLit(1))),
            Print(Var("y"))
        ]
    ),
    If(
        condition=BinOp("!=", Var("y"), IntLit(6)),  # <--- MUDADO
        then_branch=[Assign("result", IntLit(1))],
        else_branch=[Assign("result", IntLit(0))]
    ),
    Return(Var("result"))
])

programa2_mut = Program([
    Assign("sum", IntLit(0)),
    For(
        var="i",
        start=IntLit(1),
        end=IntLit(4),
        body=[
            Assign("sum", BinOp("-", Var("sum"), Var("i"))),  # <--- MUDADO
            Print(Var("sum"))
        ]
    ),
    If(
        condition=BoolLit(True),
        then_branch=[Assign("z", IntLit(5))],
        else_branch=[Assign("z", IntLit(5))]
    ),
    Return(Var("sum"))
])

programa3_mut = Program([
    FunctionDef(
        name="check_and_add",
        params=["a", "b"],
        body=[
            If(
                condition=BinOp("&&", BinOp(">", Var("a"), IntLit(0)), BinOp(">", Var("b"), IntLit(0))),
                then_branch=[Assign("r", BinOp("*", Var("a"), Var("b")))],  # <--- MUDADO
                else_branch=[Assign("r", IntLit(0))]
            ),
            Return(Var("r"))
        ]
    ),
    Assign("x", FunctionCall("check_and_add", [Var("a"), Var("b")])),  # <--- MUDADO
    Print(Var("x")),
    Return(Var("x"))
])

# Programas de teste mutados
runTestSuitePrograma1Mut = runTestSuite(programa1_mut, testSuite1)
runTestSuitePrograma2Mut = runTestSuite(programa2_mut, testSuite2)
runTestSuitePrograma3Mut = runTestSuite(programa3_mut, testSuite3)


# Programa com instrução Print
programa_com_print = Program([
    Assign("x", IntLit(42)),
    Print(Var("x")),
    Return(Var("x"))
])

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


def test_all_with_evaluate():
    print("======================== Testar evaluate() ========================")
    
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
    print("\n========================  Testar runTest() ========================")
    
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



def test_sbfl():
    programas = [
        ("programa1", programa1_mut, testSuite1),
        ("programa2", programa2_mut, testSuite2),
        ("programa3", programa3_mut, testSuite3)
    ]

    for nome, prog, suite in programas:
        print(f"\n SBFL para {nome}_mut")
        scores = spectrum_based_fault_localization(prog, suite)
        for instr_id, score in scores:
            print(f"Instrução {instr_id}: score = {score:.4f}")


def main():
    with open("resultado_evaluate.txt", "w", encoding="utf-8") as f:
        with redirect_stdout(f):
            test_all_with_evaluate()
            test_all_with_runTest()

            print("\n========================  Testar runTestSuite() para os 3 programas escolhidos ========================")
            print("Programa 1:", runTestSuitePrograma1)
            print("Programa 2:", runTestSuitePrograma2)
            print("Programa 3:", runTestSuitePrograma3)

            print("\n========================  Testar runTestSuite() para os 3 programas mutados ========================")
            print("Programa 1 Mutado:", runTestSuitePrograma1Mut)
            print("Programa 2 Mutado:", runTestSuitePrograma2Mut)
            print("Programa 3 Mutado:", runTestSuitePrograma3Mut)

            print("\n========================  Testar programa com Print ========================")
            print("Programa Print:", runTestSuite(programa_com_print, testPrintSuite))

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

            print("\n========================  SBFL (Spectrum-Based Fault Localization) ========================")
            test_sbfl()


if __name__ == "__main__":
    main()

