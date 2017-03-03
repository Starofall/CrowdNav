from setuptools import setup, find_packages

# this is a python install script
# call it with >setup.py install
# to install all dependencies

setup(
    name='CrowdNav',
    version='0.2',
    long_description="RealTime Simulation in SUMO",
    packages=find_packages(),
    include_package_data=False,
    zip_safe=False,
    install_requires=[
        'msgpack-python',
        'colorama',
        'kafka-python',
        'Dijkstar',
        'paho-mqtt'
    ]
)
