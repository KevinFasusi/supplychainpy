from setuptools import setup

setup(name='supplychainpy',
      version='0.1',
      description='Supply Chain Analysis, Modeling and Simulation Tools',
      url='https://github.com/supplybi/supplychainpy',
      author='Kevin Fasusi',
      author_email='kevin@supplybi.com',
      license='BSD 3',
      packages=['supplychainpy', 'supplychainpy/demand'],
      test_suite='supplychainpy/tests',
      zip_safe=False,
      install_requires=['numpy'],
      entry_points={
            'console_scripts':[
                  'supplychainpy=supplychainpy.supplybi:main'
            ]
      }
      )
