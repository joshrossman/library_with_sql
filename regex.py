import re
#Regex checker to check user inpputed data.
def regex_checker(text,pattern,error):
    while True:
        try:
            month= text[5:7]
            days= text[8:]
            if re.match(pattern,text) and text!='':
                #Extra check to make sure that each month has valid amount of days (leap years not currently taken into account.)
                if pattern==r"^[1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]$":
                    if ((month == "09" or month == "04" or month == "06" or month == "11") and (0<int(days)<31)) or (month=="02" and 0<int(days)<30) or ((month=="01" or month=="03" or month=="05" or month=="07" or month =="08" or month =="10" or month=="12") and (0<int(days)<32)):
                        return text
                    else:
                        print(error)
                        text=input("New Input:")   
                else:
                    return text
            else:
                print('Error:',error)
                text=input("New Input:")
        except Exception as e:
            print(f'Error:{e}')
