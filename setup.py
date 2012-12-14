import os
from distutils.core import setup  


REPODIR = os.path.dirname(os.path.realpath(__file__))


def _get_longdesc(repodir):
    return open(os.path.join(repodir, 'README')).read()

def _get_license(repodir):
    return open(os.path.join(repodir, 'LICENSE')).read()

def _get_version(repodir):
    version = 'UNKNOWN'
    init = open(os.path.join(repodir, 'src', 'awake', '__init__.py'))
    for line in init.readlines():
        if '__version__' in line and '=' in line:
            version = line.split('=')[-1].strip()
            version = version.replace('"', '').replace("'", '')
            break
    init.close()
    return version

version = _get_version(REPODIR)
longdesc = _get_longdesc(REPODIR)
license_ = _get_license(REPODIR)

classifiers=['Environment :: Console',
             'Operating System :: OS Independent',
             'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
             'Programming Language :: Python :: 2.4',
             'Programming Language :: Python :: 2.5',
             'Programming Language :: Python :: 2.6',
             'Programming Language :: Python :: 2.7',
             'Programming Language :: Python :: 3.0',
             'Programming Language :: Python :: 3.1',
             'Programming Language :: Python :: 3.2',
             'Programming Language :: Python :: 3.3',
             'Intended Audience :: End Users/Desktop',
             'Intended Audience :: Developers',
             'Intended Audience :: System Administrators']

setup(name='awake',
      version=version,
      author='Joel Rivera',
      author_email='rivera@joel.mx',
      maintainer='Joel Rivera',
      maintainer_email='rivera@joel.mx',
      url='http://github.com/cyraxjoe/awake',
      download_url='https://github.com/cyraxjoe/awake/archive/v%s.zip' % version,
      license=license_,
      package_dir={'': 'src'},
      scripts=['src/scripts/awake',],
      packages=['awake',],
      provides=['awake',],
      classifiers=classifiers,
      platforms=['linux2', 'win32', 'cygwin', 'darwin'],
      description='Command and library to "wake on lan" a remote host.',
      long_description=longdesc)
