#!/usr/bin/env bash

# Builds darma-vt against a specific fmt version, to confirm a version
# declared as supported in package.py actually compiles (concretizing
# successfully does not guarantee that).

set -euo pipefail

cur_path=$(pwd)
vt_spack_package="$cur_path/spack-package"

git clone --depth=2 https://github.com/spack/spack.git
. spack/share/spack/setup-env.sh

branch_name=${1:-master}
vt_version=${2}
fmt_version=${3}

git clone -b "$branch_name" https://github.com/DARMA-tasking/spack-package.git

spack repo add "$vt_spack_package"
spack external find

spack install "darma-vt@${vt_version}" build_type=Release "^fmt@${fmt_version}"
