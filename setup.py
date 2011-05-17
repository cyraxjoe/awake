from distutils.core import setup

setup(name='awake',
      version='0.6.1',
      author='Joel Rivera',
      author_email='joelriv@gmail.com',
      url='http://github.com/cyraxjoe/awake',
      license='GPL',
      package_dir={'':'lib/'},
      scripts=['awake.py',],
      py_modules=['wol',],
      provides=['wol',],
      classifiers=['Environment :: Console',
                   'Operating System :: OS Independent',
                   'License :: OSI Approved :: GNU General Public License (GPL)',
                   'Programming Language :: Python :: 2.4'],
      description='Command line program to wake-on-lan a remote host.'
      )
