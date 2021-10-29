
# Use this as an Adacord CLI

```bash
# create a new user
adacord user create

# login with your email and passowrd
adacord login --email me@my-email.com

# create a new bucket bucket
adacord bucket create --description "My first bucket"

# Push data to your bucket
adacord bucket push your-bucket-id --file data.csv

# Query your data
adacord bucket query 'select * from `push your-bucket-id`'

# Create a Bucket Token
adacord bucket token create your-bucket-id

# Login with a bucket token
adacord login --token your-bucket-token
```
