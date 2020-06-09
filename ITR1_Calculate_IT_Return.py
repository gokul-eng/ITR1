import datetime as dt
import math
from ITR1_Constants_Common_Functions import *

def calculate_tax(total_income,age):
    tax_payable = 0
    log=[]
    try:
        if age > 59 and age <= 79:
            if total_income <= 300000:
                tax_payable = 0
            elif total_income >= 300001 and total_income <= 500000 :
                    tempTax = (total_income - 300000) * (0.05)
                    tax_payable = round(tempTax)
            elif total_income >= 500001 and total_income <= 1000000 :
                    tempTax = (total_income - 500000) * (0.2)
                    tax_payable = round((tempTax + 10000))
            elif total_income >= 1000001 :
                    tempTax = (total_income - 1000000) * (0.3)
                    tax_payable = round((tempTax + 110000))
        elif age > 79 :
            if total_income <= 500000 :
                tax_payable = 0
            elif total_income >= 500001 and total_income <= 1000000 :
                tempTax = (total_income - 500000) * (0.2)
                tax_payable = round(tempTax)
            elif total_income >= 1000001 :
                tempTax = (total_income - 1000000) * (0.3)
                tax_payable = round((tempTax + 100000))
                
        elif total_income <= 250000 :
            tax_payable = 0
                
        elif total_income >= 250001 and total_income <= 500000 :
            tempTax = (total_income - 250000) * (0.05)
            tax_payable = round(tempTax)
                
        elif total_income >= 500001 and total_income <= 1000000 :
            tempTax = (total_income - 500000) * (0.2)
            tax_payable = round((tempTax + 12500))
                
        elif total_income >= 1000001 :
            tempTax = (total_income - 1000000) * (0.3)
            tax_payable = round((tempTax + 112500))
        
        return tax_payable, log
    except Exception as e:
        log.append(e)
        return "err", log

def calc_234F(mytree,data,tax_data,ns):
    log=[]
    try:
        Returnfiledstatus=gettval('ReturnFileSec',data)
        res=gettval('OrigRetFiledDate',data)
        if res=='notfound':
            date_original_filing=dt.datetime.today().date()
        else:
            date_original_filing=dt.datetime.strptime(res,"%Y-%m-%d").date()
        state_code=mytree.find('.//ITRForm:PersonalInfo//ITRForm:Address//ITRForm:StateCode',ns).text
        total_income=tax_data['TotalIncome']
        VerificationDate=dt.datetime.today().date()
        
        if state_code==14 or state_code==37:
            duedate = FILING_DUE_DATE_EXCEPTION
        else:
            duedate = FILING_DUE_DATE_NORMAL

        if Returnfiledstatus == "17" or Returnfiledstatus == "18":
            VerificationDate = date_original_filing
        
        intrst234F=0
        if (Returnfiledstatus == "14" or Returnfiledstatus == "15" or Returnfiledstatus == "16" or Returnfiledstatus == "20") or (VerificationDate <= duedate):
            intrst234F = 0
        elif (Returnfiledstatus == "13" or Returnfiledstatus == "11" or Returnfiledstatus == "12") and total_income <= 500000:
            intrst234F = 1000
        elif (Returnfiledstatus == "13" or Returnfiledstatus == "11" or Returnfiledstatus == "12") and total_income > 500000 and (VerificationDate > duedate) and (VerificationDate <= LATE_FILING_234F_MID_YEAR_CUTOFF) :
            intrst234F = 5000
        elif (Returnfiledstatus == "17" or Returnfiledstatus == "18" or Returnfiledstatus == "19") and (date_original_filing <= duedate) :
            intrst234F = 0
        elif (Returnfiledstatus == "17" or Returnfiledstatus == "18" or Returnfiledstatus == "19") and total_income <= 500000 :
            intrst234F = 1000
        elif (Returnfiledstatus =="17" or Returnfiledstatus == "18" or Returnfiledstatus == "19") and total_income > 500000 and (date_original_filing > duedate) and (date_original_filing <= LATE_FILING_234F_MID_YEAR_CUTOFF) :
            intrst234F = 5000
        else:
            intrst234F = 10000
        return intrst234F, log
    except Exception as e:
        log.append(e)
        return "err", log

def calc_TDS_from_sal(mytree,ns):
    log=[]
    try:
        total_tds=0
        for deduction in mytree.findall('.//ITRForm:TDSonSalaries',ns):
            tds=0
            chrg=0
            for snode in deduction.iter():
                if rn(snode.tag)=='IncChrgSal':
                    chrg=float(nz(snode.text))
                if rn(snode.tag)=='TotalTDSSal':    
                    tds=float(nz(snode.text))
                    if tds <= chrg: 
                        total_tds+=tds
                    chrg=0
                    tds=0
        return total_tds, log
    except Exception as e:
        log.append(e)
        return "err", log

def calc_TDS_oth_sal(mytree,ns):
    log=[]
    try:
        total_tds=0
        for deduction in mytree.findall('.//ITRForm:TDSonOthThanSals',ns):
            tds=0
            claim=0
            for snode in deduction.iter():
                if rn(snode.tag)=='TotTDSOnAmtPaid':
                    tds=float(nz(snode.text))
                if rn(snode.tag)=='ClaimOutOfTotTDSOnAmtPaid':    
                    claim=float(nz(snode.text))
                    if tds >=claim: 
                        total_tds+= claim
                    tds=0
                    claim=0
        return total_tds, log
    except Exception as e:
        log.append(e)
        return "err", log

def calc_TDS_3(mytree,ns):
    log=[]
    try:
        total_tds=0
        for deduction in mytree.findall('.//ITRForm:ScheduleTDS3Dtls',ns):
            tds=0
            claim=0
            for snode in deduction.iter():
                if rn(snode.tag)=='TDSDeducted':
                    tds=float(nz(snode.text))
                if rn(snode.tag)=='TDSClaimed':    
                    claim=float(nz(snode.text))
                    if tds >=claim: 
                        total_tds+= claim
                    tds=0
                    claim=0
        return total_tds, log
    except Exception as e:
        log.append(e)
        return "err", log

