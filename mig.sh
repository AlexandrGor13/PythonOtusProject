 set -a
 source .env
# alembic revision --autogenerate -m "create tables"
 alembic upgrade head
 set +a