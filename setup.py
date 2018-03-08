from setuptools import setup

required_packages = ['numpy', 'tensorflow', 'matplotlib', 'scipy', 'scipy', 'scikit-learn', 'scikit-image', 'keras']

setup(
    name='ailabtools',
    packages=['ailabtools'],
    version='0.1rc',
    description='Common tools for Zalo AI Lab',
    url='http://lab.zalo.ai',
    include_package_data=True,
    install_requires=required_packages,
)
