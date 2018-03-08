# Zalo AI Lab tools

Pip package tools for Deep learning task

## Installation

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

## Develop instruction

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

## Module

### `common`

1. `check`

    check package install status
