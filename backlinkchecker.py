import requests
from lxml.html import fromstring
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import time
from flask import Flask
from flask import jsonify
from flask import request

def parse(url):
    text = requests.get(url).text
    html_parsed_object  = fromstring(text)
    return html_parsed_object.xpath('//a/@href'),[x.strip() for x in html_parsed_object.xpath('//a/text()') if x.strip() != '']


def gen_cloud(text):
    wordcloud = WordCloud().generate(text.lower())
    fig = plt.figure(frameon=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    plt.imshow(wordcloud, interpolation='bilinear')
    file = 'static/{}.png'.format(time.time())
    fig.savefig(file)
    return file


def main(url):
    hrefs, text = parse(url)
    text        = ' '.join(text)
    file        = '/'+gen_cloud(text)

    return({
           'hrefs' : hrefs,
           'image' : file,
           })

app = Flask(__name__)
@app.route("/", methods=["GET"])
def index():
    link = request.args.get('url')
    JSONobj = main(link)
    return jsonify(JSONobj)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