def calc_TCS_from_sal(mytree,ns):
    log=[]
    try:
        total_tcs=0
        for deduction in mytree.findall('.//ITRForm:ScheduleTCS',ns):
            tcs=0
            claim=0
            for snode in deduction.iter():
                if rn(snode.tag)=='TotalTCS':
                    tcs=float(nz(snode.text))
                if rn(snode.tag)=='AmtTCSClaimedThisYear':    
                    claim=float(nz(snode.text))
                    if claim <= tcs: 
                        total_tcs+= claim
                    tcs=0
                    claim=0
        return total_tcs, log
    except Exception as e:
        log.append(e)
        return "err", log

def calc_adv_self_tax(mytree,data,ns):
    log=[]
    try:
        statecode=mytree.find('.//ITRForm:PersonalInfo//ITRForm:Address//ITRForm:StateCode',ns).text
        selfAssessmentTax=0
        advanceTax=0
        selfAssessmentTax234A=0
        for deduction in mytree.findall('.//ITRForm:TaxPayment',ns):
            for snode in deduction.iter():
                if rn(snode.tag)=='DateDep':
                    datedep=dt.datetime.strptime(snode.text,"%Y-%m-%d").date()
                if rn(snode.tag)=='Amt':    
                    if FIN_YEAR_START <= datedep and datedep <= FIN_YEAR_END:
                        advanceTax = advanceTax + float(nz(snode.text))
                    elif datedep > FIN_YEAR_END :
                        selfAssessmentTax = selfAssessmentTax + float(nz(snode.text))

                    if statecode=='14' or statecode=='37':
                        if FIN_YEAR_END < datedep and datedep <= CUTOFF_DATE_CALC_SELF_ASSESSMENT_EXCEPTION:
                            selfAssessmentTax234A = selfAssessmentTax234A + float(nz(snode.text))
                    else:
                        if FIN_YEAR_END < datedep and datedep <= CUTOFF_DATE_CALC_SELF_ASSESSMENT_NORMAL:
                            selfAssessmentTax234A = selfAssessmentTax234A + float(nz(snode.text))
                        
        return advanceTax, selfAssessmentTax, selfAssessmentTax234A, log
    except Exception as e:
        log.append(e)
        return "err","err","err", log

def calc_months(d1,d2):
    if d1==d2:
        return 1
    else:
        num_months = (d1.year - d2.year) * 12 + (d1.month - d2.month) + 1
        return max(num_months,0)

