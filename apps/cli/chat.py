import asyncio

from host.chat_engine import run_chat
from host.settings import load_settings


def main():
    s = load_settings()
    print(f"Chat local (modelo: {s.model}). Escribe 'salir'.\n")
    while True:
        txt = input("Tú> ").strip()
        if txt.lower() in {"salir", "exit", "quit"}:
            break
        ans = asyncio.run(run_chat(txt, s, use_history=True))
        print(f"\nIA> {ans}\n")


if __name__ == "__main__":
    main()
