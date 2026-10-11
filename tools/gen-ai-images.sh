#!/bin/bash
# codex 내장 image_gen으로 AI 이미지를 생성한다. 사용: tools/gen-ai-images.sh [동시실행수]
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/assets/img/ai"; LOG="$ROOT/tools/logs"; mkdir -p "$OUT" "$LOG"
N="${1:-4}"
COMMON=$(python3 -I -c 'import json,sys;print(json.load(open(sys.argv[1]))["common"])' "$ROOT/tools/ai-images.json")
while IFS=$'\t' read -r file prompt; do
  { [ -f "$OUT/$file" ] || [ -f "$OUT/${file%.png}.jpg" ]; } && { echo "skip $file"; continue; }
  while [ "$(jobs -rp | wc -l)" -ge "$N" ]; do sleep 3; done
  (
    codex exec --skip-git-repo-check -s workspace-write -C "$OUT" \
      "Use the built-in image_gen tool (imagegen skill, built-in mode) to generate ONE image, then copy the final PNG into the current working directory as $file. Do nothing else.
Use case: photorealistic-natural
Asset type: website image for a Korean residential village pre-sale introduction page
Primary request: $prompt
$COMMON" < /dev/null > "$LOG/$file.log" 2>&1
    [ -f "$OUT/$file" ] && echo "done $file" || echo "FAIL $file"
  ) &
done < <(python3 -I -c 'import json,sys
for i in json.load(open(sys.argv[1]))["images"]: print(i["file"]+"\t"+i["prompt"])' "$ROOT/tools/ai-images.json")
wait
echo ALL_DONE
