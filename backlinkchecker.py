#mheaders =  {'user-agent': 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5'}
#dheaders={'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'}

# "Look into xpath ----- alternative to BeautifulSoup" -Sal


import requests #used to send requests to web server and get the html we'd otherwise c in browser
import sys
import os
reload(sys)  #this line is reloading the system module and isn't necessary - sys module is standard library and is included in python so we're basically reloading somethign that hasn't been changed
sys.setdefaultencoding("utf-8") # this line is also probably not necessary
from bs4 import BeautifulSoup as bs

file=open("backlinks.csv",'w')  #opening csv file
#
#def getinfo(link):
#    print("I am in getInfo")
#    j=requests.get(link,headers=dheaders)
#    j=bs(j.content)
#    all_anchor_tag=j.findAll('a') #looking for all links in the webpage
#    linksJSON = {} #creating a python dictionary
#    for link in all_anchor_tag: #looping through all the links in the webpage
#        try:
#            ref=link.attrs['href']
#            if ref.startswith('http'):
#                file.write(ref+"\n")
#                print(ref+"\n")
#                print(ref)
#        except:
#            pass


#file.close()





import requests
from lxml.html import fromstring
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import base64

def parse(url):
    text = requests.get(url).text
    html_parsed_object  = fromstring(text)
    #words_list = html_parsed_object.xpath('//a/text()')
    #clean_list = []
    #for text in words_list :
    #    if text.strip() != '' :
    #        clean_list.append(text.strip())
    
    return html_parsed_object.xpath('//a/@href'),[x.strip() for x in html_parsed_object.xpath('//a/text()') if x.strip() != '']


def gen_cloud(text):
    wordcloud = WordCloud().generate(text)
    fig = plt.figure(frameon=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    plt.imshow(wordcloud, interpolation='bilinear')
    fig.savefig('word_cloud.png')


def main(url):
    hrefs, text = parse(url)
    text        = ' '.join(text)
    gen_cloud(text)
    encoded = ''
    with open('word_cloud.png','rb') as f :
        encoded = base64.b64encode(f.read())
    return({
           'hrefs' : hrefs,
           'image' : encoded,
           })










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
#    j=requests.get(link,headers=dheaders)
#    j=bs(j.content)
#    all_anchor_tag=j.findAll('a')
#    links = []
#    for link in all_anchor_tag:
#        try:
#            ref=link.attrs['href']
#
#            if ref.startswith('http'):
#                print(ref)
#                links.append(ref)
#                file.write(ref+"\n")
#        except:
#            pass
#    print("json",links)
#    JSONobj = {'urls' : links}
    JSONobj = main(link)
    
    return jsonify(JSONobj)


if __name__ == "__main__":

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)








