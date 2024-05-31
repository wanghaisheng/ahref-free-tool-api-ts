from DrissionPage import ChromiumOptions, ChromiumPage

from fastapi import FastAPI

from src.dtos.ISayHelloDto import ISayHelloDto
from checkDA import check_DA

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/hello")
async def hello_message(dto: ISayHelloDto):
    return {"message": f"Hello {dto.message}"}


@app.get("/ahref/{keyword}")
async def getAhrefKD(domain: str):

    co = ChromiumOptions().auto_port()
    page1 = ChromiumPage(co)

    url = "https://ahrefs.com/keyword-difficulty/"
    page1.get(url)
    keyword = "remini.ai"
    page1.ele("@placeholder=Enter keyword").input(keyword)

    # 点击登录按钮
    page1.ele("text=Check keyword").click()
    kd = page1.ele(".css-16bvajg-chartValue").text

    kds = page1.ele(".css-1wi5h2-row css-1crciv5 css-6rbp9c").text
    #     print(kd)
    #     print(kds)

    return {"domain": domain, "kd": kd, "des": kds}


@app.get("/domainda/{domain}")
async def getDomainDA(domain: str):
    data = check_DA(domain)
    return data
