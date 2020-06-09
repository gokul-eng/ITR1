import datetime as dt
import math

FILE_NAME_WITH_PATH_XML_FILE='C:\\Users\\gokul\\Google Drive\\Gokul Learning\\Indian IT Project\\Master Excel\\ITR1_ABBPK7259H.xml'
FILE_NAME_WITH_PATH_XSD_FILE='C:\\Users\\gokul\\Google Drive\\Gokul Learning\\Indian IT Project\\ITR-1_2019_Main.xsd'
FILE_NAME_WITH_PATH_IFSC_CODES="C:\\Users\\gokul\\Google Drive\\Gokul Learning\\Indian IT Project\\ifsc_codes.txt"
#FILE_NAME_WITH_PATH_XML_FILE = sys.argv[1]
#FILE_NAME_WITH_PATH_XSD_FILE = sys.argv[2]
#FILE_NAME_WITH_PATH_IFSC_CODES = sys.argv[2]


ASS_YEAR=2019
INCOME_LIMIT_ITR1=5000000
SUM_80C_80CCC_80CCD1_LIMIT=150000
#ASSESSMENT_YEAR_TO_CALC_AGE =2019 - same as ASS_YEAR
AGE_LIMIT_FOR_MINOR_TO_FILE_TAX=18
HOUSE_PROPERTY_STD_DEDUCTION_PERCENTAGE=0.3
MAX_INCOME_REBATE87A=350000
GROSS_INCOME_LIMIT_80CCG=1200000
DEPENDENT_WITH_DISABILITY_80DD=75000
SELF_OR_DEPENDENT_MEDICAL_TREATMENT_80DDB=40000
SELF_WITH_DISABILITY_80U=75000
STANDARD_DEDUCTION_16ia=40000
ENTERTAINEMENT_ALLOWANCE_16=5000
PROFESSIONAL_TAX_16=5000
INTEREST_ON_BORROWED_CAPITAL_HOUSE=200000
AGRICULTURE_MAX_VAL_EXEMPT=5000
HEALTH_INSURANCE_PREMIUM_1=25000
HEALTH_INSURANCE_PREMIUM_3=25000
HEALTH_INSURANCE_PREMIUM_5=50000
HEALTH_INSURANCE_PREMIUM_6=75000
HEALTH_MEDICAL_EXPENDITURE_2=50000
HEALTH_MEDICAL_EXPENDITURE_1=50000
PREVENTATIVE_HEALTH_CHECKUP_LIMIT_80D=5000
PENSIONERS_80CCD_MAX=0.2 #for 80CCD(1)
NON_PENSIONERS_80CCD_MAX=0.1  #for 80CCD(1)
DIVIDENT_MAX_VALUE_EXEMP_10_34=1000000
SECTION10B_FIRST_PROVISO=500000
SECTION10C_LIMIT=500000
DEDUCTION_57_IIA_LIMIT=15000
SECTION_80G_CASH_DONATION_LIMIT=2000
SECTION_80GGA_CASH_DONATION_LIMIT=10000
ADVANCE_TAX_PAID_LOWER_DATE="2018-04-01"
ADVANCE_TAX_PAID_UPPER_DATE="2019-03-31"
SELF_ASSESSMENT_TAX_PAID_CUT_OFF_DATE="2019-03-31"

#TAX CALC CONSTANTS
FIN_YEAR_START=dt.datetime.strptime("01/04/2018","%d/%m/%Y").date()
FIN_YEAR_END=dt.datetime.strptime("31/03/2019","%d/%m/%Y").date()
ASS_YEAR_START=dt.datetime.strptime("01/04/2020","%d/%m/%Y").date()
FILING_DUE_DATE_NORMAL=dt.datetime.strptime("31/08/2019","%d/%m/%Y").date() 
FILING_DUE_DATE_EXCEPTION=dt.datetime.strptime("31/03/2020","%d/%m/%Y").date() 
LATE_FILING_234F_MID_YEAR_CUTOFF=dt.datetime.strptime("31/12/2019","%d/%m/%Y").date()
CUTOFF_DATE_CALC_SELF_ASSESSMENT_NORMAL=dt.datetime.strptime("31/08/2019","%d/%m/%Y").date()
CUTOFF_DATE_CALC_SELF_ASSESSMENT_EXCEPTION=dt.datetime.strptime("31/03/2020","%d/%m/%Y").date()
SLAB0_234C_END=dt.datetime.strptime("15/06/2018","%d/%m/%Y").date()
SLAB1_234C_END=dt.datetime.strptime("15/09/2018","%d/%m/%Y").date()
SLAB2_234C_END=dt.datetime.strptime("15/12/2018","%d/%m/%Y").date()
SLAB3_234C_END=dt.datetime.strptime("15/03/2019","%d/%m/%Y").date()

