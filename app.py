from flask import Flask, render_template, url_for, session
from flask import request
from akamaiapiclient import AkamaiApiClient
import re
#from urllib.parse import unquote
from urlparse import unquote

app = Flask(__name__)
app.secret_key = b'5\xdf\xddT\xa3BN\x18\x89C\x1c^u3i\xd6'


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/estats')
def estats():
    cli = AkamaiApiClient()
    cpcode = request.args.get('cpcode')
    #requestid = request.args.get('requestid')

    response_body = {}
    inputdata = {'cpcode': cpcode}
    if cpcode:
        resp = cli.estats(cpcode=cpcode)
        response_body = resp.json()
        #estats = {'cpcode': cpcode}
        #estats['requestid'] = response_body['requestId']
        #estats['Date'] = resp.headers['Date']
        #session['estats'] = estats
        if resp.status_code == 202:
            link = response_body['link']
            inputdata.update({'link': link})
            requestid = response_body['requestId']
            inputdata.update({'requestid': requestid})

    session['inputdata'] = inputdata
    return render_template("estats.html", data=response_body, inputdata=inputdata)


@app.route('/estats/requestid/<int:requestid>')
def estats_getdata(requestid):
    cli = AkamaiApiClient()
    inputdata = session['inputdata']
    resp = cli.check_asyncresults(session['inputdata']['link'])
    if resp.status_code == 303:
        link = resp.headers['Location']
        resp = cli.get_asyncresponse(link=link)

    response_body = resp.json()

    #return render_template("estats.html", data=response_body, inputdata=inputdata)
    return ""


@app.route('/dparser')
def dparser():
    cli = AkamaiApiClient()
    errorstring = request.args.get('errorstring')
    requestid = request.args.get('requestid')
    response_body = {}
    if errorstring:
        resp = cli.error_translate(errorcode=errorstring)
        response_body = resp.json()
        dparser = {'errorstring': errorstring}
        dparser['requestid'] = response_body['requestId']
        dparser['link'] = response_body['link']
        dparser['Date'] = resp.headers['Date']
        session['dparser'] = dparser
    elif requestid:
        errorstring = session['dparser']['errorstring']
        resp = cli.check_asyncresults(session['dparser']['link'])
        if resp.status_code == 303:
            link = resp.headers['Location']
            resp = cli.get_asyncresponse(link=link)
        response_body = resp.json()

    return render_template("dparser.html", data=response_body, errorstring=errorstring)


@app.route('/dig')
def dig():
    cli = AkamaiApiClient()
    locations = cli.get_ghost_locations().json()

    hostname = request.args.get('hostname')
    location = request.args.get('location')
    sourcelocation = request.args.get('sourcelocation')
    ip = request.args.get('ip')
    query = request.args.get('query')
    if sourcelocation == "edgeip":
        diglocation = ip
    elif sourcelocation == "location":
        diglocation = location

    inputdata = {'hostname': hostname,
                 'location': location,
                 'ip': ip,
                 'query': query,
                 'sourcelocation': sourcelocation}

    print(inputdata)
    response_body = {}
    if hostname:
        resp = cli.dig(hostname=hostname, location=diglocation, querytype=query)
        response_body = resp.json()

    return render_template("dig.html", data=response_body, inputdata=inputdata, locations=locations)


@app.route('/mtr')
def mtr():
    return render_template("mtr.html")


@app.route('/curl')
def curl():
    return render_template("curl.html")


@app.route('/debugurl')
def debugurl():
    cli = AkamaiApiClient()
    url = request.args.get('url')
    edgeip = request.args.get('edgeip')
    requestheaders = request.args.getlist('requestheaders')

    response_body = {}
    inputdata = {'url': url,
                 'edgeip': edgeip,
                 'requestheaders': requestheaders
                 }
    if url:
        resp = cli.debug_url(url=url, edgeip=edgeip, headers=requestheaders)
        response_body = resp.json()
        if resp.status_code == 202:
            link = response_body['link']
            inputdata.update({'link': link})
            requestid = response_body['requestId']
            inputdata.update({'requestid': requestid})

    session['inputdata'] = inputdata

    return render_template("debugurl.html", data=response_body, inputdata=inputdata)


@app.route('/debugurl/requestid/<int:requestid>')
def debugurl_getdata(requestid):
    cli = AkamaiApiClient()
    inputdata = session['inputdata']
    resp = cli.check_asyncresults(session['inputdata']['link'])
    if resp.status_code == 303:
        link = resp.headers['Location']
        resp = cli.get_asyncresponse(link=link)

    response_body = resp.json()

    return render_template("debugurl.html", data=response_body, inputdata=inputdata)


@app.route('/ipdetails')
def ipdetails():
    return render_template("ipdetails.html")


@app.route('/viewlogs')
def viewlogs():
    return render_template("viewlogs.html")


with app.test_request_context():
    print(url_for('dig', url='http://www.example.com', header='Pragma: x-akamai-internal-cache'))


@app.template_filter('varnametotitle')
def reverse_filter(s):
    return ' '.join(re.findall('[a-zA-Z][^A-Z]*', s))


@app.template_filter('urldecode')
def reverse_filter(s):
    return unquote(str(s))
