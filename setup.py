import setuptools
import os

# Hole einige Package-Eigenschaften aus der init
pkg_vars = {}
with open("mydlink_api/__pkg_info__.py") as fp:
    exec(fp.read(), pkg_vars)

# Hole die Lang-Beschreibung aus dem README.md
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Hole die Abhängigkeiten aus requirements.txt
with open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    reqs = f.read().split()

setuptools.setup(name='mydlink_api',
                 version=pkg_vars['__version__'],
                 description='Python API for MyDlink Cloud',
                 long_description=long_description,
                 url='https://github.com/ageof/MyDlink-API-Python',
                 author=pkg_vars['__author__'],
                 author_email=pkg_vars['__email__'],
                 packages=['mydlink_api','mydlink_api.utils'],
                 install_requires=reqs,
                 zip_safe=False)
