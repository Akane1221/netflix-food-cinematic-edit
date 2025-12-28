from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="netflix-food-cinematic-edit",
    version="0.1.0",
    author="Akane1221",
    description="A package for cinematic editing of food content for Netflix-style presentations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Akane1221/netflix-food-cinematic-edit",
    project_urls={
        "Bug Tracker": "https://github.com/Akane1221/netflix-food-cinematic-edit/issues",
        "Documentation": "https://github.com/Akane1221/netflix-food-cinematic-edit/wiki",
        "Source Code": "https://github.com/Akane1221/netflix-food-cinematic-edit",
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Video",
        "Topic :: Multimedia :: Graphics",
    ],
    python_requires=">=3.8",
    install_requires=[
        "opencv-python>=4.5.0",
        "numpy>=1.19.0",
        "Pillow>=8.0.0",
        "scikit-image>=0.18.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.12.0",
            "black>=21.0",
            "flake8>=3.9.0",
            "isort>=5.9.0",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "netflix-food-edit=netflix_food_cinematic_edit.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
