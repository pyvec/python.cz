from setuptools import setup


install_requires = [
    'flask==0.12',
    'requests==2.18.3',
    'czech-sort==0.4',
    'pyyaml==3.12',
    'python-slugify==1.2.1',
]
tests_require = [
    'coveralls==1.1',
    'flake8==3.2.1',
    'pytest==3.0.6',
    'responses==0.7.0',
    'pytest-runner==2.11.1',
    'pytest-cov==2.5.1',
]


setup(
    name='pythoncz',
    packages=['pythoncz'],
    include_package_data=True,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={'tests': tests_require},
)
