from distutils.core import run_setup

from Cython.Build import cythonize
from setuptools import setup, find_packages, Extension

extensions = [Extension('supplychainpy.simulations.sim_summary', ['supplychainpy/simulations/sim_summary.pyx']),
              Extension('supplychainpy.inventory.eoq', ['supplychainpy/inventory/eoq.pyx'])
              ]

setup(name='supplychainpy',
      version='0.0.4',
      description='A library for supply chain, operations and manufacturing, analysis, modeling and simulation.',
      url='https://github.com/KevinFasusi/supplychainpy',
      download_url='https://github.com/KevinFasusi/supplychainpy/tarball/0.0.4',
      author='Kevin Fasusi',
      author_email='kevin@supplybi.com',
      license='BSD 3',
      packages=find_packages(exclude=['docs', 'tests', 'scratch.py']),
      test_suite='supplychainpy/tests',
      install_requires=['NumPy',
                        'cython',
                        'flask',
                        'scipy',
                        'pandas',
                        'sqlalchemy',
                        'flask-restful',
                        'flask-restless',
                        'flask-script',
                        'flask-sqlalchemy',
                        'flask-uploads',
                        'flask-wtf'
                        ],
      keywords=['supply chain', 'operations research', 'operations management', 'simulation'],
      ext_modules=cythonize(extensions),
      entry_points={
          'console_scripts': [
              'supplychainpy = supplychainpy.supplychain:main'
          ]
      },
      package_data={
          'supplychainpy': ['reporting/static/*', 'reporting/templates/*', 'sample_data/*', '_pickled/*']
      })

#run_setup()