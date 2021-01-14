# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Detector(CMakePackage):
    """Minimal C++ detection idiom implementation

    detector is a small library that implements static/compile-time type
    introspection in C++. With this code, we can check if a type has methods,
    type aliases, or members that are exactly matching or convertible to a
    particular interface. Because this library requires C++-14, it is separated
    from the other DARMA/* libraries."""

    homepage = "https://github.com/DARMA-tasking/detector"
    git      = "git@github.com:DARMA-tasking/detector.git"

    version("master", branch="master")
