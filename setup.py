from setuptools import setup

required_packages = ['numpy', 'tensorflow', 'matplotlib', 'scipy', 'scikit-learn', 'scikit-image', 'keras', 
                     # For extract_distinct_image and file_processer
                     'imagehash', # Perceptual Hash for compare image: https://github.com/JohannesBuchner/imagehash
                     'send2trash', # Just send to trash
                     'python-magic', # Fro read file info: https://github.com/ahupp/python-magic,
                     'tqdm',
                     ]

setup(
    name='ailabtools',
    packages=['ailabtools', 'ailabtools.keras'],
    version='0.1rc2',
    description='Common tools for Zalo AI Lab',
    url='http://lab.zalo.ai',
    include_package_data=True,
    install_requires=required_packages,
)
