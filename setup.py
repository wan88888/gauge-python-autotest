from setuptools import setup, find_packages

setup(
    name="gauge-python-autotest",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "getgauge",
        "requests",
        "selenium",
        "webdriver-manager",
        "pytest",
        "appium-python-client",
        "pytest-html",
        "Pillow"
    ],
) 