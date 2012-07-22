import re
import types



def IsDate(varObj):
 
    if len(varObj) == 10:
        rule = '(([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8]))))|((([0-9]{2})(0[48]|[2468][048]|[13579][26])|((0[48]|[2468][048]|[3579][26])00))-02-29)$/'
        match = re.match( rule , varObj )
        if match:
            return True
        return False
    return False

def IsEmail(varObj):
 
    rule = '[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$'
    match = re.match( rule , varObj )
 
    if match:
        return True
    return False

def IsEmpty(varObj):
 
    if len(varObj) == 0:
        return True
    return False


def IsNumber(varObj):
 
    return type(varObj) is types.IntType

def IsString(varObj):
 
    return type(varObj) is types.StringType