
echo "migration name: $1";

if [[ ! $1 ]]; then
  echo "You should provide a name for migration";
  exit 1;
fi

alembic revision --autogenerate -m "$1"