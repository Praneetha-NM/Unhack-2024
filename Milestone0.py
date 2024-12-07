import json
time=0
import threading
def machine_execution(machi,param_range,param,result,machine_count,wafer,count,machines,process):
    global time
    result["schedule"].append({"wafer_id":str(wafer["type"]+"-"+str(count)),
                   "step":process,
                   "machine":machi,
                   "start_time":time,
                   "end_time":time+wafer["processing_times"][process]})
    time+=wafer["processing_times"][process]
    machine_count[machi]+=1

def step(steps,machines,wafer,depend,step_machines,free_machines,count,param,result,total,n,machine_count):
    for step in steps :
        if step["id"] in wafer["processing_times"]:
            param_range=step["parameters"]
            break
    while n<=total:
        for machine in step_machines:
            if machine in free_machines:
                for mach in machines:
                    if mach["machine_id"]==machine:
                        machine_execution(machine,param_range,param,result,machine_count,wafer,count,machines,mach["step_id"])
                        n+=1
                        break
if __name__ == "__main__":
    with open(r"KLA-Inputs\Milestone0.json") as input:
        json_file=json.load(input)
    steps=json_file["steps"]
    machines=json_file["machines"] 
    wafers=json_file["wafers"]
    no_of_wafers = len(wafers)
    dependency_graph={}
    for st in steps:
        dependency_graph[st['id']]=[st['dependency']]
    machines_for_step={str(step["id"]):[] for step in steps}
    for machine in machines:
        machines_for_step[machine['step_id']].append(machine['machine_id'])
    print("Machines allocated for steps : " ,machines_for_step)
    print("Steps Dependency " ,dependency_graph)
    free_machines=[machine["machine_id"] for machine in machines]
    print(free_machines)
    initial_param={machine['machine_id']:{} for machine in machines}
    for machine in machines:
        initial_param[machine['machine_id']]=machine['initial_parameters']
    machine_count={machine['machine_id']:0 for machine in machines}
    print(initial_param)
    result={}
    result["schedule"]=[]
    total_no_wafers=0
    for wafer in wafers:
        total_no_wafers+=wafer["quantity"]
        print(wafer["quantity"])
    count=0
    t1=threading.Thread(target=step, args=(steps,machines,wafers,dependency_graph,machines_for_step,free_machines,count,initial_param,result,total_no_wafers,1,machine_count))
    t2=threading.Thread(target=step, args=(steps,machines,wafers,dependency_graph,machines_for_step,free_machines,count,initial_param,result,total_no_wafers,1,machine_count))
    print(result)
    json_object = json.dumps(result, indent=4)
    with open("Milestone0.json", "w") as outfile:
        outfile.write(json_object)


           
           


