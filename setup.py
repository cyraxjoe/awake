from distutils.core import setup
from glob import glob



setup(name='awake',
      version='1.0',
      author='Joel Rivera',
      author_email='joelriv@gmail.com',
      provides='wol',
      license='GPL',
      package_dir={'':'lib/'},
      scripts=['awake.py',],
      py_modules=['wol',],
      classifiers=['Enviroment :: Console',
                   'Operating System :: Os independent',],
      description='Wake on lan'
      )
