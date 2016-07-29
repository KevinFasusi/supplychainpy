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
