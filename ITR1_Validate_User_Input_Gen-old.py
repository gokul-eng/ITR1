from ITR1_Income_Details_Threshold_Values import *
from lxml import etree
import re

def validate_input(mytree,data,ns):
    error=[]
    if getfval('Salary',data) =="err":
        error.append("'Salary' is not a numeric")
    if getfval('PerquisitesValue',data) =="err":
        error.append("'PerquisitesValue' is not a numeric")
    if getfval('ProfitsInSalary',data) =="err":
        error.append("'ProfitsInSalary' is not a numeric")
    if get_tot_gen('AllwncExemptUs10','SalOthAmount',mytree,ns)=="err":
        error.append("Errors in AllwncExemptUs10 table values")            
    if getfval('DeductionUs16ia',data) =="err":
        error.append("'DeductionUs16ia' is not a numeric")
    if getfval('EntertainmentAlw16ii',data) =="err":
        error.append("'EntertainmentAlw16ii' is not a numeric")
    if getfval('ProfessionalTaxUs16iii',data) =="err":
        error.append("'ProfessionalTaxUs16iii' is not a numeric")
    if getfval('GrossRentReceived',data) =="err":
        error.append("'GrossRentReceived' is not a numeric")
    if getfval('TaxPaidlocalAuth',data) =="err":
        error.append("'TaxPaidlocalAuth' is not a numeric")
    if getfval('InterestPayable',data) =="err":
        error.append("'InterestPayable' is not a numeric")
    if getfval('ArrearsUnrealizedRentRcvd',data) =="err":
        error.append("'ArrearsUnrealizedRentRcvd' is not a numeric")
    if get_tot_gen('OthersInc','OthSrcOthAmount',mytree,ns)=="err":
        error.append("Errors in 'Income from Other Sources' table values") 
    for deduction in mytree.findall('.//ITRForm:OthersInc',ns):
        for snode in deduction.iter():
            if rn(snode.tag)=='OthSrcNatureDesc':
                if nz(snode.text) not in ('SAV','IFD','TAX','FAP','OTH'):
                    error.append("'Income from Other Sources table' selection is not in defined values") 
                    break
    if getfval('DeductionUs57iia',data) =="err":
        error.append("'DeductionUs57iia' is not a numeric")
    if get_tot_gen('UsrDeductUndChapVIA','Section80C',mytree,ns)=="err":
        error.append("Error in Chap6A, Section80C value")            
    if get_tot_gen('UsrDeductUndChapVIA','Section80CCC',mytree,ns)=="err":
        error.append("Error in Chap6A, Section80CCC value")            
    if get_tot_gen('UsrDeductUndChapVIA','Section80CCDEmployeeOrSE',mytree,ns)=="err":
        error.append("Error in Chap6A, Section80CCD(1) value")            
    if get_tot_gen('UsrDeductUndChapVIA','Section80CCD1B',mytree,ns)=="err":
        error.append("Error in Chap6A, Section80CCD1B value")            
    if get_tot_gen('UsrDeductUndChapVIA','Section80CCDEmployer',mytree,ns)=="err":
        error.append("Error in Chap6A, Section80CCDEmployer-80CCD(2) value")            
    if get_tot_gen('UsrDeductUndChapVIA','Section80CCG',mytree,ns)=="err":
        error.append("Error in Chap6A, Section80CCG value")            
    if gettval('MedicalExpenditure',data) not in ('1','2','3'):
        error.append("'MedicalExpenditure' selection is not in defined values")                        
    if gettval('PreventiveHealthCheckUp',data) not in ('1','2','3'):
        error.append("'PreventiveHealthCheckUp' selection is not in defined values")                        
    if get_tot_gen('UsrDeductUndChapVIA','Sec80DMedicalExpenditureUsr',mytree,ns)=="err":
        error.append("Error in Chap6A, Sec80D Medical Expenditure value")            
    if get_tot_gen('UsrDeductUndChapVIA','Sec80DHealthInsurancePremiumUsr',mytree,ns)=="err":
        error.append("Error in Chap6A, Sec80D Health Insurance Premium value")            
    if get_tot_gen('UsrDeductUndChapVIA','Sec80DPreventiveHealthCheckUpUsr',mytree,ns)=="err":
        error.append("Error in Chap6A, Sec80D Preventive Health CheckUp value")            
    if get_tot_gen('UsrDeductUndChapVIA','Section80DD',mytree,ns)=="err":
        error.append("Error in Chap6A, Section80DD value")            
    if gettval('Section80DDUsrType',data) not in ('1','2'):
        error.append("'Section80DD' selection is not in defined values")                        
    if get_tot_gen('UsrDeductUndChapVIA','Section80DDB',mytree,ns)=="err":
        error.append("Error in Chap6A, Section80DDB value")            
    if gettval('Section80DDBUsrType',data) not in ('1','2'):
        error.append("'Section80DDB' selection is not in defined values")                        
    if get_tot_gen('UsrDeductUndChapVIA','Section80E',mytree,ns)=="err":
        error.append("Error in Chap6A, Section80E value")            
    if get_tot_gen('UsrDeductUndChapVIA','Section80EE',mytree,ns)=="err":
        error.append("Error in Chap6A, Section80EE value")            
    if get_tot_gen('Schedule80GGA','DonationAmtCash',mytree,ns)=="err":
        error.append("Error in Chap6A, Section80GGA Donation amount cash values")         
    if get_tot_gen('UsrDeductUndChapVIA','Section80GGC',mytree,ns)=="err":
        error.append("Error in Chap6A, Section80GGC value")         
    if get_tot_gen('UsrDeductUndChapVIA','Section80TTA',mytree,ns)=="err":
        error.append("Error in Chap6A, Section80TTA value")         
    if get_tot_gen('UsrDeductUndChapVIA','Section80TTB',mytree,ns)=="err":
        error.append("Error in Chap6A, Section80TTB value")         
    if get_tot_gen('UsrDeductUndChapVIA','Section80U',mytree,ns)=="err":
        error.append("Error in Chap6A, Section80U value")         
    if gettval('Section80UUsrType',data) not in ('1','2'):
        error.append("'Section80U' selection is not in defined values")                        
    if get_tot_gen('Don100Percent','DonationAmtCash',mytree,ns)=="err":
        error.append("Error in 80G Don 100Percent 'cash' values")         
    if get_tot_gen('Don100Percent','DonationAmtOtherMode',mytree,ns)=="err":
        error.append("Error in 80G Don 100Percent 'other mode' values")         
    if get_tot_gen('Don50PercentNoApprReqd','DonationAmtCash',mytree,ns)=="err":
        error.append("Error in 80G Don 50Percent without qual limit 'cash' values")         
    if get_tot_gen('Don50PercentNoApprReqd','DonationAmtOtherMode',mytree,ns)=="err":
        error.append("Error in 80G Don 50Percent without qual limit 'other mode' values")         
    if get_tot_gen('Don100PercentApprReqd','DonationAmtCash',mytree,ns)=="err":
        error.append("Error in 80G Don 100Percent subject to qual limit 'cash' values")         
    if get_tot_gen('Don100PercentApprReqd','DonationAmtOtherMode',mytree,ns)=="err":
        error.append("Error in 80G Don 100Percent subject to qual limit 'other mode' values")         
    if get_tot_gen('Don50PercentApprReqd','DonationAmtCash',mytree,ns)=="err":
        error.append("Error in 80G Don 50Percent subject to qual limit 'cash' values")         
    if get_tot_gen('Don50PercentApprReqd','DonationAmtOtherMode',mytree,ns)=="err":
        error.append("Error in 80G Don 50Percent subject to qual limit 'other mode' values")         
    if get_tot_gen('UsrDeductUndChapVIA','Section80GG',mytree,ns)=="err":
        error.append("Error in Chap6A, Section80GG value")         
    for deduction in mytree.findall('.//ITRForm:ExemptIncAgriOthUs10',ns):
        for snode in deduction.iter():
            if rn(snode.tag)=='NatureDesc':
                if nz(snode.text) not in ('AGRI','10(10BC)','10(10D)','10(11)','10(12)','10(13)','10(16)','10(17)','10(17A)','10(18)','DMDP','10(19)','10(26)','10(26AAA)','10(34)','OTH'):
                    error.append("'Exempt Income: For reporting purpose' selection is not in defined values") 
                    break
    if get_tot_gen('ExemptIncAgriOthUs10','OthAmount',mytree,ns)=="err":
        error.append("Error in values in table 'Exempt Income: For reporting purpose'")         
    if getfval('Section89',data) =="err":
        error.append("'Relief u/s Section89' is not a numeric")
    res=gettval('OrigRetFiledDate',data)
    if res != 'notfound':
        try:
            dt.datetime.strptime(res,"%Y-%m-%d").date()
        except:
            error.append("'Date of Filing Original Return' is not a valid date in 'yyyy-mm-dd' format")
    res=gettval('NoticeDateUnderSec',data)
    if res != 'notfound':
        try:
            dt.datetime.strptime(res,"%Y-%m-%d").date()
        except:
            error.append("'Date of Notice or Order' is not a valid date in 'yyyy-mm-dd' format")
    if get_tot_gen('TDSonSalaries','IncChrgSal',mytree,ns)=="err":
        error.append("Error in TDS1 'TDS from Salary' table, 'Income chargeable under salaries' values")         
    if get_tot_gen('TDSonSalaries','TotalTDSSal',mytree,ns)=="err":
        error.append("Error in TDS1 'TDS from Salary' table, Total 'Tax Deducted' values")         
    if get_tot_gen('TDSonOthThanSals','TotTDSOnAmtPaid',mytree,ns)=="err":
        error.append("Error in TDS2 'TDS from Other than Salary' table, 'Tax Deducted' values")         
    if get_tot_gen('TDSonOthThanSals','ClaimOutOfTotTDSOnAmtPaid',mytree,ns)=="err":
        error.append("Error in TDS2 'TDS from Other than Salary' table, 'TDS Credit claimed this year' values")         
    if get_tot_gen('ScheduleTDS3Dtls','TDSDeducted',mytree,ns)=="err":
        error.append("Error in TDS3, 'TDS as per form 16C' table, 'Tax Deducted' values")         
    if get_tot_gen('ScheduleTDS3Dtls','TDSClaimed',mytree,ns)=="err":
        error.append("Error in TDS3 'TDS as per form 16C' table, 'TDS Credit claimed this year' values")         
    try:
        for deduction in mytree.findall('.//ITRForm:ScheduleTDS3Dtls',ns):
            for snode in deduction.iter():
                if rn(snode.tag)=='DeductedYr':
                    ded_yr=int(snode.text)
                    if ded_yr >= ASS_YEAR:
                        error.append("WARNING: In TDS3 'TDS as per form 16C' table, TDS for any 'Year of tax deduction' > " + ASS_YEAR-1 + " will be ignored" )         
    except:
        error.append("Error in TDS3 'TDS as per form 16C' table, error determining year of tax deduction, please enter valid year")         
    if get_tot_gen('ScheduleTCS','TotalTCS',mytree,ns)=="err":
        error.append("Error in TCS, 'TCS as per form 27D' table, 'Tax Collected' values")         
    if get_tot_gen('ScheduleTCS','AmtTCSClaimedThisYear',mytree,ns)=="err":
        error.append("Error in TCS 'TCS as per form 27D' table, 'TCS Credit claimed this year' values")         
    try:
        for deduction in mytree.findall('.//ITRForm:TaxPayment',ns):
            for snode in deduction.iter():
                if rn(snode.tag)=='DateDep':
                    datedep=dt.datetime.strptime(snode.text,"%Y-%m-%d").date()
    except:
        error.append("Error in IT 'Details of Advance Tax and Self Assessment Tax Payments' table, 'Date of Deposit' not a valid date in 'yyyy-mm-dd' format")         
    if get_tot_gen('TaxPayment','Amt',mytree,ns)=="err":
        error.append("Error in IT 'Details of Advance Tax and Self Assessment Tax Payments' table, 'Tax Paid' values")         

    #Further Error Checks
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

    val=gettval('CityOrTownOrDistrict',data) 
    if val!='notfound' and val!='err':
        if len(val)>50:
            error.append("Town/City/District in Income Details  cannot exceed 50 characters")  
    else:
        error.append("Town/City/District is mandatory in Income Details")                        

    val=gettval('StateCode',data) 
    if val!='notfound' and val!='err':
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

    val=gettval('PinCode',data) 
    if val!='notfound' and val!='err':
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
            if gettval('ReceiptNo',data)=='notfound' or gettval('ReceiptNo',data)=='err' or calcAge(data['OrigRetFiledDate']=='err'):
                error.append('Receipt Number for filed u/s 139(9) And Date of filing of Original Return for return filed u/s 139(9) is mandatory in Income Details')
            if calcAge(data['OrigRetFiledDate'])!='err':
                if dt.datetime.strptime(data['OrigRetFiledDate'],"%Y-%m-%d").date() < dt.datetime.strptime("01-04-" +ASS_YEAR,"%d-%m-%Y").date():
                    error.append("Date of Filing in Sheet Income Details  should be on or after " + "01-04-" + ASS_YEAR)                
        if val in ('18','13','14','15','16','20'):
            if gettval('NoticeNo',data)=='notfound' or gettval('NoticeNo',data)=='err' or calcAge(data['NoticeDateUnderSec'])=='err':
                error.append("Unique number and Date of Notice/Order is mandatory for 'Filed in response to notice u/s' is '139(9)/142(1)/148/153A/153C' or Filed u/s is '119(2)(b)-after condonation of delay' is mandatory in Income Details")
            if calcAge(data['NoticeDateUnderSec'])!='err':
                if dt.datetime.strptime(data['NoticeDateUnderSec'],"%Y-%m-%d").date() < dt.datetime.strptime("01-04-" +ASS_YEAR,"%d-%m-%Y").date():
                    error.append("Notice Date in Sheet Income Details  should be on or after " + "01-04-" + ASS_YEAR)                
        if len(gettval('NoticeNo',data))>23:
            error.append("Unique Number in Income Details cannot exceed 23 characters")   
        
    else:
        error.append("Please Select ""Filed u/s"" or ""Filed in response to notice u/s  in Income Details")                         

    val=gettval('TypeOfHP',data) 
    if getfval('GrossRentReceived',data)!=0 or getfval('TaxPaidlocalAuth',data)!=0 or getfval('InterestPayable',data)!=0:
        if val=='notfound' or val=='err':
                error.append("Select the Type of House Property in Income Details")
    if val!='notfound' and val!='err':
        if val in ['L','D']:
            if getfval('TaxPaidlocalAuth',data)>0 and getfval('GrossRentReceived',data)==0:
                error.append("Tax paid to local authorities can be claimed only if income from house property is declared in Income Details")
        if val=='S'and getfval('InterestPayable',data)>INTEREST_ON_BORROWED_CAPITAL_HOUSE:
            error.append("For a Self occupied House Property,Interest payable on borrowed capital value cannot exceed " + INTEREST_ON_BORROWED_CAPITAL_HOUSE)            
            
    if len(gettval('Salary',data))>14 or len(gettval('PerquisitesValue',data))>14 or len(gettval('ProfitsInSalary',data))>14:
        error.append("Salary, Perquisites, Profits salary should not exceed 14 digits in Income Details")

    for deduction in mytree.findall('.//ITRForm:AllwncExemptUs10',ns):
        for snode in deduction.iter():
            if rn(snode.tag)=='SalNatureDesc':
                if nz(snode.text) not in ('10(5)','10(6)','10(7)','10(10)','10(10A)','10(10AA)','10(10B)(i)','10(10B)(ii)','10(10C)','10(10CC)','10(13A)','10(14)(i)','10(14)(ii)','OTH'):
                    error.append("'AllwncExemptUs10 table' selection is not in the defined list of values") 
                    break

    if len(gettval('DeductionUs16',data))>14 or len(gettval('DeductionUs16ia',data))>14 or len(gettval('IncomeFromSal',data))>14:
        error.append("Deduction u/s 16, Deduction u/s 16(ia), Total Head Salary should not exceed 14 digits in Income Details")

    if getfval('DeductionUs16ia',data) > STANDARD_DEDUCTION_16ia:
        error.append("Maximum Deduction u/s 16(ia) is Rs " + STANDARD_DEDUCTION_16ia + " only in Income Details")

    if gettval('EmployerCategory',data) in ('GOV'):
        if getfval('EntertainmentAlw16ii',data)>ENTERTAINEMENT_ALLOWANCE_16:
            error.append("Deduction of Entertainment allowance u/s 16(ii) should not exceed Rs " + ENTERTAINEMENT_ALLOWANCE_16 +" in Income Details")
    else:
        if getfval('EntertainmentAlw16ii',data)>0:
            error.append("Deduction of Entertainment allowance u/s 16(ii) is allowed only for Governtment Employess in Income Details")

    if gettval('EmployerCategory',data) in ('GOV','PSU','OTH'):
        if getfval('ProfessionalTaxUs16iii',data)>PROFESSIONAL_TAX_16:
            error.append("Deduction of Entertainment allowance u/s 16(iii) should not exceed Rs" + PROFESSIONAL_TAX_16 +" in Income Details")
    else:
        if getfval('ProfessionalTaxUs16iii',data)>0:
            error.append("Deduction of Entertainment allowance u/s 16(ii) is allowed only for Nature of Employment 'Governtment Employe', 'PSU' or 'Others' in Income Details")

    if len(gettval('GrossRentReceived',data))>14 or len(gettval('TaxPaidlocalAuth',data))>14 or len(gettval('AnnualValue',data))>14:
        error.append("Gross Rent Received, Tax Paid to Local Auth, Annual Value should not exceed 14 digits in Income Details")

    if len(gettval('StandardDeduction',data))>14 or len(gettval('InterestPayable',data))>14 or len(gettval('ArrearsUnrealizedRentRcvd',data))>14 or len(gettval('TotalIncomeOfHP',data))>14:
        error.append("Standard Deduction, Interest on borrowed capital, Arreare/unrealized rent recd, Income Head House Property should not exceed 14 digits in Income Details")
    
    if getfval('TotalIncomeOfHP',data) < -1 * MAX_LOSS_HOUSE_PROPERTY:
        error.append("Maximum loss allowed on Income Head House Property is Rs " +  -1 * MAX_LOSS_HOUSE_PROPERTY  +" in Income Details")

    if getfval('TotalIncome',data) > INCOME_LIMIT_ITR1:
        error.append("ITR 1 is for individuals being a resident other than not ordinarily resident having Income from Salaries, one house property, other sources (Interest etc.), agricultural income upto Rs.5 thousand and having total income upto Rs. " + INCOME_LIMIT_ITR1 + " . Please file other ITR")

    if gettval('Section80DHealthInsPremium',data) in ('1','2','3','4','5','6','7') and getfval('Sec80DHealthInsurancePremiumUsr',data)==0:
        error.append("Please enter the value for Part A Sec 80D deduction under Chapter VIA in Income Details")
    if getfval('Sec80DHealthInsurancePremiumUsr',data) >0 and gettval('Section80DHealthInsPremium',data) not in ('1','2','3','4','5','6','7'):
        error.append("Please select an option at dropdown of Part A Sec 80D (Health Insurance Premium) deduction under Chapter VIA in Income Details")
    if gettval('Section80DHealthInsPremium',data)=='7':
        age=calcAge(data['DOB'])
        if age!='err':
            if age<=59:
                error.append("Please select a valid option from the dropdown of Part A Sec 80D (Health Insurance Premium) deduction under Chapter VIA in Income Details")

    if gettval('MedicalExpenditure',data) in ('1','2','3') and getfval('Sec80DMedicalExpenditureUsr',data)==0:
        error.append("Please enter the value for Part B Sec 80D (Medical Expenditure) deduction under Chapter VIA in Income Details")
    if getfval('Sec80DMedicalExpenditureUsr',data) >0 and gettval('MedicalExpenditure',data) not in ('1','2','3'):
        error.append("Please select an option at dropdown of Part B Sec 80D (Medical Expenditure) Deduction under Chapter VIA in Income Details")

    if gettval('PreventiveHealthCheckUp',data) in ('1','2','3') and getfval('Sec80DPreventiveHealthCheckUpUsr',data)==0:
        error.append("Please enter the value for Part C Sec 80D (Preventive Health check-up) deduction under Chapter VIA in Income Details")
    if getfval('Sec80DPreventiveHealthCheckUpUsr',data) >0 and gettval('PreventiveHealthCheckUp',data) not in ('1','2','3'):
        error.append("Please select an option at dropdown of Part C Sec 80D (Preventive Health check-up) deduction under Chapter VIA in Income Details")

    if getfval('Section80D',data) > getfval('Sec80DHealthInsurancePremiumUsr',data) + getfval('Sec80DMedicalExpenditureUsr',data) + getfval('Sec80DPreventiveHealthCheckUpUsr',data):
        error.append("Deduction u/s 80D should not be more than sum of amount claimed at 'Health Insurance, Medical Expenditure and Preventive Health Check Up' under Chapter VIA in Income Details")

    if gettval('Section80DDUsrType',data) in ('1','2') and get_tot_gen('UsrDeductUndChapVIAType','Section80DD',mytree,ns)==0:
        error.append("Please enter the value for 80DD deduction under Chapter VIA in Income Details")
    if get_tot_gen('UsrDeductUndChapVIAType','Section80DD',mytree,ns) > 0 and gettval('Section80DDUsrType',data) not in ('1','2'):
        error.append("Please select an option at dropdown of Sec.80DD under Chapter VIA in Income Details")

    if gettval('Section80DDBUsrType',data) in ('1','2') and get_tot_gen('UsrDeductUndChapVIAType','Section80DDB',mytree,ns)==0:
        error.append("Please enter the value for 80DDB deduction under Chapter VIA in Income Details")
    if get_tot_gen('UsrDeductUndChapVIAType','Section80DDB',mytree,ns) > 0 and gettval('Section80DDBUsrType',data) not in ('1','2'):
        error.append("Please select an option at dropdown of Sec.80DDB under Chapter VIA in Income Details")

    if gettval('Section80UUsrType',data) in ('1','2') and get_tot_gen('UsrDeductUndChapVIAType','Section80U',mytree,ns)==0:
        error.append("Please enter the value for 80U deduction under Chapter VIA in Income Details")
    if get_tot_gen('UsrDeductUndChapVIAType','Section80U',mytree,ns) > 0 and gettval('Section80UUsrType',data) not in ('1','2'):
        error.append("Please select an option at dropdown of Sec.80U under Chapter VIA in Income Details")

    if len(gettval('GrossTotIncome',data))>14 or len(gettval('TotalChapVIADeductions',data))>14 or len(gettval('IntrstPay',data))>14 or len(gettval('TotTaxPlusIntrstPay',data))>14:
        error.append("Gross Total income, Deductions, Total Interest, Total Tax in Sheet Income Details should not be greater than 14 digits")

    tmp_root=mytree.find('.//ITRForm:ExemptIncAgriOthUs10',ns)
    for node1 in list(tmp_root): 
        if rn(node1.tag)=='ExemptIncAgriOthUs10Dtls':
            for node2 in list(node1):
                if rn(node2.tag)=='NatureDesc':
                    if snode.text is None :
                        nature_missing=True
                    elif snode.text=='OTH':
                        other_desc_found=True



    nature_missing=False 
    other=False 
    other_desc_found=False
    deduction = mytree.find('.//ITRForm:ExemptIncAgriOthUs10',ns):
    children=deduction.getchildren()
        for child in list(children):
            if child[0].tag=='NatureDesc':





                    error.append("'AllwncExemptUs10 table' selection is not in the defined list of values") 






    return error
