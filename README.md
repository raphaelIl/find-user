* 결과 예시는 images에서 확인할 수 있습니다.

## How to run
* 외부 접속을 위한 명시가 없기에 따로 ingress를 진행하진 않습니다.
  * k8s 내부에서 `test-python/find` 엔드포인트로 호출하면 결과를 확인할 수 있습니다.
  * ```shell
    kubectl apply -f manifests/Deployment.yaml
    kubectl apply -f manifests/Service.yaml
    ```
* local
  * 필요한 변수를 입력합니다.
    * AWS_ACCESS_KEY_ID
    * AWS_SECRET_ACCESS_KEY
    * E_HOURS
  * docker로 실행시 `http://localhost:$port/find` 엔드포인트로 호출하면 결과를 확인할 수 있습니다.
    * ```shell 
      docker run -P -e "AWS_ACCESS_KEY_ID=" -e "AWS_SECRET_ACCESS_KEY=" -e "E_HOURS=" raphael1021/test-python
      ```
  * local IDE
