from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='pyregexp',
    packages=['pyregexp'],
    version='0.1.7',
    license='MIT',
    description='Simple regex library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Lorenzo Felletti',
    url='https://github.com/lorenzofelletti/pyregex',
    download_url='https://github.com/lorenzofelletti/pyregex/archive/v0.1.7.tar.gz',
    keywords=['Regex', 'RegExp', 'Engine'],
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
