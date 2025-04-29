from setuptools import setup, find_packages

setup(
    name="spotifywrapped",
    version="0.1.0",
    description="Custom Spotify Wrapped Generator with PyQt GUI",
    author="Your Name",
    author_email="your@email.com",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "spotipy",
        "tqdm",
        "matplotlib",
        "PyQt5",
        "pillow"
    ],
    entry_points={
        'console_scripts': [
            'spotifywrapped=spotifywrapped.spotify:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
