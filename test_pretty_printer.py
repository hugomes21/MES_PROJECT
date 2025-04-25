from Lang import *
from parser import *
from pretty_printing import *
import difflib
from contextlib import redirect_stdout

def show_diff(a, b):
    a_lines = repr(a).splitlines()
    b_lines = repr(b).splitlines()
    diff = difflib.unified_diff(a_lines, b_lines, fromfile='original', tofile='parsed', lineterm='')
    return "\n".join(diff)

def prop_roundtrip(ast):
    code = str(ast)
    print("Código gerado para roundtrip:\n---\n" + code + "\n---")
    try:
        ast2 = parse_code(code)
    except Exception as e:
        print(f"❌ Erro ao fazer parse: {e}")
        return False
    
    print("AST original:", repr(ast))
    print("AST roundtrip:", repr(ast2))
    if ast == ast2:
        return True
    else:
        print("❌ ASTs diferentes!")
        print(show_diff(ast, ast2))
        return False


def main():
    exemplos = [(nome, obj) for nome, obj in globals().items() if nome.startswith("programa")]

    with open("resultado_roundtrip.txt", "w", encoding="utf-8") as f:
        with redirect_stdout(f):
            for nome, prog in exemplos:
                print(f"\nTeste de roundtrip: {nome}")
                print("Código pretty-printed:")
                print(str(prog))
                resultado = prop_roundtrip(prog)
                print("✅ Roundtrip OK" if resultado else "❌ Roundtrip FALHOU")
                print("-" * 50)

if __name__ == "__main__":
    main()