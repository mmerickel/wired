from setuptools import setup, find_packages


def readfile(name):
    with open(name) as f:
        return f.read()


readme = readfile('README.rst')
changes = readfile('CHANGES.rst')

requires = ['zope.interface']

docs_require = ['Sphinx', 'pylons-sphinx-themes']

tests_require = ['pytest', 'pytest-cov']

setup(
    name='wired',
    version='0.1.2',
    description='An inversion-of-control (IoC) container.',
    long_description=readme + '\n\n' + changes,
    author='Michael Merickel',
    author_email='pylons-discuss@googlegroups.com',
    url='https://wired.readthedocs.io',
    packages=find_packages('src', exclude=['tests']),
    package_dir={'': 'src'},
    include_package_data=True,
    python_requires='>=3.4',
    install_requires=requires,
    extras_require={'docs': docs_require, 'testing': tests_require},
    test_suite='tests',
    zip_safe=False,
    keywords=','.join(
        [
            'ioc container',
            'inversion of control',
            'dependency injection',
            'service locator',
            'singleton',
            'service factory',
        ]
    ),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
