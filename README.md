# k8s-devops-flask
使用Jenkins自动化部署flask项目到k8s集群
### 本地启动命令
```
python .\manage.py  runserver
```

# 一、概述
最近在研究基于k8s实现一套devops流程，由于搭建一套k8s集群比较麻烦，所有打算使用`minikube`在我本地的windows上面实现整套devops流程，在这里记录一下整个实践过程，希望对需要的同学提供一些参考，也便于自己以后查阅。
> minikube官方地址：https://minikube.sigs.k8s.io/docs/start/

## 运行环境
windows 10
minikube 1.18.1
kubernetes 1.20.2
# 二、安装minikube
`minikube`是本地的Kubernetes，致力于使Kubernetes易于学习和开发。
你需要的只是Docker（或类似兼容）容器或虚拟机环境，只需一个命令即可： `minikube start`即可在本地启动一个kubernetes集群。

## 1. 运行minikube的条件
*   2个或更多CPU
*   2GB的可用内存
*   20GB的可用磁盘空间
*   网络连接
*   容器或虚拟机管理器，例如：[Docker](https://minikube.sigs.k8s.io/docs/drivers/docker/)，[Hyperkit](https://minikube.sigs.k8s.io/docs/drivers/hyperkit/)，[Hyper-V](https://minikube.sigs.k8s.io/docs/drivers/hyperv/)，[KVM](https://minikube.sigs.k8s.io/docs/drivers/kvm2/)，[Parallels](https://minikube.sigs.k8s.io/docs/drivers/parallels/)，[Podman](https://minikube.sigs.k8s.io/docs/drivers/podman/)，[VirtualBox](https://minikube.sigs.k8s.io/docs/drivers/virtualbox/)或[VMWare](https://minikube.sigs.k8s.io/docs/drivers/vmware/)
>说明：minikube 提供了跨平台搭建k8s的能力，支持mac ，linux ，windows平台，每一个平台上也支持多种驱动架构，windows 支持docker，Hyper-V，virtualBox等，由于win10已经内置了Hyper-V，这里选择Hyper-V。
## 2. 在windows中开启Hyper-V
[Hyper-V](https://docs.microsoft.com/en-us/virtualization/hyper-v-on-windows/)是内置于现代Microsoft Windows版本中的本机虚拟机管理程序，需要是Windows 10企业版，专业版或教育版的64位版本系统才能开启，我这里使用的是windows 10 专业版系统，通过如下方式开启Hyper-V。
![image.png](https://upload-images.jianshu.io/upload_images/8103938-7fbf13972936ee33.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
以管理员身份打开PowerShell控制台，然后运行以下命令：
```
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All
```
如果Hyper-V先前未处于活动状态，则需要重新启动。我这里已经开启了，所以如下图所示，显示online ，并且不需要重新。
![image.png](https://upload-images.jianshu.io/upload_images/8103938-df727fa754df5c8e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 3. 下载minikube
下载并运行[Windows安装程序](https://storage.googleapis.com/minikube/releases/latest/minikube-installer.exe)
![image.png](https://upload-images.jianshu.io/upload_images/8103938-02efe40368a23ec5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
安装完成后，搜索cmd并以管理员身份打开
![image.png](https://upload-images.jianshu.io/upload_images/8103938-e4f191d80435064c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
## 4. 启动minikube
使用如下命令启动minikube会导致有的镜像无法拉取，接着往下面看成功的运行命令
```bash
minikube start --driver=hyperv --registry-mirror=https://registry.docker-cn.com,https://shraym0v.mirror.aliyuncs.com --embed-certs=true --image-mirror-country=cn --image-repository=registry.cn-hangzhou.aliyuncs.com/google_containers

```

**参数说明**
可以通过`minikube start --help`查看其它参数的详细说明，这里说明上面使用的参数
- `minikube start`：启动一个本地单节点kubernetes集群。
- `--driver=hyperv `：指定驱动为hyperv，默认为自动检测(virtualbox, vmwarefusion, hyperv, vmware, docker, ssh)中的一个。
- `--registry-mirror=https://registry.docker-cn.com`：使用国内的镜像地址来提高拉取镜像的速度，可以设置多个用`,`分割即可。
-  `--embed-certs=true`: 如果为true，将在kubeconfig中嵌入证书，默认为false，在kubeconfig中将以绝对路径的方式读取证书文件。
-  `--image-mirror-country=cn`：需要使用的镜像的国家/地区代码，留空以使用全球代码，对于中国大陆用户，请将其设置为 **cn**。
-  `--image-repository=registry.cn-hangzhou.aliyuncs.com/google_containers`：设置用来拉取 Kubernetes 集群所需镜像的仓库，如果无法访问`gcr.io`可以设置为 "auto" 让minikube 为你自动选择可以访问的镜像仓库。对于中国大陆用户可以设置`registry.cn-hangzhou.aliyuncs.com/google_containers`，但是我设置此参数导致有的镜像无法拉取。

>说明：通过上面的命令启动minikube，会出现有的镜像无法拉取的问题，也就是说`registry.cn-hangzhou.aliyuncs.com/google_containers`镜像仓库很多镜像不存在，经过不断的测试，使用如下命令就可以正常启动并拉取镜像，所有我们**不需要设置**这两个参数：`--image-mirror-country=cn`和 `--image-repository=registry.cn-hangzhou.aliyuncs.com/google_containers`

**成功启动minikube的命令如下：**
```
minikube start --driver=hyperv --registry-mirror=https://registry.docker-cn.com,https://shraym0v.mirror.aliyuncs.com --embed-certs=true
```

## 5. 验证minikube
使用如下命令查看minikube的状态
```
C:\WINDOWS\system32>minikube status
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured
timeToStop: Nonexistent
# 这里会自动下载kubectl工具
C:\WINDOWS\system32>minikube kubectl get node
NAME       STATUS   ROLES                  AGE   VERSION
minikube   Ready    control-plane,master   11m   v1.20.2

```
部署一个nginx，快速体验minikube
```
C:\WINDOWS\system32>kubectl create deployment nginx --image=nginx
deployment.apps/nginx created

C:\WINDOWS\system32>kubectl get pod
NAME                     READY   STATUS    RESTARTS   AGE
nginx-6799fc88d8-z7xzh   1/1     Running   0          33s

C:\WINDOWS\system32>kubectl expose deployment nginx --type=NodePort --port=80
service/nginx exposed

C:\WINDOWS\system32>minikube service nginx
|-----------|-------|-------------|----------------------------|
| NAMESPACE | NAME  | TARGET PORT |            URL             |
|-----------|-------|-------------|----------------------------|
| default   | nginx |          80 | http://172.23.130.60:31593 |
|-----------|-------|-------------|----------------------------|
* 正通过默认浏览器打开服务 default/nginx...

C:\WINDOWS\system32>
```
会自动打开默认浏览器，如下图所示：
![image.png](https://upload-images.jianshu.io/upload_images/8103938-6da24697b5301204.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


使用如下命令启动k8s的dashboard
```
C:\WINDOWS\system32>minikube dashboard
* 正在开启 dashboard ...
  - Using image kubernetesui/dashboard:v2.1.0
  - Using image kubernetesui/metrics-scraper:v1.0.4
* 正在验证 dashboard 运行情况 ...
* Launching proxy ...
* 正在验证 proxy 运行状况 ...
* Opening http://127.0.0.1:61589/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/ in your default browser...

```
如下图所示：
![image.png](https://upload-images.jianshu.io/upload_images/8103938-1fcd4974bfd186ea.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# 三、安装jenkins
我这里使用`yaml`的方式部署jenkins，并且创建pv和pvc来持久化jenkins的数据，所有创建三个文件：
- `jenkins-pvc.yaml`：设置jenkins数据持久化方式。
- `jenkins-rbac.yaml`：设置jenkins用户访问权限。
- `jenkins-deploy.yaml`：创建jenkins的deployment 和 service。
 `jenkins-pvc.yaml`文件内容如下：
```yaml
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: jenkins-pvc
  namespace: devops
spec:
  accessModes:
  - ReadWriteMany
  # 如果集群中有一个默认的storageClass能满足需求，这里可以不用配置storageClass
  storageClassName: standard
  resources:
    requests:
      storage: 5Gi
```
> 说明：因为使用minikube创建的k8s集群默认已经创建了一个基于`hostpath`的`storageClass`，通过如下命令查看
>
>```
>C:\windows\system32>kubectl get sc
>NAME                 PROVISIONER                RECLAIMPOLICY   VOLUMEBINDINGMODE   >ALLOWVOLUMEEXPANSION   AGE
>standard (default)   k8s.io/minikube-hostpath   Delete          Immediate           false                  98m
>```
>
>storageClass会自动创建pv，并将pv和pvc进行绑定，所以我们无需自己创建pv。

`jenkins-rbac.yaml`文件内容如下：
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: jenkins-sa
  namespace: devops

---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: jenkins-cr
rules:
  - apiGroups: ["extensions", "apps"]
    resources: ["deployments"]
    verbs: ["create", "delete", "get", "list", "watch", "patch", "update"]
  - apiGroups: [""]
    resources: ["services"]
    verbs: ["create", "delete", "get", "list", "watch", "patch", "update"]
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["create","delete","get","list","patch","update","watch"]
  - apiGroups: [""]
    resources: ["pods/exec"]
    verbs: ["create","delete","get","list","patch","update","watch"]
  - apiGroups: [""]
    resources: ["pods/log"]
    verbs: ["get","list","watch"]
  - apiGroups: [""]
    resources: ["secrets"]
    verbs: ["get"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: jenkins-crd
roleRef:
  kind: ClusterRole
  name: jenkins-cr
  apiGroup: rbac.authorization.k8s.io
subjects:
- kind: ServiceAccount
  name: jenkins-sa
  namespace: devops

```
`jenkins-deploy.yaml`文件内容如下：
```yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jenkins
  namespace: devops 
spec:
  replicas: 1
  selector:
    matchLabels:
      app: jenkins
  template:
    metadata:
      labels:
        app: jenkins
    spec:
      terminationGracePeriodSeconds: 10
      serviceAccount: jenkins-sa
      containers:
      - name: jenkins
        image: jenkins/jenkins:latest
        imagePullPolicy: IfNotPresent
        env:
        - name: JAVA_OPTS
          value: -Duser.timezone=Asia/Shanghai
        ports:
        - containerPort: 8080
          name: web
          protocol: TCP
        - containerPort: 50000
          name: agent
          protocol: TCP
        resources:
          limits:
            cpu: 1000m
            memory: 1Gi
          requests:
            cpu: 500m
            memory: 512Mi
        livenessProbe:
          httpGet:
            path: /login
            port: 8080
          initialDelaySeconds: 60
          timeoutSeconds: 5
          failureThreshold: 12
        readinessProbe:
          httpGet:
            path: /login
            port: 8080
          initialDelaySeconds: 60
          timeoutSeconds: 5
          failureThreshold: 12
        volumeMounts:
          - name: jenkinshome
            mountPath: /var/jenkins_home
      volumes:
        - name: jenkinshome
          persistentVolumeClaim:
            claimName: jenkins-pvc

---
apiVersion: v1
kind: Service
metadata:
  name: jenkins
  namespace: devops 
  labels:
    app: jenkins
spec:
  selector:
    app: jenkins
  type: NodePort
  ports:
  - name: web
    port: 8080
    targetPort: web
    
    
---
apiVersion: v1
kind: Service
metadata:
  name: jenkins-agent
  namespace: devops 
  labels:
    app: jenkins
spec:
  selector:
    app: jenkins
  type: ClusterIP
  ports:
  - name: agent
    port: 50000
    targetPort: agent

```
使用下面的命令部署jenkins
1. 创建devops命名空间
```
C:\WINDOWS\system32>kubectl create namespace devops
namespace/devops created
```
2. 执行下面的命令启动jenkins
```
kubectl apply -f jenkins-pvc.yaml
kubectl apply -f jenkins-rbac.yaml
kubectl apply -f jenkins-deploy.yaml
```
3. 使用minikube service命令提供浏览器访问地址
```
C:\WINDOWS\system32>minikube service jenkins -n devops
|-----------|---------|-------------|----------------------------|
| NAMESPACE |  NAME   | TARGET PORT |            URL             |
|-----------|---------|-------------|----------------------------|
| devops    | jenkins | web/8080    | http://172.23.130.60:30002 |
|-----------|---------|-------------|----------------------------|
* 正通过默认浏览器打开服务 devops/jenkins...
```
![image.png](https://upload-images.jianshu.io/upload_images/8103938-cebf607ff7752f6c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
4. 使用如下命令查看登录jenkins的初始密码
```
C:\WINDOWS\system32>kubectl get pod -n devops
NAME                       READY   STATUS    RESTARTS   AGE
jenkins-6bb66dcf88-2c4tv   1/1     Running   0          9m59s

C:\WINDOWS\system32>kubectl logs -f jenkins-6bb66dcf88-2c4tv -n devops
```
查看jenkins初始密码如下图：
![image.png](https://upload-images.jianshu.io/upload_images/8103938-8adf89498d59dac8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
选择自定义插件安装，因为回去官网下载插件，下载比较慢，而且很多插件我们不需要
![image.png](https://upload-images.jianshu.io/upload_images/8103938-5a1f8f15d97efdb6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
取消推荐插件的选择
![image.png](https://upload-images.jianshu.io/upload_images/8103938-c19ee5893b816f49.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
创建一个管理员账号
![image.png](https://upload-images.jianshu.io/upload_images/8103938-3ec61b352ad55dc0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
开始使用jenkins
![image.png](https://upload-images.jianshu.io/upload_images/8103938-53083adea7597850.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

[Jenkins下载插件设置国内源](https://www.jianshu.com/p/e6c9dffefb5a)
![image.png](https://upload-images.jianshu.io/upload_images/8103938-4101f78b873737bd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

安装如下插件
![image.png](https://upload-images.jianshu.io/upload_images/8103938-0808db1bec21849e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# 四、在jenkins中配置k8s实现CI/CD
## 1. k8s相关配置
- 选择 [节点管理] -> [Configure Clouds]
![image.png](https://upload-images.jianshu.io/upload_images/8103938-b95193e60c21054e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- 安装了kubernetes插件就可看到下图所示，添加一个kubernetes的cloud
![image.png](https://upload-images.jianshu.io/upload_images/8103938-fb2302bab439ee84.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- 配置连接k8s的api server
![image.png](https://upload-images.jianshu.io/upload_images/8103938-0e1a6056da8a2c2c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- 创建pod template
![image.png](https://upload-images.jianshu.io/upload_images/8103938-cb11bb2e0501e7e5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 添加第一个容器 jnlp（jnlp-slave）
![image.png](https://upload-images.jianshu.io/upload_images/8103938-bd9dc30a6c961e82.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.png](https://upload-images.jianshu.io/upload_images/8103938-a764d6b254c01ef2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 添加第二个容器 docker（因为要在pipeline中构建镜像，需要使用docker客户端，此镜像提供了docker客户端）
![image.png](https://upload-images.jianshu.io/upload_images/8103938-537c51de554ecd69.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 添加第三个容器 maven (这里使用的镜像为：registry.cn-beijing.aliyuncs.com/acs-sample/jenkins-slave-maven:3.3.9-jdk-8-alpine， 也可以使用自定义的maven镜像)
![image.png](https://upload-images.jianshu.io/upload_images/8103938-f33e4e7abfe378dd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- pod 模板的数据卷的设置，如下图所示：
创建docker推送镜像到私用仓库的secret
命令如下：`kubectl create secret generic my-secret --from-file=/root/.docker/config.json`
> 注意： 这里不是 `kubectl create secret docker-registry my-secret --docker-server=DOCKER_REGISTRY_SERVER --docker-username=DOCKER_USER --docker-password=DOCKER_PASSWORD --docker-email=DOCKER_EMAIL
`
这里遇到一个问题，docker 无法推送镜像，报错显示docker没有登录私有仓库，查询原因发现因为我使用docker-registry创建了my-secret，当我改为generic就可以了，详细信息可以查看k8s的secret说明文档。

![image.png](https://upload-images.jianshu.io/upload_images/8103938-76c1e2022968ce10.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


- [Manage Credentials] -> [jenkins] -> [全局凭据] -> [添加凭据]
配置访问k8s的kubeconfig，在pipeline中使用`kubernetesDeploy`的时候会使用到
![image.png](https://upload-images.jianshu.io/upload_images/8103938-794baeff022cdcda.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- [Manage Credentials] -> [jenkins] -> [全局凭据] -> [添加凭据]
设置登录私有镜像仓库的用户名和密码
![image.png](https://upload-images.jianshu.io/upload_images/8103938-1b636ea28adc051f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# 五、使用jenkins CI/CD demo演示
- 新建一个任务 devops-demo
![image.png](https://upload-images.jianshu.io/upload_images/8103938-3f8dce2235275f0a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- devops-demo任务配置如下：
1、指定docker私有仓库地址
![image.png](https://upload-images.jianshu.io/upload_images/8103938-895d366e30fefcde.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
2、指定项目名称
![image.png](https://upload-images.jianshu.io/upload_images/8103938-689d7d49f44d864b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
3、指定要部署的命名空间
![image.png](https://upload-images.jianshu.io/upload_images/8103938-ff53a71e8a82d292.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
4、选择构建的分支
![image.png](https://upload-images.jianshu.io/upload_images/8103938-649f51bfa71e7805.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


5、任务流水线配置
![image.png](https://upload-images.jianshu.io/upload_images/8103938-3b8ddc63da2db369.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
>  说明: 这里使用的仓库代码示例地址如下：https://gitee.com/peterwd/devops-demo.git
在仓库中需要添加三个文件才能实现此devops流程：`Jenkinsfile、Dockerfile、deployment.yaml`
文件的内容可以点击到仓库中查看。

- 保存配置并构建如下图所示
![image.png](https://upload-images.jianshu.io/upload_images/8103938-6719596f1845cfe0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


- 构建成功的效果如下
![image.png](https://upload-images.jianshu.io/upload_images/8103938-12342d748283377e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这里打包阶段用时比较长，那是因为每次构建都需要下载依赖，因为slave运行完成就会被销毁，默认下载的依赖就在slave容器中，会随着slave容器的销毁而消失，所以我们应该把下载的依赖持久化下来，下面介绍如何实现：
1、将下载的依赖持久化到宿主机，使用如下方式配置：
在maven容器中，默认将依赖包放在`/root/.m2/repository`目录下面，所以我们可以将宿主机的指定目录挂载到此目录中：
![image.png](https://upload-images.jianshu.io/upload_images/8103938-2ee90d2361e2e860.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
再次构建可以通过如下方式登录到宿主机查看下载的依赖已经持久化到宿主机对应的目录中：
```
# 登录到minikube节点中
C:\windows\system32>minikube ssh
                         _             _
            _         _ ( )           ( )
  ___ ___  (_)  ___  (_)| |/')  _   _ | |_      __
/' _ ` _ `\| |/' _ `\| || , <  ( ) ( )| '_`\  /'__`\
| ( ) ( ) || || ( ) || || |\`\ | (_) || |_) )(  ___/
(_) (_) (_)(_)(_) (_)(_)(_) (_)`\___/'(_,__/'`\____)

$ cd /tmp/maven/repository/
$ ls -al
total 0
drwxr-xr-x 16 root root 320 Mar 15 10:25 .
drwxr-xr-x  3 root root  60 Mar 15 10:21 ..
drwxr-xr-x  3 root root  60 Mar 15 10:24 backport-util-concurrent
drwxr-xr-x  3 root root  60 Mar 15 10:22 ch
drwxr-xr-x  3 root root  60 Mar 15 10:23 classworlds
drwxr-xr-x  5 root root 100 Mar 15 10:24 com
drwxr-xr-x  3 root root  60 Mar 15 10:23 commons-cli
drwxr-xr-x  3 root root  60 Mar 15 10:25 commons-codec
drwxr-xr-x  3 root root  60 Mar 15 10:25 commons-lang
drwxr-xr-x  4 root root  80 Mar 15 10:25 commons-logging
drwxr-xr-x  8 root root 160 Mar 15 10:22 io
drwxr-xr-x  3 root root  60 Mar 15 10:22 jakarta
drwxr-xr-x  3 root root  60 Mar 15 10:23 junit
drwxr-xr-x  3 root root  60 Mar 15 10:24 log4j
drwxr-xr-x  3 root root  60 Mar 15 10:25 net
drwxr-xr-x 13 root root 260 Mar 15 10:23 org
$
```
2、使用pvc 持久化mave的依赖包，进行如下图所示配置：
![image.png](https://upload-images.jianshu.io/upload_images/8103938-64fa4a082d399374.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 持久化maven依赖包，再次构建耗时对比如下：
![image.png](https://upload-images.jianshu.io/upload_images/8103938-9012513237b307aa.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



# 遇到的问题
## 1. minikube启动失败
```
* 正在 Docker 20.10.3 中准备 Kubernetes v1.20.2…| E0313 13:19:52.379165   33644 start.go:99] Unable to get host IP: No virtual switch found
X Exiting due to GUEST_START: Failed to setup kubeconfig: No virtual switch found
```
如下图所示：
![image.png](https://upload-images.jianshu.io/upload_images/8103938-e695ffee182e1403.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
**出现错误的原因**
第一次由于电脑内存不足导致安装失败，再次启动minikube时报出此错误。
**解决方式**
执行如下命令，删除所有minikube集群，再重新启动即可恢复正常：
```
minikube delete --all
```
## 2. jenkins插件下载失败
部分插件由于缺少依赖无法加载。要恢复这些插件提供的功能，需要修复这些问题并重启 Jenkins。
Dependency errors:
SSH Credentials Plugin (1.18.2)
Jenkins (2.282) or higher required
由于一个或者多个上面的错误导致这些插件无法加载。修复后插件将会再次加载。
![image.png](https://upload-images.jianshu.io/upload_images/8103938-85e0cac1f192bdf6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
**解决方式**
升级jenkins版本为提示的版本，可以直接修改`jenkins-deploy.yaml`文件中的`image: jenkins/jenkins:latest`为`image: jenkins/jenkins:2.283`



参考文章
[minikube快速搭建k8s](https://blog.csdn.net/u014636124/article/details/105145674/)
[kubernetes中部署Jenkins并简单使用](https://www.cnblogs.com/coolops/p/13129955.html) 
[Jenkins 和 Kubernetes -云上的神秘代理](https://www.jenkins.io/zh/blog/2018/09/14/kubernetes-and-secret-agents/ "Jenkins 和 Kubernetes -云上的神秘代理")
[k8s学习笔记之StorageClass+NFS](https://www.cnblogs.com/panwenbin-logs/p/12196286.html)


