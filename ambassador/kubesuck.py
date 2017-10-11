import os, sys
from kubernetes import client, config

output = sys.argv[1]

# XXX: is there a better way to check if we are inside a cluster or not?
if "KUBERNETES_SERVICE_HOST" in os.environ:
    config.load_incluster_config()
else:
    config.load_kube_config()

v1 = client.CoreV1Api()

for svc in v1.list_service_for_all_namespaces().items:
    name = svc.metadata.name
    annotations = svc.metadata.annotations
    # XXX: need to figure out the proper conventions for third party annotation keys
    if annotations and "ambassador" in annotations:
        config = annotations["ambassador"]
        fname = os.path.join(output, "%s.yaml" % name)
        with open(fname, "write") as fd:
            fd.write(config)
        print ("Wrote %s to %s" % (name, fname))