def calculate_interest(mytree,data,tax_data,ns):
    log=[]
    ierrors=[]
    try:
        log.append("Inside function calculate_interest")
        statecode=mytree.find('.//ITRForm:PersonalInfo//ITRForm:Address//ITRForm:StateCode',ns).text
        #Calculate total TDS and TCS
        res1=calc_TDS_from_sal(mytree,ns)
        res2=calc_TDS_oth_sal(mytree,ns)
        res3=calc_TDS_3(mytree,ns)
        res4=calc_TCS_from_sal(mytree,ns) #TCS
        if res1[0]=='err':
            ierrors.append("Interest calc TDS1: Error calculating TDS from Salary")
            for x in res1[1]:
                log.append(x)
        elif res2[0]=='err':
            for x in res2[1]:
                log.append(x)
            ierrors.append("Interest calc TDS2: Error calculating TDS Other than Salary")
        elif res3[0]=='err':
            for x in res3[1]:
                log.append(x)
            ierrors.append("Interest calc TDS3: Error calculating TDS as per Form 16C")
        elif res4[0]=='err':
            for x in res4[1]:
                log.append(x)
            ierrors.append("Interest calc TCS: Error calculating TCS as per Form 27D")
        else:
            tds=res1[0] + res2[0] + res3[0]
            tcs=res4[0]
        
        res=calc_adv_self_tax(mytree,data,ns)
        if res[0]=='err':
            for x in res[3]:
                log.append(x)
            ierrors.append("Interest calc: Error calculating Advance Tax paid/ Self assessment Tax")
        else:
            adv_tax=res[0]
            selfAssessmentTax=res[1]
            self_ass_234a=res[2]
    except Exception as e:
        log.append(e)
        ierrors.append("Interest calc: Unknown error calculating TDS/TCS/Adv Tax")

    #234A calc
    try:
        log.append("start 234A calc")
        calculated_net_tax_liability=tax_data['NetTaxLiability']
        if (calculated_net_tax_liability - adv_tax - tds - tcs - self_ass_234a < 0):
            intrst234Aprinciple = 0
        else:
            intrst234Aprinciple = calculated_net_tax_liability - adv_tax - tds - tcs - self_ass_234a
            intrst234Aprinciple = RoundDown(intrst234Aprinciple, 100)

        ver_date=dt.datetime.today().date()
    
        if statecode=='14' or statecode=='37':
            MonthsAfterDueDate = calc_months(ver_date, FILING_DUE_DATE_EXCEPTION + dt.timedelta(days=1))
            if gettval('ReturnFileSec',data)=='17' or gettval('ReturnFileSec',data)=='18':
                origDate = gettval('OrigRetFiledDate',data)
                if origDate != 'notfound':
                    MonthsAfterDueDate = calc_months(dt.datetime.strptime(origDate,"%Y-%m-%d").date(), FILING_DUE_DATE_EXCEPTION + dt.timedelta(days=1))
        else:
            MonthsAfterDueDate = calc_months(ver_date, FILING_DUE_DATE_NORMAL + dt.timedelta(days=1))
            if gettval('ReturnFileSec',data)=='17' or gettval('ReturnFileSec',data)=='18':
                origDate = gettval('OrigRetFiledDate',data)
                if origDate != 'notfound':
                    MonthsAfterDueDate = calc_months(dt.datetime.strptime(origDate,"%Y-%m-%d").date(), FILING_DUE_DATE_NORMAL + dt.timedelta(days=1))
        intrst234A = intrst234Aprinciple * INTEREST_234A_CALCULATION * MonthsAfterDueDate    
    except Exception as e:
        log.append(e)
        ierrors.append("Interest calc: Unknown error calculating interest u/s 234A")
    
    try:
        log.append("start age calc")
        age=calcAge(data['DOB'])
        if (age <= 59):
            agestatus = "NC"
        elif age > 59 and age <= 79 :
            agestatus = "SC"
        else:
            agestatus = "SSC"
        
        intrst234F = 0
        if (agestatus == "NC" and tax_data['GrossTotIncome'] > 250000) or \
            (agestatus == "SC" and tax_data['GrossTotIncome'] > 300000) or \
            (agestatus == "SSC" and tax_data['GrossTotIncome'] > 500000) :
            res = calc_234F(mytree,data,tax_data,ns)
            if res[0]!='err':
                intrst234F=res[0]
            else:
                ierrors.append("Interest calc: Unknown error calculating interest u/s 234F")
                for x in res[1]:
                    log.append(x)
        else:
            intrst234F = 0
    except Exception as e:
        log.append(e)
        ierrors.append("Interest calc: Unknown error calculating interest u/s 234F")
    
    #calculate calcIntrst234C
    try:
        log.append("start 234C calc")
        intrst234C = 0
        slab0 = 0
        slab1 = 0
        slab2 = 0
        slab3 = 0
        for deduction in mytree.findall('.//ITRForm:TaxPayment',ns):
            for snode in deduction.iter():
                if rn(snode.tag)=='DateDep':
                    datedep=dt.datetime.strptime(snode.text,"%Y-%m-%d").date()
                if rn(snode.tag)=='Amt': 
                    if FIN_YEAR_START <= datedep and datedep <= SLAB0_234C_END:
                        slab0 = slab0 + float(nz(snode.text))
                    elif SLAB0_234C_END < datedep and datedep <= SLAB1_234C_END:
                        slab1 = slab1 + float(nz(snode.text))
                    elif SLAB1_234C_END < datedep and datedep <= SLAB2_234C_END:
                        slab2 = slab2 + float(nz(snode.text))
                    elif SLAB2_234C_END < datedep and datedep <= SLAB3_234C_END:
                        slab3 = slab3 + float(nz(snode.text))

        if calculated_net_tax_liability - tds - tcs >= 10000:
            temp12PerQtr1 = RoundDown(0.12 * (calculated_net_tax_liability - tds - tcs), 100)
        
            if slab0 < (calculated_net_tax_liability - tds - tcs) * 0.15:
                if slab0 >= temp12PerQtr1:
                    tempintrst234C0i=0
                else:
                    tempintrst234C0i=((calculated_net_tax_liability - tds - tcs) * 0.15) - slab0
                if tempintrst234C0i > 100:
                    tempintrst234C0i = RoundDown(tempintrst234C0i, 100)
                intrst234C0i = tempintrst234C0i * 0.01 * 3
            temp36PerQtr2 = RoundDown(0.36 * (calculated_net_tax_liability - tds - tcs),100)
            if (slab0 + slab1 < ((calculated_net_tax_liability - tds - tcs) * (0.45))) :
                if slab0 + slab1 >= temp36PerQtr2:
                    tempintrst234Ci=0
                else:
                    tempintrst234Ci=(calculated_net_tax_liability - tds - tcs) * 0.45 - slab0 - slab1
                if tempintrst234Ci > 100 :
                    tempintrst234Ci = RoundDown(tempintrst234Ci, 100)
                intrst234Ci = tempintrst234Ci * (0.01) * (3)
            
            if (slab0 + slab1 + slab2) < ((calculated_net_tax_liability - tds - tcs) * (0.75)) :
                tempintrst234Cii = (calculated_net_tax_liability - tds - tcs) * 0.75 - slab0 - slab1 - slab2
                if tempintrst234Cii > 100 :
                    tempintrst234Cii = RoundDown(tempintrst234Cii, 100)
                intrst234Cii = tempintrst234Cii * (0.01) * 3
            if ((slab0 + slab1 + slab2 + slab3) < (calculated_net_tax_liability - tds - tcs)) :
                tempintrst234Ciii = (calculated_net_tax_liability - tds - tcs - slab0 - slab1 - slab2 - slab3)
                if tempintrst234Ciii > 100 :
                    tempintrst234Ciii = RoundDown(tempintrst234Ciii, 100)
                intrst234Ciii = tempintrst234Ciii * 0.01
        else:
            intrst234C0i = 0
            intrst234Ci = 0
            intrst234Cii = 0
            intrst234Ciii = 0
        intrst234C = intrst234C0i + intrst234Ci + intrst234Cii + intrst234Ciii
        if (age > 59):
            intrst234C = 0
    except Exception as e:
        log.append(e)
        ierrors.append("Interest calc: Unknown error calculating interest u/s 234C")

    #calculate 234B    
    try:
        log.append("start 234B calc")
        calcInterestPayable234B = 0
        if ((calculated_net_tax_liability - (tds + tcs)) >= 10000 and \
            adv_tax < 90 / 100 * (calculated_net_tax_liability - (tds + tcs))) and age<=59:
            deps={}
            for deduction in mytree.findall('.//ITRForm:TaxPayment',ns):
                for snode in deduction.iter():
                    if rn(snode.tag)=='DateDep':
                        dep_date=dt.datetime.strptime(snode.text,"%Y-%m-%d").date()
                        dep_period=dep_date.month + (dep_date.year - ASS_YEAR) * 12
                    if rn(snode.tag)=='Amt':    
                        if dep_date > FIN_YEAR_END:
                            if dep_period in deps:
                                deps[dep_period]=deps[dep_period] + float(nz(snode.text))
                            else:
                                deps[dep_period]=float(nz(snode.text))
            shortFall= RoundDown(max(0, calculated_net_tax_liability - (adv_tax + tds + tcs)),100)
            carryForwardPrinicipal = shortFall
            for i in range(4,4 + dt.datetime.today().date().month - 4 + (dt.datetime.today().date().year - ASS_YEAR) * 12 + 1):
                balancePrincipal = carryForwardPrinicipal
                calcIntrst234BOnPeriod = round(0.01 * balancePrincipal)
                calcInterestPayable234B = calcInterestPayable234B + calcIntrst234BOnPeriod
                if i==4:
                    balanceInterest = intrst234A + calcIntrst234BOnPeriod + intrst234C + intrst234F
                else:
                    balanceInterest = carryForwardInterest + calcIntrst234BOnPeriod
                if i in deps:
                    SATPaidAtPeriod = deps[i]
                else:
                    SATPaidAtPeriod = 0
                adjustedInterest = min(SATPaidAtPeriod, balanceInterest)
                adjustedPrincipal = max(0, min(SATPaidAtPeriod - adjustedInterest, balancePrincipal))
                carryForwardPrinicipal = max(0, balancePrincipal - adjustedPrincipal)
                carryForwardInterest = max(0, balanceInterest - adjustedInterest)
    except Exception as e:
        log.append(e)
        ierrors.append("Interest calc: Unknown error calculating interest u/s 234B")

    return ierrors, intrst234A, calcInterestPayable234B, intrst234C, intrst234F, adv_tax, tds, tcs, selfAssessmentTax, log

