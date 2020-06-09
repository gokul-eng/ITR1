from ITR1_Constants_Common_Functions import *

def prep_input_file():
    rem=[]
    #delete chap6 separatly
    rem.append('GrossSalary')
    rem.append('TotalAllwncExemptUs10')
    rem.append('NetSalary')
    rem.append('DeductionUs16ia')
    rem.append('DeductionUs16')
    rem.append('IncomeFromSal')
    rem.append('AnnualValue')
    rem.append('StandardDeduction')
    rem.append('TotalIncomeOfHP')
    rem.append('IncomeOthSrc')
    rem.append('GrossTotIncome')
    rem.append('TotalChapVIADeductions')
    rem.append('TotalIncome')
    rem.append('ExemptIncAgriOthUs10Total')
    rem.append('TotalTaxPayable')
    rem.append('Rebate87A')
    rem.append('TaxPayableOnRebate')
    rem.append('EducationCess')
    rem.append('GrossTaxLiability')
    rem.append('NetTaxLiability')
    rem.append('IntrstPayUs234A')
    rem.append('IntrstPayUs234B')
    rem.append('IntrstPayUs234C')
    rem.append('LateFilingFee234F')
    rem.append('TotalIntrstPay')
    rem.append('TotTaxPlusIntrstPay')
    rem.append('AdvanceTax')
    rem.append('TDS')
    #skipping TCS
    rem.append('SelfAssessmentTax')
    rem.append('TotalTaxesPaid')
    rem.append('BalTaxPayable')
    rem.append('RefundDue')
    rem.append('TotalTDSonSalaries')
    rem.append('TotalTDSonOthThanSals')
    rem.append('TotalTDS3Details')
    rem.append('TotalSchTCS')
    rem.append('TotalTaxPayments')
    rem.append('DonationAmt')
    rem.append('EligibleDonationAmt')
    rem.append('TotDon100PercentCash')
    rem.append('TotDon100PercentOtherMode')
    rem.append('TotDon100Percent')
    rem.append('TotEligibleDon100Percent')
    rem.append('TotDon50PercentNoApprReqdCash')
    rem.append('TotDon50PercentNoApprReqdOtherMode')
    rem.append('TotDon50PercentNoApprReqd')
    rem.append('TotEligibleDon50Percent')
    rem.append('TotDon100PercentApprReqdCash')
    rem.append('TotDon100PercentApprReqdOtherMode')
    rem.append('TotDon100PercentApprReqd')
    rem.append('TotEligibleDon100PercentApprReqd')
    rem.append('TotDon50PercentApprReqdCash')
    rem.append('TotDon50PercentApprReqdOtherMode')
    rem.append('TotDon50PercentApprReqd')
    rem.append('TotEligibleDon50PercentApprReqd')
    rem.append('TotalDonationsUs80GCash')
    rem.append('TotalDonationsUs80GOtherMode')
    rem.append('TotalDonationsUs80G')
    rem.append('TotalEligibleDonationsUs80G')
    rem.append('TotalDonationAmtCash80GGA')
    rem.append('TotalDonationAmtOtherMode80GGA')
    rem.append('TotalDonationsUs80GGA')
    rem.append('TotalEligibleDonationAmt80GGA')

    master = open(FILE_NAME_WITH_PATH_XML_FILE, 'r')
    finput=open('C:\\Users\\gokul\\Google Drive\\Gokul Learning\\Indian IT Project\\Master Excel\\input.xml','w')
    skip=False
    while True: 
        line_master = master.readline()
        if not line_master:
            break
        if line_master[line_master.find(':')+1:line_master.find('>')].strip() =='DeductUndChapVIA':
            skip=not skip
            continue
        if line_master[line_master.find(':')+1:line_master.find('>')].strip() not in rem and skip==False:
            finput.write( line_master)
    master.close()
    finput.close()
