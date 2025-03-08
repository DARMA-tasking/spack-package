#                           DARMA Toolkit v. 1.0.0
#                        DARMA/vt => Virtual Transport
#
# Copyright 2019 National Technology & Engineering Solutions of Sandia, LLC
# (NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the U.S.
# Government retains certain rights in this software.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Questions? Contact darma@sandia.gov

import spack.build_systems.cmake
from spack.package import *


class DarmaMagistrate(CMakePackage):
    """Serialization and checkpointing library"""

    homepage = "https://github.com/DARMA-tasking/magistrate"
    git = "https://github.com/DARMA-tasking/magistrate.git"

    version("develop", branch="develop")
    variant("kokkos", default=False, description="Enable Kokkos support")

    sanity_check_is_dir = ["include/checkpoint"]
    sanity_check_is_file = [
        "cmake/magistrateConfig.cmake",
        "cmake/magistrateTargets.cmake",
        "lib/libmagistrate.a"
    ]

    depends_on("kokkos", when="+kokkos")
    depends_on("googletest", type=("test"))

    def cmake_args(self):
        args = [
            self.define("magistrate_tests_enabled", self.run_tests),
            self.define("magistrate_examples_enabled", self.run_tests)
        ]

        if "+kokkos" in self.spec:
            args.append(self.define("Kokkos_ROOT={}", self.spec['kokkos'].prefix))

        return args
