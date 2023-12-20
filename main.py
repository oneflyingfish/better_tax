from prettytable import PrettyTable
import numpy as np

def GetTax(income_year, bonus_year,stable_bonus_year, accumulation_found_year,special_deduction_year, annuity_year, show=False):
    nobonus=np.array(range(0,int(bonus_year*100)+1))
    income_year=income_year+nobonus/100.0
    bonus_year=bonus_year-nobonus/100.0+stable_bonus_year
   
    Free=60000
        
    income_total=np.where(income_year-(accumulation_found_year)-(special_deduction_year+annuity_year)-Free>=0,income_year-(accumulation_found_year)-(special_deduction_year+annuity_year)-Free,0)
    income_tax=np.where(
        income_total<=36000,
        income_total*0.03,
        np.where(
            income_total<=144000,
            income_total*0.10-2520,
            np.where(
                income_total<=300000,
                income_total*0.2-16920,
                np.where(
                    income_total<=420000,
                    income_total*0.25-31920,
                    np.where(
                        income_total<=660000,
                        income_total*0.3-52920,
                        np.where(
                            income_total<=960000,
                            income_total*0.35-85920,
                            income_total*0.45-181920
                        )
                    )
                )
            )
        )
    )
    
    bonus_tax=np.where(
        bonus_year/12<=3000,
        bonus_year*0.03,
        np.where(
            bonus_year/12<=12000,
            bonus_year*0.10-210,
            np.where(
                bonus_year/12<=25000,
                bonus_year*0.20-1410,
                np.where(
                    bonus_year/12<=35000,
                    bonus_year*0.25-2660,
                    np.where(
                        bonus_year/12<=55000,
                        bonus_year*0.30-4410,
                        np.where(
                            bonus_year/12<=55000,
                            bonus_year*0.35-7160,
                            bonus_year*0.45-15160
                        )
                    )
                )
            )
        )
    )
    
    total=income_tax+bonus_tax
    
    min_index=np.argmin(total)
    if show:
        print("如果您不调整奖金发放，缴税如下:")
        data=[
            ["全年税前收入",str(np.round(income_year,2)[0]),"全年一次性奖金收入",str(np.round(bonus_year,2)[0])],
            ["专项扣除",str(np.round(accumulation_found_year,2)),"",""],
            ["专项附加扣除+个人养老金",str(np.round(special_deduction_year+annuity_year,2)),"",""],
            ["年度个税起征点",str(np.round(Free,2)),"",""],
            ["年度工资应纳税所得额",str(np.round(income_total,2)[0]),"年度奖金应纳税所得额",str(np.round(bonus_year,2)[0])],
            ["年综合所得个税",str(np.round(income_tax,2)[0]),"全年一次性奖金税",str(np.round(bonus_tax,2)[0])],
        ]
        
        
        table=PrettyTable(["年综合所得个税（工资税）","个税金额（元）","全年一次性奖金税（奖金税）","奖金金额（元）"])
        table.align["年综合所得个税（工资税）"] = "l"
        table.align["个税金额（元）"] = "l"
        table.align["全年一次性奖金税（奖金税）"] = "l"
        table.align["奖金金额（元）"] = "l"
        for row in data:
            table.add_row(row)
        print(table)
        print("累计个税：",total[0],"\n")
        
        print("=>经过计算，对您的缴税建议：")
        data=[
            ["全年税前收入",str(np.round(income_year,2)[min_index]),"全年一次性奖金收入",str(np.round(bonus_year,2)[min_index])],
            ["专项扣除",str(np.round(accumulation_found_year,2)),"",""],
            ["专项附加扣除+个人养老金",str(np.round(special_deduction_year+annuity_year,2)),"",""],
            ["年度个税起征点",str(np.round(Free,2)),"",""],
            ["年度工资应纳税所得额",str(np.round(income_total,2)[min_index]),"年度奖金应纳税所得额",str(np.round(bonus_year,2)[min_index])],
            ["年综合所得个税",str(np.round(income_tax,2)[min_index]),"全年一次性奖金税",str(np.round(bonus_tax,2)[min_index])],
        ]

        table=PrettyTable(["年综合所得个税（工资税）","个税金额（元）","全年一次性奖金税（奖金税）","奖金金额（元）"])
        table.align["年综合所得个税（工资税）"] = "l"
        table.align["个税金额（元）"] = "l"
        table.align["全年一次性奖金税（奖金税）"] = "l"
        table.align["奖金金额（元）"] = "l"
        for row in data:
            table.add_row(row)
        print(table)
        print("累计个税：",round(total[min_index]),"\n")
        print("[*结论*] 可为您减少扣税：", round(total[0]-total[min_index],2),"元")
    
    return total

def ReadFloat(name)->float:
    while True:
        try:
            i=input(name)
            if i.endswith("%"):
                return float(i.strip("%"))/100.0
            else:
                return float(i)
        except Exception as e:
            continue

def automode():
    income_year=ReadFloat("请输入全年税前收入（单位：元）：")
    bonus_year=ReadFloat("请输入可调节奖金（单位：元）：")
    stable_bonus_year=ReadFloat("请输入其它奖金（不可调整部分，单位：元）：")
    accumulation_found_year=ReadFloat("请输入全年累计社保公积金（个人支付部分，单位：元）：")
    special_deduction_year=ReadFloat("请输入年度专项附加扣除（单位：元）：")
    annuity_year=ReadFloat("请输入年度个人养老金（单位：元）：")

    GetTax(income_year,bonus_year,stable_bonus_year,accumulation_found_year,special_deduction_year,annuity_year,True)

def ReadDetail(tips:str,addition:str):
    months=[]
    while len(months)<12:
        income_month=ReadFloat(f"请输入您的{tips}（{len(months)+1}月份{addition}）：")
        if len(months)<11:
            count=int(ReadFloat(f"请输入上述{tips}持续月数："))
            if len(months)+count>12:
                count=12-len(months)
        else:
            count=1
        
        months+=[income_month]*count
    return np.array(months[:12])

def handlemode():
    income_months=ReadDetail("月薪【税前】",", 单位：元")
    income_year=np.sum(income_months)
        
    income_year+=ReadFloat("请输入全年其它劳务所得（不含年终奖金，单位：元）：")
    bonus_year=ReadFloat("请输入可调节奖金（单位：元）：")
    stable_bonus_year=ReadFloat("请输入其它单独计税奖金（不可调整部分, 单位：元）：")  
          
    accumulation_found_ratios=ReadDetail("社保公积金缴纳比例", "， 小数, -1表示最高(12+2+0.3)%")
    accumulation_found_ratios=np.where(accumulation_found_ratios<0,0.143,accumulation_found_ratios)
    accumulation_found_year=np.sum(income_months*accumulation_found_ratios)
    annuity_ratios=ReadDetail("个人养老金缴纳比例", "， 小数, -1表示最高（8）%")
    annuity_ratios=np.where(annuity_ratios<0,0.143,annuity_ratios)
    annuity_year=np.sum(income_months*annuity_ratios)
    
    special_deduction_year=ReadFloat("请输入年度专项附加扣除（单位：元）：")
    GetTax(income_year,bonus_year,stable_bonus_year,accumulation_found_year,special_deduction_year,annuity_year,True)

def main():
    while True:
        end=int(ReadFloat("请选择程序运行模式（0：自助模式；1：手动模式）："))
        if end==0:
            handlemode()
        elif end==1:
            automode()
        
        while True:
            end=input("请输入\"exit\"退出，输入\"continue\"继续：")
            if end.lower()=="exit":
                return
            elif end.lower()=="continue":
                break
    
if __name__ == '__main__':
    main()