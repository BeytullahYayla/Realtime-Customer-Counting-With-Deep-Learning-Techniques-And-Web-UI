from configparser import ConfigParser



def parse_config():
    
    config_parser=ConfigParser()
    config_parser["CEVAHIR"]={
        "x1":0,
        "y1":450,
        "x2":1920,
        "y2":450
    }
    config_parser["EMAR168"]={

         "x1":0,
         "y1":688,
         "x2":1920,
         "y2":688
        
    }
    config_parser["EMAR169"]={
        
         "x1":0,
         "y1":648,
         "x2":1920,
         "y2":648
    }
    config_parser["GEBZE"]={
       
         "x1":0,
         "y1":505,
         "x2":1920,
         "y2":505
    }
    
    config_parser["MALLOFF"]={
       
         "x1":0,
         "y1":700,
         "x2":1920,
         "y2":650
    }
    config_parser["YENIBOSNA"]={
       
         "x1":0,
         "y1":410,
         "x2":1920,
         "y2":410
    }
    config_parser["AKYAKA168"]={
    
         "x1":0,
         "y1":620,
         "x2":1920,
         "y2":620
    }
    
    config_parser["AKYAKA169"]={
       
         "x1":0,
         "y1":357,
         "x2":1920,
         "y2":357
    }
    config_parser["BAYRAMPASA"]={
    
         "x1":0,
         "y1":840,
         "x2":1920,
         "y2":840
    }
  
    config_parser["ANKARA"]={
       
         "x1":0,
         "y1":766,
         "x2":1920,
         "y2":940
    }
    config_parser["CEV"]={
        
         "x1":0,
         "y1":416,
         "x2":1920,
         "y2":416
    }
    config_parser["FOR"]={
         "x1":0,
         "y1":750,
         "x2":1920,
         "y2":750
    }
    config_parser["OUT"]={

         "x1":0,
         "y1":960,
         "x2":1920,
         "y2":960
    }
    
    return config_parser



if __name__=="__main__":
    
    config_parser=parse_config()
    with open("customer_counting.ini","w") as f:
        config_parser.write(f)
        
