from setuptools import setup

setup(name='supplybipy',
      version='0.1',
      description='Supply Chain Analysis, Modeling and Simulation Tools',
      url='192.168.1.119:/opt/git/supplybipy.git',
      author='Kevin Fasusi',
      author_email='fasusi.kevin@gmail.com',
      license='BSD 3',
      packages=['supplybipy', 'supplybipy/demand'],
      test_suite='supplybipy/tests',
      zip_safe=False,
      install_requires=['numpy'],
      entry_points={
            'console_scripts':[
                  'supplybi=supplybipy.supplybi:main'
            ]
      }
      )
