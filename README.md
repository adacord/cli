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
adacord endpoint create --name my_new_endpoint
```

## List endpoints

```bash
adacord endpoint list
```

## Query endpoint

```bash
adacord endpoint query --name my-endpoint-1 --query 'select * from my-endpoint-1'
```

## Create webhook

```bash
adacord webhook create --endpoint my-endpoint --query "select * from my-endpoint" --url https://my-url.com
```
