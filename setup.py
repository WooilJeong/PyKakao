import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyKakao",
    version="0.0.1",
    license='MIT',
    author="Wooil Jeong",
    author_email="wooil@kakao.com",
    description="kakao api for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WooilJeong/PyKakao",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)