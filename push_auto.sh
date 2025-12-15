#!/usr/bin/env bash
set -e

# ====== CONFIG ======
REPO_DIR="$HOME/github/Internship"
USERNAME="hazbiu"

# ⛔ PUT YOUR TOKEN HERE LOCALLY (DO NOT COMMIT THIS FILE)
TOKEN="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"
# ====================

cd "$REPO_DIR"

if [[ "$TOKEN" == "PASTE_YOUR_GITHUB_TOKEN_HERE" ]]; then
  echo "ERROR: Token not set"
  exit 1
fi

ASKPASS=$(mktemp)
cat <<EOF > "$ASKPASS"
#!/usr/bin/env bash
case "\$1" in
  Username*) echo "$USERNAME" ;;
  Password*) echo "$TOKEN" ;;
esac
EOF

chmod +x "$ASKPASS"

GIT_ASKPASS="$ASKPASS" \
GIT_TERMINAL_PROMPT=1 \
git push

rm -f "$ASKPASS"

