import datetime as dt
from lxml import etree
import xmlschema
from ITR1_Constants_Common_Functions import *

def Generate_XML(data,mytree,ns,tax_data,chap6a,l_don_cash,l_don_oth,l_tot_don,l_elig_don,don_cash_gga,don_oth_gga,tot_don_gga,elig_don_gga,total_TDS_from_sal,total_TDS_oth_sal,total_TDS_3,total_TCS):   #l-> list
    log=[]
    try:
        etree.register_namespace('ITRETURN',"http://incometaxindiaefiling.gov.in/main")
        etree.register_namespace('ITR1FORM',"http://incometaxindiaefiling.gov.in/ITR1")
        etree.register_namespace('ITRForm',"http://incometaxindiaefiling.gov.in/master")
        etree.register_namespace('xsi',"http://www.w3.org/2001/XMLSchema-instance")
        root = etree.Element("{http://incometaxindiaefiling.gov.in/main}ITR")
        root_ITR1 = etree.SubElement(root, "{http://incometaxindiaefiling.gov.in/ITR1}ITR1")
        x='http://incometaxindiaefiling.gov.in/master'

        CreationDate = dt.datetime.today().strftime("%Y-%m-%d")
        log.append('Generate ceation info')
        e1=etree.SubElement(root_ITR1, "{http://incometaxindiaefiling.gov.in/master}CreationInfo")
        etree.SubElement(e1, "{" + x + "}SWVersionNo").text='R1'
        etree.SubElement(e1, "{" + x + "}SWCreatedBy").text='SW92201920'
        etree.SubElement(e1, "{" + x + "}XMLCreatedBy").text='SW92201920'
        etree.SubElement(e1, "{" + x + "}XMLCreationDate").text=CreationDate
        etree.SubElement(e1, "{" + x + "}IntermediaryCity").text='Delhi'
        etree.SubElement(e1, "{" + x + "}Digest").text='-'

        e1=etree.SubElement(root_ITR1, "{http://incometaxindiaefiling.gov.in/master}Form_ITR1")
        etree.SubElement(e1, "{" + x + "}FormName").text='ITR-1'
        etree.SubElement(e1, "{" + x + "}Description").text='For Indls having Income from Salary, Pension, family pension and Interest'
        etree.SubElement(e1, "{" + x + "}AssessmentYear").text=str(ASS_YEAR)
        etree.SubElement(e1, "{" + x + "}SchemaVer").text='Ver1.1'
        etree.SubElement(e1, "{" + x + "}FormVer").text='Ver1.0'

        #Personal Info
        log.append('Generate personal info')
        e1=etree.SubElement(root_ITR1, "{http://incometaxindiaefiling.gov.in/master}PersonalInfo")
        ver_root=mytree.find('.//ITRForm:PersonalInfo',ns)
        for node in list(ver_root): #e2
            if rn(node.tag)=='AssesseeName' or rn(node.tag)=='Address':
                e2= etree.SubElement(e1, node.tag)
                for detl in list(node):
                    etree.SubElement(e2, detl.tag).text=detl.text
            else:
                etree.SubElement(e1, node.tag).text=node.text
        
        #Filing Status
        log.append('Generate Filing Status')
        e1=etree.SubElement(root_ITR1, "{http://incometaxindiaefiling.gov.in/master}FilingStatus")
        ver_root=mytree.find('.//ITRForm:FilingStatus',ns)
        for node in list(ver_root): #e2
            etree.SubElement(e1, node.tag).text=node.text
        
        #Income Deductions
        log.append('Generate ITR1_IncomeDeductions')
        e1=etree.SubElement(root_ITR1, "{http://incometaxindiaefiling.gov.in/master}ITR1_IncomeDeductions")
        etree.SubElement(e1, "{" + x + "}GrossSalary").text= str(round(tax_data['GrossSalary']))
        etree.SubElement(e1, "{" + x + "}Salary").text= str(getfval('Salary',data)) 
        etree.SubElement(e1, "{" + x + "}PerquisitesValue").text= str(getfval('PerquisitesValue',data)) 
        etree.SubElement(e1, "{" + x + "}ProfitsInSalary").text=str(getfval('ProfitsInSalary',data))

        #Allowance Exempt u/s 10
        log.append('Generate AllwncExemptUs10')
        e2=etree.SubElement(e1, "{http://incometaxindiaefiling.gov.in/master}AllwncExemptUs10")
        for deduction in mytree.findall('.//ITRForm:AllwncExemptUs10',ns):
            for snode in deduction.findall('.//ITRForm:AllwncExemptUs10Dtls',ns):
                e3= etree.SubElement(e2, snode.tag)
                for nodes in list(snode):
                    etree.SubElement(e3, nodes.tag).text=nodes.text
        etree.SubElement(e2, "{" + x + "}TotalAllwncExemptUs10").text=str(round(tax_data['TotalAllwncExemptUs10']))

        etree.SubElement(e1, "{" + x + "}NetSalary").text=str(round(tax_data['NetSalary']))
        etree.SubElement(e1, "{" + x + "}DeductionUs16").text=str(round(tax_data['DeductionUs16']))
        etree.SubElement(e1, "{" + x + "}DeductionUs16ia").text=str(round(tax_data['DeductionUs16ia']))
        etree.SubElement(e1, "{" + x + "}EntertainmentAlw16ii").text=str(round(getfval('EntertainmentAlw16ii',data)))
        etree.SubElement(e1, "{" + x + "}ProfessionalTaxUs16iii").text=str(round(getfval('ProfessionalTaxUs16iii',data)))
        etree.SubElement(e1, "{" + x + "}IncomeFromSal").text=str(round(tax_data['IncomeFromSal']))
        if 'TypeOfHP' in data:
            etree.SubElement(e1, "{" + x + "}TypeOfHP").text=gettval('TypeOfHP',data).upper()
        if 'GrossRentReceived' in data:
            etree.SubElement(e1, "{" + x + "}GrossRentReceived").text= gettval('GrossRentReceived',data)
        if 'TaxPaidlocalAuth' in data:
            etree.SubElement(e1, "{" + x + "}TaxPaidlocalAuth").text= gettval('TaxPaidlocalAuth',data)
        if tax_data['AnnualValue'] !=0:
            etree.SubElement(e1, "{" + x + "}AnnualValue").text= str(round(tax_data['AnnualValue']))
        if tax_data['StandardDeduction'] !=0:
            etree.SubElement(e1, "{" + x + "}StandardDeduction").text= str(round(tax_data['StandardDeduction']))
        if 'InterestPayable' in data:
            etree.SubElement(e1, "{" + x + "}InterestPayable").text= gettval('InterestPayable',data)
        if 'ArrearsUnrealizedRentRcvd' in data:
            etree.SubElement(e1, "{" + x + "}ArrearsUnrealizedRentRcvd").text= gettval('ArrearsUnrealizedRentRcvd',data)
        etree.SubElement(e1, "{" + x + "}TotalIncomeOfHP").text= str(round(tax_data['TotalIncomeOfHP']))
        etree.SubElement(e1, "{" + x + "}IncomeOthSrc").text= str(round(tax_data['IncomeOthSrc']))
        #Inc from oth sources
        log.append('Generate OthersInc')
        e2=etree.SubElement(e1, "{http://incometaxindiaefiling.gov.in/master}OthersInc")
        for deduction in mytree.findall('.//ITRForm:OthersInc',ns):
            for snode in deduction.findall('.//ITRForm:OthersIncDtlsOthSrc',ns):
                e3= etree.SubElement(e2, snode.tag)
                for nodes in list(snode):
                    etree.SubElement(e3, nodes.tag).text=nodes.text
        if 'DeductionUs57iia' in data:
            etree.SubElement(e1, "{" + x + "}DeductionUs57iia").text= str(round(getfval('DeductionUs57iia',data)))
        etree.SubElement(e1, "{" + x + "}GrossTotIncome").text= str(round(tax_data['GrossTotIncome']))
        
        #deductions Chapter6A
        log.append('Generate UsrDeductUndChapVIA')
        e2=etree.SubElement(e1, "{http://incometaxindiaefiling.gov.in/master}UsrDeductUndChapVIA")
        deduction =mytree.find('.//ITRForm:UsrDeductUndChapVIA',ns)
        for lst in list(deduction):
            if rn(lst.tag)=='Section80DHealthInsPremium':
                e3= etree.SubElement(e2, lst.tag)
                for nodes in list(lst):
                    etree.SubElement(e3, nodes.tag).text=nodes.text
            elif rn(lst.tag)=='Section80GGA':
                usr_gga = etree.SubElement(e2, lst.tag) #only for GGA, the usr section = total donations and not eligible donations!
                #totalusr6a+=chap6a['Section80GGA']  'This will be updated in the GGA section futher down
            else:
                if rn(lst.tag)!='TotalChapVIADeductions':
                    etree.SubElement(e2, lst.tag).text=lst.text
        deduction =mytree.find('.//ITRForm:UsrDeductUndChapVIA',ns)
        totalusr6a=0
        for node in deduction.iter():
            if rn(node.tag) not in ('UsrDeductUndChapVIA','TotalChapVIADeductions','Section80GGA','Section80DHealthInsPremium','HealthInsurancePremium','MedicalExpenditure','PreventiveHealthCheckUp','Section80DDUsrType','Section80DDBUsrType','Section80UUsrType'):
                totalusr6a+=float(nz(node.text))
        usr_total_ded = etree.SubElement(e2, "{" + x + "}TotalChapVIADeductions")
        usr_total_ded.text = str(round(totalusr6a)) # GGA will be addded to this further down
        
        log.append('Generate DeductUndChapVIA')
        e2=etree.SubElement(e1, "{http://incometaxindiaefiling.gov.in/master}DeductUndChapVIA")
        etree.SubElement(e2, "{" + x + "}Section80C").text= str(round(chap6a['a']))
        etree.SubElement(e2, "{" + x + "}Section80CCC").text= str(round(chap6a['b']))
        etree.SubElement(e2, "{" + x + "}Section80CCDEmployeeOrSE").text= str(round(chap6a['c']))
        etree.SubElement(e2, "{" + x + "}Section80CCD1B").text= str(round(chap6a['d']))
        etree.SubElement(e2, "{" + x + "}Section80CCDEmployer").text= str(round(chap6a['e']))
        etree.SubElement(e2, "{" + x + "}Section80D").text= str(round(chap6a['g']))
        etree.SubElement(e2, "{" + x + "}Section80DD").text= str(round(chap6a['h']))
        etree.SubElement(e2, "{" + x + "}Section80DDB").text= str(round(chap6a['i']))
        etree.SubElement(e2, "{" + x + "}Section80E").text= str(round(chap6a['j']))
        etree.SubElement(e2, "{" + x + "}Section80EE").text= str(round(chap6a['k']))
        etree.SubElement(e2, "{" + x + "}Section80G").text= str(round(chap6a['l']))
        etree.SubElement(e2, "{" + x + "}Section80GG").text= str(round(chap6a['m']))
        etree.SubElement(e2, "{" + x + "}Section80GGA").text= str(round(chap6a['n']))
        etree.SubElement(e2, "{" + x + "}Section80GGC").text= str(round(chap6a['o']))
        etree.SubElement(e2, "{" + x + "}Section80U").text= str(round(chap6a['r']))
        etree.SubElement(e2, "{" + x + "}Section80CCG").text= str(round(chap6a['f']))
        etree.SubElement(e2, "{" + x + "}Section80TTA").text= str(round(chap6a['p']))
        etree.SubElement(e2, "{" + x + "}Section80TTB").text= str(round(chap6a['q']))
        etree.SubElement(e2, "{" + x + "}TotalChapVIADeductions").text= str(round(tax_data['TotalChapVIADeductions']))

        etree.SubElement(e1, "{" + x + "}TotalIncome").text= str(round(tax_data['TotalIncome']))

        #Exempt Income for reporting purposes
        log.append('Generate ExemptIncAgriOthUs10')
        e2=etree.SubElement(e1, "{http://incometaxindiaefiling.gov.in/master}ExemptIncAgriOthUs10")
        for deduction in mytree.findall('.//ITRForm:ExemptIncAgriOthUs10',ns):
            for snode in deduction.findall('.//ITRForm:ExemptIncAgriOthUs10Dtls',ns):
                e3= etree.SubElement(e2, snode.tag)
                for nodes in list(snode):
                    etree.SubElement(e3, nodes.tag).text=nodes.text
        etree.SubElement(e2, "{" + x + "}ExemptIncAgriOthUs10Total").text= str(round(tax_data['ExemptIncAgriOthUs10Total']))
        
        #Tax Computation
        log.append('Generate ITR1_TaxComputation')
        e1=etree.SubElement(root_ITR1, "{http://incometaxindiaefiling.gov.in/master}ITR1_TaxComputation")
        etree.SubElement(e1, "{" + x + "}TotalTaxPayable").text= str(round(tax_data['TotalTaxPayable']))
        etree.SubElement(e1, "{" + x + "}Rebate87A").text= str(round(tax_data['Rebate87A']))
        etree.SubElement(e1, "{" + x + "}TaxPayableOnRebate").text= str(round(tax_data['TaxPayableOnRebate']))
        etree.SubElement(e1, "{" + x + "}EducationCess").text= str(round(tax_data['EducationCess']))
        etree.SubElement(e1, "{" + x + "}GrossTaxLiability").text= str(round(tax_data['GrossTaxLiability']))
        etree.SubElement(e1, "{" + x + "}Section89").text= str(round(tax_data['Section89']))
        etree.SubElement(e1, "{" + x + "}NetTaxLiability").text= str(round(tax_data['NetTaxLiability']))
        etree.SubElement(e1, "{" + x + "}TotalIntrstPay").text= str(round(tax_data['TotalIntrstPay']))
        e2=etree.SubElement(e1, "{http://incometaxindiaefiling.gov.in/master}IntrstPay")
        etree.SubElement(e2, "{" + x + "}IntrstPayUs234A").text= str(round(tax_data['IntrstPayUs234A']))
        etree.SubElement(e2, "{" + x + "}IntrstPayUs234B").text= str(round(tax_data['IntrstPayUs234B']))
        etree.SubElement(e2, "{" + x + "}IntrstPayUs234C").text= str(round(tax_data['IntrstPayUs234C']))
        etree.SubElement(e2, "{" + x + "}LateFilingFee234F").text= str(round(tax_data['LateFilingFee234F']))

        etree.SubElement(e1, "{" + x + "}TotTaxPlusIntrstPay").text= str(round(tax_data['TotTaxPlusIntrstPay']))

        #Tax Paid
        log.append('Generate TaxPaid')
        e1=etree.SubElement(root_ITR1, "{http://incometaxindiaefiling.gov.in/master}TaxPaid")
        e2=etree.SubElement(e1, "{http://incometaxindiaefiling.gov.in/master}TaxesPaid")
        etree.SubElement(e2, "{" + x + "}AdvanceTax").text= str(round(tax_data['AdvanceTax']))
        etree.SubElement(e2, "{" + x + "}TDS").text= str(round(tax_data['TDS']))
        etree.SubElement(e2, "{" + x + "}TCS").text= str(round(tax_data['TCS']))
        etree.SubElement(e2, "{" + x + "}SelfAssessmentTax").text= str(round(tax_data['SelfAssessmentTax']))
        etree.SubElement(e2, "{" + x + "}TotalTaxesPaid").text= str(round(tax_data['TotalTaxesPaid']))
        
        etree.SubElement(e1, "{" + x + "}BalTaxPayable").text= str(round(tax_data['BalTaxPayable']))

        #Refund Due
        log.append('Generate Refund')
        e1=etree.SubElement(root_ITR1, "{http://incometaxindiaefiling.gov.in/master}Refund")
        etree.SubElement(e1, "{" + x + "}RefundDue").text= str(round(tax_data['RefundDue']))
        e2=etree.SubElement(e1, "{http://incometaxindiaefiling.gov.in/master}BankAccountDtls")
        bankdtls =mytree.find('.//ITRForm:BankAccountDtls',ns)
        for lst in list(bankdtls):
            if rn(lst.tag)=='AddtnlBankDetails':
                e3= etree.SubElement(e2, lst.tag)
                for nodes in list(lst):
                    etree.SubElement(e3, nodes.tag).text=nodes.text
        
        # #Schedule 80G
        # e1=etree.SubElement(root_ITR1, "{http://incometaxindiaefiling.gov.in/master}Schedule80G")
        # s80g_root=mytree.find('.//ITRForm:Schedule80G',ns)
        # row_count=0
        # gtot=[0,0,0,0]  #grand totals
        # gtot_index=0
        # for don_type in list(s80g_root): #e2
        #     stot=[0,0,0,0] #sub totals
        #     if rn(don_type.tag)=='Don100Percent' or rn(don_type.tag)=='Don50PercentNoApprReqd' or rn(don_type.tag)=='Don100PercentApprReqd' or rn(don_type.tag)=='Don50PercentApprReqd':
        #         stot_index=0
        #         e2= etree.SubElement(e1, don_type.tag)
        #         for don in list(don_type):
        #             if rn(don.tag)=='DoneeWithPan':
        #                 e3=etree.SubElement(e2, don.tag)
        #                 for donee in list(don):
        #                     if rn(donee.tag)=='AddressDetail':
        #                         e4=etree.SubElement(e3, donee.tag)
        #                         for add in list(donee):
        #                             etree.SubElement(e4, add.tag).text=add.text
        #                     else:
        #                         if rn(donee.tag)=='DonationAmtCash':
        #                             etree.SubElement(e3, donee.tag).text=donee.text
        #                             stot[0]+=l_don_cash[row_count]
        #                         elif rn(donee.tag)=='DonationAmtOtherMode':
        #                             etree.SubElement(e3, donee.tag).text=donee.text
        #                             stot[1]+=l_don_oth[row_count]
        #                         elif rn(donee.tag)=='DonationAmt':
        #                             etree.SubElement(e3, donee.tag).text=str(round(l_tot_don[row_count]))
        #                             stot[2]+=l_tot_don[row_count]
        #                         elif rn(donee.tag)=='EligibleDonationAmt':
        #                             etree.SubElement(e3, donee.tag).text=str(round(l_elig_don[row_count]))
        #                             stot[3]+=l_elig_don[row_count]
        #                             row_count+=1
        #                         else:
        #                             etree.SubElement(e3, donee.tag).text=donee.text
        #             else:  
        #                 etree.SubElement(e2, don.tag).text=str(round(stot[stot_index]))
        #                 stot_index+=1
        #     else:
        #         etree.SubElement(e1, don_type.tag).text=str(round(gtot[gtot_index]))
        #         gtot_index+=1
        #     for i in range(0,4):
        #         gtot[i]+=stot[i]

        #Schedule 80G
        log.append('Generate Schedule80G')
        e1=etree.SubElement(root_ITR1, "{http://incometaxindiaefiling.gov.in/master}Schedule80G")
        s80g_root=mytree.find('.//ITRForm:Schedule80G',ns)
        row_count=0
        gtot=[0,0,0,0]  #grand totals
        for don_type in list(s80g_root): #e2
            stot=[0,0,0,0] #sub totals
            if rn(don_type.tag)=='Don100Percent' or rn(don_type.tag)=='Don50PercentNoApprReqd' or rn(don_type.tag)=='Don100PercentApprReqd' or rn(don_type.tag)=='Don50PercentApprReqd':
                e2= etree.SubElement(e1, don_type.tag)
                for don in list(don_type):
                    if rn(don.tag)=='DoneeWithPan':
                        e3=etree.SubElement(e2, don.tag)
                        for donee in list(don):
                            if rn(donee.tag)=='AddressDetail':
                                e4=etree.SubElement(e3, donee.tag)
                                for add in list(donee):
                                    etree.SubElement(e4, add.tag).text=add.text
                            else:
                                if rn(donee.tag)=='DonationAmtCash':
                                    etree.SubElement(e3, donee.tag).text=donee.text
                                    stot[0]+=l_don_cash[row_count]
                                elif rn(donee.tag)=='DonationAmtOtherMode':
                                    etree.SubElement(e3, donee.tag).text=donee.text
                                    stot[1]+=l_don_oth[row_count]
                                    etree.SubElement(e3, "{" + x + "}DonationAmt").text=str(round(l_tot_don[row_count]))
                                    stot[2]+=l_tot_don[row_count]
                                    etree.SubElement(e3, "{" + x + "}EligibleDonationAmt").text=str(round(l_elig_don[row_count]))
                                    stot[3]+=l_elig_don[row_count]
                                    row_count+=1
                                elif rn(donee.tag)=='DonationAmt' or rn(donee.tag)=='EligibleDonationAmt':
                                    continue
                                else:
                                    etree.SubElement(e3, donee.tag).text=donee.text
                    else:
                        continue
                if rn(don_type.tag)=='Don100Percent':
                    etree.SubElement(e2, "{" + x + "}TotDon100PercentCash").text=str(round(stot[0]))
                    etree.SubElement(e2, "{" + x + "}TotDon100PercentOtherMode").text=str(round(stot[1]))
                    etree.SubElement(e2, "{" + x + "}TotDon100Percent").text=str(round(stot[2]))
                    etree.SubElement(e2, "{" + x + "}TotEligibleDon100Percent").text=str(round(stot[3]))
                elif rn(don_type.tag)=='Don50PercentNoApprReqd':
                    etree.SubElement(e2, "{" + x + "}TotDon50PercentNoApprReqdCash").text=str(round(stot[0]))
                    etree.SubElement(e2, "{" + x + "}TotDon50PercentNoApprReqdOtherMode").text=str(round(stot[1]))
                    etree.SubElement(e2, "{" + x + "}TotDon50PercentNoApprReqd").text=str(round(stot[2]))
                    etree.SubElement(e2, "{" + x + "}TotEligibleDon50Percent").text=str(round(stot[3]))
                elif rn(don_type.tag)=='Don100PercentApprReqd':
                    etree.SubElement(e2, "{" + x + "}TotDon100PercentApprReqdCash").text=str(round(stot[0]))
                    etree.SubElement(e2, "{" + x + "}TotDon100PercentApprReqdOtherMode").text=str(round(stot[1]))
                    etree.SubElement(e2, "{" + x + "}TotDon100PercentApprReqd").text=str(round(stot[2]))
                    etree.SubElement(e2, "{" + x + "}TotEligibleDon100PercentApprReqd").text=str(round(stot[3]))
                elif rn(don_type.tag)=='Don50PercentApprReqd':
                    etree.SubElement(e2, "{" + x + "}TotDon50PercentApprReqdCash").text=str(round(stot[0]))
                    etree.SubElement(e2, "{" + x + "}TotDon50PercentApprReqdOtherMode").text=str(round(stot[1]))
                    etree.SubElement(e2, "{" + x + "}TotDon50PercentApprReqd").text=str(round(stot[2]))
                    etree.SubElement(e2, "{" + x + "}TotEligibleDon50PercentApprReqd").text=str(round(stot[3]))
                for i in range(0,4):
                    gtot[i]+=stot[i]
            else:
                continue
        etree.SubElement(e1, "{" + x + "}TotalDonationsUs80GCash").text=str(round(gtot[0]))
        etree.SubElement(e1, "{" + x + "}TotalDonationsUs80GOtherMode").text=str(round(gtot[1]))
        etree.SubElement(e1, "{" + x + "}TotalDonationsUs80G").text=str(round(gtot[2]))
        if tax_data['GrossTotIncome'] > 0:
            val=min(round(gtot[3],0),tax_data['GrossTotIncome'])
        else:
            val=0
        etree.SubElement(e1, "{" + x + "}TotalEligibleDonationsUs80G").text= str(round(val))

        #Schedule 80GGA
        log.append('Generate Schedule80GGA')
        row_count=0
        e1=etree.SubElement(root_ITR1, "{http://incometaxindiaefiling.gov.in/master}Schedule80GGA")
        s80gga_root=mytree.find('.//ITRForm:Schedule80GGA',ns)
        stot=[0,0,0,0] #sub totals
        for don_type in list(s80gga_root): #e2
            if rn(don_type.tag)=='DonationDtlsSciRsrchRuralDev':
                e2= etree.SubElement(e1, don_type.tag)
                for don in list(don_type):
                    if rn(don.tag)=='AddressDetail':
                        e3=etree.SubElement(e2, don.tag)
                        for add in list(don):
                            etree.SubElement(e3, add.tag).text=add.text
                    elif rn(don.tag).find('Donation')!=-1:
                        if rn(don.tag)=='DonationAmtCash':
                            etree.SubElement(e2, don.tag).text=don.text
                            stot[0]+=don_cash_gga[row_count]
                        elif rn(don.tag)=='DonationAmtOtherMode':
                            etree.SubElement(e2, don.tag).text=don.text
                            stot[1]+=don_oth_gga[row_count]
                            etree.SubElement(e2, "{" + x + "}DonationAmt").text=str(round(tot_don_gga[row_count]))
                            stot[2]+=tot_don_gga[row_count]
                            etree.SubElement(e2, "{" + x + "}EligibleDonationAmt").text=str(round(elig_don_gga[row_count]))
                            stot[3]+=elig_don_gga[row_count]
                            row_count+=1
                        else:
                            continue
                    else:
                        etree.SubElement(e2, don.tag).text=don.text
            else:
                continue
        etree.SubElement(e1, "{" + x + "}TotalDonationAmtCash80GGA").text=str(round(stot[0]))
        etree.SubElement(e1, "{" + x + "}TotalDonationAmtOtherMode80GGA").text=str(round(stot[1]))
        etree.SubElement(e1, "{" + x + "}TotalDonationsUs80GGA").text=str(round(stot[2]))
        etree.SubElement(e1, "{" + x + "}TotalEligibleDonationAmt80GGA").text=str(round(stot[3]))
        usr_gga.text = str(round(stot[2]))  #Updating GGA in the UsrDeductUndChapVIA section
        usr_total_ded.text = str(int(usr_total_ded.text) + round(stot[2])) #Updating total to include GGA in the UsrDeductUndChapVIA section

        #TDS from Sal
        log.append('Generate TDSonSalaries')
        e1=etree.SubElement(root_ITR1, "{http://incometaxindiaefiling.gov.in/master}TDSonSalaries")
        tds_root=mytree.find('.//ITRForm:TDSonSalaries',ns)
        for tds_type in list(tds_root): #e2
            if rn(tds_type.tag)=='TDSonSalary':
                e2= etree.SubElement(e1, tds_type.tag)
                for sal in list(tds_type):
                    if rn(sal.tag)=='EmployerOrDeductorOrCollectDetl':
                        e3=etree.SubElement(e2, sal.tag)
                        for detl in list(sal):
                            etree.SubElement(e3, detl.tag).text=detl.text
                    else:
                        etree.SubElement(e2, sal.tag).text=sal.text
        etree.SubElement(e1, "{" + x + "}TotalTDSonSalaries").text=str(round(total_TDS_from_sal))


        #TDS other than Sal
        log.append('Generate TDSonOthThanSals')
        e1=etree.SubElement(root_ITR1, "{http://incometaxindiaefiling.gov.in/master}TDSonOthThanSals")
        tds_root=mytree.find('.//ITRForm:TDSonOthThanSals',ns)
        for tds_type in list(tds_root): #e2
            if rn(tds_type.tag)=='TDSonOthThanSal':
                e2= etree.SubElement(e1, tds_type.tag)
                for sal in list(tds_type):
                    if rn(sal.tag)=='EmployerOrDeductorOrCollectDetl':
                        e3=etree.SubElement(e2, sal.tag)
                        for detl in list(sal):
                            etree.SubElement(e3, detl.tag).text=detl.text
                    else:
                        etree.SubElement(e2, sal.tag).text=sal.text
        etree.SubElement(e1, "{" + x + "}TotalTDSonOthThanSals").text=str(round(total_TDS_oth_sal))

        #TDS3
        log.append('Generate ScheduleTDS3Dtls')
        e1=etree.SubElement(root_ITR1, "{http://incometaxindiaefiling.gov.in/master}ScheduleTDS3Dtls")
        tds_root=mytree.find('.//ITRForm:ScheduleTDS3Dtls',ns)
        for tds_type in list(tds_root): #e2
            if rn(tds_type.tag)=='TDS3Details':
                e2= etree.SubElement(e1, tds_type.tag)
                for sal in list(tds_type):
                    if rn(sal.tag)=='EmployerOrDeductorOrCollectDetl':
                        e3=etree.SubElement(e2, sal.tag)
                        for detl in list(sal):
                            etree.SubElement(e3, detl.tag).text=detl.text
                    else:
                        etree.SubElement(e2, sal.tag).text=sal.text
        etree.SubElement(e1, "{" + x + "}TotalTDS3Details").text=str(round(total_TDS_3))


        #TCS
        log.append('Generate ScheduleTCS')
        e1=etree.SubElement(root_ITR1, "{http://incometaxindiaefiling.gov.in/master}ScheduleTCS")
        tds_root=mytree.find('.//ITRForm:ScheduleTCS',ns)
        for tds_type in list(tds_root): #e2
            if rn(tds_type.tag)=='TCS':
                e2= etree.SubElement(e1, tds_type.tag)
                for sal in list(tds_type):
                    if rn(sal.tag)=='EmployerOrDeductorOrCollectDetl':
                        e3=etree.SubElement(e2, sal.tag)
                        for detl in list(sal):
                            etree.SubElement(e3, detl.tag).text=detl.text
                    else:
                        etree.SubElement(e2, sal.tag).text=sal.text
        etree.SubElement(e1, "{" + x + "}TotalSchTCS").text=str(round(total_TCS))

        #Tax Paid
        log.append('Generate TaxPayments')
        total_it=0
        e1=etree.SubElement(root_ITR1, "{http://incometaxindiaefiling.gov.in/master}TaxPayments")
        tax_root=mytree.find('.//ITRForm:TaxPayments',ns)
        for payments in list(tax_root): #e2
            if rn(payments.tag)=='TaxPayment':
                e2= etree.SubElement(e1, payments.tag)
                for payment in list(payments):
                    etree.SubElement(e2, payment.tag).text=payment.text
                    if rn(payment.tag)=='Amt':
                        total_it+=int(payment.text)
        etree.SubElement(e1, "{" + x + "}TotalTaxPayments").text=str(round(total_it))

        #Verification
        log.append('Generate Verification')
        e1=etree.SubElement(root_ITR1, "{http://incometaxindiaefiling.gov.in/master}Verification")
        ver_root=mytree.find('.//ITRForm:Verification',ns)
        for node in list(ver_root): #e2
            if rn(node.tag)=='Declaration':
                e2= etree.SubElement(e1, node.tag)
                for detl in list(node):
                    etree.SubElement(e2, detl.tag).text=detl.text
            else:
                etree.SubElement(e1, node.tag).text=node.text

        #Preparer
        log.append('Generate TaxReturnPreparer')
        ver_root=mytree.find('.//ITRForm:TaxReturnPreparer',ns)
        if ver_root is not None:
            e1=etree.SubElement(root_ITR1, "{http://incometaxindiaefiling.gov.in/master}TaxReturnPreparer")
            for node in list(ver_root): #e2
                etree.SubElement(e1, node.tag).text=node.text

        #write xml file to disk
        tree=etree.ElementTree(root)
        #tree.write("C:\\Users\\gokul\\Google Drive\\Gokul Learning\\Indian IT Project\\Master Excel\\page.xml",xml_declaration=True,encoding='ISO-8859-1',method="xml", pretty_print=True)
        tree.write("/tmp/page.xml",xml_declaration=True,encoding='ISO-8859-1',method="xml", pretty_print=True) #AWS
        #validate xml against XSD
        #xml=etree.parse(FILE_NAME_WITH_PATH_XML_FILE)
        log.append('Validate xml against XSD')
        xs=etree.XMLSchema(etree.parse(FILE_NAME_WITH_PATH_XSD_FILE))
        try:
            xs.assertValid(tree)
            return 'ok','ok',tree, log
        except etree.DocumentInvalid as err:
            return 'Schema Error',str(err.error_log),tree, log
    except Exception as e:
        log.append(e)
        return "Critical Error","Critical Error","Critical Error", log