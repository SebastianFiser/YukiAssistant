#!/usr/bin/env python3
import sys
from openai import OpenAI


# --- Inicializace klienta (OpenAI automaticky načte API klíč z prostředí) ---
client = OpenAI()


# --- Funkce pro volání OpenAI ---
def openai_call(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Jsi Yuki, virtuální asistent."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()


# --- Funkce pro parsování odpovědi ---
def parse_response(text: str):
    odpoved = ""
    prikaz = ""

    lines = text.splitlines()
    for line in lines:
        if line.startswith("- odpověď:"):
            odpoved = line.replace("- odpověď:", "").strip()
        elif line.startswith("- příkaz:"):
            prikaz = line.replace("- příkaz:", "").strip()
    return odpoved, prikaz


# --- Hlavní funkce pro zpracování příkazu ---
def prikaz(cmd: str):
    print(f"Zpracovávám příkaz: {cmd}")

    prompt = f"""Uživatelský příkaz: {cmd}
Odpověz striktně ve formátu:
- odpověď: <co říkáš uživateli>
- příkaz: <modul>, <akce>, <parametry>"""

    try:
        response_text = openai_call(prompt)
        odpoved, prikaz_text = parse_response(response_text)

        print(f"Odpověď: {odpoved}")
        print(f"Příkaz: {prikaz_text}")
    except Exception as e:
        print("Chyba při komunikaci s OpenAI API:", e)


# --- Hlavní program ---
def main():
    print('Program běží. Napiš "hey yuki" pro aktivaci.')
    while True:
        try:
            text = input().strip()
        except (EOFError, KeyboardInterrupt):
            print()
            continue

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

                if cmd.lower() == 'vypnout':
                    print('Vypínám.')
                    sys.exit(0)
                if cmd.lower() in ('exit', 'quit', 'konec', 'bye'):
                    print('Ukončuji aktivaci, čekám na wake word.')
                    break

                prikaz(cmd)


if __name__ == '__main__':
    main()
