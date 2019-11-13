import json
import requests
import argparse

parser = argparse.ArgumentParser(description='Disables or Enables specific pool under CloudFlare Load Balancer')
parser.add_argument('--pool', required=True, help='name of the pool to be updated')
parser.add_argument('--lbname', required=True, help='name of the load balancer')
parser.add_argument('--authkey', required=True, help='CloudFlare API key')
parser.add_argument('--authemail', required=True, help='email associated with CloudFlare API key')
parser.add_argument('--enabled', action='store_true', help='Enables pool if specified, else it defaults to False')
args = parser.parse_args()


headers = {
           'Content-Type': 'application/json',
           'X-Auth-Key': args.authkey,
           'X-Auth-Email': args.authemail
          }

# Gets Zone ID based ID off of URL
def get_cloudflare_zone_id(url):
    response = requests.get("https://api.cloudflare.com/client/v4/zones?per_page=50", headers=headers)
    for zone in json.loads(response.text)['result']:
        if zone['name'] == url:
            return zone['id']
    raise ValueError('could not find ID for {}'.format(url))


# Enables or Disables Pool
def update_pool_status(status):
    pool_origin_data['enabled'] = status
    response = requests.put("https://api.cloudflare.com/client/v4/organizations/{}/load_balancers/pools/{}".format(
        cloud_flare_org_id, pool_to_update_id), headers=headers, data=json.dumps(pool_origin_data))
    result = json.loads(response.text)['success']
    print("Update Success: {}".format(str(result)))

lb_name = args.lbname
lb_identifier = ""
lb_pool_ids = ""
pool_to_update = args.pool
pool_to_update_id = ""
pool_origin_data = {
    'name': pool_to_update,
    'enabled': '',
    'origins': ''
}
url = lb_name.split('.')[-2] + '.' + lb_name.split('.')[-1]
status = args.enabled
cloud_flare_org_id = "ee9c3d2ec9767ae7f85f283f88100a48"
cloud_flare_zone = get_cloudflare_zone_id(url)

# Get CF Load Balancer ID and Pools
response = requests.get("https://api.cloudflare.com/client/v4/zones/{}/load_balancers".format(cloud_flare_zone),
                        headers=headers)
lb_response = json.loads(response.text)

for load_balancer in lb_response['result']:
    if load_balancer['name'] == lb_name:
        lb_identifier = load_balancer["id"]
        lb_pool_ids = load_balancer["default_pools"]


# Get specified Pool Origin data
response = requests.get("https://api.cloudflare.com/client/v4/organizations/{}/load_balancers/pools".format(
                        cloud_flare_org_id), headers=headers)
pool_response = json.loads(response.text)

for lb_pool_id in lb_pool_ids:
    for pool in pool_response['result']:
        if lb_pool_id == pool["id"] and pool["name"] == pool_to_update:
            pool_to_update_id = lb_pool_id
            pool_origin_data['origins'] = pool['origins']


update_pool_status(status)