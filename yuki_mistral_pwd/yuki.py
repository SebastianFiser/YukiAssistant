#!/usr/bin/env python3
import sys
from llama_cpp import Llama 

# -------------------------------
# Konfigurace modelu
# -------------------------------
MODEL_PATH = "/home/sebastian/yuki assistant/models/mistral-7b-v0.1.Q4_K_M.gguf"
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=1024,
    n_threads=4,
    verbose=False
)

# -------------------------------
# Funkce pro dotaz modelu
# -------------------------------
def llama_call(prompt: str) -> str:
    output = llm(prompt, max_tokens=200, temperature=0.1)
    return output["choices"][0]["text"].strip()

# -------------------------------
# Parsování odpovědi
# -------------------------------
def parse_response(text: str):
    odpoved = ""
    prikaz_text = ""
    lines = text.splitlines()
    for line in lines:
        if line.lower().startswith("- odpověď:"):
            odpoved = line.split(":", 1)[1].strip()
        elif line.lower().startswith("- příkaz:"):
            prikaz_text = line.split(":", 1)[1].strip()
    return odpoved, prikaz_text

# -------------------------------
# Zpracování příkazu
# -------------------------------
def prikaz(cmd: str):
    print(f"Prompt: příkaz přijat -> {cmd}")

    prompt = f"""Uživatelský vstup: {cmd}
Pokud je vstup otázka, napiš:
- odpověď: <odpověď na otázku>
- příkaz: none

Pokud je vstup příkaz aplikace, napiš:
- odpověď: potvrzení příkazu
- příkaz: <modul>, <akce>, <parametry>"""

    response_text = llama_call(prompt)
    odpoved, prikaz_text = parse_response(response_text)
    print(f"Odpověď: {odpoved}")
    print(f"Příkaz: {prikaz_text}")

# -------------------------------
# Hlavní loop mini-shellu
# -------------------------------
def main():
    print('Program běží. Napiš "hey yuki" pro aktivaci.')

    while True:
        try:
            text = input().strip()
        except (EOFError, KeyboardInterrupt):
            print()
            continue

        if not text:
            continue

        # --- globální vypnutí ---
        if text.lower() == 'vypnout':
            print('Vypínám celý program.')
            sys.exit(0)

        # čekání na wake word
        if text.lower() == 'hey yuki':
            print('aktivováno... čekám na příkaz')
            while True:
                try:
                    cmd = input('> ').strip()
                except (EOFError, KeyboardInterrupt):
                    print()
                    break

                if not cmd:
                    continue

                # --- v aktivaci, exit jen ukončí aktivaci ---
                if cmd.lower() in ('exit', 'quit', 'konec', 'bye'):
                    print('Ukončuji aktivaci, čekám na wake word.')
                    break

                # --- v aktivaci, vypnout ukončí celý program ---
                if cmd.lower() == 'vypnout':
                    print('Vypínám celý program.')
                    sys.exit(0)

                # zpracování příkazu modelem
                prikaz(cmd)

if __name__ == '__main__':
    main()
