try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(name='livetest',
      version='0.1dev',
      description='Live WebTesting',
      long_description='Make live website tests look like Paste WebTest',
      author='Crooked Media',
      author_email='admin@crookedmedia.com',
      packages=find_packages(exclude=['ez_setup', 'tests']),
      install_requires=['WebTest'],
      test_suite='nose.collector',
      zip_safe=False)
