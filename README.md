# Zalo AI Lab tools

[![PyPI version fury.io](https://badge.fury.io/py/ailabtools.svg)](https://pypi.python.org/pypi/ailabtools/)

[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

[![PyPI pyversions](https://img.shields.io/pypi/pyversions/ailabtools.svg)](https://pypi.python.org/pypi/ailabtools/)

Pip package tools for Deep learning task

## Installation

```
pip install ailabtools
```

## Develop instruction

### Installation for developing

1. Clone project to folder `ailabtools`

2. Go to `ailabtools` folder, install using `pip`:

    ```
    pip install .
    ```

    for editable package (for development process), run:

    ```
    pip install --editable .
    ```

3. Check if package installed succesfully by running this python code:

    ```
    from ailabtools import common
    common.check()
    ```

    right output:

    ```
    >>> from ailabtools import common
    >>> common.check()
    AILab Server Check OK
    ```

    make sure that the output is `AILab Server Check OK` without any problems.

4. Optional, check information of package:
    ```
    pip show ailabtools
    ```

### Contribution process

- Deployment branch: `master`.

- Development branch: `develop`.

- Contribution process steps:
    1. Checkout new branch.
    2. Add own module.
    3. Create pull request to branch `develop`.
    4. Waiting for pull request review.
    5. Pull request merged, ready for beta deployment.
    6. Stable, ready for `master` merge for offical deployment.

### Package modified

Checkout `setup.py` for package information.

### Add module

Add module in `ailabtools` folder.

## Documents

Check wiki pages
