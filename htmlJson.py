import pandas as pd
import json
import requests
import re
import time
from random import seed
from random import randint

####### ID #######
def existsId(value):
    if re.search(r"[I|i][D|d]=[\"|\'][\w\W]+?[\"|\']", value):     # any words end with ing?
        return True
    else:
        return False

def getId(value):
    id = re.findall(r"[I|i][D|d]=[\"|\'][\w\W]+?[\"|\']",value)

####### ID #######
def existsName(value):
    if re.search(r"[N|n][A|a][M|m][E|e]=[\"|\'][\w\W]+?[\"|\']", value):     # any words end with ing?
        return True
    else:
        return False

def getName(value):
    id = re.findall(r"[N|n][A|a][M|m][E|e]=[\"|\'][\w\W]+?[\"|\']",value)

####### Class #######
def existsClass(value):
    if re.search(r"[C|c][L|l][A|a][S|s][S|s]", value):     # any words end with ing?
        return True
    else:
        return False

def getClass(value):
    clas = re.findall(r"[C|c][L|l][A|a][S|s][S|s]=[\"|\'][\w\W]+?[\"|\']",value)

####### Href #######
def existsHref(value):
    if re.search(r"[h|H][r|R][e|E][f|F]=[\"|\'][\w\W]+?[\"|\']", value):     # any words end with ing?
        return True
    else:
        return False

def getHref(id):
    id = re.findall(r"[h|H][r|R][e|E][f|F]=[\"|\'][\w\W]+?[\"|\']",value)

#######  SRC #######
def existsSrc(value):
    if re.search(r"[S|s][R|r][C|c]=[\"|\'][\w\W]+?[\"|\']", value):     # any words end with ing?
        return True
    else:
        return False

def getSrc(value):
    src = re.findall(r"[S|s][R|r][C|c]=[\"|\'][\w\W]+?[\"|\']",value)

####### Value #######
def existsValue(value):
    if re.search(r"[V|v][A|a][L|l][U|u][E|e]=[\"|\'][\w\W]+?[\"|\']", value):     # any words end with ing?
        return True
    else:
        return False

def getValue(value):
    value = re.findall(r"[V|v][A|a][L|l][U|u][E|e]=[\"|\'][\w\W]+?[\"|\']",value)

####### get Style #######
def existsStyle(value):
    if re.search(r"[S|s][T|t][Y|y][L|l][E|e]", value):     # any words end with ing?
        return True
    else:
        return False

def getStyle(value):
    style = re.findall(r"[S|s][T|t][Y|y][L|l][E|e]=[\"|\'][\w\W]+?[\"|\']",value)

def getEtiqueta(value):
    if re.search(r"\<(?:\/)?[\w|\!]+", value):
        value = re.findall(r"\<(?:\/)?[\w|\!]+", value)
        value = re.sub(r"\<(?:[\/])?", "", value[0])
        return value

def labelType(value):
    if re.search(r"\<[\w|\!]+",value):
        return True
    elif re.search(r"\<\/[\w]+",value):
        return False

def getPropertis(value, count):

    values = re.findall(r"\<[\w|\!]+|[\w|\-]+\=[\"|\'][a-zA-Z0-9|\/|\:|\.|0-9|\-|\=|\#|\,|\_|\;|\!|\+|\(|\)|\'|\[|\]|\%|\&|\$|\?|\s,]+?[\"|\']",value)
    valu = re.findall(r"[s|S][t|T][y|Y][l|L][e|E]\=[\"|\'][\w\W]+?[\"|\'](?:[\w|\:|\/|\.|\'|\(|\)|\-|\;|\"|\s]+)?", value)
    array = []
    jsonn = {}
    elements = {}

    if(values):
        etiqueta = values[0]
        if re.search(r"<[\w|\!]+", etiqueta):
            etiqueta = re.findall(r"<[\w|\!]+",etiqueta)
            etiqueta = etiqueta[0].replace("<", "")
            text= re.findall(r"\>[\w\W]+",value)
            if(text):
                text = text[0].replace(">", "")
                elements["text"] = text

        for v in values:
            i = 0
            if(i == 0):
                propertis = re.findall(r"[\w|\-]+=[\"|\']", v)
                value = re.findall(r"[\"|\'][a-zA-Z0-9|\/|\:|\.|0-9|\-|\=|\#|\,|\_|\;|\!|\+|\(|\)|\'|\[|\]|\%|\&|\$|\?|\s]+?[\"|\']", v)
                y=0
                for p in propertis:
                    p = p.replace("\"", "")
                    p = p.replace("\'", "")
                    nodo = p.replace("=", "")
                
                    if(nodo == "style"):
                        r = valu[0].replace("style=\"", "")
                        if(existsStyle(nodo)):
                            r = r.split(";")
                                        
                    else:
                        r = value[y].replace("\"", "")
                        if(existsClass(nodo)):
                            r = r.split(" ")

                    elements[nodo] = r
                    y += 1            
            
            i += 1
    array.append(elements)
    jsonn[etiqueta + "_" + str(count)] = array
    
    return jsonn