MAX_LOSS_HOUSE_PROPERTY=200000
CHAP6A_80C_LIMIT=150000
CHAP6A_80CCC_LIMIT=150000
CHAP6A_80CCD1B_LIMIT=50000
GOV_PSU_OTH_80CCD2_PERCENT_LIMIT=0.1
ABSOLUTE_80CCG_VALUE_LIMIT=25000
HEALTH_INSURANCE_PREMIUM_2=50000
HEALTH_INSURANCE_PREMIUM_4=50000
HEALTH_INSURANCE_PREMIUM_7_NON_SENIOR=75000
HEALTH_INSURANCE_PREMIUM_7_SENIOR=100000
HEALTH_MEDICAL_EXPENDITURE_3=100000
DEPENDENT_WITH_SEVERE_DISABILITY_80DD=125000
SELF_OR_DEPENDENT_SENIOR_CITIZEN_MEDICAL_TREATMENT_80DDB=100000
INTEREST_ON_LOAN_HOUSE_LIMIT=50000
SECTION80G_QUALIFICATION_LIMIT_PERCENTAGE=0.1
SECTION_80GG_VALUE=60000
SECTION_80GG_PERCENTAGE_VALUE=0.25
SECTION_80TTA_LIMIT=10000
SECTION_80TTB_LIMIT=50000
SELF_WITH_SEVERE_DISABILITY_80U=125000
REBATE_UNDER_87A_LIMIT=350000
REBATE_UNDER_87A=2500
EDUCATION_HEALTH_CESS_PERCENT=0.04
INTEREST_234A_CALCULATION=0.01

def nz(str):
    #Return 0 if str does not exisit i.e. is 'None'
    if str is None:
        return 0
    else:
        return str

def RndMax0(mynum):
    #Return Round number if number > 0, else return 0
    if mynum<0:
        return(0)
    else:
        return(round(mynum))
    
def getfval(str,data):
    #get floating values from parsed xml file if found, else return 0
    try:
        if str in data:
            return(int(data[str]))
        else:
            return 0
    except:
        return "err"

def gettval(str,data):
    #get text values from parsed xml file if found, else return 'notfound'
    try:
        if str in data:
            return(data[str])
        else:
            return 'notfound'
    except:
        return "err"

def calcAge(str):
    #Calculate age as per assessment year
    try:
        d = dt.datetime.strptime(str,"%Y-%m-%d")
        d = d.date()
        age=ASS_YEAR-d.year
        if 4 < d.month:
            age = age - 1
        elif d.month == 4 and 1 < d.day:
            age = age - 1
        return age
    except:
        return "err"

def rn(str):
    #remove namespace
    if str is None:
        return ""
    else:
        str1=str[str.find('}')+1:]
        return str1

def get_tot(elem,str,mytree,ns):
    #Function to derive totals in section 10. Do not use for other sections.
    try:
        total=0
        nodefound=False
        for deduction in mytree.findall('.//ITRForm:'+elem,ns):
            for snode in deduction.iter():
                if rn(snode.tag).find('Nature')!=-1 and snode.text==str:
                    nodefound=True
                    continue
                if rn(snode.tag).find('OthAmount')!=-1 and nodefound==True:    
                    total=total+float(nz(snode.text))
                    nodefound=False
        return total
    except:
        return 'err'

def get_tot_gen(elem,str,mytree,ns):
    #Get total as specified by 'str' from parsed tree. This function can be used to sum columns in a table.
    #elem - top node which specifies the table, str - the column name
    try:
        total=0
        for deduction in mytree.findall('.//ITRForm:'+elem,ns):
            for snode in deduction.iter():
                if rn(snode.tag)==str:
                    total=total+float(nz(snode.text))
        return total
    except:
        return 'err'

# def Check_80G_donations_present_err(str_stem,mytree,ns):
#     try:
#         val1=0
#         val2=0
#         error_found=False
#         for deduction in mytree.findall('.//ITRForm:'+ str_stem,ns):
#             for don in deduction.findall('.//ITRForm:DoneeWithPan',ns):
#                 for snode in don.iter():
#                     if rn(snode.tag)=='DonationAmtCash':
#                         val1=float(nz(snode.text))
#                     if rn(snode.tag)=='DonationAmtOtherMode':
#                         val2=float(nz(snode.text))
#                 if val1==0 and val2==0:
#                     error_found=True
#         return error_found
#     except:
#         return "err"

def Check_80G_donations_total_err(str_stem,mytree,ns):
    #Specific function to check if (total donation = cash donation + donation in other mode) in Section 80G tables
    try:
        val1=0
        val2=0
        error_found=False
        for deduction in mytree.findall('.//ITRForm:'+ str_stem,ns):
            for don in deduction.findall('.//ITRForm:DoneeWithPan',ns):
                for snode in don.iter():
                    if rn(snode.tag)=='DonationAmtCash':
                        val1=float(nz(snode.text))
                    if rn(snode.tag)=='DonationAmtOtherMode':
                        val2=float(nz(snode.text))
                    if rn(snode.tag)=='DonationAmt':
                        if float(nz(snode.text))!=val1+val2:
                            error_found=True
        return error_found
    except:
        return "err"

def RoundDown(num,floor):
    #Round down. e.g. RoundDown(199,100)=100; RoundDown(550,100)=500
    return (num - (num%floor))

# def cround(n, floor): 
#     a = (n // floor) * floor
#     b = a + floor
#     return (b if n - a > b - n else a) 

#def roundup(x,val):
#    return int(math.ceil(x / val)) * 10

def round_nearest(n, nearest): 
    #Round to nearest 10 or 100 (as specificied by vairiable 'nearest')
    rem = n  % nearest
    if rem >= (5 * nearest/10):
        return round((n//nearest) * nearest + nearest)
    else:
        return round((n//nearest) * nearest)

def check_date(str):
    isValidDate = True
    try :
        dt.datetime.strptime(str,"%Y-%m-%d")
    except ValueError :
        isValidDate = False
    return isValidDate

def check_num_input(str,data):
    #Check that input is a non negative integer
    try:
        if str in data:
            int(data[str])
            if int(data[str]) < 0:
                return 'err'
    except:
        return "err"

def check_if_int(str1):
    #check if str is an integer
    try:
        s=str(str1)
        int(s)
        return True
    except:
        return False