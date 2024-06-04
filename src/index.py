from DrissionPage import ChromiumOptions, ChromiumPage

from fastapi import FastAPI

from src.dtos.ISayHelloDto import ISayHelloDto
from src.checkDA import check_DA
import os

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


@app.get("/ahref/kd/{keyword}")
async def getAhrefKD(keyword: str):
    path = "/tmp/chromium"

    # Try each path in sequence until a valid one is found

    # Check if the path exists
    if os.path.exists(path):
        print("tmp is found")
        # List all files and directories in the path
        files_and_dirs = os.listdir(path)

        # Filter out directories and only list files
        files = [f for f in files_and_dirs if os.path.isfile(os.path.join(path, f))]

        # Print all files
        for file in files:
            print(file)
    else:
        print("The path does not exist")

    co = ChromiumOptions().set_browser_path(path).auto_port()
    page1 = ChromiumPage(co)

    url = "https://ahrefs.com/keyword-difficulty/"
    page1.get(url)
    # keyword = "remini.ai"
    page1.ele("@placeholder=Enter keyword").input(keyword)

    # 点击登录按钮
    page1.ele("text=Check keyword").click()
    kd = page1.ele(".css-16bvajg-chartValue").text

    kds = page1.ele(".css-1wi5h2-row css-1crciv5 css-6rbp9c").text
    #     print(kd)
    #     print(kds)

    return {"keyword": keyword, "kd": kd, "des": kds}


@app.get("/domain/da/{domain}")
async def getDomainDA(domain: str):
    data = check_DA(domain)
    return data
