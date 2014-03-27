from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='pyrofactory',
      version=version,
      description="SauceCI Robot Framework Factory for Python",
      long_description="""\
Simple interface factory to spawn multiple pybot instances based on the environment variables intersected by SauceCI Plugin""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='selenium python pybot factory sauce teamcity',
      author='Tallis Vanek',
      author_email='talliskane@gmail.com',
      url='https://github.com/Tallisado/pyrofactory',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          "robotframework-selenium2library",
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )