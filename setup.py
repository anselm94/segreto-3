from setuptools import setup, find_packages

setup(name='segreto3',
      packages=find_packages(),
      version='0.1',
      description='A simple secret ideating app with AES256 encryption, written with Kivy and Flat UI themed',
      long_description=open('README.md').read(),
      url="https://github.com/anselm94/segreto-3",
      download_url="https://codeload.github.com/anselm94/segreto-3/zip/master",
      author='Merbin J Anselm',
      author_email='merbinjanselm@gmail.com',
      license=open('LICENSE.txt').read(),
      install_requires=["simple-crypt", "jsonpickle", "kivy"],
      keywords=["kivy", "note", "app", "application",
                "flat design", "themed", "secret"],
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
          "Development Status :: 4 - Beta",
          "Environment :: Other Environment",
          "Intended Audience :: End Users/Desktop",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Topic :: Utilities"
      ])
