from setuptools import setup

required_packages = ['numpy', 'tensorflow', 'matplotlib', 'scipy', 'scikit-learn', 'scikit-image', 'keras', 
                     # For extract_distinct_image and file_processer
                     'imagehash', # Perceptual Hash for compare image: https://github.com/JohannesBuchner/imagehash
                     'subprocess', # For call command 
                     'send2trash', # Just send to trash
                     'python-magic', # Fro read file info: https://github.com/ahupp/python-magic
                     ]

setup(
    name='ailabtools',
    packages=['ailabtools'],
    version='0.1rc',
    description='Common tools for Zalo AI Lab',
    url='http://lab.zalo.ai',
    include_package_data=True,
    install_requires=required_packages,
)
