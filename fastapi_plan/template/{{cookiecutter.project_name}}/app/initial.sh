cd build

python -m pytest app/tests

aerich upgrade

python app/initial_data.py