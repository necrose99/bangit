from setuptools import setup

setup(
    name="bangit",
    version="0.1.0",
    py_modules=["bangit"],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "bangit=bangit:main",
        ],
    },
)
