import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='ts-microsoftgraph-python',
      version='0.2.0',
      description='API wrapper for Microsoft Graph written in Python',
      long_description=read('README.md'),
      url='https://github.com/ThinkingStudio/microsoftgraph-python',
      long_description_content_type="text/markdown",
      author='Miguel Ferrer, Nerio Rincon, Yordy Gelvez, James Martindale, Joe Cincotta',
      author_email='joe@thinking.studio',
      license='MIT',
      packages=['ts_microsoftgraph'],
      install_requires=[
          'requests','msal'
      ],
      zip_safe=False)
