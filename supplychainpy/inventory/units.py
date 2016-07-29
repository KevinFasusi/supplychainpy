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
