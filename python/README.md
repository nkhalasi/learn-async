# learn-async

## How to get started running the examples

### Setting up the workspace

```
git clone git@github.com:nkhalasi/learn_async.git
cd learn_async
pyvenv-3.4 --without-pip pyenv
source pyenv/bin/activate

SETUPTOOLS_VERSION="14.3.1"
wget https://pypi.python.org/packages/source/s/setuptools/setuptools-${SETUPTOOLS_VERSION}.tar.gz
tar -xvzf setuptools-${SETUPTOOLS_VERSION}.tar.gz
cd setuptools-${SETUPTOOLS_VERSION}
python setup.py install
cd ..

PIP_VERSION="6.0.8"
wget https://pypi.python.org/packages/source/p/pip/pip-${PIP_VERSION}.tar.gz
tar -xvzf pip-${PIP_VERSION}.tar.gz
cd pip-${PIP_VERSION}
python setup.py install
cd ..
deactivate

rm -rf setuptools* pip*
```

### Setting up the development environment

```
source pyenv/bin/activate
python setup.py develop
```

### Running the examples

```
python -m timeit -n 25 'import sequential' 'sequential.main()'
python -m timeit -n 25 'import threaded' 'threaded.main()'
python -m timeit -n 25 'import parallel_using_requests' 'parallel_using_requests.main()'
python -m timeit -n 25 'import parallel_using_aiohttp' 'parallel_using_aiohttp.main()'
```
