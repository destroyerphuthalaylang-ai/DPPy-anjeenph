#!/usr/bin/env python3

print("Enter a number less than 25")
number_less = int(input())

if number_less > 25:
   print("Error")
else:
   while number_less <= 25:
     print("Inside the loop, my variable is", number_less)
     number_less = number_less + 1 
