from setuptools import setup, find_packages

setup(name='supplychainpy',
      version='0.0.1',
      description='A library for supply chain, operations and manufacturing, analysis, modeling and simulation.',
      url='https://github.com/KevinFasusi/supplychainpy',
      download_url='https://github.com/KevinFasusi/supplychainpy/tarball/0.1',
      author='Kevin Fasusi',
      author_email='kevin@supplybi.com',
      license='BSD 3',
      packages=find_packages(exclude=['docs', 'tests']),
      test_suite='supplychainpy/tests',
      install_requires=['MumPy'],
      keywords=['supply chain', 'operations research', 'operations management', 'simulation'],
      )
