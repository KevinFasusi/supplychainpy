# Copyright (c) 2015-2016, The Authors and Contributors
# <see AUTHORS file>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the
# following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

class SKU:
    def __init__(self):
        self.length = None
        self.width = None
        self.height = None
        self.weight = None
        self.__bill_of_materials = list


class Package(SKU):
    def __init__(self):
        super().__init__()
        self.contents = []


class PalletBuilder:
    def __init__(self):
        self.package = None

    def make_new_pallet(self):
        self.package = Package()


class PackageDirector:
    def __init__(self, pallet_builder: PalletBuilder):
        self._package_builder = pallet_builder

    def construct_package(self, length: float, width: float, height: float, weight: float):
        self._package_builder.make_new_pallet()
        self._package_builder.package.height = height
        self._package_builder.package.length = length
        self._package_builder.package.width = width
        self._package_builder.package.width = weight

    def add_package(self, package: Package):
        self._package_builder.package.package.append(package)

    def recalculate_dimensions(self):
        self._package_builder.package.recalculate_weight()
        self._package_builder.package.recalculate_height()

    @property
    def Package(self) -> Package():
        return self._package_builder.package


class ShippingContainer(Package):
    def __init__(self):
        super().__init__()
