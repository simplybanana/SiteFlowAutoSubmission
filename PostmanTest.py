import requests, json, hmac, hashlib, datetime, base64, string, random

key = 'x'
secret = 'x'
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
    print("Submitting Order")
    return request_post('/api/order', order)


def random_job():
    with open('JSONTemplate.txt') as json_file:
        data = json.load(json_file)
        random_int = random.randint(0,100000)
        data['orderData']['sourceOrderId'] = 'PythonTest_' + str(random_int)
    with open('x\Test_'+str(random_int)+'.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return 'Test_'+str(random_int)


if __name__ == "__main__":
    a = random_job()
    path = 'x'
    contents = open(path+a+'.json','rb').read()
    print(submit_order(contents).json())
