from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='pyregexp',
    packages=['pyregexp'],
    version='0.3.2',
    license='MIT',
    description='Simple regex library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Lorenzo Felletti',
    url='https://github.com/lorenzofelletti/pyregex',
    download_url='https://github.com/lorenzofelletti/pyregex/archive/v0.3.1.tar.gz',
    keywords=['regex', 'regexp', 'engine'],
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: General',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
