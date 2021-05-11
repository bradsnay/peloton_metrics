echo "Sorting imports..."
isort /app

echo "Fixing formatting..."
black /app
