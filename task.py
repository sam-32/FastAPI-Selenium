import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from langdetect import detect
from io import BytesIO
from PIL import Image
from bs4 import BeautifulSoup
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates




app=FastAPI()
templates=Jinja2Templates(directory="templates")
@app.get("/", response_class=HTMLResponse)
async def showForm(request:Request):
    return templates.TemplateResponse("index.html", {"request":request})

@app.post("/process_url")
async def process_url(url:str, request:Request):
    result=[]
    result.append(websiteTranslated(url))
    result.append(checkResolution(url))
    return templates.TemplateReponse("results.html", {"request":request}, {"results":result})


browser=webdriver.Chrome("C:/Users/Samuel S/Desktop/task/FastAPI-Selenium/chromedriver.exe")
def websiteTranslated(url):
    browser.get(url)
    html1=browser.page_source
    soup1=BeautifulSoup(html1, 'html.parser')
    pageText=browser.find_element(By.TAG_NAME, 'body').text
    language=detect(pageText)
    if language!='hi':
        return "Not translated"
    return "Translated"

def checkResolution(url):
    response=requests.get(url)
    soup=BeautifulSoup(response.text, 'html.parser')
    images=soup.find_all('img')
    for imgTag in images:
        imgUrl=imgTag.get('src')
        if not imgUrl.startswith('http'):
            imgUrl=f'{url}/{imgUrl}'
        imgData=requests.get(imgUrl).content
        try:
            image=Image.open(BytesIO(imgData))
        except (OSError):
            continue
        width, height=image.size
        pixels=width*height
        if pixels < 300000 and image.mode !='P':
            return "Low resolution"
    return "High resolution"


    """url2="https://graceful-sunburst-78f35d.netlify.app/www.classcentral.com/index.html"
    browser.get(url2)
    html2=browser.page_source
    soup2=BeautifulSoup(html2, 'html.parser')

    if soup1.get_text()==soup2.get_text():
        print("son iguales")
    else:
        print("son diferentes")
        
    dropdown=[
        "//a[@class='relative inline-block symbol-report']",
        "//button[contains(text(),'पाठ्यक्रम')]"
    ]

    for dropdownSelector in dropdown:
        dropdownElement=browser.find_element(By.XPATH, dropdownSelector)
        dropdownElement.click()
"""



