import datetime as dt
from ITR1_Constants_Common_Functions import *


def Validate_Tax_Calc_Itdept_Rules(mytree,data,datausr,ns):
    lst_errors=[]   #The master list of errors. This list will be empty if no errors are found in the xml file
    log=[]
    try:
        #validations as per file "CBDT_e-Filing_ITR 1_Validation Rules for AY 2019-20"
        log.append('Output XML validation Rule 0')
        try:
            total_income=max(float(data['GrossTotIncome']),0)
            if total_income > INCOME_LIMIT_ITR1:
                lst_errors.append("0: ITR1 is for  individuals having Income from Salaries, One House Property, Other Sources(Interest  etc.)and having taxable income upto Rs.50 lakh. Please fill other ITR")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 0")

        log.append('Output XML validation Rule 1')
        try:
            if getfval('TotTaxPlusIntrstPay',data)!=0 and getfval('GrossTotIncome',data)==0:
                lst_errors.append("1: Tax computed but GTI (Gross Total Income) is nil or 0")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 1")

        log.append('Output XML validation Rule 2')
        try:
            if getfval('IncomeFromSal',data)==0 and getfval('GrossSalary',data)==0 and getfval('Salary',data)==0 and getfval('PerquisitesValue',data)==0 and getfval('ProfitsInSalary',data)==0 \
            and getfval('DeductionUs16',data)==0 and getfval('TotalIncomeOfHP',data)==0 and getfval('GrossRentReceived',data)==0 and getfval('TaxPaidlocalAuth',data)==0 \
            and getfval('AnnualValue',data)==0 and getfval('StandardDeduction',data)==0 and getfval('InterestPayable',data)==0 and getfval('IncomeOthSrc',data)==0 \
            and (getfval('TotalTaxesPaid',data)-getfval('TCS',data) >0) :
                lst_errors.append("2: No Income details or tax computation is provided in ITR but details regarding taxes paid is provided")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 2")

        log.append('Output XML validation Rule 3')
        try:
            if getfval('GrossTotIncome',data)!= getfval('IncomeFromSal',data) + getfval('TotalIncomeOfHP',data) + getfval('IncomeOthSrc',data):
                lst_errors.append("3: Gross Total Income is not matching with total of Incomes from Salary, House Property & Other Sources")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 3")

        log.append('Output XML validation Rule 4')
        try:
            adv_tax=0
            nodefound=False
            for deduction in mytree.findall('.//ITRForm:TaxPayments',ns):
                for snode in deduction.iter():
                    if rn(snode.tag)=='DateDep':
                        d=dt.datetime.strptime(nz(snode.text),"%Y-%m-%d").date()
                        if d>= dt.datetime.strptime(ADVANCE_TAX_PAID_LOWER_DATE,"%Y-%m-%d").date() and d<=dt.datetime.strptime(ADVANCE_TAX_PAID_UPPER_DATE,"%Y-%m-%d").date():
                            nodefound=True
                            continue
                    if rn(snode.tag)=='Amt' and nodefound==True :
                        nodefound=False
                        adv_tax+=float(nz(snode.text))
            self_claimed=0
            nodefound=False
            for deduction in mytree.findall('.//ITRForm:TaxPayments',ns):
                for snode in deduction.iter():
                    if rn(snode.tag)=='DateDep':
                        d=dt.datetime.strptime(nz(snode.text),"%Y-%m-%d")
                        if d>dt.datetime.strptime(SELF_ASSESSMENT_TAX_PAID_CUT_OFF_DATE,"%Y-%m-%d"):
                            nodefound=True
                            continue
                    if rn(snode.tag)=='Amt' and nodefound==True :
                        nodefound=False
                        self_claimed+=float(nz(snode.text))
            tcs_val=0
            #Note that TCS is used as both an element name as well as well as a collector
            #so getfval('TCS',data) will not work because the element value is overwritten by the collector that comes later in the tree
            for deduction in mytree.findall('.//ITRForm:TaxesPaid',ns):
                for snode in deduction.iter():
                    if rn(snode.tag)=='TCS':
                        tcs_val=float(nz(snode.text))
        
            if getfval('AdvanceTax',data)!=adv_tax or \
            getfval('TDS',data) != getfval('TotalTDSonSalaries',data) + getfval('TotalTDSonOthThanSals',data) + getfval('TotalTDS3Details',data) or \
            getfval('TotalSchTCS',data)!=tcs_val or \
            getfval('SelfAssessmentTax',data)!=self_claimed:
                lst_errors.append("4: 'Total Taxes Paid' shown in 'Part D' are inconsistent with the claims made in relevant schedules")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 4")

        log.append('Output XML validation Rule 7')
        try:
            tcs_val=0
            #Note that TCS is used as both an element name as well as well as a collector
            #so getfval('TCS',data) will not work because the element value is overwritten by the collector that comes later in the tree
            for deduction in mytree.findall('.//ITRForm:TaxesPaid',ns):
                for snode in deduction.iter():
                    if rn(snode.tag)=='TCS':
                        tcs_val=float(nz(snode.text))    
            if getfval('TotalTaxesPaid',data)!= getfval('AdvanceTax',data) + getfval('TDS',data) + tcs_val + getfval('SelfAssessmentTax',data):
                lst_errors.append("7: The total of Advance Tax, Self Asst Tax, TDS, TCS fields should match with the field 'Total Taxes Paid'")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 7")


        log.append('Output XML validation Rule 8')
        try:
            if getfval('Section80G',data)!=getfval('TotalEligibleDonationsUs80G',data):
                lst_errors.append("8: Deduction u/s 80G is claimed but no details provided in Schedule 80G")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 8")

        log.append('Output XML validation Rule 12')
        try:
            if getfval('TotalChapVIADeductions',data) > getfval('GrossTotIncome',data):
                lst_errors.append("12: Total of Chapter VI A claim shall not exceed the 'Gross Total Income'")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 12")

        log.append('Output XML validation Rule 13')
        try:
            if  getfval('RefundDue',data) != round_nearest(max(getfval('TotalTaxesPaid',data) - getfval('TotTaxPlusIntrstPay',data),0),10):
                lst_errors.append("13: Amount of refund claimed is inconsistent with the difference between 'Total Taxes Paid' and 'Total Tax and Interest payable'")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 13")

        log.append('Output XML validation Rule 14')
        try:
            if  getfval('BalTaxPayable',data) != round_nearest(max(getfval('TotTaxPlusIntrstPay',data) - getfval('TotalTaxesPaid',data),0),10):
                lst_errors.append("14: Amount of tax payable is inconsistent with the difference between 'Total Tax and Interest payable' and 'Total Taxes Paid'")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 14")


        log.append('Output XML validation Rule 16')
        try:
            if(float(data['TotalIncome'])>MAX_INCOME_REBATE87A and float(data['Rebate87A'])>0):
                lst_errors.append("16: Assessee's total income is greater than Rs 350000/-, hence assessee cannot claim Rebate u/s 87A. Please refer section 87A of Income tax act, 1961")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 16")

        log.append('Output XML validation Rule 17')
        try:
            if(float(data['GrossTotIncome'])>GROSS_INCOME_LIMIT_80CCG and float(data['Section80CCG'])>0):
                lst_errors.append("17: Assessee cannot claim deduction u/s 80CCG, If assessee's Gross total income is more than Rs. 1200000/-")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 17")

        log.append('Output XML validation Rule 18')
        try:
            tmpsum=0.0
            nodefound=False
            for deduction in mytree.findall('.//ITRForm:OthersIncDtlsOthSrc',ns):
                for snode in deduction.iter():
                    if rn(snode.tag)=='OthSrcNatureDesc':
                        if nz(snode.text)=="SAV":
                            nodefound=True
                            continue
                    if rn(snode.tag)=='OthSrcOthAmount' and nodefound==True:    
                        tmpsum=tmpsum+float(nz(snode.text))
                        nodefound=False
            if float(data['Section80TTA'])>tmpsum:
                lst_errors.append("18: Deduction u/s 80TTA cannot be more than income disclosed under 'Savings Account Interest income' in Other sources")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 18")

        log.append('Output XML validation Rule 19')
        try:
            if getfval('Section80C',data)+getfval('Section80CCC',data)+getfval('Section80CCDEmployeeOrSE',data)>SUM_80C_80CCC_80CCD1_LIMIT:
                lst_errors.append("19: Deduction u/s 80TTA cannot be more than income disclosed under 'Savings Account Interest income' in Other sources")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 19")

        log.append('Output XML validation Rule 20')
        try:
            if ('StandardDeduction' in data): 
                if('AnnualValue' in data):
                    if(int(data['StandardDeduction']) != round((RndMax0(float(data['AnnualValue']))*HOUSE_PROPERTY_STD_DEDUCTION_PERCENTAGE),0)):
                        lst_errors.append(r"20: Deduction on annual value on House property should be equal to 30% of Annual value")
                else:
                    lst_errors.append(r"20: Deduction on annual value on House property should be equal to 30% of Annual value")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 20")


        log.append('Output XML validation Rule 25')
        try:
            if (round_nearest(max(float(data['GrossTotIncome'])-float(data['TotalChapVIADeductions']),0),10) != int(data['TotalIncome'])):
                lst_errors.append("25: Total income should be the difference between 'Gross total income' and 'Total deductions")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 25")

        log.append('Output XML validation Rule 26')
        try:
            tmpsum=0.0
            for deduction in mytree.findall('.//ITRForm:DeductUndChapVIA',ns):
                for snode in deduction.iter():
                    if (rn(snode.tag)!='DeductUndChapVIA' and rn(snode.tag)!='TotalChapVIADeductions'):
                        tmpsum=tmpsum+float(snode.text)
            if min(round(tmpsum),int(data['GrossTotIncome'])) != int(data['TotalChapVIADeductions']):
                lst_errors.append("26: Total of chapter VI-A deductions is not consistent with the breakup of individual deductions but restricted to GTI")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 26")

        log.append('Output XML validation Rule 27')
        try:
            if(float(data['Section80CCDEmployer'])>0):
                if(data['EmployerCategory']=="PE"):
                    lst_errors.append("27: Deduction u/s 80CCD(2) cannot be claimed by pensioners")
                netsal=getfval('NetSalary',data)
                perq=getfval('PerquisitesValue',data)
                if(float(data['Section80CCDEmployer']) > 0.1*max(netsal-perq,0)):
                    lst_errors.append(r"27: Deduction u/s 80CCD(2) should not be more than 10% of salary")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 27")

        log.append('Output XML validation Rule 28')
        try:
            if float(data['Section80DD'])>0:
                if ('Section80DDUsrType' in datausr):
                    if (datausr['Section80DDUsrType']=="1"):
                        if(float(data['Section80DD'])>DEPENDENT_WITH_DISABILITY_80DD):
                            lst_errors.append("28: Maximum amount that can be claimed for category Dependent with disability u/s 80DD is 75000")
                else:
                    lst_errors.append("28: Maximum amount that can be claimed for category 'Dependent with disability' u/s 80DD is 75000. Dependent status missing")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 28")

        log.append('Output XML validation Rule 29')
        try:
            if float(data['Section80DDB'])>0:
                if ('Section80DDBUsrType' in datausr):
                    if (datausr['Section80DDBUsrType']=="1"):
                        if(float(data['Section80DDB'])>SELF_OR_DEPENDENT_MEDICAL_TREATMENT_80DDB):
                            lst_errors.append("29: Maximum amount that can be claimed for category Self or Dependent u/s 80DDB is 40000")
                else:
                    lst_errors.append("29: Maximum amount that can be claimed for category Self or Dependent u/s 80DDB is 40000. Medical treatment category missing")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 29")

        log.append('Output XML validation Rule 30')
        try:
            if float(data['Section80U'])>0:
                if ('Section80UUsrType' in datausr):
                    if (datausr['Section80UUsrType']=="1"):
                        if(float(data['Section80U'])>SELF_WITH_DISABILITY_80U):
                            lst_errors.append("30: Maximum amount that can be claimed for category Self with disability u/s 80U is 75000")
                else:
                    lst_errors.append("30: Maximum amount that can be claimed for category Self with disability u/s 80U is 75000. Disability category missing")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 30")

        log.append('Output XML validation Rule 31')
        try:
            if int(data['TaxPayableOnRebate'])!=RndMax0(float(data['TotalTaxPayable'])-float(data['Rebate87A'])):
                lst_errors.append("31: The amount at 'Tax after Rebate' should be consistent with the amount of Tax Payable on Total Income as reduced by Rebate u/s 87A")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 31")

        log.append('Output XML validation Rule 32')
        try:
            if (int(data['GrossTaxLiability'])!=round(float(data['TaxPayableOnRebate'])+float(data['EducationCess']),0)):
                lst_errors.append("32: The amount at 'Total tax and Cess' should be consistent with the sum of 'Tax after Rebate' and 'Heath & Education Cess'")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 32")

        log.append('Output XML validation Rule 33')
        try:
            if (int(data['TotTaxPlusIntrstPay'])!=RndMax0(float(data['TotalIntrstPay'])+RndMax0(float(data['GrossTaxLiability'])-float(data['Section89'])))):
                lst_errors.append("33: 'Total Tax, Fees & Interest' is different with the sum of 'Total Tax & Cess, Interest u/s 234A, 234B, 234C and fee u/s 234F as reduced by Relief u/s 89'")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 33")

        #This check is invalid, because during calculation of total 80D value, the 5000 cutoff limit is implemented
        #For other sections, when user enters a value more than the specified limit, the value is automatically truncated to the limit. 
        #The same happens here as well, so there is no need to warn the user only for this check
        # try:
        #     if 'Sec80DPreventiveHealthCheckUpUsr' in data:
        #         if (float(data['Sec80DPreventiveHealthCheckUpUsr'])>PREVENTATIVE_HEALTH_CHECKUP_LIMIT_80D):
        #             lst_errors.append("34: Deduction u/s 80D-Preventive Health Check cannot exceed Rs 5000/-")
        # except Exception as e:
            log.append(e)
        #     lst_errors.append("Error in assessing Rule 34")


        log.append('Output XML validation Rule 36')
        try:
            if getfval('Section80TTA',data)!=0:
                age=calcAge(data['DOB'])
                if age>=60:
                    lst_errors.append("36: Deduction u/s 80TTA claimed by Senior Citizen taxpayer")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 36")


        log.append('Output XML validation Rule 39')
        try:
            if (float(data['GrossTotIncome'])!=(float(data['IncomeOthSrc'])+float(data['TotalIncomeOfHP'])+float(data['IncomeFromSal']))):
                lst_errors.append("39: In Schedule Gross total Income, Gross salary should be equal to sum of individual fields")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 39")

        log.append('Output XML validation Rule 40')
        try:
            if(getfval('NetSalary',data)!=max(getfval('GrossSalary',data)-getfval('TotalAllwncExemptUs10',data),0)):
                lst_errors.append("40: In Schedule Gross total Income, 'Net Salary' should be difference of 'Gross salary' and 'Allowances to the extent exempt u/s 10'")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 40")

        log.append('Output XML validation Rule 41')
        try:
            if getfval('DeductionUs16',data)!= getfval('DeductionUs16ia',data) + getfval('EntertainmentAlw16ii',data) + getfval('ProfessionalTaxUs16iii',data):
                lst_errors.append("41: In Schedule Gross total Income, 'Deductions u/s 16' should be sum of of individual fields")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 41")

        log.append('Output XML validation Rule 42')
        try:
            if(getfval('IncomeFromSal',data)!=max(getfval('NetSalary',data)-getfval('DeductionUs16',data),0)):
                lst_errors.append("42: In Schedule Gross total Income, 'Income chargeable under Salaries' should be difference of 'Net salary' and 'Deductions u/s 16'")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 42")


        log.append('Output XML validation Rule 44')
        try:
            if getfval('AnnualValue',data)!= max(getfval('GrossRentReceived',data)-getfval('TaxPaidlocalAuth',data),0):
                lst_errors.append("44: In Schedule Gross total Income, 'Annual Value' should be difference of 'Gross rent received/ receivable/ lettable value during the year' and 'Tax paid to local authorities'")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 44")

        log.append('Output XML validation Rule 45')
        try:
            if(getfval('TotalIncomeOfHP',data)!=max(-200000,getfval('AnnualValue',data)-getfval('StandardDeduction',data)-getfval('InterestPayable',data)+getfval('ArrearsUnrealizedRentRcvd',data))):
                lst_errors.append("45: In Schedule Gross total Income, 'Income chargeable under the head House Property' is not equal to value of B2iii-B2iv-B2v+B2vi")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 45")


        log.append('Output XML validation Rule 49')
        try:
            if getfval('Section80TTB',data)!=0:
                age=calcAge(data['DOB'])
                if age<60:
                    lst_errors.append("49: Assessee not being a senior citizen and claiming deduction under section 80TTB")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 49")

        log.append('Output XML validation Rule 50')
        try:
            if getfval('Section80TTB',data)>0:
                tmpsum=0.0
                nodefound=False
                for deduction in mytree.findall('.//ITRForm:OthersIncDtlsOthSrc',ns):
                    for snode in deduction.iter():
                        if rn(snode.tag)=='OthSrcNatureDesc':
                            if snode.text.find("SAV")!=-1 or snode.text.find("IFD")!=-1:
                                nodefound=True
                                continue
                        if rn(snode.tag)=='OthSrcOthAmount' and nodefound==True:    
                            tmpsum=tmpsum+float(snode.text)
                            nodefound=False
                if float(data['Section80TTB'])>tmpsum:
                    lst_errors.append("50: Deduction under section 80TTB is more than interest income at 'Savings Account & Deposit(Bank/Cooperative/Post)' shown under 'Income from other source'")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 50")



        log.append('Output XML validation Rule 54')
        try:
            don=0
            elig=0
            test_failed=False
            for deduction in mytree.findall('.//ITRForm:Don100Percent',ns):
                for snode in deduction.iter():
                    if rn(snode.tag)=="DonationAmt":
                        don=float(snode.text)
                    if rn(snode.tag)=='EligibleDonationAmt' :
                        elig=float(snode.text)
                        if elig>don:
                            test_failed=True
            for deduction in mytree.findall('.//ITRForm:Don50PercentNoApprReqd',ns):
                for snode in deduction.iter():
                    if rn(snode.tag)=='DonationAmt':
                        don=float(snode.text)
                    if rn(snode.tag)=='EligibleDonationAmt':
                        elig=float(snode.text)
                        if elig>don:
                            test_failed=True
            for deduction in mytree.findall('.//ITRForm:Don100PercentApprReqd',ns):
                for snode in deduction.iter():
                    if rn(snode.tag)=='DonationAmt':
                        don=float(snode.text)
                    if rn(snode.tag)=='EligibleDonationAmt':
                        elig=float(snode.text)
                        if elig>don:
                            test_failed=True
            for deduction in mytree.findall('.//ITRForm:Don50PercentApprReqd',ns):
                for snode in deduction.iter():
                    if rn(snode.tag)=='DonationAmt':
                        don=float(snode.text)
                    if rn(snode.tag)=='EligibleDonationAmt':
                        elig=float(snode.text)
                        if elig>don:
                            test_failed=True
            if test_failed==True:
                lst_errors.append("54: In Schedule 80G, 'Eligible amount of Donations' cannot be more than the 'Total Donations'.")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 54")

        log.append('Output XML validation Rule 55')
        try:
            if getfval('TotalEligibleDonationsUs80G',data)!=getfval('Section80G',data):
                lst_errors.append("55: In Schedule VIA, deduction claimed u/s 80G cannot be more than the eligible amount of donation mentioned in Schedule 80G")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 55")

        #checks 56, 57 and 58 are not valid
        #80D calculation takes into account all limits automatically
        # try:
        #     premium=getfval('Sec80DHealthInsurancePremiumUsr',data)
        #     preventative=getfval('Sec80DPreventiveHealthCheckUpUsr',data)
        #     if premium !=0:
        #         if 'HealthInsurancePremium' in data:
        #             if (data['HealthInsurancePremium']=="1" and premium>HEALTH_INSURANCE_PREMIUM_1):
        #                 lst_errors.append("56: Deduction u/s 80D for Self and family for health insurance & for Self and family for preventive health checkup cannot be more than Rs 25000/-")
        #         else:
        #             lst_errors.append("56: HealthInsurancePremium not defined, unable to evaluate rule")
        # except Exception as e:
        #    log.append(e)
        #     lst_errors.append("Error in assessing Rule 56")

        # try:
        #     premium=getfval('Sec80DHealthInsurancePremiumUsr',data)
        #     preventative=getfval('Sec80DPreventiveHealthCheckUpUsr',data)
        #     if premium !=0:
        #         if 'HealthInsurancePremium' in data:
        #             if (data['HealthInsurancePremium']=="3" and premium>HEALTH_INSURANCE_PREMIUM_3):
        #                 lst_errors.append("57: Deduction u/s 80D for Parents for health insurance & for parents for preventive health checkup cannot be more than Rs 25000/-")
        #         else:
        #             lst_errors.append("57: HealthInsurancePremium not defined, unable to evaluate rule")
        # except Exception as e:
        #    log.append(e)
        #     lst_errors.append("Error in assessing Rule 57")

        # try:
        #     premium=getfval('Sec80DHealthInsurancePremiumUsr',data)
        #     preventative=getfval('Sec80DPreventiveHealthCheckUpUsr',data)
        #     if premium !=0:
        #         if 'HealthInsurancePremium' in data:
        #             if (data['HealthInsurancePremium']=="5" and premium>HEALTH_INSURANCE_PREMIUM_5):
        #                 lst_errors.append("58: Deduction u/s 80D for self and family including parents for health insurance & for self and family including parents for preventive health checkup cannot be more than Rs 50000/-")
        #         else:
        #             lst_errors.append("58: HealthInsurancePremium not defined, unable to evaluate rule")
        # except Exception as e:
        #    log.append(e)
        #     lst_errors.append("Error in assessing Rule 58")

        log.append('Output XML validation Rule 59')
        try:
            if data['EmployerCategory']=="PE":
                if getfval('Section80CCDEmployeeOrSE',data)>PENSIONERS_80CCD_MAX*getfval('GrossTotIncome',data):
                    lst_errors.append(r"59: For employer category 'Pensioners', Deduction u/s 80CCD (1) should not be more than 20% of Gross total Income.")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 59")

        log.append('Output XML validation Rule 60')
        try:
            if data['EmployerCategory']!="PE":
                sal=getfval('NetSalary',data)-getfval('PerquisitesValue',data)
                if getfval('Section80CCDEmployeeOrSE',data)>NON_PENSIONERS_80CCD_MAX*sal:
                    lst_errors.append(r"60: Maximum amount that can be claimed u/s 80CCD(1) for 'employees' other than 'pensioners' should not be more than 10% of Salary")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 60")


        #checks 64, 65 and 66 are not valid
        #80D calculation takes into account all limits automatically
        # try:
        #     premium=getfval('Sec80DHealthInsurancePremiumUsr',data)
        #     if premium !=0:
        #         if 'HealthInsurancePremium' in data:
        #             if (data['HealthInsurancePremium']=="6" and premium>HEALTH_INSURANCE_PREMIUM_6):
        #                 lst_errors.append("64: Deduction u/s 80D for Self and Family including Senior Citizen Parents for health insurance & preventive health checkup cannot be more than Rs 75000/-")
        #         else:
        #             lst_errors.append("64: HealthInsurancePremium not defined, unable to evaluate rule")
        # except Exception as e:
        #    log.append(e)
        #     lst_errors.append("Error in assessing Rule 64")

        # try:
        #     exp=getfval('Sec80DMedicalExpenditureUsr',data)
        #     if exp !=0:
        #         if 'MedicalExpenditure' in data:
        #             if (data['MedicalExpenditure']=="2" and exp>HEALTH_MEDICAL_EXPENDITURE_2):
        #                 lst_errors.append("65: Deduction u/s 80D for parents senior citizen medical expenditure cannot be more than Rs 50000/-")
        #         else:
        #             lst_errors.append("65: MedicalExpenditure not defined, unable to evaluate rule")
        # except Exception as e:
        #    log.append(e)
        #     lst_errors.append("Error in assessing Rule 65")

        # try:
        #     exp=getfval('Sec80DMedicalExpenditureUsr',data)
        #     if exp !=0:
        #         if 'MedicalExpenditure' in data:
        #             if (data['MedicalExpenditure']=="1" and exp>HEALTH_MEDICAL_EXPENDITURE_1):

        #                 lst_errors.append("66: Deduction u/s 80D for self and family (Senior Citizen)- medical expenditure cannot be more than Rs 50000/-")
        #         else:
        #             lst_errors.append("66: MedicalExpenditure not defined, unable to evaluate rule")
        # except Exception as e:
        #    log.append(e)
        #     lst_errors.append("Error in assessing Rule 66")


        log.append('Output XML validation Rule 81')
        try:
            tot=getfval('IntrstPayUs234A',data)+getfval('IntrstPayUs234B',data)+getfval('IntrstPayUs234C',data)+getfval('LateFilingFee234F',data)
            if tot != getfval('TotalIntrstPay',data):
                lst_errors.append("81: In 'Schedule Income Details' Total Interest, Fee Payable should be equal to the sum of Interest u/s 234 A+ Interest u/s 234 B+ Interest u/s 234 C+ Fee u/s 234F")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 81")

        log.append('Output XML validation Rule 82')
        try:
            tot=getfval('NetTaxLiability',data)+getfval('TotalIntrstPay',data)
            if tot != getfval('TotTaxPlusIntrstPay',data):
                lst_errors.append("82: In 'Schedule Income Details' Total Tax, Fee & Interest should be equal to sum of Balance Tax after Relief +Total Interest, Fee Payable")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 82")

        log.append('Output XML validation Rule 83')
        try:
            tot=get_tot_gen('TDSonSalaries','TotalTDSSal',mytree,ns)
            if tot != getfval('TotalTDSonSalaries',data):
                lst_errors.append("83: In Schedule TDS1 total of col 4 'Total Tax deducted' should be equal to sum of individual values of col 4")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 83")

        log.append('Output XML validation Rule 84')
        try:
            tot=get_tot_gen('TDSonOthThanSals','ClaimOutOfTotTDSOnAmtPaid',mytree,ns)
            if tot != getfval('TotalTDSonOthThanSals',data):
                lst_errors.append("84: In Schedule TDS2 total of col 6 'TDS Credit out of(5) claimed this year should be equal to sum of individual values of col 5")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 84")

        log.append('Output XML validation Rule 85')
        try:
            tot=get_tot_gen('TDS3Details','TDSClaimed',mytree,ns)
            if tot != getfval('TotalTDS3Details',data):
                lst_errors.append("85: In Schedule TDS3 total of col 6' 'TDS Credit out of(5) claimed this year should be equal to sum of individual values of col 5")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 85")

        log.append('Output XML validation Rule 86')
        try:
            tot=get_tot_gen('TaxPayment','Amt',mytree,ns)
            if tot != getfval('TotalTaxPayments',data):
                lst_errors.append("86: In Schedule IT total of col 4 Tax Paid should be equal to sum of individual values")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 86")

        log.append('Output XML validation Rule 87')
        try:
            tot=get_tot_gen('AllwncExemptUs10','SalOthAmount',mytree,ns)
            if tot != getfval('TotalAllwncExemptUs10',data):
                lst_errors.append("87: In 'Schedule Income Details' allowance to extent exempt u/s 10 should be equal to sum of individual values entered")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 87")

        log.append('Output XML validation Rule 88')
        try:
            tot=get_tot_gen('OthersInc','OthSrcOthAmount',mytree,ns)
            if max(tot-getfval('DeductionUs57iia',data),0) != getfval('IncomeOthSrc',data):
                lst_errors.append("88: In 'Schedule Income Details' Income from other sources should be equal to amount entered in individual col. Of income from other sources")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 88")

        log.append('Output XML validation Rule 89')
        try:
            tot=get_tot_gen('ExemptIncAgriOthUs10','OthAmount',mytree,ns)
            if tot != getfval('ExemptIncAgriOthUs10Total',data):
                lst_errors.append("89: In 'Schedule Income Details Exempt income should be equal to sum of amount entered in individual col. Of exempt income")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 89")

        log.append('Output XML validation Rule 90')
        try:
            tot=get_tot_gen('TCS','AmtTCSClaimedThisYear',mytree,ns)
            if tot != getfval('TotalSchTCS',data):
                lst_errors.append("90: In Schedule TCS total of col 6 TCS credit out of (5) being claimed this year should be equal to sum of individual values")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 90")

        log.append('Output XML validation Rule 91')
        try:
            tot=getfval('TotalTDSonSalaries',data)+getfval('TotalTDSonOthThanSals',data)+getfval('TotalTDS3Details',data)
            if tot != getfval('TDS',data):
                lst_errors.append("91: In Schedule Taxes Paid and Verification Total TDS Claimed should be equal to the sum of total TDS claimed in TDS 1, 2 & 3")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 91")

        log.append('Output XML validation Rule 92')
        try:
            #Note that TCS is used as both an element name as well as well as a collector
            #so getfval('TCS',data) will not work because the element value is overwritten by the collector that comes later in the tree
            tcs=get_tot_gen('TaxPaid','TCS',mytree,ns)
            if getfval('TotalSchTCS',data) != tcs:
                lst_errors.append("92: In 'Schedule Taxes Paid and Verification' Total TCS Claimed should be equal to the sum of total TCS claimed in TCS schedule")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 92")




        log.append('Output XML validation Rule 97')
        try:
            cats=['Don100Percent','Don50PercentNoApprReqd','Don100PercentApprReqd','Don50PercentApprReqd']
            t_amt_cash=0
            t_amt_oth=0
            t_amt_total=0
            t_amt_eleg=0
            error_found=False
            for cat in cats:
                ret=get_tot_gen(cat,'DonationAmtCash',mytree,ns)
                if ret=="err":
                    raise Exception
                else:
                    amt_cash=ret
                ret=get_tot_gen(cat,'DonationAmtOtherMode',mytree,ns)
                if ret=="err":
                    raise Exception
                else:
                    amt_oth=ret
                ret=get_tot_gen(cat,'DonationAmt',mytree,ns)
                if ret=="err":
                    raise Exception
                else:
                    amt_total=ret
                ret=get_tot_gen(cat,'EligibleDonationAmt',mytree,ns)
                if ret=="err":
                    raise Exception
                else:
                    amt_eleg=ret
                t_amt_cash+=amt_cash
                t_amt_oth+=amt_oth
                t_amt_total+=amt_total
                t_amt_eleg+=amt_eleg
                if cat=='Don100Percent':
                    if amt_cash!=getfval('TotDon100PercentCash',data) or amt_oth!=getfval('TotDon100PercentOtherMode',data) or amt_total!=getfval('TotDon100Percent',data) or amt_eleg!=getfval('TotEligibleDon100Percent',data):
                        error_found=True
                if cat=='Don50PercentNoApprReqd':
                    if amt_cash!=getfval('TotDon50PercentNoApprReqdCash',data) or amt_oth!=getfval('TotDon50PercentNoApprReqdOtherMode',data) or amt_total!=getfval('TotDon50PercentNoApprReqd',data) or amt_eleg!=getfval('TotEligibleDon50Percent',data):
                        error_found=True
                if cat=='Don100PercentApprReqd':
                    if amt_cash!=getfval('TotDon100PercentApprReqdCash',data) or amt_oth!=getfval('TotDon100PercentApprReqdOtherMode',data) or amt_total!=getfval('TotDon100PercentApprReqd',data) or amt_eleg!=getfval('TotEligibleDon100PercentApprReqd',data):
                        error_found=True
                if cat=='Don50PercentApprReqd':
                    if amt_cash!=getfval('TotDon50PercentApprReqdCash',data) or amt_oth!=getfval('TotDon50PercentApprReqdOtherMode',data) or amt_total!=getfval('TotDon50PercentApprReqd',data) or amt_eleg!=getfval('TotEligibleDon50PercentApprReqd',data):
                        error_found=True
            if  error_found==True or t_amt_cash!=getfval('TotalDonationsUs80GCash',data) or t_amt_oth!=getfval('TotalDonationsUs80GOtherMode',data) or t_amt_total!=getfval('TotalDonationsUs80G',data) or t_amt_eleg!=getfval('TotalEligibleDonationsUs80G',data):
                lst_errors.append(r"97: In Schedule 80G in table (E) Donations should be equal to the sum of (Donations entitled for 100% deduction without qualifying limit + Donations entitled for 50% deduction without qualifying limit + Donations entitled for 100% deduction subject to qualifying limit + Donations entitled for 100% deduction subject to qualifying limit)")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 97")




        log.append('Output XML validation Rule 99')
        try:
            ret=Check_80G_donations_total_err('Don100Percent',mytree,ns)
            if ret=="err":
                raise Exception
            if ret==True:
                lst_errors.append(r"99: 'Total Donation' should be equal to sum of 'Donation in cash' AND 'Donation in other mode' in table (80G) (A) 'Donations entitled for 100% deduction without qualifying limit'")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 99")

        log.append('Output XML validation Rule 100')
        try:
            ret=Check_80G_donations_total_err('Don50PercentNoApprReqd',mytree,ns)
            if ret=="err":
                raise Exception
            if ret==True:
                lst_errors.append(r"100: 'Total Donation' should be equal to sum of 'Donation in cash' AND 'Donation in other mode' in table (80G) (B) 'Donations entitled for 50% deduction without qualifying limit'")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 100")

        log.append('Output XML validation Rule 101')
        try:
            ret=Check_80G_donations_total_err('Don100PercentApprReqd',mytree,ns)
            if ret=="err":
                raise Exception
            if ret==True:
                lst_errors.append(r"101: 'Total Donation' should be equal to sum of 'Donation in cash' AND 'Donation in other mode' in table (80G) (C) 'Donations entitled for 100% deduction subject to qualifying limit'")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 101")

        log.append('Output XML validation Rule 102')
        try:
            ret=Check_80G_donations_total_err('Don50PercentApprReqd',mytree,ns)
            if ret=="err":
                raise Exception
            if ret==True:
                lst_errors.append(r"102: 'Total Donation' should be equal to sum of 'Donation in cash' AND 'Donation in other mode' in table (80G) (D) 'Donations entitled for 50% deduction subject to qualifying limit'")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 102")

        log.append('Output XML validation Rule 103')
        try:
            error_found=False
            for deduction in mytree.findall('.//ITRForm:Schedule80GGA',ns):
                for don in deduction.findall('.//ITRForm:DonationDtlsSciRsrchRuralDev',ns):
                    for snode in don.iter():
                        if rn(snode.tag)=='DonationAmtCash':
                            val1=float(nz(snode.text))
                        if rn(snode.tag)=='DonationAmtOtherMode':
                            val2=float(nz(snode.text))
                        if rn(snode.tag)=='DonationAmt':
                            if float(nz(snode.text))!=val1+val2:
                                error_found=True
            if error_found==True:
                lst_errors.append("103: 'Total Donation' should be equal to sum of 'Donation in cash' AND 'Donation in other mode' in table (80GGA)")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 103")


        #Not a valid check
        #80GGA details are calculated, user does not enter a value for 80GGA in the 'Income Details' sheet
        # try:
        #     if getfval('Section80GGA',data)!=getfval('TotalEligibleDonationAmt80GGA',data):
        #         lst_errors.append(r"106: Deduction u/s 80GGA is claimed but details are not provided in Schedule 80GGA")
        # except Exception as e:
            log.append(e)
        #     lst_errors.append("Error in assessing Rule 106")

        log.append('Output XML validation Rule 107')
        try:
            if getfval('TotalEligibleDonationAmt80GGA',data)>getfval('TotalDonationsUs80GGA',data):
                lst_errors.append(r"107: In Schedule 80GGA, 'Eligible amount of Donations' cannot be more than the 'Total Donations'")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 107")

        #Not a valid check
        #80GGA details are calculated, user does not enter a value for 80GGA in the 'Income Details' sheet
        # try:
        #     if getfval('Section80GGA',data)>getfval('TotalEligibleDonationAmt80GGA',data):
        #         lst_errors.append(r"108: In Schedule VIA, deduction claimed u/s 80GGA cannot be more than the eligible amount of donation mentioned in Schedule 80GGA")
        # except Exception as e:
        #    log.append(e)
        #     lst_errors.append("Error in assessing Rule 108")



        log.append('Output XML validation Rule 111')
        try:
            if getfval('Section80G',data)>0:
                income=max(getfval('GrossTotIncome',data),0)
                error_found=False
                for deduction in mytree.findall('.//ITRForm:Schedule80G',ns):
                    cash=0
                    oth=0
                    for snode in deduction.iter():
                        if rn(snode.tag)=='DonationAmtCash':
                            cash=float(nz(snode.text))
                            continue
                        if rn(snode.tag)=='DonationAmtOtherMode':
                            oth=float(nz(snode.text))
                            continue
                        if rn(snode.tag)=='EligibleDonationAmt':
                            if cash > SECTION_80G_CASH_DONATION_LIMIT:
                                cash=0    
                            if float(nz(snode.text)) > min(cash + oth,income):
                                error_found=True
                if error_found==True:
                    lst_errors.append(r"111: Deduction u/s 80G is not allowed for donation made in cash above Rs. 2,000/-")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 111")

        log.append('Output XML validation Rule 112')
        try:
            if getfval('Section80GGA',data)>0:
                income=max(getfval('GrossTotIncome',data),0)
                error_found=False
                for deduction in mytree.findall('.//ITRForm:Schedule80GGA',ns):
                    cash=0
                    oth=0
                    for snode in deduction.iter():
                        if rn(snode.tag)=='DonationAmtCash':
                            cash=float(nz(snode.text))
                            continue
                        if rn(snode.tag)=='DonationAmtOtherMode':
                            oth=float(nz(snode.text))
                            continue
                        if rn(snode.tag)=='EligibleDonationAmt':
                            if cash > SECTION_80GGA_CASH_DONATION_LIMIT:
                                cash=0    
                            if float(nz(snode.text)) > min(cash + oth,income):
                                error_found=True
                if error_found==True:
                    lst_errors.append(r"112: Deduction u/s 80GGA is not allowed for donation made in cash above Rs. 10,000/-")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 112")


        log.append('Output XML validation Rule 127')
        try:
            val=0
            nodefound=False
            for deduction in mytree.findall('.//ITRForm:TaxPayments',ns):
                for snode in deduction.iter():
                    if rn(snode.tag)=='DateDep':
                        d=dt.datetime.strptime(nz(snode.text),"%Y-%m-%d").date()
                        if d>= dt.datetime.strptime(ADVANCE_TAX_PAID_LOWER_DATE,"%Y-%m-%d").date() and d<=dt.datetime.strptime(ADVANCE_TAX_PAID_UPPER_DATE,"%Y-%m-%d").date():
                            nodefound=True
                            continue
                    if rn(snode.tag)=='Amt' and nodefound==True :
                        nodefound=False
                        val+=float(nz(snode.text))
            if val!=getfval('AdvanceTax',data):
                lst_errors.append("127: 'In 'Schedule Taxes Paid and Verification' Total Advance Tax paid is not equal to the sum of total Tax Paid in schedule IT where date of deposit is between 01/04/2018 and 31/03/2019")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 127")

        log.append('Output XML validation Rule 128')
        try:
            val=0
            nodefound=False
            for deduction in mytree.findall('.//ITRForm:TaxPayments',ns):
                for snode in deduction.iter():
                    if rn(snode.tag)=='DateDep':
                        d=dt.datetime.strptime(nz(snode.text),"%Y-%m-%d")
                        if d>dt.datetime.strptime(SELF_ASSESSMENT_TAX_PAID_CUT_OFF_DATE,"%Y-%m-%d"):
                            nodefound=True
                            continue
                    if rn(snode.tag)=='Amt' and nodefound==True :
                        nodefound=False
                        val+=float(nz(snode.text))
            if val!=getfval('SelfAssessmentTax',data):
                lst_errors.append("128: In 'Schedule Taxes Paid and Verification' Total Self-Assessment Tax Paid is not equal to the sum of total Tax Paid in schedule IT where date of deposit is after 31/03/2019 for A.Y 2019-20")
        except Exception as e:
            log.append(e)
            lst_errors.append("Error in assessing Rule 128")

        if getfval('TotalIncomeOfHP',data) < -1 * MAX_LOSS_HOUSE_PROPERTY:
            lst_errors.append("Maximum loss allowed on Income Head House Property is Rs " +  -1 * MAX_LOSS_HOUSE_PROPERTY  +" in Income Details")

        if getfval('TotalIncome',data) > INCOME_LIMIT_ITR1:
            lst_errors.append("ITR 1 is for individuals being a resident other than not ordinarily resident having Income from Salaries, one house property, other sources (Interest etc.), agricultural income upto Rs.5 thousand and having total income upto Rs. " + str(INCOME_LIMIT_ITR1) + " . Please file other ITR")

        if getfval('Section80D',data) > getfval('Sec80DHealthInsurancePremiumUsr',datausr) + getfval('Sec80DMedicalExpenditureUsr',datausr) + getfval('Sec80DPreventiveHealthCheckUpUsr',datausr):
            lst_errors.append("Deduction u/s 80D should not be more than sum of amount claimed at 'Health Insurance, Medical Expenditure and Preventive Health Check Up' under Chapter VIA in Income Details")

        if getfval('GrossSalary',data)< (getfval('TotalTDSonSalaries',data)- 10):
            lst_errors.append(r"Amount of gross salary disclosed in Income details is less than (100% of Salary reported in Schedule TDS1 - Rs 10)")
        return 'ok', lst_errors, log
    except Exception as e:
        lst_errors.append('Unknown error while validating user input - generic checks')
        log.append(e)
        return 'err', lst_errors, log        





