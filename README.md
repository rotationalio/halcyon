# halcyon
Tools for "hype" and AI-generated text detection.

### Keep the formatting clean

This repository uses [black](https://black.readthedocs.io/en/stable/), [flake8](https://flake8.pycqa.org/en/latest/), and [pre-commit](https://pre-commit.com/) to maintain good [PEP8](https://www.python.org/dev/peps/pep-0008/) code quality and readability, and to prevent against commits that are hard to read because of variations across formatting tools and IDEs.

Set up your repository (one-time step) by running:

```bash
pip install pre-commit
pre-commit install
```

Now, every time you do a local commit, pre-commit will analyze the formatting and let you know if there are any errors that need to be corrected.

You should also install `black`'s autoformatter:

```bash
pip install black
```

And which you can run with:

(for a specific file)

```bash
black codes.py
```

(for a directory)

```bash
black tests/
```

## Running the AI generated text detector demo

```
$ pip install -r requirements.txt
$ streamlit run demo_app.py
```

## Running the Hype Detector demo

```
$ pip install -r requirements.txt
$ streamlit run hype_detector_demo.py
```