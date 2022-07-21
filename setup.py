from importlib.metadata import entry_points
from setuptools import setup

setup(
    name='Seminare',
    version='0.2.0',
    description=('Aplikace pro tvorbu rozvrhu seminarnich predmetu a '
                    'roztrizeni studentu do nich.'),
    author='Hung Do',
    author_email='hungdojan@gmail.com',
    license='MIT',
    url='https://github.com/hungdojan/gymul_seminare',
    packages=['sort_lib', 'gui_lib'],
    install_requires=['PySide6'],
    entry_points={
        'console_scripts': ['seminare=gui_lib.__main__:main']
    }
)