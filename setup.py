from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 1 - Planning',
  'Intended Audience :: Developers',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

packages = [
    'cake'
]

setup(
    name='Cake',
    version='0.0.1a',
    description='An object orientated math library',
    long_description=open('README.md').read(),
    long_description_content_type = "text/markdown",

    url = "https://github.com/Mecha-Karen/Cake", 
    project_urls={
        "Documentation": "https://docs.mechakaren.xyz/cake",
        "Issue tracker": "https://github.com/Mecha-Karen/Cake/issues",
    },

    author='Seniatical',

    license='MIT License',
    classifiers=classifiers,
    keywords='Math,Python,OOP', 
    
    packages=packages,
    install_requires=[] 
)