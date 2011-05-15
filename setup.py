from distutils.core import setup

setup(name='awake',
      version='0.6',
      author='Joel Rivera',
      author_email='joelriv@gmail.com',
      license='GPL',
      package_dir={'':'lib/'},
      scripts=['awake.py',],
      py_modules=['wol',],
      classifiers=['Environment :: Console',
                   'Operating System :: OS Independent'],
      description='Command line program to wake-on-lan a remote host.'
      )
