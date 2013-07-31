from setuptools import setup, find_packages

setup(
    name='socrata',
    version='0.0.1',
    packages=find_packages(),

    install_requires=[
        'lxml',
        'requests',
    ],

    author='Thomas Levine',
    maintainer='Thomas Levine',
    maintainer_email='occurrence@thomaslevine.com',
    description='Nominate datasets from Socrata',
    license='MIT License',
    keywords='opendata',

    url='http://thomaslevine.com',
    download_url='https://github.com/tlevine/socrata',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ],
    include_package_data=True,
    zip_safe=False,
)
