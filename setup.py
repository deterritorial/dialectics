from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8', errors='ignore') as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding='utf-8', errors='ignore') as fh:
    requirements = [x.strip() for x in fh.read().split('\n') if x.strip()]

setup(
    name='totality',
    version='0.0.3',
    url='https://github.com/deterritorial/totality.git',
    author='Ryan Heuser',
    author_email='rj416@cam.ac.uk',
    description='Resources for studying, modeling, resisting, coding, and conceptualizing the totalityual.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    packages=find_packages(),    
    license='MIT',
    install_requires=requirements,
    classifiers=[
        #'Development Status :: 3 - Alpha',
        #'Intended Audience :: Science/Research',
        #'Programming Language :: Python :: 2.7',
        #'Programming Language :: Python :: 3.6'
    ],
)