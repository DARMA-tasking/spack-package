# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


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
    git      = "git@github.com:DARMA-tasking/vt.git"

    version("1.0.0", tag="1.0.0")
    version("develop", branch="develop")

    depends_on("mpi")
    depends_on("detector")
    depends_on("checkpoint")

    def cmake_args(self):
        args = [
            "-Ddetector_DIR={}".format(self.spec["detector"].prefix),
            "-Dcheckpoint_DIR={}".format(self.spec["checkpoint"].prefix),
            "-Denable_gtest=OFF",
            "-DVT_NO_BUILD_TESTS=ON",
            "-DVT_NO_BUILD_EXAMPLES=ON",
            "-DVT_THREADING_BACKEND=none"
        ]
        return args
