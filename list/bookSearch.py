import os
import requests
#from . import keys

class gbooks():

    
    #API_KEY=keys.google_api_key
    API_KEY=os.environ.get('API_KEY')
    def search(self, value):
        ls=[]
        parms = {"q":value, 'key':self.API_KEY}
        r = requests.get(url="https://www.googleapis.com/books/v1/volumes", params=parms)
        #print (r.url)
        rj = r.json()
        for i in rj["items"]:
            info={}
            try:
                info["title"]=repr(i["volumeInfo"]["title"])
                info["authors"]=repr(i["volumeInfo"]["authors"])
                info["id"]=repr(i["id"])[1:-1]
                info["description"]=repr(i["volumeInfo"]["description"])
            except:
                pass
            try:
                info["img"]=(repr(i["volumeInfo"]["imageLinks"]["thumbnail"])[1:-1])
                pass
            except:
                pass
            ls.append(info)
        #print(ls)
        return ls
    def getBook(self,id):
        ls=[]
        parms = {"q":id, 'key':self.API_KEY}
        r = requests.get(url="https://www.googleapis.com/books/v1/volumes", params=parms)
        rj = r.json()
        i= rj["items"][0]
        info={}
        try:
            info["title"]=repr(i["volumeInfo"]["title"])
            info["authors"]=repr(i["volumeInfo"]["authors"])
            info["id"]=repr(i["id"])[1:-1]
            info["description"]=repr(i["volumeInfo"]["description"])
        except:
            pass
        try:
            info["img"]=(repr(i["volumeInfo"]["imageLinks"]["thumbnail"])[1:-1])
            pass
        except:
            pass
        return info
if __name__ == "__main__":
    bk = gbooks()
    #bk.search("stephen king")
    #bk.search("stephen king")
    print(bk.getBook("d999Z2KbZJYC"))

