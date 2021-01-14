# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Checkpoint(CMakePackage):
    """Serialization and checkpointing library"""

    homepage = "https://github.com/DARMA-tasking/checkpoint"
    git      = "git@github.com:DARMA-tasking/checkpoint.git"

    version("develop", branch="develop")

    depends_on("detector")

    def cmake_args(self):
        args = ["-Ddetector_DIR={}".format(self.spec["detector"].prefix)]
        return args
