import requests, json, hmac, hashlib, datetime, base64, string, random
from RandomAttributes import random_job
import os, time

key = 'XX'
secret = 'XX'
destination = 'hp.odsca'
baseUrl = 'https://orders.oneflow.io'


def create_headers(method, path, timestamp):
    string_to_sign = method + ' ' + path + ' ' + timestamp
    local_secret = secret.encode('utf-8')
    string_to_sign = string_to_sign.encode('utf-8')
    signature = hmac.new(local_secret, string_to_sign, hashlib.sha1).hexdigest()
    auth = key + ':' + signature
    return {'Content-Type': 'application/json',
        'x-oneflow-authorization': auth,
        'x-oneflow-date': timestamp,
    }


def request_post(path, data):
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    url = baseUrl + path
    headers = create_headers("POST", path, timestamp)
    result = requests.post(url, data, headers=headers)
    return result


def submit_order(order):
    return request_post('/api/order', order)


def random_job_json():
    random_int = random.randint(0, 100000)
    data = random_job(100000)
    data['destination']['name'] = destination
    data['orderData']['sourceOrderId'] = 'PythonTest_' + str(random_int)
    data['orderData']['items'][0]['description'] = str(100000)
    with open('XX'+str(random_int)+'.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return 'Test_'+str(random_int)


def watch_folder():
    path_to_watch = "XX"
    destination_path = "XXX"
    while 1:
        print('Searching....')
        time.sleep(1)
        added = os.listdir(path_to_watch)
        if added:
            print('Processing files...')
            for item in added:
                contents = open(path_to_watch+item,'rb').read()
                print(submit_order(contents).json())
                shutil.move(path_to_watch + item, destination_path)


if __name__ == "__main__":
    watch_folder()
    