# def it_check_value(str,value):
#     try:
#         if(float(str)>value):
#             return("Exceeded")
#         else:
#             return("Pass")
#     except Exception as e:
#            log.append(e)
#         lst_errors.append("Error in: " + str)

# if (it_check_value(data['DeductionUs16ia'],40000)=="Exceeded"):
#     lst_errors.append("Maximum Deduction u/s 16(ia) is  40,000/- only in Income Details")

# if (data['EmployerCategory']=="Public Sector Undertaking" and it_check_value(data['DeductionUs16ii'],10000)=="Exceeded"):
#     lst_errors.append("Deduction of Entertainment allowance u/s 16(ii) should not exceed 10,000 in Income Details")    

# if (data['EmployerCategory']=="Others" and it_check_value(data['DeductionUs16ii'],5000)=="Exceeded"):
#     lst_errors.append("For employee category 'Others' maximum amount that can be claimed for the Deduction of Entertainment allowance u/s 16(ii) is 5000 in Income Details")

# if (data['EmployerCategory']=="Not Applicable (eg. Family pension etc)" and it_check_value(data['DeductionUs16ii'],0)=="Exceeded"):
#     lst_errors.append("Deduction of Entertainment allowance u/s 16(ii) is not applicable for employer category 'Not Applicable' in Income Details")


# if ( data['TypeOfHP']=="S" and it_check_value(data['InterestPayable'],200000)=="Exceeded"):
#     lst_errors.append("For a Self occupied House Property,Interest payable on borrowed capital value cannot exceed Rs. 2,00,000 in Income Details")










  
