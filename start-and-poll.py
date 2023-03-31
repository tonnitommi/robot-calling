# pip install requests
# pip install rpaframework

import requests
import time
from RPA.Robocorp.Process import Process

# Start Robocorp process over API and poll for the status and output work item

WORKSPACE_ID = "YOUR_WORKSPACE_ID"
PROCESS_ID = "YOUR_PROCESS_ID"
API_KEY = "YOUR_API_KEY"
URL_BASE = "https://api.eu1.robocorp.com/process-v1"

#https://api.eu1.robocorp.com/v1/workspaces/<WORKSPACE_ID>/processes/<PROCESS_ID>/process-runs/<PROCESS_RUN_ID>/outputs

def run(process):
    payload = {"message": "greeting"}
    r = process.start_process(work_items=payload)
    return r["id"]

def get_status(run_id, process):
    r = process.get_process_run_status(run_id)
    return r["state"]

def get_output(run_id):
    # NOTE: RPA.Robocorp.Process does not have a method to get the output work item yet.
    # This API endoint is not yet documented, but it is available. !! It might still change !!
    url = f"{URL_BASE}/workspaces/{WORKSPACE_ID}/processes/{PROCESS_ID}/runs/{run_id}/outputs"
    headers = {"Authorization": "RC-WSKEY " + API_KEY}

    r = requests.get(url, headers=headers)
    return r.json()["data"][0]["payload"]

if __name__ == '__main__':

    process = Process(
        WORKSPACE_ID,
        PROCESS_ID,
        API_KEY
    )

    run_id = run(process)
    print(f"Started process with id: {run_id}")

    state = get_status(run_id, process)

    # loop and poll until the process status is finished
    while state != "COMPL":
        print (f"Process status: {state}")
        time.sleep(5)   ## Adjust sleep for realistic value depending on the process
        state = get_status(run_id, process)

    # Get the output work item
    output = get_output(run_id)
    print (f"Output: {output}")
    
