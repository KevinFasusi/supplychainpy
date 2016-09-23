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

from supplychainpy.inventory.units import SKU, Package


class Pallet:
    def __init__(self):
        self.length = None
        self.width = None
        self.height = None
        self.weight = None
        self.package = []

    def recalculate_weight(self):
        pass

    def recalculate_height(self):
        pass


class PalletBuilder:
    def __init__(self):
        self.pallet = None

    def make_new_pallet(self):
        self.pallet = Pallet()


class PalletDirector:
    def __init__(self, pallet_builder: PalletBuilder):
        self._pallet_builder = pallet_builder

    def construct_pallet(self, length: float, width: float, height: float, weight: float):
        self._pallet_builder.make_new_pallet()
        self._pallet_builder.pallet.height = height
        self._pallet_builder.pallet.length = length
        self._pallet_builder.pallet.width = width
        self._pallet_builder.pallet.width = weight

    def add_package(self, package: Package):
        self._pallet_builder.pallet.package.append(package)

    def recalculate_dimensions(self):
        self._pallet_builder.pallet.recalculate_weight()
        self._pallet_builder.pallet.recalculate_height()

    def __add__(self, other):
        self._pallet_builder.pallet.package.append(other)

    @property
    def pallet(self)-> Pallet():
        return self._pallet_builder.pallet


class ShippingContainer(Pallet):
    def __init__(self):
        super().__init__()

        # how to represent a unit of packaging
        # parameter for unt nase shape circular or square to calculate fill
