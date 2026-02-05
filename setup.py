from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gl-py2pyd",
    version="0.2.0",
    author="gu lei",
    author_email="youjunxiaji@gmail.com",
    description="将Python文件转换为pyd/so文件的工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/youjunxiaji/py2pyd-arg",
    packages=["module"],
    include_package_data=True,
    py_modules=["py2pyd"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "cython",
        "rich",
        "setuptools",
    ],
    entry_points={
        "console_scripts": [
            "py2pyd=py2pyd:main",
        ],
    },
) 