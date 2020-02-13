import re
import os
import base64
from datetime import datetime
from bs4 import BeautifulSoup as bs


def extract_shapes(file):  
    content = []

    with open("Sample Superstore - Sales Performance.twb", "r") as file:
        content = file.readlines()
        content = "".join(content)
        bs_content = bs(content, "lxml")

    count = 0 

    tab_shap_path = "Shapes" # Replace with the path to your Tableau Repo Shapes folder
    if not os.path.exists(tab_shap_path):
        os.makedirs(tab_shap_path)
        
    for shape in bs_content.find_all("shape"):
        shape_name = shape.get("name")

        if shape_name is None:
            continue
        shape_data = bytes(shape.text.strip(), 'utf8')
        shape_path = tab_shap_path+"/"+shape_name 

        temp = shape_path.split("/")
        if len(temp)>2:
            if not os.path.exists(tab_shap_path+"/"+temp[1]):
                os.mkdir(tab_shap_path+"/"+temp[1])

        if os.path.exists(shape_path):
            temp_shape_path = shape_path.rsplit('.', 1) 
            today = re.sub("[^0-9]", "", str(datetime.today()))
            shape_path = temp_shape_path[0]+" "+today+"."+temp_shape_path[1]
        with open(shape_path, "wb") as s:
            s.write(base64.decodebytes(shape_data))
            count += 1

    print(f"{count} shapes saved.")
