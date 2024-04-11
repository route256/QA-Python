from setuptools import setup

setup(
    name="route256_plugin",
    # the following makes a plugin available to pytest
    packages=["route256_plugin"],
    entry_points={"pytest11": ["route256_plugin = route256_plugin.fixtures"]},
    # custom PyPI classifier for pytest plugins
    classifiers=["Framework :: Pytest"],
)
