"""
api_test_project - FastAPI Web Application
"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="api_test_project", version="0.1.0")

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to api_test_project!"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
