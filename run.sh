#!/usr/bin/env bash
set -euo pipefail

# --- konfigurace ---
VENV_DIR="${HOME}/yuki-env"            # virtuální prostředí
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY_SCRIPT="${PROJECT_DIR}/yuki.py"
ENV_FILE="${PROJECT_DIR}/.env"
LOCALAI_BIN="${PROJECT_DIR}/localai"
MODEL_DIR="${PROJECT_DIR}/models"
MODEL_FILE="$MODEL_DIR/mistral-7b-q4_0.ggml"
MODEL_URL="https://huggingface.co/TheBloke/Mistral-7B-Instruct-GGML/resolve/main/mistral-7b-q4_0.ggml"

# --- kontrola Pythonu a pip ---
command -v python3 >/dev/null 2>&1 || { echo "Python3 nenalezen. Instalujte: sudo apt install python3 python3-venv python3-pip"; exit 1; }
command -v pip3 >/dev/null 2>&1 || { echo "pip3 nenalezen. Instalujte: sudo apt install python3-pip"; exit 1; }

# --- vytvoření venv pokud neexistuje ---
if [ ! -d "$VENV_DIR" ]; then
  echo "Vytvářím virtuální prostředí: $VENV_DIR"
  python3 -m venv "$VENV_DIR"
fi

# --- aktivace venv ---
# shellcheck source=/dev/null
source "${VENV_DIR}/bin/activate"

# --- aktualizace pip a instalace závislostí ---
python -m pip install --upgrade pip setuptools wheel
pip install requests python-dotenv

# --- načtení .env (pokud existuje) ---
if [ -f "$ENV_FILE" ]; then
  echo "Načítám proměnné z .env"
  set -a
  # shellcheck disable=SC1090
  . "$ENV_FILE"
  set +a
fi

# --- stáhnout LocalAI pokud neexistuje ---
if [ ! -f "$LOCALAI_BIN" ]; then
  echo "Stahuji LocalAI..."
  wget https://github.com/go-skynet/LocalAI/releases/download/v1.0.0/localai-linux-arm64.tar.gz -O localai.tar.gz
  tar -xzf localai.tar.gz
  chmod +x localai
  rm localai.tar.gz
fi

# --- stáhnout model pokud neexistuje ---
mkdir -p "$MODEL_DIR"
if [ ! -f "$MODEL_FILE" ]; then
  echo "Stahuji LLaMA model (Mistral 7B quantized)..."
  wget "$MODEL_URL" -O "$MODEL_FILE"
fi

# --- spustit LocalAI ---
echo "Spouštím LocalAI..."
"$LOCALAI_BIN" serve --model "$MODEL_FILE" &
LOCALAI_PID=$!
sleep 5  # počkej, až server naběhne

# --- spustit Yukiho Python skript ---
echo "Spouštím Yukiho..."
python3 "$PY_SCRIPT"

# --- ukončit LocalAI po ukončení Python skriptu ---
kill $LOCALAI_PID
echo "Yuki ukončen, LocalAI zastaven."
