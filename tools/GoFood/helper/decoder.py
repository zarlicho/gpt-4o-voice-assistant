import regex as re
import json,os


class Credential:
    def __init__(self):
        self.headers = {}
        self.cooki = {}
        self.payload = {}
        self.cookies = ""
        self.url = ""
        self.data = None
        self.Setup()
        self.Main()

    def Setup(self):
        try:
            files = fr"{os.path.abspath(os.path.join(os.getcwd(), 'entity'))}\network_log1.json"
            with open(files) as f:
                jsonstr = f.read()
            json_str = re.sub(r',\s*([\]}])', r'\1', jsonstr)
            self.data = json.loads(json_str)
        except Exception as e:
            print(e)

    def GetHeader(self):
        try:
            for x in self.data:
                if x['method'] == "Network.requestWillBeSent":
                    if "https://gofood.co.id/api/outlets/search" in x['params']['request']['url']:
                        self.headers = x['params']['request']['headers']  # Menyimpan headers yang benar
        except Exception as e:
            print(e)
    def GetCookies(self):
        try:
            for x in self.data:
                if x['method'] == "Network.requestWillBeSentExtraInfo":
                    try:
                        if x['params']['headers'][":path"] == "/api/outlets/search":
                            self.cookies = x['params']['headers']['cookie']
                    except:
                        pass
        except Exception as e:
            print(e)

    def Format(self):
        try:
            for cookie in self.cookies.strip().split('; '):
                # print(cookie)
                key, value = cookie.split('=', 1)
                self.cooki[key] = value
        except Exception as e:
            print(e)

    def Main(self):
        self.GetHeader()
        self.GetCookies()
        self.Format()
