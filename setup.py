from setuptools import setup, find_packages

setup(
    name="metrolang",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "flask",
        "requests",
        "streamlit",
        "google-generativeai",
        "python-dotenv",
    ],
    include_package_data=True,
    description="MetroLang backend service",
    author="Your Name",
    author_email="your@email.com",
)