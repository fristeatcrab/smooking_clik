import requests,json

# from  requests import
import logging,re
logging.getLogger("requests").setLevel(logging.WARNING)
logging.captureWarnings(True)
import urllib3
urllib3.disable_warnings()
# urllib3.PoolManager(num_pools=50)
def judge_ip(ip):
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36";
        headers['Connection'] = "close";
        s = requests.session()
        s.keep_alive = False
        proxy_dict = re.sub('http://1813482282:hxm5bz2m@','',ip)
        r = requests.get('https://dps.kdlapi.com/api/checkdpsvalid/?orderid=956920344938769&signature=fcmnnv1z1puvikthg83pqg5y80nhrfjt&proxy={0}'.format(proxy_dict), headers=headers,timeout = 30, verify=False)
        porxy_dict_1 = json.loads(str(r.text))
        # logging.info(porxy_dict_1)
        if 'True' in str(porxy_dict_1['data']):
            logging.info('true')
            return True
        else:
            logging.info('Flase')
            return False
