from setuptools import find_packages, setup

setup(
    name='torch_finance',
    packages=['torch_finance'],
    version='0.0.1',
    description='PyTorch library for finance',
    author='Mohit Raghavendra',
    license='MIT',
    install_requires=['numpy', 'torch'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
