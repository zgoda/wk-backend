import ast
import codecs
import re
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))


def read(*parts):
    with codecs.open(path.join(here, *parts), 'r') as fp:
        return fp.read()


_version_re = re.compile(r"__version__\s+=\s+(.*)")


def find_version(*where):
    return str(ast.literal_eval(_version_re.search(read(*where)).group(1)))


test_reqs = [
    'pytest',
    'pytest-cov',
    'pytest-mock',
]

doc_reqs = [
]

dev_reqs = test_reqs + doc_reqs + [
    'pip',
    'setuptools',
    'wheel',
    'ipython',
    'ipdb',
    'watchdog',
    'httpie',
    'flake8',
    'flake8-builtins',
    'flake8-bugbear',
    'flake8-comprehensions',
    'flake8-pytest-style',
    'pep8-naming',
    'dlint',
    'python-dotenv',
]


setup(
    name='wk',
    description='Backend for Wymarsz Kwartalny service',
    version=find_version('src', 'wk', '__init__.py'),
    author='Jarek Zgoda',
    author_email='jarek.zgoda@gmail.com',
    url='https://github.com/zgoda/wk-back',
    long_description=read('README.rst'),
    long_description_content_type='text/x-rst',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    python_requires='~=3.7',
    zip_safe=False,
    install_requires=[
        'Flask',
        'Werkzeug',
        'python-jose',
        'requests',
    ],
    extras_require={
        'dev': dev_reqs,
        'docs': doc_reqs,
        'test': test_reqs,
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