def Calculate_It_Return(mytree,data,datausr,ns):
    errors=[]
    log=[]
    tax_data=0
    chap6a={}
    don_cash=[]
    don_oth=[]
    tot_don=[]
    elig_don=[]
    don_cash_gga=[]
    don_oth_gga=[]
    tot_don_gga=[]
    elig_don_gga=[]
    res1=[]
    res2=[]
    res3=[]
    res4=[]
    try:
        tax_data={}  #All calculated values stored in this variable
        try:   
            tax_data['GrossSalary']=max(0,getfval('Salary',data) + getfval('PerquisitesValue',data) + getfval('ProfitsInSalary',data))
        except Exception as e:
            log.append(e)
            errors.append("Error encountered while calculating Gross Salary (1-i)")
        
        try:    
            tax_data['TotalAllwncExemptUs10'] = get_tot_gen('AllwncExemptUs10','SalOthAmount',mytree,ns)
        except Exception as e:
            log.append(e)
            errors.append("Error encountered while calculating Allowances Exempt u/s 10 (1-ii)")
        try:
            tax_data['NetSalary']=max(float(tax_data['GrossSalary'])-float(tax_data['TotalAllwncExemptUs10']) ,0)
        except Exception as e:
            log.append(e)
            errors.append("Error encountered while calculating Net Salary (1-iii)")    

        try:
            tax_data['DeductionUs16ia']=min(tax_data['NetSalary'],STANDARD_DEDUCTION_16ia)
        except Exception as e:
            log.append(e)
            errors.append("Error encountered while calculating Standard Deduction u/s 16 (1-iv-a)")

        try:
            tax_data['DeductionUs16']=tax_data['DeductionUs16ia'] + getfval('EntertainmentAlw16ii',data) + getfval('ProfessionalTaxUs16iii',data)
        except Exception as e:
            log.append(e)
            errors.append("Error encountered while calculating Deductions u/s 16 (1-iv)")

        #income chargeable under head 'Salaries'
        try:    
            tax_data['IncomeFromSal']=max(float(tax_data['NetSalary'])-float(tax_data['DeductionUs16']),0)
        except Exception as e:
            log.append(e)
            errors.append("Error encountered while calculating Income chargeable under Head 'Salaries' (1-v)")

        #House Property
        try:
            tax_data['AnnualValue']=getfval('GrossRentReceived',data) - getfval('TaxPaidlocalAuth',data)
        except Exception as e:
            log.append(e)
            errors.append("Error encountered while calculating Annual Value (2-iii)")
        try:
            tax_data['StandardDeduction']=RndMax0(float(tax_data['AnnualValue']) * HOUSE_PROPERTY_STD_DEDUCTION_PERCENTAGE)
        except Exception as e:
            log.append(e)
            errors.append("Error encountered while calculating House property standard deduction (30%) (2-iv)")

        #Income chargeable under the head ‘House Property’
        try:
            tax_data['TotalIncomeOfHP']=max(-1 * MAX_LOSS_HOUSE_PROPERTY,float(tax_data['AnnualValue']) - float(tax_data['StandardDeduction']) - getfval('InterestPayable',data) + getfval('ArrearsUnrealizedRentRcvd',data))
        except Exception as e:
            log.append(e)
            errors.append("Error encountered while calculating Income chargeable under head 'House Property' (2-vii)")
        try:
            tax_data['IncomeOthSrc']=max(0,get_tot_gen('OthersInc','OthSrcOthAmount',mytree,ns) - getfval('DeductionUs57iia',data))
        except Exception as e:
            log.append(e)
            errors.append("Error encountered while calculating Income from Other sources (3)")
        try:
            tax_data['GrossTotIncome']=float(tax_data['IncomeFromSal']) + float(tax_data['TotalIncomeOfHP']) + float(tax_data['IncomeOthSrc'])
        except Exception as e:
            log.append(e)
            errors.append("Error encountered while calculating Gross Total Income (4)")

        #Chaper 6A Calculations
        chap6a={}
        total_income=max(float(tax_data['GrossTotIncome']),0)

        #80C
        try:
            val=get_tot_gen('UsrDeductUndChapVIA','Section80C',mytree,ns)
            if val=='err':
                errors.append("Chapter6A (5-a): Error calculating 80C value")
                chap6a['a']=0
            else:
                chap6a['a']=min(val,CHAP6A_80C_LIMIT,total_income)
        except Exception as e:
            log.append(e)
            errors.append("Chapter6A (5-a): Error calculating 80C value")

        #80CCC
        try:
            val=get_tot_gen('UsrDeductUndChapVIA','Section80CCC',mytree,ns)
            t1=0
            if val=='err':
                errors.append("Chapter6A (5-b): Error calculating 80CCC value")
                chap6a['b']=0
            else:
                if min(min(val, min(150000,abs(float(tax_data['GrossTotIncome']))),min(150000,abs(float(tax_data['GrossTotIncome']))) - float(chap6a['a'])),total_income) > 150000:
                    t1=150000
                else:
                    t1=min(min(val, min(150000,abs(float(tax_data['GrossTotIncome']))),min(150000,abs(float(tax_data['GrossTotIncome']))) - float(chap6a['a'])),total_income)
                    chap6a['b']=t1
        except Exception as e:
            log.append(e)
            errors.append("Chapter6A (5-b): Error calculating 80CCC value")
            
        #80CCD(1)
        try:
            val=get_tot_gen('UsrDeductUndChapVIA','Section80CCDEmployeeOrSE',mytree,ns)
            t1=0
            t2=0
            if val=='err':
                errors.append("Chapter6A (5-c): Error retrieving 80CCD(1) value")
                chap6a['c']=0
            else:
                if gettval('EmployerCategory',data)=='PE':
                    t2=round(PENSIONERS_80CCD_MAX * tax_data['GrossTotIncome'])
                else:
                    t2=round(NON_PENSIONERS_80CCD_MAX * (float(tax_data['NetSalary'])-getfval('PerquisitesValue',data)))
                if max(0,min(min(val, t2, 150000 - float(chap6a['a']) - float(chap6a['b']) ),min(150000,abs(float(tax_data['GrossTotIncome'])) - float(chap6a['a'])-float(chap6a['b'])),total_income)) > 150000:
                    t1=150000
                else:
                    t1=max(0,min(min(val, t2, 150000 - float(chap6a['a']) - float(chap6a['b']) ),min(150000,abs(float(tax_data['GrossTotIncome'])) - float(chap6a['a'])-float(chap6a['b'])),total_income))
                    chap6a['c']=t1
        except Exception as e:
            log.append(e)
            errors.append("Chapter6A (5-c): Error calculating 80CCD(1) value")

        #80CCD(1B)
        try:

            val=get_tot_gen('UsrDeductUndChapVIA','Section80CCD1B',mytree,ns)
            if val=='err':
                errors.append("Chapter6A (5-d): Error retrieving 80CCD(1B) value")
                chap6a['d']=0
            else:
                chap6a['d']=min(val,CHAP6A_80CCD1B_LIMIT,total_income)
        except Exception as e:
            log.append(e)
            errors.append("Chapter6A (5-d): Error calculating 80CCD(1B) value")

        #80CCD(2)
        try:
            val=get_tot_gen('UsrDeductUndChapVIA','Section80CCDEmployer',mytree,ns)
            t2=0
            if val=='err':
                errors.append("Chapter6A(5-e): Error retrieving 80CCD(2) value")
                chap6a['e']=0
            else:
                if gettval('EmployerCategory',data)=='GOV' or gettval('EmployerCategory',data)=='PSU' or gettval('EmployerCategory',data)=='OTH':
                    t2=GOV_PSU_OTH_80CCD2_PERCENT_LIMIT * max(float(tax_data['NetSalary'])-getfval('PerquisitesValue',data),0)
                else:
                    t2=0
                chap6a['e']=min(val,t2,total_income)
        except Exception as e:
            log.append(e)
            errors.append("Chapter6A (5-e): Error calculating 80CCD(2) value")

        #80CCG
        try:
            val=get_tot_gen('UsrDeductUndChapVIA','Section80CCG',mytree,ns)
            if val=='err':
                errors.append("Chapter6A (5-f): Error retrieving 80CCG value")
                chap6a['f']=0
            else:
                if total_income > GROSS_INCOME_LIMIT_80CCG:
                    chap6a['f']=0
                else:
                    chap6a['f']=min(val,ABSOLUTE_80CCG_VALUE_LIMIT,total_income)
        except Exception as e:
            log.append(e)
            errors.append("Chapter6A (5-f): Error calculating 80CCG value")
        try:
            #80D
            typ_b=gettval('MedicalExpenditure',datausr)
            val_b=get_tot_gen('UsrDeductUndChapVIA','Sec80DMedicalExpenditureUsr',mytree,ns)
            incd80db=min(eval('HEALTH_MEDICAL_EXPENDITURE_' + typ_b),total_income,val_b)

            typ_a=gettval('HealthInsurancePremium',datausr)
            if typ_a!='7':
                lim_a=eval('HEALTH_INSURANCE_PREMIUM_' + typ_a)
            else:
                age=calcAge(data['DOB'])
                if age<=59:
                    lim_a=HEALTH_INSURANCE_PREMIUM_7_NON_SENIOR
                else:
                    lim_a=HEALTH_INSURANCE_PREMIUM_7_SENIOR
            val_a=get_tot_gen('UsrDeductUndChapVIA','Sec80DHealthInsurancePremiumUsr',mytree,ns)
            incd80d=min(lim_a,val_a,total_income)

            val_c=get_tot_gen('UsrDeductUndChapVIA','Sec80DPreventiveHealthCheckUpUsr',mytree,ns)
            bd60= incd80d+ min(PREVENTATIVE_HEALTH_CHECKUP_LIMIT_80D,total_income,val_c)
            typ_c=gettval('PreventiveHealthCheckUp',datausr)
            if typ_a=='1' and typ_c=='1':
                bd61='1'
            elif typ_a=='3' and typ_c=='2':
                bd61='2'
            elif typ_a=='5' and typ_c=='3':
                bd61='3'
            elif typ_a=='6':
                bd61='4'
            else:
                bd61='0'
            if bd61=='1' or bd61=='2':
                bd62=min(25000,bd60)
            elif bd61=='3':
                bd62=min(50000,bd60)
            elif bd61=='4':
                bd62=min(75000,bd60)
            else:
                bd62=bd60
            chap6a['g']=min(100000,bd62+incd80db)
        except Exception as e:
            log.append(e)
            errors.append("Chapter6A (5-g): Error calculating 80D value")

        #80DD
        try:    
            val=0
            lim=0
            val=get_tot_gen('UsrDeductUndChapVIA','Section80DD',mytree,ns)
            if val=='err':
                errors.append("Chapter6A (5-h): Error retrieving 80DD value")
                chap6a['h']=0
            else:
                typ=gettval('Section80DDUsrType',datausr)
                if typ=='1':
                    lim=DEPENDENT_WITH_DISABILITY_80DD
                elif typ=='2':
                    lim=DEPENDENT_WITH_SEVERE_DISABILITY_80DD
                val=min(val,lim)
                chap6a['h']=min(val,total_income)
        except Exception as e:
            log.append(e)
            errors.append("Chapter6A (5-h): Error calculating 80DD value")

        #80DDB
        try:
            val=0
            lim=0
            val=get_tot_gen('UsrDeductUndChapVIA','Section80DDB',mytree,ns)
            if val=='err':
                errors.append("Chapter6A (5-i): Error retrieving 80DDB value")
                chap6a['i']=0
            else:
                typ=gettval('Section80DDBUsrType',datausr)
                if typ=='1':
                    lim=SELF_OR_DEPENDENT_MEDICAL_TREATMENT_80DDB
                elif typ=='2':
                    lim=SELF_OR_DEPENDENT_SENIOR_CITIZEN_MEDICAL_TREATMENT_80DDB
                val=min(val,lim)
                chap6a['i']=min(val,total_income)
        except Exception as e:
            log.append(e)
            errors.append("Chapter6A (5-i): Error calculating 80DDB value")

        #80E
        try:
            val=get_tot_gen('UsrDeductUndChapVIA','Section80E',mytree,ns)
            if val=='err':
                errors.append("Chapter6A (5-j): Error retrieving 80E value")
                chap6a['j']=0
            else:
                chap6a['j']=min(val,total_income)
        except Exception as e:
            log.append(e)
            errors.append("Chapter6A (5-j): Error calculating 80E value")

        #80EE
        try:    
            val=get_tot_gen('UsrDeductUndChapVIA','Section80EE',mytree,ns)
            if val=='err':
                errors.append("Chapter6A (5-k): Error retrieving 80EE value")
                chap6a['k']=0
            else:
                chap6a['k']=min(val,INTEREST_ON_LOAN_HOUSE_LIMIT,total_income)
        except Exception as e:
            log.append(e)
            errors.append("Chapter6A (5-k): Error computing 80EE value")

        #80GGC
        try:
            val=get_tot_gen('UsrDeductUndChapVIA','Section80GGC',mytree,ns)
            if val=='err':
                errors.append("Chapter6A (5-o): Error retrieving 80GGC value")
                chap6a['o']=0
            else:
                chap6a['o']=min(val,total_income)
        except Exception as e:
            log.append(e)
            errors.append("Chapter6A (5-o): Error calculating 80GGC value")

        #80TTA
        try:
            val=get_tot_gen('UsrDeductUndChapVIA','Section80TTA',mytree,ns)
            if val=='err':
                errors.append("Chapter6A (5-p): Error retrieving 80TTA value")
                chap6a['p']=0
            else:
                tmpsum=0
                nodefound=False
                for deduction in mytree.findall('.//ITRForm:OthersInc',ns):
                    for snode in deduction.iter():
                        if rn(snode.tag)=='OthSrcNatureDesc':
                            if nz(snode.text)=="SAV":
                                nodefound=True
                                continue
                        if rn(snode.tag)=='OthSrcOthAmount' and nodefound==True:    
                            tmpsum=tmpsum+float(nz(snode.text))
                            nodefound=False
                chap6a['p']=min(min(val,SECTION_80TTA_LIMIT),max(0,min(total_income,max(0,tmpsum))))
        except Exception as e:
            log.append(e)
            errors.append("Chapter6A (5-p): Error calculating 80TTA value")

        #80TTB
        try:
            val=get_tot_gen('UsrDeductUndChapVIA','Section80TTB',mytree,ns)
            if val=='err':
                errors.append("Chapter6A (5-q): Error retrieving 80TTB value")
                chap6a['q']=0
            else:
                tmpsum=0
                nodefound=False
                for deduction in mytree.findall('.//ITRForm:OthersInc',ns):
                    for snode in deduction.iter():
                        if rn(snode.tag)=='OthSrcNatureDesc':
                            if nz(snode.text)=="SAV" or nz(snode.text)=="IFD":
                                nodefound=True
                                continue
                        if rn(snode.tag)=='OthSrcOthAmount' and nodefound==True:    
                            tmpsum=tmpsum+float(nz(snode.text))
                            nodefound=False
                chap6a['q']=min(min(val,SECTION_80TTB_LIMIT),min(total_income,max(0,tmpsum)))
        except Exception as e:
            log.append(e)
            errors.append("Chapter6A (5-q): Error calculating 80TTB value")

        #80U
        try:
            val=0
            lim=0
            val=get_tot_gen('UsrDeductUndChapVIA','Section80U',mytree,ns)
            if val=='err':
                errors.append("Chapter6A (5-r): Error calculating 80U value")
                chap6a['r']=0
            else:
                typ=gettval('Section80UUsrType',datausr)
                if typ=='1':
                    lim=SELF_WITH_DISABILITY_80U
                elif typ=='2':
                    lim=SELF_WITH_SEVERE_DISABILITY_80U
                val=min(val,lim)
                chap6a['r']=min(val,total_income)
        except Exception as e:
            log.append(e)
            errors.append("Chapter6A (5-r): Error calculating 80U value")

        #80GGA
        try:
            t_amt_eleg=0
            don_cash_gga=[] #Donation in cash
            don_oth_gga=[] #Donation in other mode
            tot_don_gga=[] #Total Donation
            elig_don_gga=[] #Eligible Amount Donation

            for deduction in mytree.findall('.//ITRForm:Schedule80GGA',ns):
                cash=0
                oth=0
                for snode in deduction.iter():
                    if rn(snode.tag)=='DonationAmtCash':
                        cash=float(nz(snode.text))
                        don_cash_gga.append(cash)
                        continue
                    if rn(snode.tag)=='DonationAmtOtherMode':
                        oth=float(nz(snode.text))
                        don_oth_gga.append(oth)
                        tot_don_gga.append(max(cash+oth,0))
                        if cash > SECTION_80GGA_CASH_DONATION_LIMIT:
                            cash=0
                        t_amt_eleg+=min(cash + oth,total_income)
                        elig_don_gga.append(min(cash + oth,total_income))
                        cash=0
                        oth=0
            chap6a['n']=t_amt_eleg
        except Exception as e:
            log.append(e)
            errors.append("Chapter6A(5-n): Error calculating 80GGA value")

        #80G
        #80G can be caclulated only at the end because it depends on values from other chap6a deductions. Do not move the position of this code.
        try:
            #get 80G qualification amount
            don_cash=[] #Donation in cash
            don_oth=[] #Donation in other mode
            tot_don=[] #Total Donation
            elig_don=[] #Eligible Amount Donation
            cats=['Don100Percent','Don50PercentNoApprReqd','Don100PercentApprReqd']
            t1=0
            for key in chap6a:  #compute values of all chapter 6A deductions except 80G itself and 80GG
                if key != 'l' and key != 'm':
                    t1+=float(chap6a[key])
            val=get_tot_gen('UsrDeductUndChapVIA','Section80GG',mytree,ns) #Add 80GG user value ad not calcauted value
            if val=='err':
                errors.append("Chapter6A (5-l): Error retrieving 80G value")
                chap6a['l']=0
            else:
                t1+=val
            qual_80g=round(SECTION80G_QUALIFICATION_LIMIT_PERCENTAGE * max(0,total_income-t1))

            t_amt_eleg=0
            t_amt_eleg_100=0
            t_amt_eleg_50_noapp=0
            t_amt_eleg_100_noapp=0
            for cat in cats:
                for deduction in mytree.findall('.//ITRForm:'+cat,ns):
                    cash=0
                    oth=0
                    for snode in deduction.iter():
                        if rn(snode.tag)=='DonationAmtCash':
                            cash=float(nz(snode.text))
                            don_cash.append(cash)
                            continue
                        if rn(snode.tag)=='DonationAmtOtherMode':
                            oth=float(nz(snode.text))
                            don_oth.append(oth)
                            tot_don.append(cash+oth)
                            if cash > SECTION_80G_CASH_DONATION_LIMIT:
                                cash=0
                            if cat=='Don100Percent':
                                don=min(cash + oth,total_income)
                                t_amt_eleg_100+= don
                                elig_don.append(don)
                            elif cat=='Don50PercentNoApprReqd':
                                don=round(min((cash + oth)/2,total_income))
                                t_amt_eleg_50_noapp+= don
                                elig_don.append(don)
                            elif cat=='Don100PercentApprReqd':
                                don=min(cash + oth,total_income,qual_80g)
                                elig_don.append(don) 
                                t_amt_eleg_100_noapp+=don
                            cash=0
                            oth=0
            t_amt_eleg_100=min(t_amt_eleg_100,total_income)
            t_amt_eleg_50_noapp=min(t_amt_eleg_50_noapp,total_income)
            t_amt_eleg_100_noapp=round(min(t_amt_eleg_100_noapp,qual_80g))    
            t_amt_eleg=t_amt_eleg_100 + t_amt_eleg_50_noapp + t_amt_eleg_100_noapp
            
            #get CDE eligible amount
            cde_elig=max(0,round((qual_80g-t_amt_eleg_100_noapp)/2))

            for deduction in mytree.findall('.//ITRForm:Don50PercentApprReqd',ns):
                cash=0
                oth=0
                don_50_qual=0
                don_50_cash_adj=0
                tot_don_oth=0
                for snode in deduction.iter():
                    if rn(snode.tag)=='DonationAmtCash':
                        cash=float(nz(snode.text))
                        don_cash.append(cash)
                        continue
                    if rn(snode.tag)=='DonationAmtOtherMode':
                        oth=float(nz(snode.text))
                        don_oth.append(oth)
                        tot_don.append(cash+oth)
                        tot_don_oth+=oth
                        if cash > SECTION_80G_CASH_DONATION_LIMIT:
                            cash=0
                        don=round(min(total_income,min(cde_elig,(cash + oth)/2)))
                        don_50_qual+=don
                        don_50_cash_adj+=cash
                        elig_don.append(don)
            don_50_qual=round(min(total_income,min(cde_elig,(don_50_cash_adj+tot_don_oth)/2)))
            t_amt_eleg+= don_50_qual
            if tax_data['GrossTotIncome']>0:
                chap6a['l']=min(round(t_amt_eleg,0),tax_data['GrossTotIncome'])
            else:
                chap6a['l']=0
        except Exception as e:
            log.append(e)
            errors.append("Chapter6A (5-l): Error computing 80G value")

        try:    
            #80GG
            val=get_tot_gen('UsrDeductUndChapVIA','Section80GG',mytree,ns)
            if val=='err':
                errors.append("Chapter6A (5-m): Error retrieving 80GG value")
                chap6a['m']=0
            else:
                t1=0
                for key in chap6a:  #compute cvalues of all 6A deductions except 80G itself and 80GG
                    if key != 'm':
                        t1+=float(chap6a[key])
                chap6a['m']=min(round(min(SECTION_80GG_VALUE, SECTION_80GG_PERCENTAGE_VALUE*(max(0,total_income-t1)))),val,total_income)
        except Exception as e:
            log.append(e)
            errors.append("Chapter6A (5-m): Error calculating 80GG value")       
        try:
            #calc 6
            tempsum=0
            for key in chap6a:
                tempsum+=float(chap6a[key])
            tax_data['TotalChapVIADeductions']=min(tempsum,tax_data['GrossTotIncome'])
        except Exception as e:
            log.append(e)
            errors.append("Chapter6A: Error calculating total 6A deductions (6)")   

        try:
            #calc 7
            tax_data['TotalIncome']=round_nearest(max(0,float(tax_data['GrossTotIncome'])-float(tax_data['TotalChapVIADeductions']))+1,10)
        except Exception as e:
            log.append(e)
            errors.append("Chapter6A: Error calculating Total Income (7)")   
        try:
            #calc 7.5
            val=get_tot_gen('ExemptIncAgriOthUs10','OthAmount',mytree,ns)
            if val=='err':
                errors.append("Income Details: Error retrieving Total Exempt Income")
                tax_data['ExemptIncAgriOthUs10Total']=0
            else:
                tax_data['ExemptIncAgriOthUs10Total']=val
        except Exception as e:
            log.append(e)
            errors.append("Chapter6A: Error calculating Total Exempt Income (7.5)")   
        try:
            #calc 8
            res=calculate_tax(float(tax_data['TotalIncome']),calcAge(data['DOB']))
            for x in res[1]:
                log.append(x)
            if res[0]!="err":
                tax_data['TotalTaxPayable']=res[0]
            else:
                errors.append("Error encountered while calculating 'Tax Payable on total Income' (8)")  
        except Exception as e:
            log.append(e)
            errors.append("Error encountered while calculating 'Tax Payable on total Income' (8)") 
        try:
            #calc 9
            if float(tax_data['TotalIncome']) <= REBATE_UNDER_87A_LIMIT:
                tax_data['Rebate87A']=min(float(tax_data['TotalTaxPayable']),REBATE_UNDER_87A)
            else:
                tax_data['Rebate87A']=0
        except Exception as e:
            log.append(e)
            errors.append("Error encountered while calculating Rebats u/s 87A (9)") 
        try:
            #calc 10
            tax_data['TaxPayableOnRebate']=round(tax_data['TotalTaxPayable']-tax_data['Rebate87A'])
        except Exception as e:
            log.append(e)
            errors.append("Error encountered while calculating 'Tax Payable After Rebate' (10)") 
        try:
            #calc 11
            tax_data['EducationCess']=round(tax_data['TaxPayableOnRebate']*EDUCATION_HEALTH_CESS_PERCENT)
        except Exception as e:
            log.append(e)
            errors.append("Error encountered while calculating 'Health and Education Cess' (11)") 
        try:
            #calc 12
            tax_data['GrossTaxLiability']=round(tax_data['TaxPayableOnRebate']+tax_data['EducationCess'])
        except Exception as e:
            log.append(e)
            errors.append("Error encountered while calculating 'Total Tax and Cess' (12)") 
        try:
            #calc 13
            tax_data['Section89']=getfval('Section89',data)
        except Exception as e:
            log.append(e)
            errors.append("Error encountered while calculating 'Relief u/s 89' (13)") 
        try:
            #calc 14
            tax_data['NetTaxLiability']=RndMax0(tax_data['GrossTaxLiability']-tax_data['Section89'])
        except Exception as e:
            log.append(e)
            errors.append("Error encountered while calculationg 'Balance Tax After Relief' (7 to 14)")    

        try:
            #calc 15
            log.append("calling function 'calculate_interest'")
            res=calculate_interest(mytree,data,tax_data,ns)
            for x in res[0]:
                errors.append(x)
            for x in res[9]:
                log.append(x)
            if res!='err':
                tax_data['IntrstPayUs234A']=res[1]
                tax_data['IntrstPayUs234B']=res[2]
                tax_data['IntrstPayUs234C']=res[3]
                tax_data['LateFilingFee234F']=res[4]
            else:
                errors.append('Error encountered while calculationg Interest u/s 234A, 234B, 234C, 234F')
        except Exception as e:
            log.append(e)
            errors.append("Error encountered while calculationg Interest u/s 234A, 234B, 234C, 234F")  

        #calc 16
        if res!='err':
            tax_data['TotalIntrstPay']=res[1]+res[2]+res[3]+res[4]
        else:
            errors.append("Error encountered while calculating 'Total Interest, Fee Payable' (16)") 

        try:
            #calc 17
            tax_data['TotTaxPlusIntrstPay']=tax_data['NetTaxLiability'] + tax_data['TotalIntrstPay']
        except Exception as e:
            log.append(e)
            errors.append("Error encountered while calculating 'Total Tax, Fee and Interest' (17)") 

        #calc 23
        if res!='err':
            tax_data['AdvanceTax']=res[5]
            tax_data['TDS']=res[6]
            tax_data['TCS']=res[7]
            tax_data['SelfAssessmentTax']=res[8]
        else:
            errors.append("Error encountered while calculating 'Advance tax, TDS, TCS and Self Assessment Taxes Paid' (23-a,b,c,d)") 

        #calc 24
        if res!='err':
            tax_data['TotalTaxesPaid']= max(0,res[5]+res[6]+res[7]+res[8])
        else:
            errors.append("Error encountered while calculating 'Total Taxes Paid' (24)") 

        try:
            #calc 25
            tax_data['BalTaxPayable']= round_nearest(max(tax_data['TotTaxPlusIntrstPay']-tax_data['TotalTaxesPaid'],0),10)
        except Exception as e:
            log.append(e)
            errors.append("Error encountered while calculating 'Amount Payable' (25)") 
        try:
            #calc 26
            tax_data['RefundDue']=round_nearest(max(tax_data['TotalTaxesPaid']-tax_data['TotTaxPlusIntrstPay'],0),10)
        except Exception as e:
            log.append(e)
            errors.append("Error encountered while calculating 'Refund' (26)") 

        res1=calc_TDS_from_sal(mytree,ns)
        res2=calc_TDS_oth_sal(mytree,ns)
        res3=calc_TDS_3(mytree,ns)
        res4=calc_TCS_from_sal(mytree,ns)
        return errors,tax_data,chap6a,don_cash,don_oth,tot_don,elig_don,don_cash_gga,don_oth_gga,tot_don_gga,elig_don_gga,res1[0],res2[0],res3[0],res4[0],'ok',log
    except Exception as e:
        log.append(e)
        errors.append("Unknown error encountered while calculating ITR1")
        return errors,tax_data,chap6a,don_cash,don_oth,tot_don,elig_don,don_cash_gga,don_oth_gga,tot_don_gga,elig_don_gga,res1[0],res2[0],res3[0],res4[0],'err',log