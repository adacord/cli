# Adacord CLI


## Install the cli

```bash
poetry install
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
adacord bucket query my-endpoint-1 --query 'select * from my-endpoint-1'
```

## Create webhook

```bash
adacord webhook create --bucket my-endpoint --query "select * from my-endpoint" --url https://my-url.com
```
