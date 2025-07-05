#!/usr/bin/env bash
set -e

ROOT="chatops-telegram-bot"

# Directories to create
DIRS=(
  "$ROOT"
  "$ROOT/config"
  "$ROOT/bot"
  "$ROOT/bot/handlers"
  "$ROOT/bot/services"
  "$ROOT/tests"
  "$ROOT/.github"
  "$ROOT/.github/workflows"
)

# Files to create
FILES=(
  "$ROOT/README.md"
  "$ROOT/.gitignore"
  "$ROOT/docker-compose.yml"
  "$ROOT/Dockerfile"
  "$ROOT/config/config.yaml.example"
  "$ROOT/bot/main.py"
  "$ROOT/bot/handlers/commands.py"
  "$ROOT/bot/services/github_api.py"
  "$ROOT/bot/services/ci_api.py"
  "$ROOT/tests/test_github_api.py"
  "$ROOT/tests/test_handlers.py"
  "$ROOT/.github/workflows/ci.yml"
)

# Create directories
for DIR in "${DIRS[@]}"; do
  mkdir -p "$DIR"
done

# Create files
for FILE in "${FILES[@]}"; do
  if [ ! -e "$FILE" ]; then
    touch "$FILE"
  fi
done

echo "Project skeleton created at ./$ROOT/"
