from ITR1_Constants_Common_Functions import *
from lxml import etree
import re

def Validate_User_Input_Gen(mytree,data,datausr,ns):
    error=[]
    log=[]
    try:    
        #Check if all values are numeric value and all drop downs are valid selections
        if check_num_input('Salary',data) =="err":
            error.append("'Salary' is not a non negative integer value")
        if check_num_input('PerquisitesValue',data) =="err":
            error.append("'Perquisites Value' is not a non negative integer value")
        if check_num_input('ProfitsInSalary',data) =="err":
            error.append("'Profits In Salary' is not a non negative integer value")
        if check_num_input('EntertainmentAlw16ii',data) =="err":
            error.append("'Entertainment Alw 16ii' is not a non negative integer value")
        if check_num_input('ProfessionalTaxUs16iii',data) =="err":
            error.append("'Professional Tax u/s 16iii' is not a non negative integer value")
        if check_num_input('GrossRentReceived',data) =="err":
            error.append("'Gross Rent Received' is not a non negative integer value")
        if check_num_input('TaxPaidlocalAuth',data) =="err":
            error.append("'Tax Paid local Auth' is not a non negative integer value")
        if check_num_input('InterestPayable',data) =="err":
            error.append("'Interest Payable' is not a non negative integer value")
        if check_num_input('ArrearsUnrealizedRentRcvd',data) =="err":
            error.append("'Arrears or Unrealized Rent Rcvd' is not a non negative integer value")
        if check_num_input('DeductionUs57iia',data) =="err":
            error.append("'DeductionUs57iia' is not a non negative integer value")

        if check_num_input('Section80C',datausr)=='err':
            error.append("Error in Chap6A, Section80C value is not a non negative integer value")            
        if check_num_input('Section80CCC',datausr)=='err':
            error.append("Error in Chap6A, Section80CCC is not a non negative integer value")            
        if check_num_input('Section80CCDEmployeeOrSE',datausr)=='err':
            error.append("Error in Chap6A, Section80CCD(1) is not a non negative integer value")            
        if check_num_input('Section80CCD1B',datausr)=='err':
            error.append("Error in Chap6A, Section80CCD1B is not a non negative integer value")            
        if check_num_input('Section80CCDEmployer',datausr)=='err':
            error.append("Error in Chap6A, Section80CCDEmployer-80CCD(2) is not a non negative integer value")            
        if check_num_input('Section80CCG',datausr)=='err':
            error.append("Error in Chap6A, Section80CCG is not a non negative integer value")            
        if check_num_input('Sec80DMedicalExpenditureUsr',datausr)=='err':
            error.append("Error in Chap6A, Sec80D Medical Expenditure is not a non negative integer value")            
        if check_num_input('Sec80DHealthInsurancePremiumUsr',datausr)=='err':
            error.append("Error in Chap6A, Sec80D Health Insurance Premium is not a non negative integer value")            
        if check_num_input('Sec80DPreventiveHealthCheckUpUsr',datausr)=='err':
            error.append("Error in Chap6A, Sec80D Preventive Health CheckUp is not a non negative integer value")            
        if check_num_input('Section80DD',datausr)=='err':
            error.append("Error in Chap6A, Section80DD is not a non negative integer value")            
        if check_num_input('Section80DDB',datausr)=='err':
            error.append("Error in Chap6A, Section80DDB is not a non negative integer value")            
        if check_num_input('Section80E',datausr)=='err':
            error.append("Error in Chap6A, Section80E is not a non negative integer value")            
        if check_num_input('Section80EE',datausr)=='err':
            error.append("Error in Chap6A, Section80EE is not a non negative integer value")            
        if check_num_input('Section80GG',datausr)=='err':
            error.append("Error in Chap6A, Section80GG is not a non negative integer value")            
        if check_num_input('Section80GGC',datausr)=='err':
            error.append("Error in Chap6A, Section80GGC is not a non negative integer value")         
        if check_num_input('Section80TTA',datausr)=='err':
            error.append("Error in Chap6A, Section80TTA is not a non negative integer value")         
        if check_num_input('Section80TTB',datausr)=='err':
            error.append("Error in Chap6A, Section80TTB is not a non negative integer value")         
        if check_num_input('Section80U',datausr)=='err':
            error.append("Error in Chap6A, Section80U is not a non negative integer value")         

        if check_num_input('Section89',data) =="err":
            error.append("'Relief u/s Section89' is not a non negative integer value")

        val=gettval('OrigRetFiledDate',data)
        if val!='err' and val!='notfound':
            if check_date(data['OrigRetFiledDate'])==False:
                error.append("'Date of Filing Original Return' is not a valid date in 'yyyy-mm-dd' format")
        elif val=='err':
            error.append("'Date of Filing Original Return' is not a valid date in 'yyyy-mm-dd' format")
        val=gettval('NoticeDateUnderSec',data)
        if val!='err' and val!='notfound':
            if check_date(data['NoticeDateUnderSec'])==False:
                error.append("'Date of Notice or Order' is not a valid date in 'yyyy-mm-dd' format")
        elif val=='err':
                error.append("'Date of Notice or Order' is not a valid date in 'yyyy-mm-dd' format")

        #Check values entered in the tables
        err1=False
        err2=False
        for deduction in mytree.findall('.//ITRForm:AllwncExemptUs10',ns):
            for snode in deduction.iter():
                if rn(snode.tag)=='SalNatureDesc':
                    if nz(snode.text) not in ('10(5)','10(6)','10(7)','10(10)','10(10A)','10(10AA)','10(10B)(i)','10(10B)(ii)','10(10C)','10(10CC)','10(13A)','10(14)(i)','10(14)(ii)','OTH'):
                        if err1==False:
                            err1=True 
                if rn(snode.tag)=='SalOthAmount':
                    if err2==False:
                        err2=not check_if_int(snode.text)
        if err1==True:
            error.append("'Allowance Exempt u/s 10 table' selection is not in defined values") 
        if err2==True:
            error.append("Negative/ non integer values in Allowance Exempt u/s 10 table") 

        err1=False
        err2=False
        for deduction in mytree.findall('.//ITRForm:OthersInc',ns):
            for snode in deduction.iter():
                if rn(snode.tag)=='OthSrcNatureDesc':
                    if nz(snode.text) not in ('SAV','IFD','TAX','FAP','OTH'):
                        if err1==False:
                            err1=True 
                if rn(snode.tag)=='OthSrcOthAmount':
                    if err2==False:
                        err2=not check_if_int(snode.text)
        if err1==True:
            error.append("'Income from Other Sources table' selection is not in defined values") 
        if err2==True:
            error.append("Negative/ non integer values in Income from Other Sources table") 

        err1=False
        err2=False
        for deduction in mytree.findall('.//ITRForm:ExemptIncAgriOthUs10',ns):
            for snode in deduction.iter():
                if rn(snode.tag)=='NatureDesc':
                    if nz(snode.text) not in ('AGRI','10(10BC)','10(10D)','10(11)','10(12)','10(13)','10(16)','10(17)','10(17A)','10(18)','DMDP','10(19)','10(26)','10(26AAA)','10(34)','OTH'):
                        if err1==False:
                            err1=True 
                if rn(snode.tag)=='OthAmount':
                    if err2==False:
                        err2=not check_if_int(snode.text)
        if err1==True:
            error.append("Nature of Income in table 'Exempt Income: For reporting purpose' not in defined values")  
        if err2==True:
            error.append("Negative/ non integer values in Exempt Income: For reporting purpose table") 

        #Further Error Checks based on excel utility
        special_char=['<','>','&']

        val=gettval('SurNameOrOrgName',data)
        if val!='notfound' and val!='err':
            if len(val)>75:
                error.append("LastName in Income Details cannot exceed 75 characters")                        
            if any(x in val for x in special_char):
                error.append("Last name should not Contain <, >, & characters")                        
        else:
            error.append("LastName is mandatory in Income Details")   

        val=gettval('MiddleName',data)                         
        if val!='notfound' and val!='err':
            if any(x in val for x in special_char):
                error.append("Middle Name should not Contain <, >, & characters")                        
            if len(val)>25:
                error.append("Middle Name in Income Details cannot exceed 25 characters")                        

        val=gettval('FirstName',data)     
        if val!='notfound' and val!='err':
            if any(x in val for x in special_char):
                error.append("First name should not Contain <, >, & characters")                        
            if len(val)>25:
                error.append("First Name in Income Details cannot exceed 25 characters")                        

        val=gettval('PAN',data) 
        if val!='notfound' and val!='err':
            if bool(re.match('[A-Z]{3}[P][A-Z][0-9]{4}[A-Z]$',val))==False:
                error.append("Invalid PAN in Income Details. PAN format should be First 5 Alphabets, next 4 digits, then 1 Alphabet and the 4th character must be 'P'")  
        else:
            error.append("PAN is mandatory in Income Details")                        

        val=gettval('ResidenceNo',data) 
        if val!='notfound' and val!='err':
            if len(val)>50:
                error.append("Flat/Door/Block No in Income Details  cannot exceed 50 characters")  
        else:
            error.append("Flat/Door/block Number is mandatory in Income Details")                        

        val=gettval('ResidenceName',data) 
        if val!='notfound' and val!='err':
            if len(val)>50:
                error.append("Residence Name in Income Details cannot exceed 50 characters")  

        val=gettval('RoadOrStreet',data) 
        if val!='notfound' and val!='err':
            if len(val)>50:
                error.append("Road Or Street in Income Details cannot exceed 50 characters")  
            
        val=gettval('LocalityOrArea',data) 
        if val!='notfound' and val!='err':
            if len(val)>50:
                error.append("Area/ Locality in Income Details  cannot exceed 50 characters")  
        else:
            error.append("Area/ Locality is mandatory in Income Details")                        

        val=mytree.find('.//ITRForm:PersonalInfo//ITRForm:Address//ITRForm:CityOrTownOrDistrict',ns).text
        if val is not None:
            if len(val)>50:
                error.append("Town/City/District in Income Details  cannot exceed 50 characters")  
        else:
            error.append("Town/City/District is mandatory in Income Details")                        

        val=mytree.find('.//ITRForm:PersonalInfo//ITRForm:Address//ITRForm:StateCode',ns).text
        if val is not None:
            if val not in ('01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37'):
                error.append("'StateCode' selection in Income Details is not in the defined list of values")                        
        else:
            error.append("State is mandatory in Income Details")                        

        val=gettval('CountryCode',data) 
        if val!='notfound' and val!='err':
            if val!='91':
                error.append("Country is has to be 91")                        
        else:
            error.append("Country is mandatory in Income Details")                        

        val=mytree.find('.//ITRForm:PersonalInfo//ITRForm:Address//ITRForm:PinCode',ns).text 
        if val is not None:
            if bool(re.match('[1-9]{1}[0-9]{5}$',val))==False:
                error.append("PinCode format incorrect: must start with a digit between 1 and 9, followed by 5 digits between 0 and 9")                        
        else:
            error.append("PinCode is mandatory in Income Details")                        

        val=gettval('CountryCodeMobile',data) 
        if val!='notfound' and val!='err':
            if bool(re.match('[0-9]{2}$',val))==False:
                error.append("Country Code (Mobile Number) has to be 2 digits")                        
        else:
            error.append("Country Code (Mobile Number) is mandatory in Income Details")                        

        val=gettval('MobileNo',data) 
        if val!='notfound' and val!='err':
            if bool(re.match('[1-9]{1}[0-9]{9}$',val))==False:
                error.append("Mobile Number format incorrect: has to start with a non zero digit, followed by 9 digits between 0 and 9")                        
        else:
            error.append("Mobile Number is mandatory in Income Details")                        

        val=gettval('EmailAddress',data) 
        if val!='notfound' and val!='err':
            if bool(re.match('([\.a-zA-Z0-9_\-])+@([a-zA-Z0-9_\-])+(([a-zA-Z0-9_\-])*\\.([a-zA-Z0-9_\-])+)+',val))==False:
                error.append("Email Address format incorrect")                        
            if len(val)>125:
                error.append("Email Address in Income Details cannot exceed 125 characters")                        
        else:
            error.append("Email Address is mandatory in Income Details")                        

        val=gettval('DOB',data) 
        if val!='notfound' and val!='err':
            if calcAge(data['DOB'])=='err':
                error.append("Date of Birth incorrect")            
        else:
            error.append("Date of Birth is mandatory in Income Details")                        

        val=gettval('EmployerCategory',data) 
        if val!='notfound' and val!='err':
            if val not in ('GOV','PSU','PE','OTH','NA'):
                error.append("Nature of Employment is not in the defined list of values")                        
        else:
            error.append("Nature of Employment is mandatory in  Income Details")                        

        val=gettval('AadhaarCardNo',data) 
        if val!='notfound' and val!='err':
            if not bool(re.match('[0-9]{12}$',val)) or val=='000000000000' or val=='111111111111':
                error.append("Please enter valid Aadhaar Number in Income Details")                        

        val=gettval('AadhaarEnrolmentId',data) 
        if val!='notfound' and val!='err':
            if not bool(re.match('[0-9]{28}$',val)) or val=='0000000000000000000000000000' or val=='1111111111111111111111111111':
                error.append("Please enter valid Aadhaar Enrolment Id in Income Details")                        

        val=gettval('ReturnFileSec',data) 
        if val!='notfound' and val!='err':
            if val not in ('11','12','13','14','15','16','17','18','20'):
                error.append("'Return Filed u/s section/ Filed in response to notice u/s' selection is not in the list of defined values")                        
            if val in ('17','18'):
                if gettval('ReceiptNo',data)=='notfound' or gettval('ReceiptNo',data)=='err':
                    error.append('Receipt Number for filed u/s 139(9) And Date of filing of Original Return for return filed u/s 139(9) is mandatory in Income Details')
                if 'OrigRetFiledDate' in data and check_date(data['OrigRetFiledDate'])==True:
                    if dt.datetime.strptime(data['OrigRetFiledDate'],"%Y-%m-%d").date() < dt.datetime.strptime("01-04-" + str(ASS_YEAR),"%d-%m-%Y").date():
                        error.append("Date of Filing in Sheet Income Details  should be on or after " + "01-04-" + str(ASS_YEAR))                
                else:
                    error.append("Date of Filing in Sheet Income Details is mandatory")                
            if val in ('18','13','14','15','16','20'):
                if gettval('NoticeNo',data)=='notfound' or gettval('NoticeNo',data)=='err':
                    error.append("Unique number and Date of Notice/Order is mandatory for 'Filed in response to notice u/s' is '139(9)/142(1)/148/153A/153C' or Filed u/s is '119(2)(b)-after condonation of delay' is mandatory in Income Details")
                if 'NoticeDateUnderSec' in data and check_date(data['NoticeDateUnderSec'])==True:
                    if dt.datetime.strptime(data['NoticeDateUnderSec'],"%Y-%m-%d").date() < dt.datetime.strptime("01-04-" +str(ASS_YEAR),"%d-%m-%Y").date():
                        error.append("Notice Date in Sheet Income Details  should be on or after " + "01-04-" + str(ASS_YEAR))                
                else:
                    error.append("Notice Date in Sheet Income Details is mandatory") 
            if len(gettval('NoticeNo',data))>23:
                error.append("Unique Number in Income Details cannot exceed 23 characters")   
        else:
            error.append("Please Select ""Filed u/s"" or ""Filed in response to notice u/s  in Income Details")                         

        if getfval('GrossRentReceived',data)!=0 or getfval('TaxPaidlocalAuth',data)!=0 or getfval('InterestPayable',data)!=0:
            val=gettval('TypeOfHP',data) 
            if val=='notfound' or val=='err':
                    error.append("Select the Type of House Property in Income Details")
        if val!='notfound' and val!='err':
            if val in ['L','D']:
                if getfval('TaxPaidlocalAuth',data)>0 and getfval('GrossRentReceived',data)==0:
                    error.append("Tax paid to local authorities can be claimed only if income from house property is declared in Income Details")
            if val=='S'and getfval('InterestPayable',data)>INTEREST_ON_BORROWED_CAPITAL_HOUSE:
                error.append("For a Self occupied House Property,Interest payable on borrowed capital value cannot exceed " + str(INTEREST_ON_BORROWED_CAPITAL_HOUSE))            
                

        if getfval('DeductionUs16ia',data) > STANDARD_DEDUCTION_16ia:
            error.append("Maximum Deduction u/s 16(ia) is Rs " + str(STANDARD_DEDUCTION_16ia) + " only in Income Details")

        if gettval('EmployerCategory',data) in ('GOV'):
            if getfval('EntertainmentAlw16ii',data)>ENTERTAINEMENT_ALLOWANCE_16:
                error.append("Deduction of Entertainment allowance u/s 16(ii) should not exceed Rs " + str(ENTERTAINEMENT_ALLOWANCE_16) +" in Income Details")
        else:
            if getfval('EntertainmentAlw16ii',data)>0:
                error.append("Deduction of Entertainment allowance u/s 16(ii) is allowed only for Governtment Employess in Income Details")

        if gettval('EmployerCategory',data) in ('GOV','PSU','OTH'):
            if getfval('ProfessionalTaxUs16iii',data)>PROFESSIONAL_TAX_16:
                error.append("Deduction of Professional allowance u/s 16(iii) should not exceed Rs" + str(PROFESSIONAL_TAX_16) +" in Income Details")
        else:
            if getfval('ProfessionalTaxUs16iii',data)>0:
                error.append("Deduction of Professional allowance u/s 16(ii) is allowed only for Nature of Employment 'Governtment Employe', 'PSU' or 'Others' in Income Details")

        if gettval('HealthInsurancePremium',datausr) in ('1','2','3','4','5','6','7') and getfval('Sec80DHealthInsurancePremiumUsr',datausr)==0:
            error.append("Please enter the value for Part A Sec 80D deduction under Chapter VIA in Income Details")
        if getfval('Sec80DHealthInsurancePremiumUsr',datausr) >0 and gettval('HealthInsurancePremium',datausr) not in ('1','2','3','4','5','6','7'):
            error.append("Please select a valid option at dropdown of Part A Sec 80D (Health Insurance Premium) deduction under Chapter VIA in Income Details")
        if gettval('HealthInsurancePremium',datausr)=='7' and 'DOB' in data:
            age=calcAge(data['DOB'])
            if age!='err':
                if age<=59:
                    error.append("Please select a valid option from the dropdown (self not senior citizen) of Part A Sec 80D (Health Insurance Premium) deduction under Chapter VIA in Income Details")

        if gettval('MedicalExpenditure',datausr) in ('1','2','3') and getfval('Sec80DMedicalExpenditureUsr',datausr)==0:
            error.append("Please enter the value for Part B Sec 80D (Medical Expenditure) deduction under Chapter VIA in Income Details")
        if getfval('Sec80DMedicalExpenditureUsr',datausr) >0 and gettval('MedicalExpenditure',datausr) not in ('1','2','3'):
            error.append("Please select a valid option at dropdown of Part B Sec 80D (Medical Expenditure) Deduction under Chapter VIA in Income Details")

        if gettval('PreventiveHealthCheckUp',datausr) in ('1','2','3') and getfval('Sec80DPreventiveHealthCheckUpUsr',datausr)==0:
            error.append("Please enter the value for Part C Sec 80D (Preventive Health check-up) deduction under Chapter VIA in Income Details")
        if getfval('Sec80DPreventiveHealthCheckUpUsr',datausr) >0 and gettval('PreventiveHealthCheckUp',datausr) not in ('1','2','3'):
            error.append("Please select a valid option at dropdown of Part C Sec 80D (Preventive Health check-up) deduction under Chapter VIA in Income Details")


        if gettval('Section80DDUsrType',datausr) in ('1','2') and get_tot_gen('UsrDeductUndChapVIA','Section80DD',mytree,ns)==0:
            error.append("Please enter the value for 80DD deduction under Chapter VIA in Income Details")
        if get_tot_gen('UsrDeductUndChapVIA','Section80DD',mytree,ns) > 0 and gettval('Section80DDUsrType',datausr) not in ('1','2'):
            error.append("Please select a valid option at dropdown of Sec.80DD under Chapter VIA in Income Details")

        if gettval('Section80DDBUsrType',datausr) in ('1','2') and get_tot_gen('UsrDeductUndChapVIA','Section80DDB',mytree,ns)==0:
            error.append("Please enter the value for 80DDB deduction under Chapter VIA in Income Details")
        if get_tot_gen('UsrDeductUndChapVIA','Section80DDB',mytree,ns) > 0 and gettval('Section80DDBUsrType',datausr) not in ('1','2'):
            error.append("Please select a valid option at dropdown of Sec.80DDB under Chapter VIA in Income Details")

        if gettval('Section80UUsrType',datausr) in ('1','2') and get_tot_gen('UsrDeductUndChapVIA','Section80U',mytree,ns)==0:
            error.append("Please enter the value for 80U deduction under Chapter VIA in Income Details")
        if get_tot_gen('UsrDeductUndChapVIA','Section80U',mytree,ns) > 0 and gettval('Section80UUsrType',datausr) not in ('1','2'):
            error.append("Please select a valid option at dropdown of Sec.80U under Chapter VIA in Income Details")

        #Check that table deduction u/s 10 has nature of allowance, description if 'oth' is selected and desc <= 125 characters
        tmp_root=mytree.find('.//ITRForm:AllwncExemptUs10',ns)
        row_count=0
        if tmp_root is not None:
            for row in list(tmp_root): 
                row_oth=False
                oth_desc=False
                row_count+=1
                col=0
                for row_data in row.iter():
                    if rn(row_data.tag)=='SalNatureDesc':
                        col+=1
                        if row_data.text is None:
                            error.append("Nature of Income at row " + str(row_count) + " for Allowances exemp u/s 10 in Income Details is mandatory")
                        elif row_data.text=='OTH':
                            row_oth=True
                    elif rn(row_data.tag)=='SalOthNatOfInc':
                        col+=1
                        if row_data.text is not None:
                            oth_desc=True
                            if len(row_data.text) > 125:
                                error.append("Description at row" + str(row_count) + " for Allowances exemp u/s 10 in Income Details cannot exceed 125 characters")
                    elif rn(row_data.tag)=='SalOthAmount':
                        col+=1
                if row_oth==True and oth_desc==False:
                    error.append("Description missing at " + str(row_count) + " for Allowances exemp u/s 10 in Income Details")
                if ((row_oth==True and col!=3) or (row_oth==False and col!=2)) and len(row)>0:
                    error.append("Please enter all columns in row " + str(row_count) + " for Allowances exemp u/s 10 Table in Income Details")


        #Check that table Income from Other Sources has nature of income, description if 'oth' is selected and desc <= 125 characters
        tmp_root=mytree.find('.//ITRForm:OthersInc',ns)
        row_count=0
        if tmp_root is not None:
            for row in list(tmp_root): 
                row_oth=False
                oth_desc=False
                row_count+=1
                col=0
                for row_data in row.iter():
                    if rn(row_data.tag)=='OthSrcNatureDesc':
                        col+=1
                        if row_data.text is None:
                            error.append("Nature of Income at row " + str(row_count) + " for Income from Other Sources in Income Details is mandatory")
                        elif row_data.text=='OTH':
                            row_oth=True
                    elif rn(row_data.tag)=='OthSrcOthNatOfInc':
                        col+=1
                        if row_data.text is not None:
                            oth_desc=True
                            if len(row_data.text) > 125:
                                error.append("Description at row " + str(row_count) + " for Income from Other Sources in Income Details cannot exceed 125 characters")
                    elif rn(row_data.tag)=='OthSrcOthAmount':
                        col+=1
                if row_oth==True and oth_desc==False:
                    error.append("Description missing at " + str(row_count) + " for Income from Other Sources in Income Details")
                if ((row_oth==True and col!=3) or (row_oth==False and col!=2)) and len(row)>0:
                    error.append("Please enter all columns in row " + str(row_count) + " for Income from Other Sources Table in Income Details")

        #Check that table Exempt Income has nature of income, description if 'oth' is selected and desc <= 125 characters
        tmp_root=mytree.find('.//ITRForm:ExemptIncAgriOthUs10',ns)
        if tmp_root is not None:
            row_count=0
            for row in list(tmp_root): 
                row_oth=False
                oth_desc=False
                row_count+=1
                col=0
                for row_data in row.iter():
                    if rn(row_data.tag)=='NatureDesc':
                        col+=1
                        if row_data.text is None:
                            error.append("Nature of Income at row " + str(row_count) + " for Exempt Income in Income Details is mandatory")
                        elif row_data.text=='OTH':
                            row_oth=True
                    elif rn(row_data.tag)=='OthNatOfInc':
                        col+=1
                        if row_data.text is not None:
                            oth_desc=True
                            if len(row_data.text) > 125:
                                error.append("Description at row " + str(row_count) + " for Exempt Income in Income Details cannot exceed 125 characters")
                    elif rn(row_data.tag)=='OthAmount':
                        col+=1
                if row_oth==True and oth_desc==False:
                    error.append("Description missing at " + str(row_count) + " for Exempt Income in Income Details")
                if ((row_oth==True and col!=3) or (row_oth==False and col!=2)) and len(row)>0:
                    error.append("Please enter all columns in row " + str(row_count) + " for Exempt Income Table in Income Details")

        ###########################################################################################################################################
        #Validate TDS
        ###########################################################################################################################################
        #validate TDS from Salary (TDS1)
        tmp_root=mytree.find('.//ITRForm:TDSonSalaries',ns)
        if tmp_root is not None:
            row_count=0
            for row in list(tmp_root): 
                row_count+=1
                inc=0
                col=0
                for row_data in row.iter():
                    if rn(row_data.tag)=='TAN':
                        col+=1
                        if row_data.text is None:
                            error.append("TAN of Employer missing at row " + str(row_count) + " in Schedule TDS-1")
                        elif bool(re.match('[A-Z]{4}[0-9]{5}[A-Z]$',row_data.text))==False:
                            error.append("Invalid TAN. TAN format should be First 4 alphabets, then 5 digits, then alphabe at row " + str(row_count) + " in Schedule TDS-1")
                    elif rn(row_data.tag)=='EmployerOrDeductorOrCollecterName':
                        col+=1
                        if row_data.text is None:
                            error.append("Please enter the Name of Employer at row " + str(row_count) + " in Schedule TDS-1")
                        elif len(row_data.text) > 125:
                            error.append("Name of Deductor cannot exceed 125 characters at row " + str(row_count) + " in Schedule TDS-1")
                    elif rn(row_data.tag)=='IncChrgSal':
                        col+=1
                        if row_data.text is None:
                            error.append("Income Chargeable is mandatory at row " + str(row_count) + " in Schedule TDS-1")
                        else:
                            if check_if_int(row_data.text)==False:
                                error.append("Income Chargeable should be an integer value at row " + str(row_count) + " in Schedule TDS-1")
                            elif int(row_data.text) <0:
                                error.append("Income Chargeable cannot be negative at row " + str(row_count) + " in Schedule TDS-1")
                            else:
                                inc=int(row_data.text)
                    elif rn(row_data.tag)=='TotalTDSSal':
                        col+=1
                        if row_data.text is None:
                            error.append("Total Tax Deducted is mandatory at row " + str(row_count) + " in Schedule TDS-1")
                        else:
                            if check_if_int(row_data.text)==False:
                                error.append("Total Tax Deducted should be an integer value at row " + str(row_count) + " in Schedule TDS-1")
                            elif int(row_data.text) <0:
                                error.append("Total Tax Deducted cannot be negative at row " + str(row_count) + " in Schedule TDS-1")
                            elif int(row_data.text) > inc:
                                error.append("Total tax deducted cannot be more than Income chargeable under salaries at row " + str(row_count) + " in Schedule TDS-1")
                if col!=4 and len(row) > 0:
                    error.append("Please enter all columns in row " + str(row_count) + " table TDS-1")

        #validate TDS from Other than Salary (TDS2)
        tmp_root=mytree.find('.//ITRForm:TDSonOthThanSals',ns)
        if tmp_root is not None:
            row_count=0
            for row in list(tmp_root): 
                row_count+=1
                inc=0
                col=0
                for row_data in row.iter():
                    if rn(row_data.tag)=='TAN':
                        col+=1
                        if row_data.text is None:
                            error.append("TAN of Employer missing at row " + str(row_count) + " in Schedule TDS-1")
                        elif bool(re.match('[A-Z]{4}[0-9]{5}[A-Z]$',row_data.text))==False:
                            error.append("Invalid TAN. TAN format should be First 4 alphabets, then 5 digits, then alphabe at row " + str(row_count) + " in Schedule TDS-1")
                    elif rn(row_data.tag)=='EmployerOrDeductorOrCollecterName':
                        col+=1
                        if row_data.text is None:
                            error.append("Please enter the Name of Employer at row " + str(row_count) + " in Schedule TDS-1")
                        elif len(row_data.text) > 125:
                            error.append("Name of Deductor cannot exceed 125 characters at row " + str(row_count) + " in Schedule TDS-1")
                    elif rn(row_data.tag)=='AmtForTaxDeduct':
                        col+=1
                        if row_data.text is None:
                            error.append("Gross receipt is mandatory at row " + str(row_count) + " in Schedule TDS-1")
                        else:
                            if check_if_int(row_data.text)==False:
                                error.append("Gross receipt should be an integer value at row " + str(row_count) + " in Schedule TDS-1")
                            elif int(row_data.text) <0:
                                error.append("Gross receipt cannot be negative at row " + str(row_count) + " in Schedule TDS-1")
                    elif rn(row_data.tag)=='DeductedYr':
                        col+=1
                        if row_data.text is None:
                            error.append("Deduction Year is mandatory at row " + str(row_count) + " in Schedule TDS-2")
                        else:
                            if check_if_int(row_data.text)==False:
                                error.append("Deduction Year should be an integer between 2001 and " + str(ASS_YEAR -1) + " in Schedule TDS-2")
                            elif int(row_data.text) > ASS_YEAR-1:
                                error.append("Deduction Year should be between 2001 and " + str(ASS_YEAR -1) + " in Schedule TDS-2")
                    elif rn(row_data.tag)=='TotTDSOnAmtPaid':
                        col+=1
                        if row_data.text is None:
                            error.append("Tax deducted is mandatory at row " + str(row_count) + " in Schedule TDS-2")
                        else:
                            if check_if_int(row_data.text)==False:
                                error.append("Tax deducted should be an integer value at row " + str(row_count) + " in Schedule TDS-2")
                            elif int(row_data.text) <0:
                                error.append("Tax deducted cannot be negative at row " + str(row_count) + " in Schedule TDS-2")
                            else:
                                inc=int(row_data.text)
                    elif rn(row_data.tag)=='ClaimOutOfTotTDSOnAmtPaid':
                        col+=1
                        if row_data.text is None:
                            error.append("TDS Credit is mandatory at row " + str(row_count) + " in Schedule TDS-2")
                        else:
                            if check_if_int(row_data.text)==False:
                                error.append("TDS Credit should be an integer value at row " + str(row_count) + " in Schedule TDS-2")
                            elif int(row_data.text) <0:
                                error.append("TDS Credit cannot be negative at row " + str(row_count) + " in Schedule TDS-2")
                            elif int(row_data.text) > inc:
                                error.append("TDS credit claimed cannot be more than Tax deducted at row " + str(row_count) + " in Schedule TDS-2")
                if col!=6 and len(row)>0:
                    error.append("Please enter all columns in row " + str(row_count) + " table TDS-2")

        #validate TDS as per form6C (TDS3)
        tmp_root=mytree.find('.//ITRForm:ScheduleTDS3Dtls',ns)
        if tmp_root is not None:
            row_count=0
            for row in list(tmp_root): 
                row_count+=1
                inc=0
                col=0
                for row_data in row.iter():
                    if rn(row_data.tag)=='PANofTenant':
                        col+=1
                        if row_data.text is None:
                            error.append("PAN of Tenant missing at row " + str(row_count) + " in Schedule TDS-3")
                        elif bool(re.match('[A-Z]{5}[0-9]{4}[A-Z]$',row_data.text))==False:
                            error.append("PAN is invalid. First 5 alphabets, next 4 digits, then alphabet at row " + str(row_count) + " in Schedule TDS-3")
                    elif rn(row_data.tag)=='NameOfTenant':
                        col+=1
                        if row_data.text is None:
                            error.append("Please enter Name of Tenant at row " + str(row_count) + " in Schedule TDS-3")
                        elif len(row_data.text) > 125:
                            error.append("Name of Tenant cannot exceed 125 characters at row " + str(row_count) + " in Schedule TDS-3")
                    elif rn(row_data.tag)=='GrsRcptToTaxDeduct':
                        col+=1
                        if row_data.text is None:
                            error.append("Gross receipt is mandatory at row " + str(row_count) + " in Schedule TDS-3")
                        else:
                            if check_if_int(row_data.text)==False:
                                error.append("Gross receipt should be an integer value at row " + str(row_count) + " in Schedule TDS-3")
                            elif int(row_data.text) <0:
                                error.append("Gross receipt cannot be negative at row " + str(row_count) + " in Schedule TDS-3")
                    elif rn(row_data.tag)=='DeductedYr':
                        col+=1
                        if row_data.text is None:
                            error.append("Deduction Year is mandatory at row " + str(row_count) + " in Schedule TDS-3")
                        else:
                            if check_if_int(row_data.text)==False:
                                error.append("Deduction Year should be an integer between 2001 and " + str(ASS_YEAR -1) + " in Schedule TDS-3")
                            elif int(row_data.text) > ASS_YEAR-1:
                                error.append("Deduction Year should be between 2001 and " + str(ASS_YEAR -1) + " in Schedule TDS-3")
                    elif rn(row_data.tag)=='TDSDeducted':
                        col+=1
                        if row_data.text is None:
                            error.append("Tax deducted is mandatory at row " + str(row_count) + " in Schedule TDS-3")
                        else:
                            if check_if_int(row_data.text)==False:
                                error.append("Tax deducted should be an integer value at row " + str(row_count) + " in Schedule TDS-3")
                            elif int(row_data.text) <0:
                                error.append("Tax deducted cannot be negative at row " + str(row_count) + " in Schedule TDS-3")
                            else:
                                inc=int(row_data.text)
                    elif rn(row_data.tag)=='TDSClaimed':
                        col+=1
                        if row_data.text is None:
                            error.append("TDS Credit claimed is mandatory at row " + str(row_count) + " in Schedule TDS-3")
                        else:
                            if check_if_int(row_data.text)==False:
                                error.append("TDS Credit claimed should be an integer value at row " + str(row_count) + " in Schedule TDS-3")
                            elif int(row_data.text) <0:
                                error.append("TDS Credit claimed cannot be negative at row " + str(row_count) + " in Schedule TDS-3")
                            elif int(row_data.text) > inc:
                                error.append("TDS credit claimed cannot be more than Tax deducted at row " + str(row_count) + " in Schedule TDS-3")
                if col!=6 and len(row)>0:
                    error.append("Please enter all columns in row " + str(row_count) + " table TDS-3")

        #validate Advance Tax (IT)
        tmp_root=mytree.find('.//ITRForm:TaxPayments',ns)
        if tmp_root is not None:
            row_count=0
            for row in list(tmp_root): 
                row_count+=1
                inc=0
                col=0
                for row_data in row.iter():
                    if rn(row_data.tag)=='BSRCode':
                        col+=1
                        if row_data.text is None:
                            error.append("BSR Code missing at row " + str(row_count) + " in Schedule TDS (IT)")
                        elif bool(re.match('[0-9]{7}$',row_data.text))==False:
                            error.append("BSR Code is invalid at row " + str(row_count) + " in Schedule TDS (IT)")
                    elif rn(row_data.tag)=='DateDep':
                        col+=1
                        if row_data.text is None:
                            error.append("Please enter the date of Deposit at row " + str(row_count) + " in Schedule TDS (IT)")
                        elif check_date(row_data.text)==False:
                            error.append("Date of Credit into Govt Account not a valida date at row " + str(row_count) + " in Schedule TDS (IT)")
                        elif dt.datetime.strptime(row_data.text,"%Y-%m-%d").date() <= dt.datetime.strptime(str(ASS_YEAR-2) + "-03-31","%Y-%m-%d").date() :
                            error.append("Date of Credit into Govt Account should be after 31/03/2017 at row " + str(row_count) + " in Schedule TDS (IT)")
                    elif rn(row_data.tag)=='SrlNoOfChaln':
                        col+=1
                        if row_data.text is None:
                            error.append("Serial Number of Challan is mandatory at row " + str(row_count) + " in Schedule TDS (IT)")
                        else:
                            if check_if_int(row_data.text)==False:
                                error.append("Serial Number of Challan should be an integer value at row " + str(row_count) + " in Schedule TDS (IT)")
                            elif int(row_data.text) <0:
                                error.append("Serial Number of Challan cannot be negative at row " + str(row_count) + " in Schedule TDS c")
                    elif rn(row_data.tag)=='Amt':
                        col+=1
                        if row_data.text is None:
                            error.append("Tax Paid Amount is mandatory at row " + str(row_count) + " in Schedule (IT)")
                        else:
                            if check_if_int(row_data.text)==False:
                                error.append("Tax Paid Amount should be an integer value at row " + str(row_count) + " in Schedule (IT)")
                            elif int(row_data.text) <0:
                                error.append("Tax Paid Amount cannot be negative at row " + str(row_count) + " in Schedule (IT)")
                if col!=4 and len(row)>0:
                    error.append("Please enter all columns in row " + str(row_count) + " in table 21 IT - Advance Tax")
                
        ###########################################################################################################################################
        #Validate TCS
        ###########################################################################################################################################
        tmp_root=mytree.find('.//ITRForm:ScheduleTCS',ns)
        if tmp_root is not None:
            row_count=0
            for row in list(tmp_root): 
                row_count+=1
                inc=0
                col=0
                for row_data in row.iter():
                    if rn(row_data.tag)=='TAN':
                        col+=1
                        if row_data.text is None:
                            error.append("TAN of Employer missing at row " + str(row_count) + " in Schedule TCS")
                        elif bool(re.match('[A-Z]{4}[0-9]{5}[A-Z]$',row_data.text))==False:
                            error.append("Invalid TAN. TAN format should be First 4 alphabets, then 5 digits, then alphabe at row " + str(row_count) + " in Schedule TCS")
                    elif rn(row_data.tag)=='EmployerOrDeductorOrCollecterName':
                        col+=1
                        if row_data.text is None:
                            error.append("Please enter the Name of Employer at row " + str(row_count) + " in Schedule TCS")
                        elif len(row_data.text) > 125:
                            error.append("Name of Deductor cannot exceed 125 characters at row " + str(row_count) + " in Schedule TCS")
                    elif rn(row_data.tag)=='AmtTaxCollected':
                        col+=1
                        if row_data.text is None:
                            error.append("Gross receipt is mandatory at row " + str(row_count) + " in Schedule TCS")
                        else:
                            if check_if_int(row_data.text)==False:
                                error.append("Gross receipt should be an integer value at row " + str(row_count) + " in Schedule TCS")
                            elif int(row_data.text) <0:
                                error.append("Gross receipt cannot be negative at row " + str(row_count) + " in Schedule TCS")
                    elif rn(row_data.tag)=='CollectedYr':
                        col+=1
                        if row_data.text is None:
                            error.append("Collection Year is mandatory at row " + str(row_count) + " in Schedule TCS")
                        else:
                            if check_if_int(row_data.text)==False:
                                error.append("Collection Year should be an integer between 2001 and " + str(ASS_YEAR -1) + " in Schedule TCS")
                            elif int(row_data.text) > ASS_YEAR-1:
                                error.append("Collection Year should be between 2001 and " + str(ASS_YEAR -1) + " in Schedule TCS")
                    elif rn(row_data.tag)=='TotalTCS':
                        col+=1
                        if row_data.text is None:
                            error.append("Tax Collected is mandatory at row " + str(row_count) + " in Schedule TCS")
                        else:
                            if check_if_int(row_data.text)==False:
                                error.append("Tax Collected should be an integer value at row " + str(row_count) + " in Schedule TCS")
                            elif int(row_data.text) <0:
                                error.append("Tax Collected cannot be negative at row " + str(row_count) + " in Schedule TCS")
                            else:
                                inc=int(row_data.text)
                    elif rn(row_data.tag)=='AmtTCSClaimedThisYear':
                        col+=1
                        if row_data.text is None:
                            error.append("TCS Credit claimed is mandatory at row " + str(row_count) + " in Schedule TCS")
                        else:
                            if check_if_int(row_data.text)==False:
                                error.append("TCS Credit claimed should be an integer value at row " + str(row_count) + " in Schedule TCS")
                            elif int(row_data.text) <0:
                                error.append("TCS Credit claimed cannot be negative at row " + str(row_count) + " in Schedule TCS")
                            elif int(row_data.text) > inc:
                                error.append("TCS credit claimed cannot be more than Tax Collected at row " + str(row_count) + " in Schedule TCS")
                if col!=6 and len(row)>0:
                    error.append("Please enter all columns in row " + str(row_count) + " in table TCS")
                            
        ###########################################################################################################################################
        #Validate 80G and 80GGA
        ###########################################################################################################################################
        s80g_types=['Don100Percent','Don50PercentNoApprReqd','Don100PercentApprReqd','Don50PercentApprReqd','Schedule80GGA']
        section_short=['80G_A','80G_B','80G_C','80G_D','80GGA']
        i=-1
        for dont_type in s80g_types:
            i+=1
            tmp_root=mytree.find('.//ITRForm:' + dont_type,ns)
            if tmp_root is not None:
                row_count=0
                for row in list(tmp_root): 
                    row_count+=1
                    cash=0
                    oth=0
                    col=0
                    for row_data in row.iter():
                        if rn(row_data.tag)=='RelevantClauseUndrDedClaimed':
                            col+=1
                            if row_data.text is None:
                                error.append("Please select relevant clause at row " + str(row_count) + " in Schedule " + section_short[i])
                        elif rn(row_data.tag)=='DoneeWithPanName' or rn(row_data.tag)=='NameOfDonee':
                            col+=1
                            if row_data.text is None:
                                error.append("Name of the Donee missing at row " + str(row_count) + " in Schedule " + section_short[i])
                            elif len(row_data.text) > 125:
                                error.append("Name of the Donee cannot exceed 125 characters at row " + str(row_count) + " in Schedule " + section_short[i])
                        elif rn(row_data.tag)=='AddrDetail':
                            col+=1
                            if row_data.text is None:
                                error.append("Address of the Donee missing at row " + str(row_count) + " in Schedule " + section_short[i])
                            elif len(row_data.text) > 200:
                                error.append("Address of the Donee cannot exceed 200 characters at row " + str(row_count) + " in Schedule " + section_short[i])
                        elif rn(row_data.tag)=='CityOrTownOrDistrict':
                            col+=1
                            if row_data.text is None:
                                error.append("City/Town/District of the Donee missing at row " + str(row_count) + " in Schedule " + section_short[i])
                            elif len(row_data.text) > 50:
                                error.append("City/Town/District of the Donee cannot exceed 50 characters at row " + str(row_count) + " in Schedule " + section_short[i])
                        elif rn(row_data.tag)=='StateCode':
                            col+=1
                            if row_data.text is None:
                                error.append("State Code missing at row " + str(row_count) + " in Schedule " + section_short[i])
                            elif row_data.text not in ('01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37'):
                                error.append("State Code not valid at row " + str(row_count) + " in Schedule " + section_short[i])
                        elif rn(row_data.tag)=='PinCode':
                            col+=1
                            if row_data.text is None:
                                error.append("Pin Code is mandatory at row " + str(row_count) + " in Schedule " + section_short[i])
                            else:
                                if bool(re.match('[1-9]{1}[0-9]{5}$',row_data.text))==False:
                                    error.append("Pin Code must be 6 digits numeric value Value at row " + str(row_count) + " in Schedule " + section_short[i])
                        elif rn(row_data.tag)=='DoneePAN':
                            col+=1
                            if row_data.text is None:
                                error.append("PAN of the Donee is mandatory at row " + str(row_count) + " in Schedule " + section_short[i])
                            else:
                                if bool(re.match('[A-Z]{5}[0-9]{4}[A-Z]$',row_data.text))==False:
                                    error.append("PAN of the Donee is in incorrect format at row " + str(row_count) + " in Schedule " + section_short[i])
                                elif row_data.text==gettval('AssesseeVerPAN',data) or row_data.text==gettval('PAN',data):
                                    error.append("PAN of the Donee is invalid. Donee PAN cannot be assessee PAN or verification PAN at row " + str(row_count) + " in Schedule " + section_short[i])
                        elif rn(row_data.tag)=='DonationAmtCash':
                            col+=1
                            if row_data.text is None:
                                pass
                            else:
                                if check_if_int(row_data.text)==False:
                                    error.append("Amount of donation in cash should be an integer value at row " + str(row_count) + " in Schedule " + section_short[i])
                                elif int(row_data.text) <0:
                                    error.append("Amount of donation in cash cannot be negative at row " + str(row_count) + " in Schedule " + section_short[i])
                                else:
                                    cash=int(row_data.text)
                        elif rn(row_data.tag)=='DonationAmtOtherMode':
                            col+=1
                            if row_data.text is None:
                                pass
                            else:
                                if check_if_int(row_data.text)==False:
                                    error.append("Amount of donation in other mode should be an integer value at row " + str(row_count) + " in Schedule " + section_short[i])
                                elif int(row_data.text) <0:
                                    error.append("Amount of donation in other mode cannot be negative at row " + str(row_count) + " in Schedule " + section_short[i])
                                else:
                                    oth=int(row_data.text)
                    if cash==0 and oth==0 and len(row) > 0:
                        error.append("Both Amount of donation in cash  and Amount of donation in other mode cannot be 0 at row " + str(row_count) + " in Schedule " + section_short[i])
                    if ((dont_type!='Schedule80GGA' and col!=8) or (dont_type=='Schedule80GGA' and col!=9)) and len(row)>0:
                        error.append("Please enter all columns in row " + str(row_count) + " in table " + dont_type)
                
        ###########################################################################################################################################
        #Validate Verification Details
        ###########################################################################################################################################
        if 'AssesseeVerName' not in data:
            error.append("Assessee name is mandatory in Verification section")
        if 'FatherName' not in data:
            error.append("Father's Name is mandatory in Verification section")
        elif any(x in data['FatherName'] for x in special_char):
                error.append("Father's Name should not Contain <, >, & characters")    
        if 'Capacity' not in data:
            error.append("Selection of capacity in Verification part is mandatory")
        elif data['Capacity'] not in ('S','R'):
            error.append("Please select appropriate option for 'capcaity' in Verification part")
        if 'Place' not in data:
            error.append("Place in Verification part is mandatory")
        if 'AssesseeVerPAN' not in data:
            error.append("PAN in Verification part is mandatory")
        elif bool(re.match('[A-Z]{5}[0-9]{4}[A-Z]$',data['AssesseeVerPAN']))==False:
            error.append("Invalid PAN in Verification part. PAN format should be First 5 Alphabets, next 4 digits, then 1 Alphabet. 4th character must be 'P' only")
        if 'IdentificationNoOfTRP' in data:
            if bool(re.match('[T][0-9]{9}$|[0-9]{6}$',data['IdentificationNoOfTRP']))==False:
                error.append("Identification No Of TRP in sheet Tax Paid and Verification must be either 'T' followed by 9 numeric value digits or 6 numeric value digits")
            if 'NameOfTRP' not in data:
                error.append("Name of TRP in Verification part is mandatory")
        if 'ReImbFrmGov' in data:
            if int(data['ReImbFrmGov'])!=0:
                if 'IdentificationNoOfTRP' not in data or 'NameOfTRP' not in data:
                    error.append("Identification No Of TRP & Name of TRP in Verification part is mandatory")
        if 'NameOfTRP' in data and 'IdentificationNoOfTRP' not in data:
            error.append("Identification No of TRP in Verification part is mandatory")

        ###########################################################################################################################################
        #Validate Bank Details
        ###########################################################################################################################################
        tmp_root=mytree.find('.//ITRForm:BankAccountDtls',ns)
        if tmp_root is not None:
            refund=False
            row_count=0
            for row in list(tmp_root): 
                row_count+=1
                col=0
                for row_data in row.iter():
                    if rn(row_data.tag)=='IFSCCode':
                        col+=1
                        if row_data.text is None:
                            error.append("IFS Code of the Bank is mandatory at " + str(row_count))
                        elif bool(re.match('[A-Z]{4}[0][A-Z0-9]{6}$',row_data.text))==False:
                            error.append("Incorrect IFS Code format at row " + str(row_count))
                    elif rn(row_data.tag)=='BankName':
                        col+=1
                        if row_data.text is None:
                            error.append("Bank Name is mandatory at " + str(row_count))
                        elif len(row_data.text) > 125:
                            error.append("Bank Name cannot exceed 125 characters at row " + str(row_count))
                    elif rn(row_data.tag)=='BankAccountNo':
                        col+=1
                        if row_data.text is None:
                            error.append("Account Number is mandatory at " + str(row_count))
                        elif bool(re.match('[a-zA-Z0-9]([/-]?(((\d*[1-9]\d*)*[a-zA-Z/-])|(\d*[1-9]\d*[a-zA-Z]*))+)*[0-9]*',row_data.text))==False:
                            error.append("Account number format incorrect at row " + str(row_count))
                    elif rn(row_data.tag)=='UseForRefund':
                        col+=1
                        if row_data.text is not None:
                            if row_data.text=='true':
                                refund=True
                if col!=4 and len(row)>0:
                    error.append("Please enter all columns in table 'Details of Bank Accounts'")
            if refund==False:
                error.append("Please select atleast one account in which you prefer to get your refund")  
        return 'ok', error, log
    except Exception as e:
        error.append('Unknown error while validating user input - generic checks')
        log.append(e)
        return 'err', error, log