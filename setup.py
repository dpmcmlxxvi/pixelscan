
from codecs import open
from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    README = f.read()

with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    author='Daniel Pulido',
    author_email='dpmcmlxxvi@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
    package_data={'': ['DESCRIPTION.rst', 'README.rst']},
    include_package_data=True,
    description='A library to scan pixels on a grid in a variety of patterns.',
    keywords='distance image metric pixel raster scan',
    license='MIT',
    long_description=long_description,
    name='pixelscan',
    packages=find_packages(exclude=['tests']),
    url='https://github.com/dpmcmlxxvi/pixelscan/tarball/v0.1.0',
    version='0.1.0',
)
