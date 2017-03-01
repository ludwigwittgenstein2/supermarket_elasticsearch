import yaml
def main():
    topHouseHoldList = []
    CustomerOverTimeDict = {}
    Weekly_list=[]

    with open('/Users/Rick/Desktop/segments/topHouseHoldList', 'r' ) as f:
        topHouseHoldList =  yaml.load(f)
    f.close()

    with open('/Users/Rick/Desktop/segments/CustomerOverTimeDict.yaml', 'r' ) as f:
        CustomerOverTimeDict = yaml.load(f)
        f.close()

    count = 0
    for household_key, WeekDict in CustomerOverTimeDict.items():
        if household_key in topHouseHoldList:
            Weekly_list = [['week_no', 'sales_value']]
            for week_no, sales_value in sorted(WeekDict.items(), key=lambda k:int(k[0])):
                # for each week number, It is appending value to 2 D List
                Weekly_list.append([week_no,sales_value])
            print"*"*30
            print "Customer :", household_key,"Week No:" , len(Weekly_list) - 1
            print"*"*30
            print household_key, Weekly_list
            print"#"*30
           


if __name__ == "__main__":
    main()
