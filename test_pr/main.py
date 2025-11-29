from fastapi import FastAPI
import numpy as np

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/array")
def get_array():
    arr = np.array([1, 2, 3, 4, 5])
    return {"array": arr.tolist(), "sum": float(np.sum(arr)), "mean": float(np.mean(arr))}

@app.get("/multiply/{value}")
def multiply_array(value: int):
    arr = np.array([1, 2, 3, 4, 5])
    result = arr * value
    return {"result": result.tolist()}