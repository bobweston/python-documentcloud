
test-clean:
	rm -rf tests/cassettes/test_*/*
	rm -rf tests/cassettes/fixtures/*

test-clean-short:
	rm -rf tests/cassettes/short_fixtures/*

test-create: test-clean
	pytest --record-mode=all -m "not short"

test-create-short: test-clean-short
	pytest --record-mode=all -m "short"

test:
	pytest --record-mode=none --block-network

test-dev:
	pytest --record-mode=new_episodes

coverage:
	coverage erase
	coverage run --source documentcloud -m py.test --record-mode=none --block-network
	coverage html
	coverage report -m

check:
	pylint documentcloud
	black documentcloud
	isort -rc documentcloud

ship:
	rm -rf build/
	python setup.py sdist bdist_wheel
	twine upload dist/* --skip-existing
