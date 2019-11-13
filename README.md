# CloudFlare Script

Script to enable and disable pools in CF Loadbalancers. Useful for deployments that are being executed in productions
## Installation



```bash
pip install -r requirements.txt
```

## Example commands

```bash
# Disables pool pool 
python cloudflare.py --pool ${CF_POOL_NAME} --authemail ${CF_EMAIL} --authkey ${CF_AUTH_KEY}  --lbname ${CF_LB_NAME}
.com 

# Enables specified pool
python cloudflare.py --pool ${CF_POOL_NAME} --authemail ${CF_EMAIL} --authkey ${CF_AUTH_KEY}  --lbname ${CF_LB_NAME}
.com --enabled
```

### Arguement List

```bash

'--pool', required=True, help='name of the pool to be updated'

'--lbname', required=True, help='name of the load balancer'

'--authkey', required=True, help='CloudFlare API key'

'--authemail', required=True, help='email associated with CloudFlare API key'

'--enabled', action='store_true', help='Enables pool if specified, else it defaults to False
```

## Contributing
Contributing is allowed. Dont be afraid to make changed. :-)