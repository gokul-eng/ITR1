from lxml import etree
from ITR1_Constants_Common_Functions import *

def compare_output_xmls():
    master = open(FILE_NAME_WITH_PATH_XML_FILE, 'r') 
    new=  open('C:\\Users\\gokul\\Google Drive\\Gokul Learning\\Indian IT Project\\Master Excel\\page.xml', 'r') 
    print("COMPARE OUTPUT XML FILES")
    while True: 
        line_master = master.readline()
        line_new = new.readline()
        if not line_new:
            if not line_master:
                length_equal=True
                break
            else:
                length_equal=False
        if line_master is not None and line_new is not None:
            line_master=line_master.strip()
            line_new=line_new.strip()
            if line_master.find('xmlns')!=-1:
                line_master=line_master[:line_master.find('xmlns')-1].strip() + '>'
            if line_new.find('xmlns')!=-1:
                line_new=line_new[:line_new.find('xmlns')-1].strip() + '>'
            if line_master!=line_new:
                print(line_master + '::::' + line_new)
    print(length_equal)





