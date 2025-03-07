#                           DARMA Toolkit v. 1.5.0
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

    version("1.0.0", tag="1.0.0")
    version("1.5.0", tag="1.5.0")
    version("develop", branch="develop")

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
        "doxygen_enabled",
        default=False,
        description="Enable doxygen generation",
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
        "zoltan_enabled",
        default=False,
        description="Build with Zoltan enabled for ZoltanLB support",
    )
    variant(
        "mpi_guards",
        default=False,
        description="Guards against mis-use of MPI calls in code using vt",
    )
    variant(
        "priorities_enabled",
        default=True,
        description="Enable prioritization of work",
    )
    variant(
        "diagnostics_enabled",
        default=True,
        description="Enable VT component diagnostics for performance analysis",
    )
    variant(
        "diagnostics_runtime_enabled",
        default=False,
        description="Enable VT component diagnostics at runtime by default",
    )
    variant(
        "priority_bits_per_level",
        values=int,
        default=3,
        description="Number of bits per level of priority in envelope",
    )
    variant(
        "unity_build_enabled",
        default=False,
        description="Build with Unity/Jumbo mode enabled (requires CMake >= 3.16)",
    )
    variant(
        "fcontext_enabled",
        default=False,
        description="Force use of fcontext for threading",
    )
    variant(
        "use_openmp",
        default=False,
        description="Force use of OpenMP for threading",
    )
    variant(
        "use_std_thread",
        default=False,
        description="Force use of std::thread for threading",
    )
    variant("build_tests", default=False, description="Build all VT tests")
    variant("build_examples", default=False, description="Build all VT examples")
    variant("kokkos", default=False, description="Enable Kokkos support")

    depends_on("mpi")
    depends_on("darma-magistrate+kokkos", when="+kokkos")
    depends_on("darma-magistrate~kokkos", when="~kokkos")
    depends_on("fmt@7.1.3", when="@develop,1.5:")

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
            "-Dvt_doxygen_enabled={}".format(
                int(self.spec.variants["doxygen_enabled"].value)
            ),
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
            "-Dvt_zoltan_enabled={}".format(
                int(self.spec.variants["zoltan_enabled"].value)
            ),
            "-Dvt_mpi_guards={}".format(int(self.spec.variants["mpi_guards"].value)),
            "-Dvt_priorities_enabled={}".format(
                int(self.spec.variants["priorities_enabled"].value)
            ),
            "-Dvt_diagnostics_enabled={}".format(
                int(self.spec.variants["diagnostics_enabled"].value)
            ),
            "-Dvt_diagnostics_runtime_enabled={}".format(
                int(self.spec.variants["diagnostics_runtime_enabled"].value)
            ),
            "-Dvt_priority_bits_per_level={}".format(
                int(self.spec.variants["priority_bits_per_level"].value)
            ),
            "-Dvt_unity_build_enabled={}".format(
                int(self.spec.variants["unity_build_enabled"].value)
            ),
            "-Dvt_fcontext_enabled={}".format(
                int(self.spec.variants["fcontext_enabled"].value)
            ),
            "-DUSE_OPENMP={}".format(int(self.spec.variants["use_openmp"].value)),
            "-DUSE_STD_THREAD={}".format(
                int(self.spec.variants["use_std_thread"].value)
            ),
        ]

        if self.spec.version >= Version("1.5.0"):
            args.append("-Dvt_external_fmt=ON")

        if self.spec.version > Version("1.3.0"):
            build_tests_arg = "-Dvt_build_tests={}".format(
                int(self.spec.variants["build_tests"].value)
            )
            build_examples_arg = "-Dvt_build_examples={}".format(
                int(self.spec.variants["build_examples"].value)
            )
        else:
            build_tests_arg = "-DVT_BUILD_TESTS={}".format(
                int(self.spec.variants["build_tests"].value)
            )
            build_examples_arg = "-DVT_BUILD_EXAMPLES={}".format(
                int(self.spec.variants["build_examples"].value)
            )

        # Add the arguments to the args list
        args.append(build_tests_arg)
        args.append(build_examples_arg)

        return args
