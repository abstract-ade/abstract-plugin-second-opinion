#!/usr/bin/env python3
"""Checks this repository's plugin package the way Abstract does before it
installs one (ABS-84): the files `git archive` exports (README, tests and CI
are export-ignored), with `manifest.json` at the root, no executables, no
links, nothing outside the folder, under 25 MB, and every file the manifest
names present. It reads files only; nothing in the package runs."""

import json
import os
import re
import stat
import subprocess
import sys
import tarfile
import tempfile

LIMIT = 25 * 1024 * 1024


def main() -> int:
    problems = []
    with tempfile.TemporaryDirectory() as scratch:
        archive = os.path.join(scratch, "package.tar")
        subprocess.run(["git", "archive", "--format=tar", "-o", archive, "HEAD"], check=True)
        files = {}
        with tarfile.open(archive) as tar:
            for member in tar.getmembers():
                name = member.name
                if name.startswith("/") or ".." in name.split("/"):
                    problems.append(f"{name}: outside the package")
                if member.issym() or member.islnk():
                    problems.append(f"{name}: links aren't allowed")
                elif member.isfile():
                    if member.mode & 0o111:
                        problems.append(f"{name}: executable files aren't allowed")
                    files[name] = member.size
        total = sum(files.values())
        if total > LIMIT:
            problems.append(f"the package is {total} bytes, over the 25 MB limit")
        if "manifest.json" not in files:
            problems.append("no manifest.json at the root")
        else:
            subprocess.run(["git", "archive", "--format=tar", "-o", archive, "HEAD", "manifest.json"], check=True)
            with tarfile.open(archive) as tar:
                manifest = json.load(tar.extractfile("manifest.json"))
            for key in ("api", "id", "name", "version"):
                if key not in manifest:
                    problems.append(f"manifest.json has no {key}")
            if not re.fullmatch(r"[a-z0-9]+(\.[a-z0-9-]+)+", str(manifest.get("id", ""))):
                problems.append(f"manifest id {manifest.get('id')!r} isn't a reverse-DNS id")
            named = [manifest.get("entry") or "", manifest.get("background") or "", manifest.get("agent") or ""]
            tracker = (manifest.get("contributes") or {}).get("issueTracker") or {}
            named.append(tracker.get("icon") or "")
            named += [agent.get("icon") or "" for agent in (manifest.get("contributes") or {}).get("agents") or []]
            for path in filter(None, named):
                if path not in files:
                    problems.append(f"manifest.json names {path}, which isn't in the package")
    for problem in problems:
        print(f"::error::{problem}")
    if not problems:
        print(f"The package is valid: {len(files)} files, {total} bytes.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
