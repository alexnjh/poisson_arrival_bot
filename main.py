import time
from datetime import datetime, timezone
import random
import yaml
import os
from os import path
from kubernetes import client, config

try:
    config.load_kube_config()
except:
    # load_kube_config throws if there is no config, but does not document what it throws, so I can't rely on any particular type here
    config.load_incluster_config()

# This is the average arrival rate per hour, can be increased using environmental variables
ARRIVAL_RATE = os.getenv('ARRIVAL_RATE')
if ARRIVAL_RATE == None:
    ARRIVAL_RATE = 200



v1 = client.BatchV1Api()
NumOfRequestPerMin   = 60/int(ARRIVAL_RATE)
lamda = 1/NumOfRequestPerMin

def create_deployment(namespace, idx):

    with open(path.join(path.dirname(__file__), "deployment.yaml")) as f:
        dep = yaml.safe_load(f)
        local_time = datetime.now(timezone.utc).astimezone()
        dep["metadata"]["name"] = "experiment-job-{}".format(idx)
        dep["metadata"]["annotations"]["creationTime"] = local_time.isoformat()
        resp = v1.create_namespaced_job(body=dep, namespace="default")
        print("Job created. status='%s'" % str(resp.status))


def main():

    idx = 1

    while True:
        nextTime = random.expovariate(lamda)
        time.sleep(nextTime*60)
        create_deployment("default",idx)
        idx+=1


if __name__=="__main__":
    main()
