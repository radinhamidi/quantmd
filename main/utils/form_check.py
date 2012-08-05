import re
import types

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
    
    
    
    
   
def IsZip(varObj):
    return True
    
def IsDate(varObj):
    return True

    if len(varObj) == 10:
        rule = '(([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8]))))|((([0-9]{2})(0[48]|[2468][048]|[13579][26])|((0[48]|[2468][048]|[3579][26])00))-02-29)$/'
        match = re.match( rule , varObj )
        if match:
            return True
        return False
    return False

def IsNumber(varObj):
 
    return type(varObj) is types.IntType

def IsString(varObj):
 
    return type(varObj) is types.StringType