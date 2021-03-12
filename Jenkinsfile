pipeline{

      // 定义groovy脚本中使用的环境变量
      environment{
        // docker镜像仓库地址  目前我们使用阿里云的镜像服务
        ORIGIN_REPO =  sh(returnStdout: true,script: 'echo $origin_repo').trim()
        // 项目名称
        PROJECT_NAME =  sh(returnStdout: true,script: 'echo $project_name').trim()
        // docker镜像标签 示例：master-20210209105814
        IMAGE_TAG =  sh(returnStdout: true,script: 'echo $branch-`date +%Y%m%d%H%M%S`').trim()
        // 将容器部署到k8s集群的命名空间
        NAMESPACE = sh(returnStdout: true,script: 'echo $namespace').trim()
        // 镜像地址
        IMAGE_URL = sh(returnStdout: true,script: 'echo $image_url').trim()
      }

      // 定义本次构建使用哪个标签的构建环境
      agent{
        node{
          label 'slave-pipeline'
        }
      }

      // "stages"定义项目构建的多个模块，可以添加多个 “stage”， 可以多个 “stage” 串行或者并行执行
      stages{

        // 添加第三个stage， 将容器部署到k8s集群
        stage('Deploy to Kubernetes') {
            steps {
                kubernetesDeploy(
                    configs: 'deployment.yaml',
                    enableConfigSubstitution: true,
                    kubeconfigId: 'kubeconfig'
                )
            }
        }
      }
    }
