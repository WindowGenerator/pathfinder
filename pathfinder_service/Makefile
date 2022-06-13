.PHONY: all

CMD := poetry run

run-migrations:
	${CMD} alembic upgrade head

install-deps:
	@poetry install
