# Adacord CLI


## Installation

```bash
pip install adacord
```

## Usage

### Create a new user

```bash
adacord user create
```

### Login

```bash
adacord login --email me@my-email.com
```

### Create endpoint

```bash
adacord bucket create --description "A fancy bucket"
```

### List endpoints

```bash
adacord bucket list
```

### Query endpoint

```bash
adacord bucket query 'select * from `my-bucket`'
```

# Contributing

```bash
poetry install
```
