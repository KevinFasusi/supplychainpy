from Cython.Build import cythonize
from setuptools import setup, find_packages, Extension

extensions =[Extension('supplychainpy.simulations.sim_summary', ['supplychainpy/simulations/sim_summary.pyx']),
             Extension('supplychainpy.demand.eoq', ['supplychainpy/demand/eoq.pyx'])
             ]


setup(name='supplychainpy',
      version='0.0.2',
      description='A library for supply chain, operations and manufacturing, analysis, modeling and simulation.',
      url='https://github.com/KevinFasusi/supplychainpy',
      download_url='https://github.com/KevinFasusi/supplychainpy/tarball/0.0.2',
      author='Kevin Fasusi',
      author_email='kevin@supplybi.com',
      license='BSD 3',
      packages=find_packages(exclude=['docs', 'tests']),
      test_suite='supplychainpy/tests',
      install_requires=['NumPy'],
      keywords=['supply chain', 'operations research', 'operations management', 'simulation'],
      ext_modules=cythonize(extensions),
      )
