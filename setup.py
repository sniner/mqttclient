from setuptools import setup, find_packages

setup(
    # Metadata
    name = 'mqttclient',
    version = '0.0.1',
    author = 'Stefan Schönberger',
    author_email = 'me@s5s9r.de',
    description = 'Simple MQTT sub/pub client',
    long_description = open('README.md').read(),

    # Packages
    package_dir = {'': 'src'},
    packages = find_packages('src'),
#    package_data = {
#        'package': ['subdir/*.ext'],
#    },

    # Dependencies
    install_requires = [
        "paho-mqtt>=1.4",
    ],
    extras_require = {
        'dev': [
        ],
    },

    # Scripts
    entry_points = {
        'console_scripts': [
            'mqtt-client = de.s5s9r.mqttclient.__main__:main',
        ]
    },

    # Packaging information
    platforms = 'any',
)