def searchEndValue(c,value):
    endValue = 0
    i = 0
    for x in c:
        if(x == value):
            endValue = i
        i += 1
    return endValue

def removeComents(value):
    value = re.sub(r"\<\!\-\-\-\-\>", " ", value)
    value = re.sub(r"\<\!\-\-[\w\W]+?\-\-\>", " ", value)
    return value

def removeStyles(value):
    value = re.sub(r"\<[S|s][T|t][Y|y][L|l][E|e]\>[\w\W]+?\<\/[S|s][T|t][Y|y][L|l][E|e]\>", " ", value)
    return value

def removeScript(value):
    value = re.sub(r"\<[S|s][C|c][R|r][I|i][P|p][T|t]\>[\w\W]+?\<\/[S|s][C|c][R|r][I|i][P|p][T|t]\>", " ", value)
    value = re.sub(r"\<[S|s][C|c][R|r][I|i][P|p][T|t][\W\w]+?\<\/[S|s][C|c][R|r][I|i][P|p][T|t]\>", " ", value)
    return value
 
def insert(json, array, valor ):
    
    if(array):
        etiqueta = array[0]
    v = {}
    if(len(array) > 1):
        for a in json:
            aux = a
            for j in a:
                newArray = []
                if(j == array[0]):
                    for p in range(1, (len(array) ) ):
                        newArray.append(array[p])        
                    time.sleep(0)
                    inser = insert(aux[j], newArray, valor )

                    if( not(inser is None)):
                        return  aux[j].append( inser )
                    else:
                        return 

    else:

        if( not(valor is None) ):
            return valor
        else:
            return {}

def parseJson(html):

    html = removeComents(html)
    html = removeStyles(html)
    html = removeScript(html)

    html= re.findall(r"\<[\W\w]+?\>(?:[\w|\s|\-|\,|\.|\?|\¿|\ü|\é|\á|\í|\ó|\ú|\ñ|\Ñ|\¡|\&|\;|\:|\$]+)?",html)

    i = 0
    y = 0
    htmlArry = []
    jsonn = []
    count = {}
    f = False
    er = {}
    for value in html:

        etiqueta = getEtiqueta(value)
        if labelType(value):
            f = False
            for c in count:
                if(c == etiqueta):
                    f = True
                    break

            if(f):
                count[etiqueta] = count[etiqueta] + 1
            else:
                count[etiqueta] = 1

            htmlArry.append(etiqueta + "_" +str(count[etiqueta]))
            inser = insert(jsonn ,htmlArry, getPropertis(value, count[etiqueta]))
            if( not(inser is None) ):
                jsonn.append( inser )
            
            if(etiqueta == "br" or etiqueta == "img" or etiqueta == "meta" or etiqueta == "link" or etiqueta == "input"):
                htmlArry.pop(htmlArry.index(etiqueta +"_" +str(count[etiqueta])))

        else:

            r = re.sub(r"\_[0-9]+", "" , htmlArry[-1])

            index = len(htmlArry) - 1
            if(r == etiqueta):
                htmlArry.pop( index )
            else:
                init = searchEndValue(htmlArry ,etiqueta + "_"+str(count[etiqueta]))
                if(init != 0):
                    for remove in range(index , init -1 ,-1):
                        htmlArry.pop( remove )

        i += 1

    return jsonn

def SearchElement(jsonn, element):
    for j in jsonn:
        data = j
        for e in j:
            if(e != "class" and e != "style"):
                if(e == element):
                    return data[e]
                
                if(not(isinstance(data[e],str))):
                    value = SearchElement(data[e], element)
                    if(value != None):
                        return value

def SearchElementId(jsonn,id):
    for j in jsonn:
        data = j
        for e in j:
            if(e != "class" and e != "style"):
                if(e == "id"):
                    if(data[e] == id):
                        return 1
                
                if(not(isinstance(data[e],str))):
                    value = SearchElementId(data[e], id)
                    if(value != None):
                        if(value == 1):
                            return data[e]
                        else:
                            return value
  

    