#def numbers():

 # for num in range (1, 21):
 #   if num is not 11 and num is not 13:
      
  #    print(num)

def lowest():
  nums = [12,234,123,56,678,45,7,3,567,2423,56,-2,345,6752,-34,345,0,0,2]

  lowest= nums[0]

  for n in nums:
    if (n < lowest):
      lowest = n

    
  print (lowest)



#numbers()
lowest()