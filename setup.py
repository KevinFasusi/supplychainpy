import os
from Cython.Build import cythonize
from setuptools import setup, find_packages, Extension

extensions = [Extension('supplychainpy.simulations.sim_summary', ['supplychainpy/simulations/sim_summary.pyx']),
              Extension('supplychainpy.inventory.eoq', ['supplychainpy/inventory/eoq.pyx'])
              ]

here = os.path.dirname(os.path.abspath(__file__))
f = open(os.path.join(here,'LOG.txt'))
long_description = f.read().strip()

f.close()
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
      install_requires=['numpy',
                        'cython',
                        'flask',
                        'scipy',
                        'pandas',
                        'SqlAlchemy',
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
      long_description=long_description,
      classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.5",
    ],
      package_data={
          'supplychainpy': ['reporting/static/*', 'reporting/templates/*', 'sample_data/*.csv', 'sample_data/*.py','_pickled/*']
      })
