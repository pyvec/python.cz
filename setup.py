from setuptools import setup


install_requires = [
    'flask==1.0.2',
    'requests==2.19.1',
    'czech-sort==0.4',
    'pyyaml==3.13',
    'python-slugify==1.2.5',
]
tests_require = [
    'coveralls==1.4.0',
    'flake8==3.5.0',
    'pytest==3.7.2',
    'responses==0.9.0',
    'pytest-runner==4.2',
    'pytest-cov==2.5.1',
    'pytest-flake8==1.0.2',
]


setup(
    name='pythoncz',
    packages=['pythoncz'],
    include_package_data=True,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={'tests': tests_require},
)
