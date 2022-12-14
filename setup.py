""" setup.py for blogcast """

from setuptools import setup

setup(name='blogtopodcast',
      version='0.1',
      description='blogtopodcast',
      url='https://github.com/tbeckenhauer/blogToPodcast/',
      author='tbeckenhauer',
      author_email='thomas.beckenhauer.developer@gmail.com',
      license='MIT',
      packages=[],
      install_requires=[
          'pyyaml',
          'python-frontmatter',
      ],
      zip_safe=False)
