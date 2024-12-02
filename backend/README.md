# WTIST Backend
This is the repository for the python backend code of the WTIST Stablecoin project.

## Python
Run the gunicorn server with two workers.
The code will also initialize a SQLite db called `oil.db`.
```bash
gunicorn -w 2 -b 0.0.0.0:4500 main:app 
```

Install from requirements with pip:
```bash
pip install --no-cache-dir -r requirements.txt
```

Store requirements with pip:
```bash
pip freeze > requirements.txt
```

## Database
The data is stored in the `data` folder.
SQLite database files are used to track the status of the oil collateral to back the stablecoin.