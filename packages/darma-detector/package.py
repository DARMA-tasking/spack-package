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

from spack import *


class DarmaDetector(CMakePackage):
    """Minimal C++ detection idiom implementation

    detector is a small library that implements static/compile-time type
    introspection in C++. With this code, we can check if a type has methods,
    type aliases, or members that are exactly matching or convertible to a
    particular interface. Because this library requires C++-14, it is separated
    from the other DARMA/* libraries."""

    homepage = "https://github.com/DARMA-tasking/detector"
    git      = "git@github.com:DARMA-tasking/detector.git"

    version("master", branch="master")

    sanity_check_is_file = ['cmake/detectorConfig.cmake']
    sanity_check_is_file = ['cmake/detectorTargets.cmake']
    sanity_check_is_file = ['include/detector.h']
    sanity_check_is_file = ['include/detector_common.h']
    sanity_check_is_file = ['include/detector_headers.h']
    sanity_check_is_file = ['include/none_such.h']
    sanity_check_is_file = ['include/traits.h']
    sanity_check_is_file = ['include/void_t.h']
