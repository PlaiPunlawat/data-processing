from setuptools import setup, find_packages
setup(
    name='data_processing',
    version='0.0.0',
    python_requires='>=3.11.5',
    package_dir={"": "src"},
    packages=find_packages("src"),
    install_requires=[
        'numpy==1.24.3', 'pandas==2.0.3', 'tqdm', 'datasets', 'datasketch==1.6.5', 'nlpo3==1.3.0',
        'pytest', 'jsonlines', 'kenlm', 'scipy==1.10.1', 'sentencepiece==0.2.0', 'scikit-learn==1.2.2', 'gdown==2.3.1',
        "pythainlp>=4.0.0"],
)