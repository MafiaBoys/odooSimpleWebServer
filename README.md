# odooSimpleWebServer
```
databases = {
  'default': {

    'URI': 'http://localhost:8069/',
    'database': 'database',
    'username':'admin',
    'password':'password'
  },
  # ...
}
```
## test
```python

# test model ir.module.module

serverA = XmlrpcClient(attribute='<tagnameA>')
model_id = 'ir.module.module'

if serverA.checkPermissions(model_id,['read','write']):
   records = serverA.read(model_id,[('state','=','installed')])
   for record in records:
       print (record['id'],record['name'],record['state'])

```
