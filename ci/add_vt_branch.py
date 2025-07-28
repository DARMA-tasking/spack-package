#!/usr/bin/env python3

"""
Modifies the `darma-vt` package's `package.py` file to include a version entry for a given 'vt' branch.

This is crucial for enabling Spack integration during 'vt' pull request validation.
By appending declared 'vt' versions with the specified branch name, you can install the package using `spack install darma-vt@<GIT_BRANCH>`,
which facilitates early detection of issues before changes are merged into the 'develop' branch.

Usage:
    python add_vt_branch.py <branch_name>

Args:
    branch_name (str): The name of the branch to be added to the `package.py` file.
"""

import sys
import re
from pathlib import Path

if len(sys.argv) < 2 or sys.argv[1].strip() == "":
    sys.exit("add_vt_branch.py: Branch name not provided or empty - skipping! (usage: add_vt_branch.py <branch_name>)")

branch = sys.argv[1]

script_dir = Path(__file__).resolve().parent
package_file = script_dir.parent / "packages" / "darma-vt" / "package.py"

text = package_file.read_text().splitlines()
version_pattern = re.compile(r"^\s*version\(")
last_version_idx = max(i for i, line in enumerate(text) if version_pattern.match(line))
indent = re.match(r"^(\s*)", text[last_version_idx]).group(1)
new_entry = f'{indent}version("{branch}", branch="{branch}")'

if all(line.strip() != new_entry.strip() for line in text):
    text.insert(last_version_idx + 1, new_entry)
    package_file.write_text("\n".join(text) + "\n")
