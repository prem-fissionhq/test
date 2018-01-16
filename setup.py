#!/usr/bin/env python
import os
import shutil
import sys
import contextlib
from pip.req import parse_requirements


version='v2.1.2'
__version__ = 'v2.1.2'
version_string = 'v2.1.2'

try:
    from setuptools import Extension, setup
except ImportError:
    from distutils.core import Extension, setup


PACKAGES = [
    'illusionist',
    'illusionist.templates',
    'illusionist.models',
    'illusionist.helpers',
    'illusionist.routes'
]

MOD_NAMES = [
]


def is_source_release(path):
    return os.path.exists(os.path.join(path, 'PKG-INFO'))


def clean(path):
    # remove build folder
    build_path = os.path.join(path, 'build')
    if os.path.exists(build_path):
        shutil.rmtree(build_path)


@contextlib.contextmanager
def chdir(new_dir):
    old_dir = os.getcwd()
    try:
        os.chdir(new_dir)
        sys.path.insert(0, new_dir)
        yield
    finally:
        del sys.path[0]
        os.chdir(old_dir)


def setup_package():
    root = os.path.abspath(os.path.dirname(__file__))

    if len(sys.argv) > 1 and sys.argv[1] == 'clean':
        return clean(root)

    with open(os.path.join(root, 'illusionist', 'about.py')) as f:
        about = {}
        exec(f.read(), about)

    with chdir(root):
        with open(os.path.join(root, 'illusionist', 'about.py')) as f:
            about = {}
            exec(f.read(), about)

        with open(os.path.join(root, 'README.rst')) as f:
            readme = f.read()

        install_reqs = parse_requirements('requirements.txt', session=False)
        reqs = [str(ir.req) for ir in install_reqs]

        setup(
            name=about['__title__'],
            zip_safe=False,
            packages=PACKAGES,
            package_data={'': ['*.pyx', '*.pxd', '*.txt', '*.yaml', '*.json', '*.html', '*.js', '*.png', '*.gif',
                               '*.jpg', '*.jpeg', '*.css', '*.xml', '*.ini']},
            description=about['__summary__'],
            long_description=readme,
            author=about['__author__'],
            author_email=about['__email__'],
            version=about['__version__'],
            url=about['__uri__'],
            install_requires=reqs,
            classifiers=[
                'Development Status :: 3 - Alpha',
                'Intended Audience :: Developers',
                'Operating System :: POSIX :: Linux',
                'Operating System :: MacOS :: MacOS X',
                'Programming Language :: Python :: 2.7',
                'Programming Language :: Python :: 3.5',
                'Topic :: Scientific/Engineering'],
            setup_requires=['pytest-runner'],
            tests_require=['pytest']
        )


if __name__ == '__main__':
    setup_package()

