# Continuous Integration for Morse Code Converter

This directory contains configuration files for continuous integration (CI) using GitHub Actions.

## Workflow Configuration

The CI workflow is defined in the `.github/workflows/python-tests.yml` file. It consists of two jobs:

1. **test**: Runs the tests with coverage on multiple Python versions (3.6, 3.7, 3.8, 3.9, 3.10).
    - Installs dependencies (pygame, coverage)
    - Runs tests with coverage
    - Generates a coverage report
    - Uploads the coverage report to Codecov

2. **lint**: Checks the code for syntax errors and style issues using flake8.
    - Stops the build if there are Python syntax errors or undefined names
    - Reports other style issues as warnings

## When the Workflow Runs

The workflow runs automatically on:

- Push events to the main or master branch
- Pull request events to the main or master branch

## Viewing Results

### GitHub Actions

You can view the results of the CI workflow in the "Actions" tab of your GitHub repository. Each workflow run will show:

- Whether the tests passed or failed
- The test results for each Python version
- Any linting issues found

### Codecov

The coverage report is uploaded to Codecov, which provides a detailed analysis of your code coverage. You can view the
report on the Codecov website or through the Codecov GitHub app.

## Badges

You can add badges to your README.md file to show the status of your CI workflow and code coverage:

```markdown
![Tests](https://github.com/username/MorseCodeConverter/workflows/Python%20Tests/badge.svg)
[![codecov](https://codecov.io/gh/username/MorseCodeConverter/branch/main/graph/badge.svg)](https://codecov.io/gh/username/MorseCodeConverter)
```

Replace `username` with your GitHub username.

## Local Testing

You can run the same tests locally before pushing your changes:

```bash
# Run tests with coverage
coverage run -m unittest discover
coverage report

# Run linting
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

## Troubleshooting

If the CI workflow fails, check the following:

1. **Test failures**: Look at the test output to see which tests failed and why.
2. **Linting issues**: Check the flake8 output for syntax errors or undefined names.
3. **Dependency issues**: Make sure all required dependencies are installed in the workflow.

## Customizing the Workflow

You can customize the workflow by editing the `.github/workflows/python-tests.yml` file:

- Add or remove Python versions in the `matrix.python-version` array
- Add additional dependencies to the `Install dependencies` step
- Modify the flake8 configuration in the `Lint with flake8` step
- Add additional steps or jobs as needed