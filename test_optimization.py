from Lang import *
from pretty_printing import *
from optimization import *
from contextlib import redirect_stdout

def analisar_programa(nome, prog):
    print(f"\n=== {nome} ===\n")

    print("Original:")
    print(str(prog))

    print("Otimizado:")
    print(str(opt(prog)))

    print("Refatorado:")
    print(str(refactor(prog)))

    print("Nomes declarados:")
    print(names(prog))

    print("\nContagem de instruções:")
    print(instructions(prog))

    print("\nCode smells:")
    print(detect_smells(prog))


def main():
    exemplos = [(nome, obj) for nome, obj in globals().items() if nome.startswith("programa")]

    with open("resultado_optimization.txt", "w", encoding="utf-8") as f:
        with redirect_stdout(f):
            for nome, prog in exemplos:
                analisar_programa(nome, prog)

if __name__ == "__main__":
    main()