import json
import multiprocessing
import time
from multiprocessing.connection import wait
import threading
result_lock=threading.Lock()
machine_status={}
thread_lock=threading.Lock()
usage=[]

def machine_execution(machine,processing_time,result,process,threadd,wafer,wafer_id):
    with threading.Lock():
        start_time=max(machine_status.get(machine,0),threadd[str(wafer["type"]+"-"+str(wafer_id))])
        end_time=start_time+processing_time
    machine_status[machine]=end_time
    print(machine_status[machine])
    resultt={"wafer_id":str(wafer["type"]+"-"+str(wafer_id)),
                   "step":process,
                   "machine":machine,
                   "start_time":start_time,
                   "end_time":end_time}
    with result_lock:
        result["schedule"].append(resultt)

def step(wafer,wafer_id,steps,machines_for_step,result,free_machines,threadd):
    stepp=list(wafer["processing_times"].keys())
    while stepp:
        for step in steps :
            if step["id"] not in stepp:
                continue
            if step["id"] in usage:
                continue
            processing_time=wafer["processing_times"][step["id"]]
            for machine in machines_for_step[step["id"]]:
                usage.append(step["id"])
                
                machine_execution(machine,processing_time,result,step["id"],threadd,wafer,wafer_id)
                threadd[str(wafer["type"]+"-"+str(wafer_id))]+=processing_time
                time.sleep(1)
                usage.remove(step["id"])
                break
            stepp.remove(step["id"])
        
if __name__ == "__main__":
    with open(r"KLA-Inputs\Milestone0.json") as input:
        json_file=json.load(input)
    steps=json_file["steps"]
    machines=json_file["machines"] 
    wafers=json_file["wafers"]
    no_of_wafers = len(wafers)
    """dependency_graph={}
    for st in steps:
        dependency_graph[st['id']]=[st['dependency']]"""
    machines_for_step={str(step["id"]):[] for step in steps}
    for machine in machines:
        machines_for_step[machine['step_id']].append(machine['machine_id'])
    print("Machines allocated for steps : " ,machines_for_step)
    initial_param={machine['machine_id']:{} for machine in machines}
    for machine in machines:
        initial_param[machine['machine_id']]=machine['initial_parameters']
    result={}
    result["schedule"]=[]
    total_no_wafers=0
    for wafer in wafers:
        total_no_wafers+=wafer["quantity"]
        print(wafer["quantity"])
    count=0
    thread=[]
    waferr={}
    for wafer in wafers:
        waferr[wafer["type"]]=wafer["processing_times"]
    free_machines=[machine["machine_id"] for machine in machines]
    print(free_machines)
    threadd={}
    for wafer in wafers:
        for i in range(wafer["quantity"]): 
            threadd[str(wafer["type"]+"-"+str(i+1))]=0
            print(threadd)
            t=threading.Thread(target=step, args=(wafer,i+1,steps,machines_for_step,result,free_machines,threadd))
            t.start()
            thread.append(t)
    for t in thread:
        t.join()
    print(result)
    json_object = json.dumps(result, indent=4)
    with open("Milestone1.json", "w") as outfile:
        outfile.write(json_object)


           
           


