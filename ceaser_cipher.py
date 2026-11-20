def getting_set_of_numbers(mssg):
  numbers=[]
  for char in mssg :
    c=ord(mssg)-65
    numbers.append = [c]
  return numbers


def encrypt(mssg , key):
    letters = []
    for i in mssg:
        if 'A' <= i <= 'Z':
            e = (ord(i) - 65 + key) % 26
            letters.append(chr(e + 65))
        elif 'a' <= i <= 'z':
            e = (ord(i) - 97 + key) % 26
            letters.append(chr(e + 97))
        elif '0' <= i <= '9':
            e = (ord(i) - 48 + key) % 10
            letters.append(chr(e + 48))
        else:
            letters.append(i)

    return letters


def decrypt(text, k):
    return encrypt(text, -1*k)



def ceaser_cypher(mssg , key , choice ): 
    while choice not in(1,2):
      choice = int(input("heyy , you wanna encrypt a text (1) or decrypt it (2) ?"))  

    if(choice==1):
        return " the ecrypted mssg : ".join(encrypt(mssg , key))
    elif (choice==2):
        return " the decrypted mssg : ".join(decrypt(mssg , key))
    
  
