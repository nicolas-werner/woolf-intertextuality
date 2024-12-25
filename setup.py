from setuptools import setup, find_packages

setup(
    name="woolf-intertextuality",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "qdrant-client",
        "sentence-transformers",
        "openai",
        "rich",
        "nltk",
    ],
    extras_require={
        "dev": ["pytest", "jupyter"],
    },
    entry_points={
        "console_scripts": [
            "preprocess_dalloway=data_preparation.preprocess_dalloway:main",
            "preprocess_odyssey=data_preparation.preprocess_odyssey:main",
            "setup_vector_db=vector_store.setup_vector_db:main",
            "find_similar_vectors=analysis.find_similar_vectors:main",
        ],
    },
)
