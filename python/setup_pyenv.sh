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
