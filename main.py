#The problem of this code is that it doesn't work with spaces and punctuation. Therefore, I included some plaintexts in files that can be used to test the code.
#I tried my best to make it work with punctuation and spaces, but due to the lack of my programming skills, I did not succeed.
#This is my first time writing a serious code in python and I used someone elses code as a reference and tried to understand the syntax. Please take it into consideration.

from math import gcd
from collections import Counter

def c2i(c, alphabet):
    return alphabet.index(c) 

def i2c(i, alphabet):
    return alphabet[i]

def prepare_string(s, alphabet):
  temp = s 
  alphaList = list(alphabet)
  sList = list(temp)
  for index in range(len(sList)) : 
    for index2 in range(len(alphaList)) : 
      if temp[index] == alphaList[index2] :
        break
      if index2 + 1 == len(alphaList) :
        sList.remove(temp[index])
    
  final = ''.join(sList)
  return final

def vigenere_encode(plaintext, key, alphabet):
  plaintext = prepare_string(plaintext, alphabet)
  plainList = list(plaintext)
  keyList = list(key)
  alphaList = list(alphabet)
  encodeText = ""
  
  for index in range(len(plainList)) : 
    plainIndex = c2i(plainList[index], alphabet)
    keyIndex = c2i(((keyList[index % len(key)])), alphabet)
    encodeTextIndex = (plainIndex + keyIndex) % (26)
    encodeText += i2c(encodeTextIndex, alphabet)
    
  return encodeText

def vigenere_decode(ciphertext, key, alphabet):
  ciphertext = prepare_string(ciphertext, alphabet)
  cipherList = list(ciphertext)
  keyList = list(key)
  alphaList = list(alphabet)
  decodeText = ""
  
  for index in range(len(ciphertext)) : 
    cipherIndex = c2i(cipherList[index], alphabet)
    keyIndex = c2i(((keyList[index % len(key)])), alphabet)
    decodeTextIndex = (cipherIndex - keyIndex) % (26)
    decodeText += i2c(decodeTextIndex, alphabet)
    
  return decodeText

def index_of_coincidence(ciphertext, alpha):
    n = float(len(ciphertext))
    alphaList = list(alpha)
    #print("Length of ciphertext: " + str(n))
    c = Counter(ciphertext)
    ioc = 0
    
    for index in range(len(alphaList)) : 
      ioc += (ciphertext.count(alpha[index]) * (ciphertext.count(alpha[index]) - 1))
    
    ioc = ioc * (1/ (n * (n - 1)))
    
    #print("Index of Coincidence: " + str(ioc))
    
    return ioc
    
def kasiski_test(ciphertext):  #Code partially provided
    trigraphList = []
    distanceList = []
    
    for index in range(len(ciphertext) - 1) : 
      currentTrigraph = ciphertext[index:index + 3]
      if currentTrigraph not in trigraphList :
        trigraphList.append(currentTrigraph)
      else : 
        previousIndex = ciphertext.find(currentTrigraph)
        distance = index - previousIndex
        distanceList.append(distance)
        

    # Code is provided to find the gcd of any common distances appearing at least twice, just add your array:
    dCount = Counter(distanceList) # put your array of distances here)
    topCount = dCount.most_common(6)
    my_gcd = topCount[0][0]
    for index in range(1, len(topCount)):
        if topCount[index][1] > 1:
            my_gcd = gcd(my_gcd, topCount[index][0])
    
    return my_gcd

def run_key_test(ciphertext, alphabet): #Code provided
     """Runs Kasiski test and formats the output nicely"""
     kasiski = kasiski_test(ciphertext)
     out = "Kasiski determined the key: "  + str(kasiski);
     return out

def make_cosets(text, n):
     """Makes cosets out of a ciphertext given a key length; should return an array of strings"""
     coset = [None]*n
     testList = list(text)
    
     for k in range(0, n) : 
       i = k
       tempString = ""
       while (i) < len(testList) - 1: 
         tempString += testList[i]
         i += n
       coset[k] = tempString
      
     return coset
      
      
    

def rotate_list(old_list):  #Code provided
     """Takes the given list, removes the first element, and appends it to the end of the list, then returns the
     new list"""
     new_list = old_list[:]
     new_list.append(old_list[0])
     del new_list[0]
     return new_list

def find_total_difference(list1, list2):
    """Takes two lists of equal length containing numbers, finds the difference between each pair of matching
    numbers, sums those differences, and returns that sum"""
    sum = 0
    for index in range(len(list1)) : 
      sum += abs(list1[index] - list2[index])
    
    return sum

def find_likely_letters(coset, alpha, eng_freq):
    alphaList = list(alpha)
    cosetFreqList = [] 
    for index in range(len(alphaList)) : 
      cosetFreqList.append((coset.count(alpha[index])))
      
    
    differenceList = []
    for index in range(len(alphaList)) :
      differenceList.append(find_total_difference(cosetFreqList, eng_freq))
      cosetFreqList = rotate_list(cosetFreqList)
    
    letter1 = differenceList.index(min(differenceList))
    letter1 = i2c(letter1, alpha)
    
    secondSmallestIndex = sorted(differenceList) [1]
    letter2 = i2c(differenceList.index(secondSmallestIndex), alpha)
    #return statement provided.  feel free to replace "letter1" and "letter2" with other variable names.
    return "the most likely letter is: " + letter1 + " followed by: " + letter2

def crack(ciphertext, alpha, eng_freq):  #Code provided
     """User-friendly walkthrough of decoding methods"""
     print("Your cipher text is: " + ciphertext)
     out = run_key_test(ciphertext, alpha)
     print(out)
     x = int(input("Choose the key length you'd like to try: "))
     cosets = make_cosets(ciphertext, x)
     for index in range(len(cosets)):
         print("For coset " + str(index + 1) + ", " + find_likely_letters(cosets[index], alpha, eng_freq) + ".")
     s = input("Type the key you would like to use to decipher: ")
     print(vigenere_decode(ciphertext, s, alpha))
     print()




alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

eng_freq = [.0817, .0149, .0278, .0425, .1270, .0223, .0202, .0609, .0697, .0015, .0077, .0403, .0241, .0675, .0751,
            .0193, .0010, .0599, .0633, .0906, .0276, .0098, .0236, .0015, .0197, .0007]

YOURTEXTHERE = "KQUEEDSMWIKAIEIEFBIFNMHMTCJIIIKRBKVJYTSTEYTMFPYMPPRMTIUKQTYVUDPVUGTFPFRKFRKVFFQRTKBVRARVREGJVRUGPULVDMTTYQPVWNCQEICCWFHWQPZIRTQBJKGPULVFGTGFXCSCFHRIIIGKBMEUMGEEGMMMKJGDWVVRMIDGLUEEFYCCQCLUMEGFBVSQSSAZVFBQLNRJXLFCPJZPRBGKUFJTNTCDOJKLULVYYLIFHRIIJGESSLPBCVVCIJRXFGTGFXCSMVUYNYJGSNMJDCJRXEPFEKGBUSJJMXGRUCULVHGOHJ"

crack(YOURTEXTHERE, alpha, eng_freq)




