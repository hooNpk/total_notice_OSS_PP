from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/data")
def read_data():
    return [
        {"title": "Item 1", "date": "2024-05-30", "writer":"skku", "ctgry":"[채용]", "source" : "소프트웨어대학", "url":"https://www.skku.edu/skku/campus/skk_comm/notice01.do?mode=view&articleNo=118031&article.offset=0&articleLimit=10"},
        {"title": "Item 2", "date": "2024-05-31", "writer":"skku2", "ctgry":"[채용]", "source" : "소프트웨어융합대학", "url":"https://www.skku.edu/skku/campus/skk_comm/notice01.do?mode=view&articleNo=116747&article.offset=0&articleLimit=10"},
    ]


