# This is the doitlive session to record how to use the CLI
# $ mkdir -p ~/.config/asciinema
# $ cp asciinema-config ~/.config/asciinema
# $ pip install doitlive asciinema
# $ asciinema rec -c "doitlive play scripts/doitlive-session.sh -q"
#
#doitlive speed: 3
#doitlive prompt: nicolauj
#doitlive shell: /bin/zsh
#doitlive commentecho: true

adacord user create

adacord login --email hello@adacord.com

adacord bucket create --description "hello bucket"

adacord bucket list

adacord api_tokens create

echo "Now let's try the SDK..."

```python
token = input("The API token?")
bucket_name = input("The bucket name?")

from adacord import api

ada = api.Client(token=token)

ada.Buckets.list()

bucket = ada.Bucket.get(bucket_name)

bucket.get_data()

bucket.push_data({'name': 'dog', 'age': 2})
bucket.push_data({'name': 'frog', 'age': 4})

bucket.query(f'SELECT * FROM {bucket_name} WHERE `age` > 2')

bucket.delete()
```
