
# Use this as an Adacord SDK

```python
from adacord import api, get_token

# either pass the token or search for ADACORD_TOKEN
token = get_token()

ada = api.Client(token=token)

# create a bucket
bucket: Bucket = ada.Buckets.create(description="my-bucket", schemaless=False)

# list the buckets in my account
buckets: List[Bucket] = ada.Buckets.list()

# query the bucket
data: List[Dict[str, Any]] = ada.Buckets.query("SELECT * FROM bucket-name")

# get an existing bucket from uuid
bucket: Bucket = ada.get_bucket(uuid=bucket.uuid)

# get the bucket name
bucket_name: str = bucket.name

# get the bucket url
bucket_url: str = bucket.url

# push data to the bucket
response = bucket.push_data({"hello": "ciao"})

# fetch the whole data of a bucket
rows: List[Dict[str, Any]] = bucket.get_data()

# delete the bucket
response = bucket.delete()
```

## Use pydantic to get objects from the result of a query

```python
from pydantic import BaseModel


```
