mheaders =  {'user-agent': 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5'}
dheaders={'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'}
import requests
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from bs4 import BeautifulSoup as bs

file=open("backlinks.csv",'w')

def getinfo(link):
    print("I am in getInfo")
    j=requests.get(link,headers=dheaders)
    j=bs(j.content)
    all_anchor_tag=j.findAll('a')
    linksJSON = {}
    for link in all_anchor_tag:
        try:
            ref=link.attrs['href']
            if ref.startswith('http'):
                file.write(ref+"\n")
                print(ref+"\n")
                print(ref)
        except:
            pass


file.close()


##############

from flask import Flask
from flask import jsonify
import csv

from pprint import pprint
import StringIO
from flask import make_response,request


app = Flask(__name__)
@app.route("/", methods=["GET"])
def index():
    link = request.args.get('url')
    j=requests.get(link,headers=dheaders)
    j=bs(j.content)
    all_anchor_tag=j.findAll('a')
    links = []
    for link in all_anchor_tag:
        try:
            ref=link.attrs['href']

            if ref.startswith('http'):
                print(ref)
                links.append(ref)
                file.write(ref+"\n")
        except:
            pass
    print("json",links)
    JSONobj = {'urls' : links}
    return jsonify(JSONobj)


if __name__ == "__main__":

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
