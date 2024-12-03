from setuptools import setup, find_packages

setup(
    name="lzss",
    version="0.1.0",
    description="An implementation of lossless data compression algorithm inherited from LZ77",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "pycompress=lzss.compress:main",
            "pydecompress=lzss.decompress:main",
        ],
    },
)
