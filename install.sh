#!/usr/bin/env bash
set -euo pipefail

# Atualiza pip (garante que o ambiente tenha a última versão)
python -m pip install --upgrade pip

# Instala o Norm Code direto do repositório
pip install -U "git+https://github.com/SEU-USUARIO/norm-code.git"

cat <<'ENDMSG'

✅ Norm Code instalado com sucesso!
🚀 Use:
   norm-code ask "Sua pergunta"
   norm-code skill list
   norm-code skill run nome_da_skill args...

⚙️ Caso a Ollama esteja em outro host/porta, exporte:
   export OLLAMA_HOST="http://IP:PORT"

ENDMSG
