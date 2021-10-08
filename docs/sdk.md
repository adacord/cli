
# Use this as an Adacord SDK

```python
from adacord import api, settings

# either pass the token or search for ADACORD_TOKEN
ada = api.AdacordApi.Client(token=settings.token)

# create a bucket
bucket: Bucket = ada.create_bucket()

# get an existing bucket from uuid
bucket: Bucket = ada.get_bucket(uuid=bucket_uuid)

# get an existing bucket from bucket name
bucket: Bucket = ada.get_bucket(name=bucket_name)

# get the bucket name
bucket_name: str = bucket.name

# get the bucket url
bucket_url: str = bucket.url

# query the bucket
data: List[Dict[str, Any]] = bucket.query("SELECT * FROM bucket-name")

# push data to the bucket
response = bucket.push({"hello": "ciao"})

# upload a file to the bucket
response = bucket.upload(path=path_to_file)

# fetch the whole data of a bucket
data: List[Dict[str, Any]] = bucket.all()

# delete the bucket
response = bucket.delete()
```

## Use pydantic to get objects from the result of a query

```python
from pydantic import BaseModel


```
