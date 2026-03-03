from setuptools import setup, find_packages

setup(
    name='mkpipe-loader-timescaledb',
    version='0.1.0',
    license='Apache License 2.0',
    packages=find_packages(exclude=['tests', 'scripts', 'deploy', 'install_jars.py']),
    install_requires=['mkpipe'],
    include_package_data=True,
    entry_points={
        'mkpipe.loaders': [
            'timescaledb = mkpipe_loader_timescaledb:TimescaleDBLoader',
        ],
    },
    description='TimescaleDB loader for mkpipe (uses PostgreSQL JDBC driver).',
    author='Metin Karakus',
    author_email='metin_karakus@yahoo.com',
    python_requires='>=3.9',
)
