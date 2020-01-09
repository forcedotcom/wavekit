init:
	pip3 install -r requirements.txt --user

install:
	python3 setup.py install --user

test:
	nosetests tests --verbosity=2 --logging-clear-handlers --with-coverage --cover-erase --cover-package=wave_common --cover-html --cover-xml
