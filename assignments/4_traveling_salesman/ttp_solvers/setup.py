from setuptools import setup

with open("README.adoc", 'r') as f:
    long_description = f.read()

setup(
   name='ttp_solvers',
   version='1.0',
   description='Solvers for traveling sales person problem',
   license="MIT",
   long_description=long_description,
   author='Maxime Valin',
   packages=['ttp_solvers'],  #same as name
   install_requires=['wheel'], #external packages as dependencies
   scripts=[]
)
