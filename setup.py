from setuptools import setup

setup(name='supplybipy',
      version='0.1',
      description='Supply Chain Analysis, Modeling and Simulation Tools',
      url='192.168.1.119:/opt/git/supplybipy.git',
      author='Kevin Fasusi',
      author_email='fasusi.kevin@gmail.com',
      license='MIT',
      packages=['supplybipy','supplybipy/orders'],
      test_suite='supplybipy/tests',
      zip_safe=False)