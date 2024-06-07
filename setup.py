from setuptools import setup, find_packages

setup(
    name='llmuri',
    version='0.1.0',
    author='Mark Harrison',
    author_email='mark@tigereye.com',
    description='LLM URI Parsing.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/marhar/llmuri',
    packages=find_packages(),
    install_requires=[
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
