from ITR1_Process_Return import *
from lxml import etree

def start():
    xml_str=open(FILE_NAME_WITH_PATH_XML_FILE,'rb').read()  #for testing purposes only
    
    mytree=etree.fromstring(xml_str)
    res = Process_Return(mytree)
    for x in res[0]:
        print(x)
    for x in res[1]:
        print(x)

start()