
import os
from setuptools import find_packages

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

PACKAGE_PATH = os.path.abspath(os.path.join(__file__, os.pardir))
print(PACKAGE_PATH)

setup(name='KDE2D',
      version='0.1',
      description='Maiing pretty joint plots using seaborn',
      url='https://github.com/zanejobe/KDE-2D',
      author='Ross Meyer and Zane Jobe',
      author_email='zanejobe@gmail.com',
      packages=find_packages(PACKAGE_PATH),
      install_requires=[
        'numpy>=1.13.0',
        'scipy>=1.5',
        'matplotlib>=3.2',
        'pandas>=1.0',
        'six>=1.12'
      ],
      zip_safe=False
)
