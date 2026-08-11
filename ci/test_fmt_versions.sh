#!/usr/bin/env bash

# Verifies that darma-vt's fmt version constraints concretize as expected
# across build tags. Uses `spack spec` only, so no compiling is required

set -euo pipefail

cur_path=$(pwd)
vt_spack_package="$cur_path/spack-package"

git clone --depth=2 --branch v1.2.2 https://github.com/spack/spack.git
. spack/share/spack/setup-env.sh

branch_name=${1:-master}
git clone -b "$branch_name" https://github.com/DARMA-tasking/spack-package.git

spack repo add "$vt_spack_package"

failures=0

# Checks whether `<vt_spec> ^fmt@<fmt_version>` concretizes, and compares
# that outcome against the expected "pass" or "fail" result.
check_concretizes() {
  local vt_spec=$1
  local fmt_version=$2
  local expected=$3

  local result="fail"
  if spack spec -N --fresh "$vt_spec" "^fmt@${fmt_version}" > /dev/null 2>&1; then
    result="pass"
  fi

  if [ "$result" != "$expected" ]; then
    echo "UNEXPECTED: $vt_spec ^fmt@${fmt_version} -> $result (expected $expected)"
    failures=$((failures + 1))
  else
    echo "OK: $vt_spec ^fmt@${fmt_version} -> $result"
  fi
}

# 1.5.0 fails to compile against fmt 11 (formatter const-correctness and a
# missing <memory> include that fmt 10 used to pull in transitively)
check_concretizes "darma-vt@1.5.0" "10.2.1" "pass"
check_concretizes "darma-vt@1.5.0" "11.2.0" "fail"
check_concretizes "darma-vt@1.5.0" "10.2.0" "fail"

# 1.6.0 and 1.7.0 support the full fmt@10.2.1:11 range
for vt_version in 1.6.0 1.7.0; do
  check_concretizes "darma-vt@${vt_version}" "10.2.1" "pass"
  check_concretizes "darma-vt@${vt_version}" "11.2.0" "pass"
  check_concretizes "darma-vt@${vt_version}" "10.2.0" "fail"
  check_concretizes "darma-vt@${vt_version}" "12.0.0" "fail"
done

# develop tracks fmt@12
check_concretizes "darma-vt@develop" "12.2.0" "pass"
check_concretizes "darma-vt@develop" "11.2.0" "fail"

if [ "$failures" -ne 0 ]; then
  echo "$failures fmt version constraint check(s) failed"
  exit 1
fi

echo "All fmt version constraint checks passed"
