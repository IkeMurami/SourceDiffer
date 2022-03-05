# About

The script creates a git-repository from different versions of a source code and cleans an each commit for useless files (images, test-files, etc..).

# Pre-install

```
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $ python -m pip install -r requirements.txt
```

# Usage

Put the paths of sources to `source.list` and run differ:  

```
python main.py -i source.list -o out -r all
```

In rules directory you can add your rules and usage that later:

```
python main.py -i source.list -o out -r mycustomrules
```