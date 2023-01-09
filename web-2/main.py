from fastapi import FastAPI

app = FastAPI()


@app.get('/main')
def main():
    return 'Hello World'
