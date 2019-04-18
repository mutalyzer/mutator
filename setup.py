from setuptools import setup

setup(name='mutalyzer-mutator',
      version='0.0.1',
      description='Strings mutator.',
      url='http://github.com/mutalyzer/mutator',
      author='Mihai Lefter',
      author_email='m.lefter@lumc.nl',
      license='MIT',
      packages=['mutator'],
      zip_safe=False,
      entry_points={
            'console_scripts': ['mutator=mutator.cli:main'],
      }
      )
