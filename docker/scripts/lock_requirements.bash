echo "Uninstalling existing requirements..."
pip freeze | xargs pip uninstall -y

echo "Installing requirements from requirements.txt..."
pip install -r requirements.txt

echo "Freezing requirements into requirements.lock..."
pip freeze --disable-pip-version-check >> requirements.lock

echo "Sorting requirements in requirements.txt"
sort-requirements -q requirements.txt