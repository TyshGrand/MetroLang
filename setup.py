from setuptools import setup, find_packages

setup(
    name="metrolang",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        "flask",
        "requests",
        "streamlit",
        "google-generativeai",
        "python-dotenv",
        "langchain_ollama",
        "langchain"
    ],
    include_package_data=True,
    description="MetroLang Application",
    author="Tushar Gupta",
    author_email="tushargupta9041@gmail.com",
)