# Adacord CLI


## Install the cli

```bash
pip install adacord
```

## Create a new user

```bash
adacord user create
```

## Login

```bash
adacord user login --email me@my-email.com --password your-password
```

## Create endpoint

```bash
adacord bucket create --description "A fancy bucket"
```

## List endpoints

```bash
adacord bucket list
```

## Query endpoint

```bash
adacord bucket query my-bucket --query 'select * from my-bucket'
```

## For developmenet

```bash
poetry install
```
