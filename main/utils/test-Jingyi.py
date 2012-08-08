from form_check import *

empty = IsEmpty("a")
print "empty"
print empty

email = IsEmail("")
print "email"
print email

ssn = IsSSN("123456789");
print "SSN"
print ssn

phone = IsDate("06/08/2022")
print "phone"
print phone