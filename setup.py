from setuptools import find_packages, setup

setup(
    name='markov_chain_py',
    version='0.1.0',
    author='lausek',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['markov=markov_chain_py:main']
    }
)
