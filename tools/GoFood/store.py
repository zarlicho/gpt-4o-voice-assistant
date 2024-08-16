import requests
from helper.decoder import Credential
from geopy.distance import geodesic
import re


class Menu:
    def __init__(self):
        self.cred = Credential()
        self.StoreList = []
        self.Location = {"latitude":-6.4779776,"longitude":106.7571267}
        self.Lstore = []

    def GetStore(self,StoreName):
        payload ={
            "query":StoreName,
            "language":"en",
            "timezone":"Asia/Jakarta",
            "pageToken":"0",
            "pageSize":24,
            "location":{"latitude":-6.477941,"longitude":106.757372}
        }
        response = requests.post(url="https://gofood.co.id/api/outlets/search",cookies=self.cred.cooki,headers=self.cred.headers,json=payload)
        for store in response.json()['outlets']:
            # restoCord = (menu['core']['location']['latitude'],menu['core']['location']['longitude'])
            distance = store['delivery']['distanceKm']
            if int(distance) < 6:
                storeDict = {"name":store['core']['displayName'],"distance":distance,"link":store['core']['shortLink']}
                self.StoreList.append(storeDict)
        return self.StoreList
        
    def SearchStore(self,query):
        pattern = re.compile(query, re.IGNORECASE)
        result = []
        for Liststore in self.StoreList:
            self.Lstore.append(Liststore['name'])
            # print(Lstore)
        for index,Restrore in enumerate(self.Lstore):
            if pattern.search(Restrore):
                result.append(index)
        return result

# men = Menu()
# men.GetMenu("nasi goreng")
# print("\n")
# print(men.menuList[men.SearchMenu("nasi goreng rezky")[0]])
