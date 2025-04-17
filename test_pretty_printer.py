from Lang import programa1, programa2, programa3
from parser import parse_code

def prop_roundtrip(ast):
    code = str(ast)
    print("Código gerado para roundtrip:\n---\n" + code + "\n---")
    ast2 = parse_code(code)
    return ast == ast2

def main():
    exemplos = [("programa1", programa1), ("programa2", programa2), ("programa3", programa3)]
    for nome, prog in exemplos:
        print(f"Exemplo: {nome}")
        print("Código pretty-printed:")
        print(str(prog))
        print("Roundtrip:", "OK" if prop_roundtrip(prog) else "FALHOU")
        print("-" * 40)

if __name__ == "__main__":
    main()