import os , time , re

from bs4 import BeautifulSoup

from pathlib import Path

from shutil import copyfile


start_time=time.time()

from_path = "C:/Users/Jim/Documents/Ergasia_2_IR/Original_Collection/"
to_path = "C:/Users/Jim/Documents/Ergasia_2_IR/Converted_Collection/"
exception_path = "C:/Users/Jim/Documents/Ergasia_2_IR/Converted_Collection/Exceptions/"
# Paths with forward slashes - At the end of the run the files in the exception path should be zero

shortword = re.compile(r'\W*\b\w{1,2}\b')

# Removes numbers, non-ascii characters and two-letter words 
def remove_noise(text):
    text = text.replace('\\n',' ')
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


folder_numbers = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13'
                 ,'14','15','16','17','18','19','20','21','22','23','24','25','26','27','28']

for num in folder_numbers:   
    for files in os.listdir(from_path+num+'/'):
        to_file = Path(to_path+num+'/'+files)
        if  files.endswith(".txt") and not to_file.exists():
            print(files)
            content = open(from_path+num+'/'+files,'r',encoding='utf8').read()
        
            invalid_tags = ['<SEP>','<CHEM>','<tb>','<IMAGE>','<RTI','<\\n','<\\']
            for tag in invalid_tags:
                content = content.replace(tag,' ')
       
            valid_tags = ['DOC','DOCNO','TEXT','BIBLIOGRAPHIC-DATA'
                          ,'CLASSIFICATIONS-IPCR','CLASSIFICATIONS-ECLA'
                          ,'TITLE','ABSTRACT','DESCRIPTION','CLAIMS']
            for tag in valid_tags:
                content = content.replace('<'+tag+'>','{'+tag+'}')
                content = content.replace('</'+tag+'>','{/'+tag+'}')     
            content = content.replace('<',' ')
            content = content.replace('>',' ')
            for tag in valid_tags:
                content = content.replace('{'+tag+'}','<'+tag+'>')
                content = content.replace('{/'+tag+'}','</'+tag+'>')
             
            soup = BeautifulSoup(content,'html.parser')

            clf=soup.find('classifications-ipcr')
            if clf is not None:
                clf_text=clf.getText()
                clf_encoded=encode_clf(clf_text)
                clf.string.replace_with(clf_encoded)


            exception_flag = False         
            
            inv_title=soup.find_all('title')
            if inv_title is not None:
                try:
                    i = 0
                    for text in inv_title:
                        invt = text.getText()
                        invt = remove_noise(invt)
                        inv_title[i].string.replace_with(invt)
                        i = i+1
                except:
                    exception_flag = True 
             
                
            abstract=soup.find_all('abstract')
            if abstract is not None:
                try:
                    i = 0
                    for text in abstract:
                        abstr = text.getText()
                        abstr = remove_noise(abstr)
                        abstract[i].string.replace_with(abstr)
                        i = i+1
                except:
                    exception_flag = True

         
            description=soup.find_all('description')
            if description is not None:
                try:
                    i = 0
                    for text in description:
                        descr = text.getText()
                        descr = remove_noise(descr)
                        description[i].string.replace_with(descr)
                        i = i+1
                except:
                    exception_flag = True
                    
                
            claims = soup.find_all('claims')
            if claims is not None:
                try:
                    i = 0
                    for text in claims:      
                        cl = text.getText()
                        cl = remove_noise(cl)
                        claims[i].string.replace_with(cl)
                        i = i+1
                except:
                    exception_flag = True
                
        
            if exception_flag == False:
                f=open(to_path+num+'/'+files,'a+',encoding='utf8')
                f.write(str(soup))
                f.close()
            else:
                copyfile(from_path+num+'/'+files, exception_path+num+'/'+files)

elapsed_time=time.time()-start_time
print("Finished! Elapsed Time = " +str(round(elapsed_time)) + " sec")
