import time
import random
import yaml
from os import path
from kubernetes import client, config

try:
    config.load_kube_config()
except:
    # load_kube_config throws if there is no config, but does not document what it throws, so I can't rely on any particular type here
    config.load_incluster_config()


v1 = client.AppsV1Api()
NumOfRequestIn60Mins = 1000 # Number of scheduling requests in an hour
NumOfRequestPerMin   = 60/NumOfRequestIn60Mins
lamda = 1/NumOfRequestPerMin

def create_deployment(namespace, idx):

    with open(path.join(path.dirname(__file__), "deployment.yaml")) as f:
        dep = yaml.safe_load(f)
        dep["metadata"]["name"] = "experiment-job-{}".format(idx)
        resp = v1.create_namespaced_deployment(body=dep, namespace="default")
        print("Deployment created. status='%s'" % str(resp.status))


def main():

    idx = 1

    while True:
        nextTime = random.expovariate(lamda)
        time.sleep(nextTime*60)
        create_deployment("default",idx)
        idx+=1


if __name__=="__main__":
    main()
