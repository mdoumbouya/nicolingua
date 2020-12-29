import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wa-asr-mdoumbouya",
    version="0.0.1",
    author="Moussa Doumbouya",
    author_email="mdoumbouya@gncode.org",
    description="A multilingual virtual assistant that understand Maninka, Pular and Susu",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Multimedia :: Sound/Audio :: Speech"
    ],
    python_requires='>=3.6',
)