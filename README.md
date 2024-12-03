# LZSS algorithm

TODO:

- [X] add venv & requirements
- [X] add dockerfile
- [ ] create github actions
- [ ] decode
- [ ] encode
- [ ] tests
- [ ] bit rate

## Local development

1. Install virtualenv if you don't have it

```bash
pip3 install virtualenv
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
pip3 install -r requirements.txt
```

5. (Optional) Safe new packages

```bash
pip3 freeze > requirements.txt
```

Deactivate a virtual env

```
deactivate
```
