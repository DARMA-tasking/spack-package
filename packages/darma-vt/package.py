#                           DARMA Toolkit v. 1.7.0
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


from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class DarmaVt(CMakePackage):
    """vt : Virtual Transport HPC runtime

    vt is an active messaging layer that utilizes C++ object virtualization to
    manage virtual endpoints with automatic location management. vt is directly
    built on top of MPI to provide efficient portability across different
    machine architectures. Empowered with virtualization, vt can automatically
    perform dynamic load balancing to schedule scientific applications across
    diverse platforms with minimal user input.

    vt abstracts the concept of a node/rank/worker/thread so a program can be
    written in terms of virtual entities that are location independent. Thus,
    they can be automatically migrated and thereby executed on varying hardware
    resources without explicit programmer mapping, location, and communication
    management."""

    homepage = "https://github.com/DARMA-tasking/vt"
    git = "https://github.com/DARMA-tasking/vt.git"

    license("BSD-3-Clause")

    version("develop", branch="develop")
    version("1.7.0", tag="1.7.0")
    version("1.6.0", tag="1.6.0")
    version("1.5.0", tag="1.5.0")
    version("1.4.0", tag="1.4.0")
    version("1.3.0", tag="1.3.0")
    version("1.2.2", tag="1.2.2")

    variant(
        "lb_enabled",
        default=True,
        description="Compile with support for runtime load balancing",
    )
    variant(
        "trace_enabled",
        default=False,
        description="Compile with support for runtime tracing",
    )
    variant(
        "trace_only",
        default=False,
        description="Compile vt in trace-only mode",
    )
    variant(
        "mimalloc_enabled",
        default=False,
        description="Enable mimalloc, alternative allocator for debugging memory usage/frees/corruption",
    )
    variant(
        "asan_enabled",
        default=False,
        description="Enable building with address sanitizer",
    )
    variant(
        "werror_enabled",
        default=False,
        description="Treat all warnings as errors",
    )
    variant(
        "pool_enabled",
        default=True,
        description="Use memory pool in vt for message allocation",
    )
    variant(
        "mpi_guards",
        default=False,
        description="Guards against mis-use of MPI calls in code using vt",
    )
    variant("kokkos", default=False, description="Enable Kokkos support")

    depends_on("mpi")

    depends_on("darma-magistrate@1.6.0", when="@1.6.0")
    depends_on("darma-magistrate@develop", when="@:1.5")
    depends_on("darma-magistrate@develop+kokkos", when="@develop")

    # depends_on("fmt@11.1.3", when="@develop,1.5:")

    # VT 1.6.0 uses non-constexpr format strings which is invalid under C++20
    # (triggered when Kokkos propagates cxx_std_20 transitively). Fix:
    # - elm_id.h: make fmt_str constexpr
    # - debug_print.h: wrap runtime format string with fmt::runtime()
    # patch("vt_fmt_11_2.patch", when="@1.6.0")

    depends_on("fmt@11.2.0")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    sanity_check_is_dir = ["include/vt"]
    sanity_check_is_file = ["cmake/vtConfig.cmake", "cmake/vtTargets.cmake"]

    def cmake_args(self):
        args = [
            "-Dmagistrate_ROOT={}".format(self.spec["darma-magistrate"].prefix),
            "-Dvt_lb_enabled={}".format(int(self.spec.variants["lb_enabled"].value)),
            "-Dvt_trace_enabled={}".format(
                int(self.spec.variants["trace_enabled"].value)
            ),
            "-Dvt_trace_only={}".format(int(self.spec.variants["trace_only"].value)),
            "-Dvt_mimalloc_enabled={}".format(
                int(self.spec.variants["mimalloc_enabled"].value)
            ),
            "-Dvt_asan_enabled={}".format(
                int(self.spec.variants["asan_enabled"].value)
            ),
            "-Dvt_werror_enabled={}".format(
                int(self.spec.variants["werror_enabled"].value)
            ),
            "-Dvt_pool_enabled={}".format(
                int(self.spec.variants["pool_enabled"].value)
            ),
            "-Dvt_mpi_guards={}".format(int(self.spec.variants["mpi_guards"].value)),
        ]

        if self.spec.version >= Version("1.5.0"):
            args.append("-Dvt_external_fmt=ON")
            args.append("-Dfmt_ROOT={}".format(self.spec["fmt"].prefix))

        if self.spec.version > Version("1.3.0"):
            args.extend([
                self.define("vt_build_tests", self.run_tests),
                self.define("vt_build_examples", self.run_tests)
            ]);
        else:
            args.extend([
                self.define("VT_BUILD_TESTS", self.run_tests),
                self.define("VT_BUILD_EXAMPLES", self.run_tests)
            ]);

        return args

    def check(self):
        with working_dir(self.build_directory):
            ctest("--output-on-failure", "--label-regex", "unit_test|example")
