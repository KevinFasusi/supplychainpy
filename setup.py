import os
from Cython.Build import cythonize
from setuptools import setup, find_packages, Extension

extensions = [
    Extension('supplychainpy.simulations.sim_summary',
              ['supplychainpy/simulations/sim_summary.pyx']),
    Extension('supplychainpy.simulations.monte_carlo_simulation',
              ['supplychainpy/simulations/monte_carlo_simulation.pyx']),
    Extension('supplychainpy.inventory.eoq', ['supplychainpy/inventory/eoq.pyx']),
    Extension('supplychainpy.demand._squared_error',
              ['supplychainpy/demand/_squared_error.pyx']),
    Extension('supplychainpy.demand._evo_algo',
              ['supplychainpy/demand/_evo_algo.pyx']),
]
# only required for pypi
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here,'LOG.txt')) as f:
    long_description = f.read().strip()

setup(name='supplychainpy',
      version='0.0.5',
      description='A library for supply chain, operations and manufacturing, analysis, modelling and simulation.',
      url='https://github.com/KevinFasusi/supplychainpy',
      download_url='https://github.com/KevinFasusi/supplychainpy/tarball/0.0.5',
      author='Kevin Fasusi',
      author_email='kevin@supplybi.com',
      license='BSD 3',
      packages=find_packages(exclude=['docs', 'tests', 'scratch.py']),
      test_suite='supplychainpy/tests',
      install_requires=['numpy',
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
                        'flask-wtf',
                        'textblob',
                        'Simplejson',
                        'wtforms'
                        ],
      keywords=['supply chain', 'operations research', 'operations management', 'simulation'],
      ext_modules=cythonize(extensions),
      entry_points={
          'console_scripts': [
              'supplychainpy = supplychainpy.supplychain:main'
          ]
      },
      long_description= long_description,
      classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.5",
    ],
      package_data={
          'supplychainpy': ['reporting/dashboard/templates/dashboard/*','reporting/*','reporting/static/images/*','reporting/static/fonts/*','reporting/static/scripts/*','reporting/static/styles/*','reporting/static/*', 'reporting/templates/*', 'sample_data/*.csv', 'sample_data/*.py','_pickled/*']
      })
