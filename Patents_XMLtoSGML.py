# encoding=utf8
import os, re

from bs4 import BeautifulSoup

shortword = re.compile(r'\W*\b\w{1,2}\b')

# Removes numbers, non-ascii characters and two-letter words 
def remove_noise(text):
    text = re.sub("(\\W|\\d)"," ",text)
    text = shortword.sub(" ",text)
    return text

# Encodes classifications-ipcr: Converts digit 0 to O, 1-9 to a-i and / to X
def encode_clf(clf):
    clf=clf.replace("/","X")
    clf=clf.replace("0","O")
    clf=clf.replace("1","a")
    clf=clf.replace("2","b")
    clf=clf.replace("3","c")
    clf=clf.replace("4","d")
    clf=clf.replace("5","e")
    clf=clf.replace("6","f")
    clf=clf.replace("7","g")
    clf=clf.replace("8","h")
    clf=clf.replace("9","i")
    
    clf_list=clf.split()
    useful_elements=[]
    for word in clf_list:
        if len(word)<8:
            useful_elements.append(word)
                
    clf_elements=[]
    j=0
    while j < (len(useful_elements)-1):
        clf_elements.append(useful_elements[j])
        if useful_elements[j+1][1]=='X': 
            clf_elements.append(useful_elements[j]+useful_elements[j+1][0])
        if useful_elements[j+1][2]=='X': 
            clf_elements.append(useful_elements[j]+useful_elements[j+1][0:2])
        clf_elements.append(useful_elements[j]+useful_elements[j+1])
        j=j+2
                
    clf_encoded=' '.join(clf_elements)    
    return clf_encoded


datdir ="C:/Users/Jim/Documents/Ergasia_2_IR/PAC_topics/run_topics/"
datadest="C:/Users/Jim/Documents/Ergasia_IR/MiniCollection/SGML_Topics/"


cnt=0
for files in os.listdir(datdir):
    print(files)
    cnt=cnt+1
    if files.endswith(".xml"):
        content = open(datdir+"/"+files,'r',encoding='utf8').read()
        soup = BeautifulSoup(content,'lxml')
        texts = soup.findAll("classification-ipcr")
        texts2=soup.findAll("invention-title")
        texts3=soup.findAll("abstract")
        texts4=soup.findAll("description")
        texts9=soup.findAll("claims")
        f=open(datadest+"/"+"SGML_Topics.txt","a+",encoding='utf8')
        f.write("<TOP>\n<NUM>"+os.path.splitext(files)[0]+"</NUM>\n<TITLE>\n")
        
        for text in texts:
            clf=text.getText()
            clf_encoded=encode_clf(clf)
            f.write(clf_encoded+" ") 
            
        for text2 in texts2:
            inv_title=text2.getText()
            inv_title=remove_noise(inv_title)
            f.write(inv_title+" ") 
            
        for text3 in texts3:
            abstract=text3.getText()
            abstract=remove_noise(abstract)
            f.write(abstract+" ")    
            
        for text4 in texts4:
            description=text4.getText()
            description=remove_noise(description)
            f.write(description[0:500]+" ") 
        
        for text9 in texts9:
            claims_all=text9.getText()
            claims_all=remove_noise(claims_all)
            f.write(claims_all[0:500]+" ")  
        
        f.write("\n</TITLE>\n</TOP>\n")
        f.close()

print("Finished! Total Topics: "+str(cnt))
