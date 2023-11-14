## Configure Kustomize project

### File structure

~~~ bash
mkdir -p overlays/{base,dev,prod}


cd overlays/base
touch dockerconfig.json
touch rbac.yaml
touch deployment.yaml
touch service.yaml
touch route.yaml

kustomize create --recursive --autodetect


cd overlays/dev

kustomize create  --resources ../../base --namespace kustom-dev

cd overlays/prod

kustomize create  --resources ../../base --namespace kustom-prod

~~~ bash

.
├── README.md
├── base
│   ├── deployment.yaml
│   ├── dockerconfigjson
│   ├── kustomization.yaml
│   ├── namespace.yaml
│   ├── rbac.yaml
│   ├── route.yaml
│   └── service.yaml
└── overlays
    ├── dev
    │   └── kustomization.yaml
    ├── prod
    │   └── kustomization.yaml
    └── qa
        └── kustomization.yaml
~~~
## Create a service account

Startly we will create a service account and assign it a admin project role, after that we create a secret with kustomize secretGenerator function.

***The base kustomize present bellow:***

### Create a files

The secretGenerator can create a secret from file where key is the name of file and the key value is the content of file

~~~ bash
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
namespace: kustom-default
resources:
- rbac.yaml
commonLabels:
  oper_env: default
  app: apiimg

namePrefix: apiimg-

secretGenerator:
- name: quay-secret
  files:
  - dockerconfigjson
  type: "kubernetes.io/dockerconfigjson"
~~~

And the rbac file contents are follow:

~~~ yaml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin
imagePullSecrets:
  - name: quay-secret

---

apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: admin
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: admin
subjects:
- kind: ServiceAccount
  name: admin-rep
~~~

> Kustomize repleace automatically the name of hashed secret created by { .secretGenerator.name }
{.is-info}

### Check object after create 

~~~ bash
kustomize build
apiVersion: v1
imagePullSecrets:
- name: apiimg-quay-secret-dev-52tg72fm8m
kind: ServiceAccount
metadata:
  labels:
    app: apiimg
    oper_env: dev
  name: apiimg-admin-dev
  namespace: kustom-dev
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  labels:
    app: apiimg
    oper_env: dev
  name: apiimg-admin-dev
  namespace: kustom-dev
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: admin
subjects:
- kind: ServiceAccount
  name: apiimg-admin-dev
  namespace: kustom-dev
---
apiVersion: v1
data:
  .dockerconfigjson: |
    ewogICJhdXRocyI6IHsKICAg==
kind: Secret
metadata:
  labels:
    app: apiimg
    oper_env: dev
  name: apiimg-quay-secret-dev-52tg72fm8m
  namespace: kustom-dev
type: kubernetes.io/dockerconfigjson
~~~

### Verify objects

~~~ bash
cd prod

oc apply -k .

serviceaccount/apiimg-admin-prod created
rolebinding.rbac.authorization.k8s.io/apiimg-admin-prod created
secret/apiimg-quay-secret-prod-52tg72fm8m created

oc get -k -o wide .

NAME                               SECRETS   AGE
serviceaccount/apiimg-admin-prod   1         46s

NAME                                                      ROLE                AGE   USERS   GROUPS   SERVICEACCOUNTS
rolebinding.rbac.authorization.k8s.io/apiimg-admin-prod   ClusterRole/admin   46s                    kustom-prod/apiimg-admin-prod

NAME                                        TYPE                             DATA   AGE
secret/apiimg-quay-secret-prod-52tg72fm8m   kubernetes.io/dockerconfigjson   1      46s
~~~

## Create APP
