import re
import types
import time
import datetime

def IsEmpty(varObj):
    if len(varObj) == 0:
        return True
    return False

def IsEmail(varObj):
    if len(varObj) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", varObj) != None:
            return 1
    return 0

def IsSSN(varObj):
    if re.match(r"^(?!000|666)(?:[0-6][0-9]{2}|7(?:[0-6][0-9]|7[0-2]))(?!00)[0-9]{2}(?!0000)[0-9]{4}$", varObj) != None:
        return True 
    else:
        return False

def IsPhoneNumber(varObj):
    if len(varObj) < 10:
        return False
    try:
        float(varObj)
        return True
    except ValueError:
        return False
    
def IsDate(varObj):
    try:
        valid_date = time.strptime(varObj, '%m/%d/%Y')
        return True
    except ValueError:
        return False

def IsValidDate(varObj):
    if len(varObj) == 0:
        return False
    else:   
        try:
            format="%m/%d/%Y"
            date = datetime.datetime.strptime(varObj,format)
                
            if date.date() < datetime.datetime.now().date():
                return False
            else:
                return True
        except ValueError:
                return False
    
                
def IsNumber(varObj):
 
    return type(varObj) is types.IntType

def IsString(varObj):
 
    return type(varObj) is types.StringType