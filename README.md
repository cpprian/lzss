# LZSS algorithm

- [X] add venv & requirements
- [X] add dockerfile
- [X] create github actions
- [ ] decode
- [ ] encode
- [ ] tests
- [ ] bit rate

## Usage

## Local development

1. Install virtualenv if you don't have it

```bash
pip install virtualenv
```

2. Create new virualenv. Make sure that command below is executed in the repository

```bash
python3 -m venv lzss_env
```

3. Activate virtualenv

```bash
source lzss_env/bin/activate
```

4. Install all packages from requirements.txt

```bash
pip install -r requirements.txt
```

5. Run tests

```
pytest
```

6. Build lzss package

```bash
python3 setup.py sdist bdist_wheel && pip install .
```

7. (Optional) Safe new packages

```bash
pip freeze > requirements.txt
```

7. Deactivate a virtual env

```
deactivate
```