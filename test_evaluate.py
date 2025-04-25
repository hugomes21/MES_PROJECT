
from Lang import *
from evaluate import *

# Test suites para programa1 a programa3 (como exigido pelo enunciado para runTestSuite)
testSuite1 = [ ([("x", 10)], 15) ]  # y = x + 5 → 15
testSuite2 = [ ([], 4) ]           # max = b → 4
testSuite3 = [ ([], 10) ]          # sum = 1+2+3+4 → 10

# Programas mutados
programa1_mut = Program([
    Assign("x", IntLit(10)),
    Assign("y", BinOp("-", Var("x"), IntLit(5)))
])
programa2_mut = Program([
    Assign("a", IntLit(3)),
    Assign("b", IntLit(4)),
    If(
        condition=BinOp("<", Var("a"), Var("b")),
        then_branch=[Assign("max", Var("a"))],
        else_branch=[Assign("max", Var("b"))]
    )
])
programa3_mut = Program([
    Assign("sum", IntLit(0)),
    For(
        var="i",
        start=IntLit(1),
        end=IntLit(5),
        body=[
            Assign("sum", BinOp("-", Var("sum"), Var("i")))
        ]
    )
])

def test_all_with_evaluate():
    print("=== Testar evaluate() para programa1 a programa14 ===")
    for i in range(1, 15):
        prog = globals().get(f"programa{i}")
        if not prog:
            continue
        try:
            result = evaluate(prog, [])
            print(f"programa{i}: resultado = {result}")
        except Exception as e:
            print(f"programa{i}: erro → {e}")

def test_all_with_runTest():
    print("\n=== Testar runTest() para programa1 a programa14 ===")
    for i in range(1, 15):
        prog = globals().get(f"programa{i}")
        if not prog:
            continue
        try:
            ok = runTest(prog, ([], evaluate(prog, [])))
            print(f"programa{i}: passou = {ok}")
        except Exception as e:
            print(f"programa{i}: erro → {e}")

def main():
    test_all_with_evaluate()
    test_all_with_runTest()

    print("\n=== Testar runTestSuite() para os 3 programas escolhidos ===")
    print("Programa 1:", runTestSuite(programa1, testSuite1))
    print("Programa 2:", runTestSuite(programa2, testSuite2))
    print("Programa 3:", runTestSuite(programa3, testSuite3))

    print("\n=== Testar programas mutados (espera-se False) ===")
    print("Programa 1 Mutado:", runTestSuite(programa1_mut, testSuite1))
    print("Programa 2 Mutado:", runTestSuite(programa2_mut, testSuite2))
    print("Programa 3 Mutado:", runTestSuite(programa3_mut, testSuite3))

if __name__ == "__main__":
    main()
