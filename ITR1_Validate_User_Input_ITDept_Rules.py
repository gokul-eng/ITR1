from ITR1_Constants_Common_Functions import *

def Validate_User_Input_ITDept_Rules(mytree,data,datausr,ns):
    lst_errors=[]
    log=[]
    try:
        #Rule 5 covered under generic checks
        # try:
        #     error_found=False
        #     ass_pan=gettval('PAN',data)
        #     ver_pan=gettval('AssesseeVerPAN',data)
        #     for deduction in mytree.findall('.//ITRForm:Schedule80G',ns):
        #         for snode in deduction.iter():
        #             if rn(snode.tag)=='DoneePAN':
        #                 if nz(snode.text)==ass_pan or nz(snode.text)==ver_pan:
        #                     error_found=True
        #     if error_found==True:
        #         lst_errors.append("5: Donee PAN mentioned in Schedule 80G cannot be same as the assesse PAN or the verification PAN")
        # except:
        #     lst_errors.append("Error in assessing Rule 5")

        #Rule 6 cannot be implelemted without access to PAN database

        #Rules 9 and 10 Covered under generic checks
        # try:
        #     tot_ded=get_tot_gen('TDSonOthThanSals','TotTDSOnAmtPaid',mytree,ns)
        #     tot_claimed=get_tot_gen('TDSonOthThanSals','ClaimOutOfTotTDSOnAmtPaid',mytree,ns)
        #     if tot_claimed > tot_ded:
        #         lst_errors.append("9: In Schedule TDS 2, TDS credit claimed is more than Tax deducted")
        # except:
        #     lst_errors.append("Error in assessing Rule 9")


        # try:
        #     tot_ded=get_tot_gen('ScheduleTDS3Dtls','TDSDeducted',mytree,ns)
        #     tot_claimed=get_tot_gen('ScheduleTDS3Dtls','TDSClaimed',mytree,ns)
        #     if tot_claimed > tot_ded:
        #         lst_errors.append("10: In Schedule TDS 3, TDS credit claimed is more than Tax deducted")
        # except:
        #     lst_errors.append("Error in assessing Rule 10")

        
        #rule 11 covered under generic checks
        # try:
        #     tot_ded=get_tot_gen('ScheduleTCS','TotalTCS',mytree,ns)
        #     tot_claimed=get_tot_gen('ScheduleTCS','AmtTCSClaimedThisYear',mytree,ns)
        #     if tot_claimed > tot_ded:
        #         lst_errors.append("11: TCS credit claimed is more than Tax collected")
        # except:
        #     lst_errors.append("Error in assessing Rule 11")

        try:
            lst_ifsccodes=[]
            for deduction in mytree.findall('.//ITRForm:BankAccountDtls',ns):
                for snode in deduction.iter():
                    if rn(snode.tag)=='IFSCCode':
                        lst_ifsccodes.append(nz(snode.text))
            
            nodefound=True
            myfile= open(FILE_NAME_WITH_PATH_IFSC_CODES)
            str_file=myfile.read()
            for ifsc in lst_ifsccodes:
                if ifsc not in str_file:
                    nodefound=False
                    break
            if nodefound==False:
                lst_errors.append("15: IFSC under 'Bank Details' is not matching with the RBI database")
        except:
            lst_errors.append("Error in assessing Rule 15")

        try:
            if ('TaxPaidlocalAuth' in data):
                if 'GrossRentReceived' in data:
                    if(float(data['GrossRentReceived'])==0 and  float(data['TaxPaidlocalAuth'])!=0):
                        lst_errors.append("21: Gross rent received/ receivable/ lettable value is zero or null and assessee is claiming municipal tax")
                else:
                    lst_errors.append("21: Gross rent received/ receivable/ lettable value is zero or null and assessee is claiming municipal tax")
        except:
            lst_errors.append("Error in assessing Rule 21")

        try:
            if (float(datausr['Section80DD'])!=0):
                if('Section80DDUsrType' in datausr):
                    if gettval('Section80DDUsrType',datausr) not in ("1","2"):
                        lst_errors.append("22: Nature of deduction u/s 80DD being claimed in the return is not specified")
                else:
                    lst_errors.append("22: Nature of deduction u/s 80DD being claimed in the return is not specified")
        except:
            lst_errors.append("Error in assessing Rule 22")

        try:
            if (float(datausr['Section80DDB'])!=0):
                if('Section80DDBUsrType' in datausr):
                    if gettval('Section80DDBUsrType',datausr) not in ("1","2") :
                        lst_errors.append("23: Nature of deduction u/s 80DDB being claimed in the return is not specified")
                else:
                    lst_errors.append("23: Nature of deduction u/s 80DDB being claimed in the return is not specified")
        except:
            lst_errors.append("Error in assessing Rule 23")

        try:
            if (float(datausr['Section80U'])!=0):
                if('Section80UUsrType' in datausr):
                    if gettval('Section80UUsrType',datausr) not in ("1","2") :
                        lst_errors.append("24: Nature of deduction u/s 80U being claimed in the return is not specified")
                else:
                    lst_errors.append("24: Nature of deduction u/s 80U being claimed in the return is not specified")
        except:
            lst_errors.append("Error in assessing Rule 24")

        try:
            age=calcAge(data['DOB'])
            if age<AGE_LIMIT_FOR_MINOR_TO_FILE_TAX:
                lst_errors.append("35: As per the provisions of Indian Contract Act, 1872 read with Income Tax Act, 1961, a minor cannot perform the functions in an individual capacity. Accordingly a return upload by minor is not allowed. Only legal guardian can perform the required functions")
        except:
            lst_errors.append("Error in assessing Rule 35")

        try:
            if 'EntertainmentAlw16ii' in data:
                if (float(data['EntertainmentAlw16ii'])>0):
                    if (data['EmployerCategory']=="GOV"):
                        if (float(data['EntertainmentAlw16ii'])>ENTERTAINEMENT_ALLOWANCE_16 or float(data['EntertainmentAlw16ii'])>float(data['Salary'])/5):
                            lst_errors.append("37: Entertainment allowance for Government employees u/s 16(ii) will be allowed to the extent of Rs.5000 or 1/5th of Salary as per section 17(1) whichever is lower")
                    else:
                        lst_errors.append("37: Entertainment allowance is allowed only for Government employees u/s 16(ii)")
        except:
            lst_errors.append("Error in assessing Rule 37")

        try:
            if 'ProfessionalTaxUs16iii' in data:
                if (getfval('ProfessionalTaxUs16iii',data)>PROFESSIONAL_TAX_16):
                    lst_errors.append("38: Professional tax u/s 16(iii) will be allowed only to the extent of Rs 5000")
        except:
            lst_errors.append("Error in assessing Rule 38")

        try:
            if('TypeOfHP' in data):
                if (data['TypeOfHP']=="L" or data['TypeOfHP']=="D") and getfval('GrossRentReceived',data)==0:
                    lst_errors.append("43: Gross rent received/ receivable/ lettable value' cannot be zero or null if 'type of property' is 'let out' or 'deemed let out'")
        except:
            lst_errors.append("Error in assessing Rule 43")

        try:
            if getfval('Sec80DHealthInsurancePremiumUsr',datausr)!=0:
                if 'HealthInsurancePremium' not in datausr:
                    lst_errors.append("46: Assessee is claiming deduction under section 80D for health insurance premium but eligible category description not provided")
        except:
            lst_errors.append("Error in assessing Rule 46")

        try:
            if getfval('Sec80DMedicalExpenditureUsr',datausr)!=0:
                if 'MedicalExpenditure' not in datausr:
                    lst_errors.append("47: Assessee is claiming deduction under section 80D for medical expenditure but eligible category description not provided")
        except:
            lst_errors.append("Error in assessing Rule 47")

        try:
            if getfval('Sec80DPreventiveHealthCheckUpUsr',datausr)!=0:
                if 'PreventiveHealthCheckUp' not in datausr:
                    lst_errors.append("48: Assessee is claiming deduction under section 80D for Preventive health check-up but eligible category description not provided.")
        except:
            lst_errors.append("Error in assessing Rule 48")

        try:
            if gettval('TypeOfHP',data)=="S":
                if getfval('InterestPayable',data)>INTEREST_ON_BORROWED_CAPITAL_HOUSE:
                    lst_errors.append("51: Interest on borrowed capital is more than Rs.200000 for 'Self-Occupied' house property")
        except:
            lst_errors.append("Error in assessing Rule 51")

        #rule 52 covered under generic checks
        # try:
        #     error_found=False
        #     for deduction in mytree.findall('.//ITRForm:TDSonOthThanSal',ns):
        #         for snode in deduction.iter():
        #             if rn(snode.tag)=='DeductedYr' and snode.text is None:
        #                 error_found=True
        #     for deduction in mytree.findall('.//ITRForm:TDS3Details',ns):
        #         for snode in deduction.iter():
        #             if rn(snode.tag)=='DeductedYr' and snode.text is None:
        #                 error_found=True
        #     for deduction in mytree.findall('.//ITRForm:TCS',ns):
        #         for snode in deduction.iter():
        #             if rn(snode.tag)=='DeductedYr' and snode.text is None:
        #                 error_found=True               
        #     if error_found==True:
        #         lst_errors.append("52: In Schedule TDS or TCS, TDS / TCS is claimed but year of tax deduction is not selected")
        # except:
        #     lst_errors.append("Error in assessing Rule 52")

        try:
            agricount=0
            agrival=0
            nodefound=False
            for deduction in mytree.findall('.//ITRForm:ExemptIncAgriOthUs10Dtls',ns):
                for snode in deduction.iter():
                    if rn(snode.tag)=='NatureDesc' and snode.text=='AGRI':
                        agricount=agricount+1
                        nodefound=True
                        continue
                    if rn(snode.tag)=='OthAmount' and nodefound==True:    
                        agrival=agrival+float(snode.text)
                        nodefound=False
            if agricount>1 or agrival>AGRICULTURE_MAX_VAL_EXEMPT:
                lst_errors.append("53: Agriculture Income shown as exempt cannot be more than Rs.5000/- and cannot be selected more than one time")
        except:
            lst_errors.append("Error in assessing Rule 53")

        try:
            divcount=0
            divval=0
            nodefound=False
            for deduction in mytree.findall('.//ITRForm:ExemptIncAgriOthUs10Dtls',ns):
                for snode in deduction.iter():
                    if rn(snode.tag)=='NatureDesc' and snode.text=='10(34)':
                        divcount=divcount+1
                        nodefound=True
                        continue
                    if rn(snode.tag)=='OthAmount' and nodefound==True:    
                        divval=divval+float(snode.text)
                        nodefound=False
            if divcount>1 or divval>DIVIDENT_MAX_VALUE_EXEMP_10_34:
                lst_errors.append("61: Dividend Income u/s 10(34) shown as exempt cannot be more than Rs.1000000/- and cannot be selected more than one time.")
        except:
            lst_errors.append("Error in assessing Rule 61")

        try:
            count=0
            nodefound=False
            for deduction in mytree.findall('.//ITRForm:OthersIncDtlsOthSrc',ns):
                for snode in deduction.iter():
                    if rn(snode.tag)=='OthSrcNatureDesc' and snode.text=='SAV':
                        count=count+1
                        nodefound=True
                        continue
            if count>1:
                lst_errors.append("62: 'Interest from savings account' drop-down cannot be selected more than one time under Income from other sources")
        except:
            lst_errors.append("Error in assessing Rule 62")

        try:
            nodefound=False
            count=0
            for deduction in mytree.findall('.//ITRForm:OthersIncDtlsOthSrc',ns):
                for snode in deduction.iter():
                    if rn(snode.tag)=='OthSrcNatureDesc' and snode.text=='IFD':
                        count=count+1
                        nodefound=True
                        continue
            if count>1:
                lst_errors.append("63: 'Interest from Deposits (Bank/Post Office/Cooperative Society)' drop-down cannot be selected more than one time under Income from other sources")
        except:
            lst_errors.append("Error in assessing Rule 63")

        try:
            if getfval('ExemptIncAgriOthUs10Total',data)>getfval('GrossSalary',data):
                lst_errors.append("67: Total of exempt allowance cannot be more than gross salary")
        except:
            lst_errors.append("Error in assessing Rule 67")

        try:
            tot= get_tot('AllwncExemptUs10Dtls','10(5)',mytree,ns)
            sal=getfval('Salary',data)
            if tot > sal:
                lst_errors.append("68: Sec 10(5)-Leave Travel concession/assistance received cannot be more than Salary as per section 17(1)")
        except:
            lst_errors.append("Error in assessing Rule 68")

        try:
            tot=get_tot('AllwncExemptUs10Dtls','10(6)',mytree,ns)
            if tot > getfval('GrossSalary',data):
                lst_errors.append("69: Sec 10(6)-Remuneration received as an official, by whatever name called, of an embassy, high commission etc. cannot be more than gross salary")
        except:
            lst_errors.append("Error in assessing Rule 69")

        try:
            tot=get_tot('AllwncExemptUs10Dtls','10(7)',mytree,ns)
            if tot > getfval('GrossSalary',data):
                lst_errors.append("70: Sec 10(7)-Allowances or perquisites paid or allowed as such outside India by the Government to a citizen of India for rendering service outside India cannot be more than gross salary")
        except:
            lst_errors.append("Error in assessing Rule 70")

        try:
            if(data['EmployerCategory']!="GOV"):
                tot=get_tot('AllwncExemptUs10Dtls','10(10)',mytree,ns)
                if tot > getfval('GrossSalary',data):
                    lst_errors.append("71: When Nature of employment is OTHER THAN 'Govt.' than Sec 10(10)-Death-cum-retirement gratuity received cannot exceed Rs. 20 lakhs")
        except:
            lst_errors.append("Error in assessing Rule 71")

        try:
            tot=get_tot('AllwncExemptUs10Dtls','10(10A)',mytree,ns)
            sal=getfval('Salary',data)
            if tot > sal:
                lst_errors.append("72: Sec 10(10A)-Commuted value of pension received cannot be more than Salary as per section 17(1)")
        except:
            lst_errors.append("Error in assessing Rule 72")

        try:
            tot=get_tot('AllwncExemptUs10Dtls','10(10AA)',mytree,ns)
            sal=getfval('Salary',data)
            if tot > sal:
                lst_errors.append("73: Sec 10(10AA)-Earned leave encashment on retirement cannot be more than Salary as per section 17(1)")
        except:
            lst_errors.append("Error in assessing Rule 73")

        try:
            tot=get_tot('AllwncExemptUs10Dtls','10(10B)(i)',mytree,ns)
            if tot > SECTION10B_FIRST_PROVISO:
                lst_errors.append("74: Claim of Sec 10(10B) First proviso - Compensation limit notified by CG in the Official Gazette cannot exceed Rs. 500000/-")
        except:
            lst_errors.append("Error in assessing Rule 74")

        try:
            tot=get_tot('AllwncExemptUs10Dtls','10(10C)',mytree,ns)
            if tot > SECTION10C_LIMIT:
                lst_errors.append("75: Claim of Sec 10(10C) - 'Amount received/receivable on voluntary retirement or termination of service' cannot exceed Rs. 5 lakhs")
        except:
            lst_errors.append("Error in assessing Rule 75")

        try:
            count1=0
            count2=0
            count3=0
            nodefound=False
            for deduction in mytree.findall('.//ITRForm:AllwncExemptUs10',ns):
                for snode in deduction.iter():
                    if rn(snode.tag)=='SalNatureDesc':
                        if nz(snode.text)=='10(10B)(i)':
                            count1+=1
                        if nz(snode.text)=='10(10B)(ii)':
                            count2+=1
                        if nz(snode.text)=='10(10C)':
                            count3+=1
            if count1 > 1: count1=1
            if count2 > 1: count2=1
            if count3 > 1: count3=1
            if count1 + count2 + count3 > 1:
                lst_errors.append("76: More than one drop down is selected from 'Section 10(10B) First proviso' or 'Section 10(10B) Second proviso' or 'Section 10(10C)'")
        except:
            lst_errors.append("Error in assessing Rule 76")

        try:
            tot=get_tot('AllwncExemptUs10Dtls','10(10CC)',mytree,ns)
            if tot > getfval('PerquisitesValue',data):
                lst_errors.append("77: Sec 10(10CC)-Tax paid by employer on non-monetary perquisite cannot exceed Value of perquisites as per section 17(2)")
        except:
            lst_errors.append("Error in assessing Rule 77")

        try:
            tot=get_tot('AllwncExemptUs10Dtls','10(13A)',mytree,ns)
            sal=getfval('Salary',data)
            if tot > sal/3:
                lst_errors.append("78: Sec 10(13A)-Allowance to meet expenditure incurred on house rent cannot exceeds 1/3rd of Salary as per section 17(1)")
        except:
            lst_errors.append("Error in assessing Rule 78")

        try:
            tot=get_tot('AllwncExemptUs10Dtls','10(14)(i)',mytree,ns)
            sal=getfval('Salary',data)
            if tot > sal:
                lst_errors.append("79: Sec 10(14)(i) ‘Prescribed Allowances or benefits (not in a nature of perquisite) specifically granted to meet expenses wholly, necessarily and exclusively and to the extent actually incurred, in performance of duties of office or employment’ cannot exceed Value of Salary as per section 17(1)")
        except:
            lst_errors.append("Error in assessing Rule 79")

        try:
            tot=get_tot('AllwncExemptUs10Dtls','10(14)(ii)',mytree,ns)
            sal=getfval('Salary',data)
            if tot > sal:
                lst_errors.append("80: Sec 10(14)(ii) ‘Prescribed Allowances or benefits granted to meet personal expenses in performance of duties of office or employment or to compensate him for increased cost of living’ cannot exceed Value of Salary as per section 17(1)")
        except:
            lst_errors.append("Error in assessing Rule 80")

        #Rules 93 to 96 covered under generic checks
        # try:
        #     ret=Check_80G_donations_present_err('Don100Percent',mytree,ns)
        #     if ret=="err":
        #         raise Exception
        #     if ret==True:
        #         lst_errors.append(r"93: In Schedule 80G in table (A) 'Donations entitled for 100% deduction without qualifying limit' donation in cash or donation in other mode is to be entered mandatory")
        # except:
        #     lst_errors.append("Error in assessing Rule 93")

        # try:
        #     ret=Check_80G_donations_present_err('Don50PercentNoApprReqd',mytree,ns)
        #     if ret=="err":
        #         raise Exception
        #     if ret==True:
        #         lst_errors.append(r"94: In Schedule 80G in table (B) 'Donations entitled for 50% deduction without qualifying limit' donation in cash or donation in other mode is to be entered mandatory")
        # except:
        #     lst_errors.append("Error in assessing Rule 94")

        # try:
        #     ret=Check_80G_donations_present_err('Don100PercentApprReqd',mytree,ns)
        #     if ret=="err":
        #         raise Exception
        #     if ret==True:
        #         lst_errors.append(r"95: In Schedule 80G in table (c) 'Donations entitled for 100% deduction Subject to Qualifying Limit' Donation in cash or Donation in other mode is to be entered mandatory")
        # except:
        #     lst_errors.append("Error in assessing Rule 95")

        # try:
        #     ret=Check_80G_donations_present_err('Don50PercentApprReqd',mytree,ns)
        #     if ret=="err":
        #         raise Exception
        #     if ret==True:
        #         lst_errors.append(r"96: In Schedule 80G in table (D) 'Donations entitled for 50% deduction Subject to Qualifying Limit' Donation in cash or Donation in other mode is to be entered mandatory")
        # except:
        #     lst_errors.append("Error in assessing Rule 96")

        #Rule 98 covered under generic checks
        # try:
        #     error_found=False
        #     for deduction in mytree.findall('.//ITRForm:Schedule80GGA',ns):
        #         for don in deduction.findall('.//ITRForm:DonationDtlsSciRsrchRuralDev',ns):
        #             for snode in don.iter():
        #                 if rn(snode.tag)=='DonationAmtCash':
        #                     val1=float(nz(snode.text))
        #                 if rn(snode.tag)=='DonationAmtOtherMode':
        #                     val2=float(nz(snode.text))
        #             if val1==0 and val2==0:
        #                 error_found=True
        #     if error_found==True:
        #         lst_errors.append("98: In 'Schedule 80GGA' 'Donation in cash' or 'Donation in other mode' is to be entered mandatory")
        # except:
        #     lst_errors.append("Error in assessing Rule 98")

        try:
            if getfval('TaxPaidlocalAuth',data)>0:
                if gettval('TypeOfHP',data)=="S":
                    lst_errors.append(r"104: In 'Schedule Income Details' Tax paid to local authorities shall not be allowed for Type of House Property as 'Self-Occupied'")
        except:
            lst_errors.append("Error in assessing Rule 104")

        try:
            if getfval('DeductionUs57iia',data)>0:
                pension_val=0
                for deduction in mytree.findall('.//ITRForm:OthersInc',ns):
                    for snode in deduction.iter():
                        if rn(snode.tag)=='OthSrcNatureDesc':
                            if snode.text=="FAP":
                                nodefound=True
                                continue
                        if rn(snode.tag)=='OthSrcOthAmount' and nodefound==True:    
                            pension_val=float(nz(snode.text))
                            nodefound=False
                    if pension_val<=0:
                        lst_errors.append(r"105: In 'Schedule Income Details' Deduction u/s 57(iia) shall be allowed only if 'Family pension' is selected from other sources dropdown")
        except:
            lst_errors.append("Error in assessing Rule 105")

        #Rule 109 covered under generic checks
        # try:
        #     error_found=False
        #     ass_pan=gettval('PAN',data)
        #     ver_pan=gettval('AssesseeVerPAN',data)
        #     for deduction in mytree.findall('.//ITRForm:Schedule80GGA',ns):
        #         for snode in deduction.iter():
        #             if rn(snode.tag)=='DoneePAN':
        #                 if nz(snode.text)==ass_pan or nz(snode.text)==ver_pan:
        #                     error_found=True
        #     if error_found==True:
        #         lst_errors.append("109: Donee PAN mentioned in Schedule 80GGA cannot be same as the assesse PAN or the verification PAN")
        # except:
        #     lst_errors.append("Error in assessing Rule 109")

        try:
            if getfval('DeductionUs57iia',data)>0:
                pension_val=0
                for deduction in mytree.findall('.//ITRForm:OthersInc',ns):
                    for snode in deduction.iter():
                        if rn(snode.tag)=='OthSrcNatureDesc':
                            if snode.text=="FAP":
                                nodefound=True
                                continue
                        if rn(snode.tag)=='OthSrcOthAmount' and nodefound==True:    
                            pension_val=pension_val+float(nz(snode.text))
                            nodefound=False
                if getfval('DeductionUs57iia',data)>min(pension_val/3,DEDUCTION_57_IIA_LIMIT):
                    lst_errors.append(r"110: Deduction u/s 57(iia) cannot be more than lower of 1/3rd of Family pension or Rs. 15,000")
        except:
            lst_errors.append("Error in assessing Rule 110")

        try:
            count=0
            nodefound=False
            for deduction in mytree.findall('.//ITRForm:ExemptIncAgriOthUs10',ns):
                for snode in deduction.iter():
                    if rn(snode.tag)=='NatureDesc' and snode.text=='10(10BC)':
                        count=count+1
                        nodefound=True
                        continue
            if count>1:
                lst_errors.append("113: 'Sec 10(10BC)-Any amount from the Central/State Govt./local authority by way of compensation on account of any disaster' drop-down cannot be selected more than one time under Exempt Income")
        except:
            lst_errors.append("Error in assessing Rule 113")

        try:
            count=0
            nodefound=False
            for deduction in mytree.findall('.//ITRForm:ExemptIncAgriOthUs10',ns):
                for snode in deduction.iter():
                    if rn(snode.tag)=='NatureDesc' and snode.text=='10(10D)':
                        count=count+1
                        nodefound=True
                        continue
            if count>1:
                lst_errors.append("114: 'Sec 10(10D)- Any sum received under a life insurance policy, including the sum allocated by way of bonus on such policy except sum as mentioned in sub-clause (a) to (d) of Sec.10(10D)' drop-down cannot be selected more than one time under Exempt Income")
        except:
            lst_errors.append("Error in assessing Rule 114")

        try:
            count=0
            nodefound=False
            for deduction in mytree.findall('.//ITRForm:ExemptIncAgriOthUs10',ns):
                for snode in deduction.iter():
                    if rn(snode.tag)=='NatureDesc' and snode.text=='10(11)':
                        count=count+1
                        nodefound=True
                        continue
            if count>1:
                lst_errors.append("115: 'Sec 10(11)-Statutory Provident Fund received' drop-down cannot be selected more than one time under Exempt Income")
        except:
            lst_errors.append("Error in assessing Rule 115")

        try:
            count=0
            nodefound=False
            for deduction in mytree.findall('.//ITRForm:ExemptIncAgriOthUs10',ns):
                for snode in deduction.iter():
                    if rn(snode.tag)=='NatureDesc' and snode.text=='10(12)':
                        count=count+1
                        nodefound=True
                        continue
            if count>1:
                lst_errors.append("116: 'Sec 10(12)-Recognized Provident Fund received' drop-down cannot be selected more than one time under Exempt Income")
        except:
            lst_errors.append("Error in assessing Rule 116")

        try:
            count=0
            nodefound=False
            for deduction in mytree.findall('.//ITRForm:ExemptIncAgriOthUs10',ns):
                for snode in deduction.iter():
                    if rn(snode.tag)=='NatureDesc' and snode.text=='10(13)':
                        count=count+1
                        nodefound=True
                        continue
            if count>1:
                lst_errors.append("117: 'Sec 10(13)-Approved superannuation fund received' drop-down cannot be selected more than one time under Exempt Income")
        except:
            lst_errors.append("Error in assessing Rule 117")

        try:
            count=0
            nodefound=False
            for deduction in mytree.findall('.//ITRForm:ExemptIncAgriOthUs10',ns):
                for snode in deduction.iter():
                    if rn(snode.tag)=='NatureDesc' and snode.text=='10(16)':
                        count=count+1
                        nodefound=True
                        continue
            if count>1:
                lst_errors.append("118: 'Sec 10(16)-Scholarships granted to meet the cost of education' drop-down cannot be selected more than one time under Exempt Income")
        except:
            lst_errors.append("Error in assessing Rule 118")

        try:
            count=0
            nodefound=False
            for deduction in mytree.findall('.//ITRForm:ExemptIncAgriOthUs10',ns):
                for snode in deduction.iter():
                    if rn(snode.tag)=='NatureDesc' and snode.text=='10(17)':
                        count=count+1
                        nodefound=True
                        continue
            if count>1:
                lst_errors.append("119: 'Sec 10(17)-Allowance MP/MLA/MLC' drop-down cannot be selected more than one time under Exempt Income")
        except:
            lst_errors.append("Error in assessing Rule 119")

        try:
            count=0
            nodefound=False
            for deduction in mytree.findall('.//ITRForm:ExemptIncAgriOthUs10',ns):
                for snode in deduction.iter():
                    if rn(snode.tag)=='NatureDesc' and snode.text=='10(18)':
                        count=count+1
                        nodefound=True
                        continue
            if count>1:
                lst_errors.append("120: 'Sec 10(18)-Pension received by winner of 'Param Vir Chakra' or 'Maha Vir Chakra' or 'Vir Chakra' or such other gallantry award' drop-down cannot be selected more than one time under Exempt Income")
        except:
            lst_errors.append("Error in assessing Rule 120")

        try:
            count=0
            nodefound=False
            for deduction in mytree.findall('.//ITRForm:ExemptIncAgriOthUs10',ns):
                for snode in deduction.iter():
                    if rn(snode.tag)=='NatureDesc' and snode.text=='DMDP':
                        count=count+1
                        nodefound=True
                        continue
            if count>1:
                lst_errors.append("121: 'Defense Medical Disability Pension' drop-down cannot be selected more than one time under Exempt Income")
        except:
            lst_errors.append("Error in assessing Rule 121")

        try:
            count=0
            nodefound=False
            for deduction in mytree.findall('.//ITRForm:ExemptIncAgriOthUs10',ns):
                for snode in deduction.iter():
                    if rn(snode.tag)=='NatureDesc' and snode.text=='10(19)':
                        count=count+1
                        nodefound=True
                        continue
            if count>1:
                lst_errors.append("122: 'Sec 10(19)-Armed Forces Family pension in case of death during operational duty' drop-down cannot be selected more than one time under Exempt Income")
        except:
            lst_errors.append("Error in assessing Rule 122")

        try:
            count=0
            nodefound=False
            for deduction in mytree.findall('.//ITRForm:ExemptIncAgriOthUs10',ns):
                for snode in deduction.iter():
                    if rn(snode.tag)=='NatureDesc' and snode.text=='10(26)':
                        count=count+1
                        nodefound=True
                        continue
            if count>1:
                lst_errors.append("123: 'Sec 10(26)-Any income as referred to in section 10(26)' drop-down cannot be selected more than one time under Exempt Income")
        except:
            lst_errors.append("Error in assessing Rule 123")

        try:
            count=0
            nodefound=False
            for deduction in mytree.findall('.//ITRForm:ExemptIncAgriOthUs10',ns):
                for snode in deduction.iter():
                    if rn(snode.tag)=='NatureDesc' and snode.text=='10(26AAA)':
                        count=count+1
                        nodefound=True
                        continue
            if count>1:
                lst_errors.append("124: 'Sec 10(26AAA)-Any income as referred to in section 10(26AAA)' drop-down cannot be selected more than one time under Exempt Income")
        except:
            lst_errors.append("Error in assessing Rule 124")

        try:
            count=0
            nodefound=False
            for deduction in mytree.findall('.//ITRForm:OthersInc',ns):
                for snode in deduction.iter():
                    if rn(snode.tag)=='OthSrcNatureDesc' and snode.text=='TAX':
                        count=count+1
                        nodefound=True
                        continue
            if count>1:
                lst_errors.append("125: 'Interest from Income Tax Refund' drop-down cannot be selected more than one time under Income from other sources")
        except:
            lst_errors.append("Error in assessing Rule 125")

        try:
            count=0
            nodefound=False
            for deduction in mytree.findall('.//ITRForm:OthersInc',ns):
                for snode in deduction.iter():
                    if rn(snode.tag)=='OthSrcNatureDesc' and snode.text=='FAP':
                        count=count+1
                        nodefound=True
                        continue
            if count>1:
                lst_errors.append("126: 'Family pension' drop-down cannot be selected more than one time under Income from other sources")
        except:
            lst_errors.append("Error in assessing Rule 126")

        try:
            if getfval('EntertainmentAlw16ii',data)!=0:
                if data['EmployerCategory']!='GOV':
                    lst_errors.append("129: Entertainment allowance u/s 16(ii) will not be allowed for other than 'Government' employees")
        except:
            lst_errors.append("Error in assessing Rule 129")

        #Rule 130 covered under generic checks
        # try:
        #     nodefound=False
        #     for deduction in mytree.findall('.//ITRForm:BankAccountDtls',ns):
        #         for snode in deduction.iter():
        #             if rn(snode.tag)=='UseForRefund' and nz(snode.text)=='true':
        #                     nodefound=True
        #     if nodefound==False:
        #         lst_errors.append("130: Please select at least one account in which you prefer to get your refund")
        # except:
        #     lst_errors.append("Error in assessing Rule 130")

        try:
            count=0
            nodefound=False
            for deduction in mytree.findall('.//ITRForm:ExemptIncAgriOthUs10',ns):
                for snode in deduction.iter():
                    if rn(snode.tag)=='NatureDesc' and snode.text=='10(17A)':
                        count=count+1
                        nodefound=True
                        continue
            if count>1:
                lst_errors.append("131: 'Sec 10(17A)-Award instituted by Government' drop-down cannot be selected more than one time under Exempt Income")
        except:
            lst_errors.append("Error in assessing Rule 131")

        return 'ok', lst_errors, log
    except Exception as e:
        lst_errors.append('Unknown error while validating user input - generic checks')
        log.append(e)
        return 'err', lst_errors, log        