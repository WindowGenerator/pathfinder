# Pathfinder

Route planning web service


## Common gateway to backend:
`http://127.0.0.1/api/v1`
For example: You want to get current user:
`http://127.0.0.1/api/v1/users/me`
## Services:

* [pathfinder_service](./pathfinder_service/README.md)
* [user_service](./user_service/README.md)

**Here you can find:**
- how to run migrations
- Api docs

## Build:

- Build docker-compose:
```bash
docker-compose build
```

## Launch System:
- Primitive way:
```bash
docker-compose up -d
```

- With setting the number of workers:
```bash
docker-compose up -d --scale pathfinder_worker=2
```

#### Generate random coordinates:
```bash
poetry install
poetry run python3 -m tools.coordinates_generator
```

## Development:

- Install dependencies:
```bash
make -f Makefile install-deps
```
- Run pre-commit:
```bash
make -f Makefile pre-commit
```
