from setuptools import find_packages, setup

setup(
    name='logical-lens',
    version='0.0.0',
    description='TODO',
    url='https://github.com/mvcisback/LogicalLens',
    author='Marcell Vazquez-Chanlatte',
    author_email='marcell.vc@eecs.berkeley.edu',
    license='MIT',
    install_requires=[
        'attrs',
        'funcy',
    ],
    packages=find_packages(),
)
