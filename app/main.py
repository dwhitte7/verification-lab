from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
import uuid

app = FastAPI()

ITEMS = {
    1: {"id": 1, "name": "switch-a", "status": "ready"},
    2: {"id": 2, "name": "router-b", "status": "provisioning"},
}

JOBS = {}

class JobRequest(BaseModel):
    task: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    item = ITEMS.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/jobs")
async def create_job(req: JobRequest):
    job_id = str(uuid.uuid4())
    JOBS[job_id] = {"job_id": job_id, "task": req.task, "state": "queued"}
    asyncio.create_task(run_job(job_id))
    return {"job_id": job_id, "state": "queued"}

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    job = JOBS.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

async def run_job(job_id: str):
    JOBS[job_id]["state"] = "running"
    await asyncio.sleep(5)
    JOBS[job_id]["state"] = "completed"
