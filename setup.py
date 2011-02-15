try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages


import livetest

setup(name='livetest',
      version=livetest.__version__,
      description='Test against a live site with an API like Paste WebTest',
      long_description=file('README.rst').read(),
      classifiers=[
          "Development Status :: 4 - Beta",
          "Environment :: Web Environment",
          "Framework :: Paste",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Software Development :: Testing"
      ],
      keywords='http integration wsgi test unit tests testing web functional',
      author='Scott Torborg',
      author_email=livetest.__author__,
      url='http://github.com/storborg/livetest',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'tests']),
      include_package_data=True,
      install_requires=['WebTest>=1.2'],
      tests_require=['nose>=0.10'],
      test_suite='nose.collector',
      zip_safe=False)
