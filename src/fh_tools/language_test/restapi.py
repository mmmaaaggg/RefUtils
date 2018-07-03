import requests
import json

class APIError(Exception):

    def __init__(self,  status):

        self.status = status

    def __str__(self):
        return "APIError:status={}".format(self.status)


class Rest():

    def __init__(self, url_str):
        self.url = url_str
        self.header = {'Content-Type': 'application/json'}

    def _url(self, path: str) -> str:
        return self.url + path

    def public_post(self, path: str, req_data: str) -> list:

        print('self._url(path):', self._url(path))
        ret_data = requests.post(self._url(path), data=req_data, headers=self.header)
        if ret_data.status_code != 200:
            raise APIError('POST /  {}'.format(ret_data.status_code))
        else:
            return ret_data.status_code, ret_data.json()

    def wset(self, table_name, options):
        path = 'wset/'
        req_data = '{"table_name": "%s", "options": "%s"}' % (table_name, options)
        status_code, json_str = self.public_post(path, req_data)
        return status_code, json_str

if __name__ == "__main__":
    url_str = "http://10.0.3.66:5000/wind/"
    # url_str = "http://10.0.5.110:5000/wind/"
    path_post_dic = {
        1: {'path': 'wset/',
            'req_data': '{"table_name": "sectorconstituent", "options": "date=2017-03-21;sectorid=1000023121000000"}'},
        2: {'path': 'wss/',
            'req_data': '{"codes": "XT1522613.XT", "fields": "fund_setupdate,fund_maturitydate,fund_mgrcomp,fund_existingyear,fund_ptmyear,fund_type,fund_fundmanager", "options": ""}'},
        3: {'path': 'wsd/',
            'req_data': '{"codes": "603555.SH", "fields": "close,pct_chg", "begin_time": "2017-01-04", "end_time": "2017-02-28", "options": "PriceAdj=F"}'},
        4: {'path': 'wset/',
            'req_data': '{"table_name": "sectorconstituent", "options": "date=2017-03-27;sectorid=1000023126000000"}'},
    }
    test_id = 4
    path = path_post_dic[test_id]['path']
    req_data = path_post_dic[test_id]['req_data']
    rest = Rest(url_str)
    status_code, json_str = rest.public_post(path, req_data)
    print(status_code, json_str)
    # data = requests.post(url,data=json.dumps("123123123"),headers=header)
    # print(data.reason)
