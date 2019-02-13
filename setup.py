from setuptools import find_packages, setup

setup(
    name='logical-lens',
    version='0.0.1',
    description='Python library for using parametric specifications to'
    'embed domain specific knowledge in machine learning.',
    url='https://github.com/mvcisback/LogicalLens',
    author='Marcell Vazquez-Chanlatte',
    author_email='marcell.vc@eecs.berkeley.edu',
    license='MIT',
    install_requires=[
        'attrs',
        'funcy',
        'monotone-bipartition',
        'numpy',
    ],
    packages=find_packages(),
)
