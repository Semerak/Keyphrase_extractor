import math
import json

class SimpleDict:
    def __init__(self,init_dict={}):
        self.dictionary = {}
        for l in init_dict:
            if l=="":
                self.dictionary[""]=init_dict[""]
            else:
                self.dictionary[l]=SimpleDict(init_dict[l])
    
    def keys(self):
        return self.dictionary.keys()
    
    def get(self,letter):
        return self.dictionary.get(letter)
    
    def get_add(self, letter):
        if letter == "":
            return self.dictionary.get("")
        if self.dictionary.get(letter) is None:
            self.dictionary[letter] = SimpleDict()
        return self.dictionary.get(letter)

    def include(self, letter):
        return not (self.dictionary.get(letter) is None)

    def add(self, val):
        if self.dictionary.get("") is None:
            self.dictionary[""] = []
        self.dictionary[""].append(val)
    
    def inc(self):
        if self.dictionary.get("") is None:
            self.dictionary[""] = 1
        else:
            self.dictionary[""]+=1
            
    def value(self,val):
        self.dictionary[""]=val
            
    def clear(self,new_dic,word, val):
        if not (self.dictionary.get("") is None):
            if self.dictionary.get("") > val:
                new_dic.value(word,self.dictionary.get(""))
                
        for l in self.dictionary:
            if l !="":
                self.dictionary[l].clear(new_dic,word+l,val)

    def list(self,word):
        list_data = []
        val=self.dictionary.get("")
        if val is not None:
            list_data.append({'word':word ,'val':val})
        for letter in self.dictionary:
            if letter != "":
                list_data.extend(self.dictionary[letter].list(word+letter))
        return list_data

    def json(self):
        json_dic = {}
        for l in self.dictionary:
            if l == "":
                json_dic[""] = self.dictionary[""]
            else:
                json_dic[l] = self.dictionary[l].json()
        return json_dic



    
    
class PrefixTree:
    def __init__(self,init_dict={},num=0,crop=0):
        if init_dict.get('num') is not None:
            self.num=init_dict.get('num')
            self.mod_val=init_dict.get('mod')
            self.mod_update=True
            self.crop=init_dict.get('crop')
            self.dictionary=SimpleDict(init_dict.get('dictionary'))
        else:
            self.dictionary = SimpleDict(init_dict)
            if num==0:
                for word in self.list():
                    num+=word["val"]
            self.num=num
            self.crop=crop 
            self.mod_val=math.sqrt(sum(w['val']**2 for w in self.list()))  
            self.mod_update=True
  
 
            
    def add(self, word: str, val):
        dic = self.dictionary
        for letter in word:
            dic = dic.get_add(letter)
        dic.add(val)
        
        
    def inc(self,word:str):
        dic = self.dictionary
        for letter in word:
            dic = dic.get_add(letter)
        dic.inc()
        self.num+=1
        self.mod_update=False
    
    def mod(self,check=False):
        if check:
            self.mod_val=math.sqrt(sum(w['val']**2 for w in self.list()))
            self.mod_update=True
        else:
            if not self.mod_update:
                self.mod_val=math.sqrt(sum(w['val']**2 for w in self.list()))  
                self.mod_update=True
        return self.mod_val
        
    def value(self,word,val):
        dic = self.dictionary
        for letter in word:
            dic = dic.get_add(letter)
        dic.value(val)
        self.mod_update=False

    def get(self, word: str) -> list:
        dic = self.dictionary
        for letter in word:
            dic = dic.get(letter)
            if dic is None:
                return None
        return dic.get("")
    
    def clear(self,val):
        new_dic=PrefixTree()
        self.dictionary.clear(new_dic,"",val)
        new_dic.num=self.num
        new_dic.crop=max(self.crop,val)
        return new_dic
        

    def list(self,sort=False):
        list_data = []
        word=""
        for letter in self.dictionary.keys():
            if letter=="":
                list_data.append({'word':word, 'val': self.dictionary.get(letter)})
            else:
                list_data.extend(self.dictionary.get(letter).list(letter))
        if sort:
            return sorted(list_data,key= lambda word: word["val"], reverse=True)
        return list_data

    def json(self):
        data={'num': self.num,
             'mod':self.mod(),
             'crop':self.crop,
             'dictionary': self.dictionary.json()
             }
        return data
    
    def save(self,path):
        f = open(path, "w")
        f.write(json.dumps(self.json()))
        f.close()
    
    def norm(self,new_vector=False):
        mod=self.mod()
        if new_vector:
            new_vector=DictWords()
            for word in self.list():
                new_vector.value(word['word'],word['val']/mod)
            new_vector.num=self.num
            new_vector.crop=self.crop
            new_vector.mod_val=1
            return new_vector
        else:
            for word in self.list():
                self.value(word['word'],word['val']/mod)
            self.mod_val=1
            return self
            

