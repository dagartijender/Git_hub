#!/usr/bin/env bash
set -euo pipefail

if [[ "$#" -ne 3 ]]; then
  echo "Usage: $0 <values-file> <image-tag> <repository-root>" >&2
  exit 2
fi

values_file="$1"
image_tag="$2"
repository_root="$3"
target="${repository_root}/${values_file}"

if [[ ! -f "${target}" ]]; then
  echo "Values file not found: ${target}" >&2
  exit 1
fi

python3 - "${target}" "${image_tag}" <<'PY'
import re
import sys
from pathlib import Path

path = Path(sys.argv[1])
tag = sys.argv[2]
content = path.read_text(encoding="utf-8")
updated, count = re.subn(
    r"(?m)^(\s*tag:\s*)[^\s#]+(\s*(?:#.*)?)$",
    lambda match: f'{match.group(1)}"{tag}"{match.group(2)}',
    content,
    count=1,
)

if count != 1:
    raise SystemExit(f"Expected exactly one image tag in {path}; found {count}")

path.write_text(updated, encoding="utf-8")
PY

echo "Updated ${values_file} to image tag ${image_tag}"
