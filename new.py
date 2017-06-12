from flask import Flask, current_app
from random import randint
import urllib2
from flask.json import jsonify
import math
from stocks import stockArr
from flask import render_template
import os, sys
app = Flask(__name__)


def toGoogle(sym):
    return 'http://www.google.com/finance/historical?q={0}&startdate=Jul%207,%201991&enddate=Jun%209,%202017&output=csv'.format(sym)

def getBatch(isNew=True,gSym="",gSel="",gMax=""):
    temp = []
    if isNew == True:
        selection = stockArr[randint(0,500)]
        csv = urllib2.urlopen(toGoogle(selection)).readlines()
        csv.reverse()
        csvLen = len(csv)-1
        randMax = math.floor(csvLen/201)
        if randMax < 3:
            os.execl(sys.executable, sys.executable, *sys.argv)
        randBatchSel = randint(2,randMax)
    else:
        selection = gSym
        csv = urllib2.urlopen(toGoogle(selection)).readlines()
        csv.reverse()
        randBatchSel = gSel+1
        randMax = gMax
        if randBatchSel > randMax:
            return "No more"

    for bar in xrange(-200,200,1):
        point = randBatchSel*200+bar
        offset,oprice,hprice,lprice,cprice,volume = csv[point].split(',')
        if offset[0]!='D':
            maveragefifty = 0
            if bar >= 0:
                maveragefifty = getMAs(csv,bar,point)
            try:
                temp.append([str(offset),float(lprice),float(oprice),float(cprice),float(hprice),float(volume),float(maveragefifty)])
            except:
                continue
    return temp

def getMAs(csvInput,bar,point):
    avArr = []
    for i in xrange(0,50):
        _,_,_,_,cprice,_ = csvInput[(point-i)].split(',')
        avArr.append(float(cprice))
        #try:
        #    avArr.append(float(cprice))
        #except:
        #    avArr.append(float(0))
    return sum(avArr)/len(avArr)

def nextBatch(gSym,gSel,gmax):
    res = getBatch(gSym,gSel,gMax, False)
    return res

@app.route('/')
def hello_world():
    res = getBatch(True)
    return render_template('test.html', dataPass=res)

@app.route('/test/')
def go():
    return getBatch(True)
