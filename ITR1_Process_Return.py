from lxml import etree
import datetime as dt
from io import StringIO
from ITR1_Constants_Common_Functions import *
from ITR1_Validate_User_Input_Gen import *
from ITR1_Validate_User_Input_ITDept_Rules import *
from ITR1_Calculate_IT_Return import *
from ITR1_Generate_XML import *
from ITR1_Validate_Tax_Calc_ITDept_Rules import *
from ITR1_Compare_Output_xmls import *
from ITR1_Prep_Input_File import * #for testing purposes only
import boto3

#Read the xml file
prep_input_file()
 ##########Replace next line with string from front end##########
#xml_str=open('C:\\Users\\gokul\\Google Drive\\Gokul Learning\\Indian IT Project\\Master Excel\\input.xml','rb').read()  #for testing purposes only
key="C:\\Users\\gokul\\Google Drive\\Gokul Learning\\Indian IT Project\\Master Excel\\input.xml"
localFilename = '/tmp/{}'.format(os.path.basename(key))
s3 = boto3.resource('s3')
s3.download_file(Bucket=bucket, Key=key, Filename=localFilename)
xmlstr = open(localFilename, "r").read()
mytree=etree.fromstring(xml_str)

def conv_xml_list(mytree):
    #Iterate through the xml file and store values in 2 dictionaries 1->all values except UsrDeductUndChapVIA 2-> all values in UsrDeductUndChapVIA
    #This is because element names are repeated between UsrDeductUndChapVIA and DeductUndChapVIA
    data={}     #Iterate through the xml file and store all tags and values in dictionay 'data'
    datausr={}  #Iterate through the xml file and store all CHAP6A user input values in dictionay 'datausr'
    tcs_count=0
    usr_active=False
    log=[]
    try:
        for element in mytree.iter():
            tmptag=rn(element.tag)
            if tmptag=='UsrDeductUndChapVIA':
                usr_active=True
            elif tmptag=='Section80TTB' and usr_active==True: #Switch off usr_active tag when the end is reached
                usr_active=False
            if element.text is not None:
                if tmptag=='TCS':  #TCS is an element as well as tree to store TCS details. Store only the element value in 'data'
                    tcs_count+=1
                    if tcs_count==1:
                        data[tmptag]= str(element.text)
                else:
                    if usr_active==True:
                        datausr[tmptag]= str(element.text)
                    else:
                        data[tmptag]= str(element.text)
        return 'ok', data, datausr, log
    except Exception as e:
        log.append(e)
        return 'err', data, datausr, log

try:
    ns={'ITRETURN':"http://incometaxindiaefiling.gov.in/main",'ITR1FORM':'http://incometaxindiaefiling.gov.in/ITR1','ITRForm':'http://incometaxindiaefiling.gov.in/master'} #Name spaces used in the xml file
    log=[]
    master_errors=[]
    log.append("************Start of Script**************")
    log.append("**Start: Convert input tree received into 2 lists - data and datausr")
    res = conv_xml_list(mytree)
    for x in res[3]:
        log.append(x)
    if res[0] != 'ok':
        master_errors.append('Unknown error while iterating through input XML')
        raise Exception
    data=res[1]
    datausr=res[2]
    log.append("**End: Convert input tree received into 2 lists - data and datausr")

    log.append("**Start: Validate user input data - generic checks")
    res = Validate_User_Input_Gen(mytree,data,datausr,ns)
    for x in res[1]:
        master_errors.append(x)
    for x in res[2]:
        log.append(x)
    if res[0] != 'ok':
        master_errors.append('Unknown error while validating user input data - generic checks')
        raise Exception
    log.append("**End: Validate user input data - generic checks")

    log.append("**Start: Validate user input data - IT Dept checks")
    res = Validate_User_Input_ITDept_Rules(mytree,data,datausr,ns)
    for x in res[1]:
        master_errors.append(x)
    for x in res[2]:
        log.append(x)
    if res[0] != 'ok':
        master_errors.append('Unknown error while validating user input data - IT Dept checks')
        raise Exception
    log.append("**End: Validate user input data - IT Dept checks")

    log.append("**Start: ITR1 Calculation")
    res = Calculate_It_Return(mytree,data,datausr,ns)
    for x in res[0]:
        master_errors.append(x)
    for x in res[16]:
        log.append(x)
    if res[15] != 'ok':
        master_errors.append('Unknown error while calculating ITR1')
        raise Exception
    log.append("**End: ITR1 Calculation")

    log.append("**Start: Generate XML")
    res = Generate_XML(data,mytree,ns,res[1],res[2],res[3],res[4],res[5],res[6],res[7],res[8],res[9],res[10],res[11],res[12],res[13],res[14])
    for x in res[3]:
        log.append(x)
    if res[0]=="Critical Error":
        master_errors.append('Unknown error while generating xml')
        raise Exception
    elif res[0]=='Schema Error':
        master_errors.append('XML generated failed validation against schema')
        master_errors.append(res[1])
        raise Exception
    mytree=res[2]   #mytree is now the generated tree, not input tree
    log.append("**End: Generate XML")

    log.append("**Start: Validate XML generated against IT Dept rules")
    log.append("****Start: Convert XML generated into 2 lists - data and datausr")
    res = conv_xml_list(res[2])
    for x in res[3]:
        log.append(x)
    if res[0] != 'ok':
        master_errors.append('Unknown error while iterating through generated XML')
        raise Exception
    data=res[1]
    datausr=res[2]
    log.append("****End: Convert XML generated into 2 lists - data and datausr")
    data=res[1]
    datausr=res[2]

    res = Validate_Tax_Calc_Itdept_Rules(mytree,data,datausr,ns)
    for x in res[1]:
        master_errors.append(x)
    for x in res[2]:
        log.append(x)
    if res[0] != 'ok':
        master_errors.append('Unknown error while validating XML generated against IT Dept rules')
        raise Exception
    log.append("**End: Validate XML generated against IT Dept rules")
    compare_output_xmls()
    log.append("************Normal Termination of Script**************")
    raise Exception
except:
    #return master_errors, log
    for x in master_errors:
        print(x)
    #with open('C:\\Users\\gokul\\Google Drive\\Gokul Learning\\Indian IT Project\\Master Excel\\log.txt', 'w') as f:
    with("/tmp/log.txt", 'wb') as f:  #AWS
        for item in log:
            f.write("%s\n" % item)