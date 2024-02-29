Gradio & FastAPI 동시성 테스트

## 데모 기능
- `click_button1()` : `time.sleep(10)`으로 강제 시간 지연
- `click_button2()` : `for i in range(100000000)`으로 연산을 통한 시간 지연 (약 8초)

## 테스트
- gradio 버튼의 `concurrency_limit` 속성 조절
  - `concurrency_limit=1`
  - `concurrency_limit=3`
- uvicorn의 `workers` 속성 조절
  - `uvicorn test:app --workers 1`
  - `uvicorn test:app --workers 3`
- gunicorn의 `workers` 속성 조절
  - `gunicorn test:app --worker-class uvicorn.workers.UvicornWorker --workers 1`
  - `gunicorn test:app --worker-class uvicorn.workers.UvicornWorker --workers 3`

## 결론
- 데모의 `concurrency_limit` 속성은 데모 페이지에서 버튼을 누를 때만 적용되고 API 호출과는 무관하다.
  - 쓰레드 기반으로 동작함. 따라서, **button2(연산)** 기능을 동시에 사용하면 모든 요청의 속도가 느려짐.
- 데모 및 API 함수 모두에 `async def`를 적용해야, 데모 페이지에서 기능 실행 중에 API 호출이 동시 실행되는 현상을 방지할 수 있음.
- 따라서, 동기적 처리를 원한다면 데모 및 API 모든 함수에서 `async def`를 사용해야함!
  - 대신, 해당 함수를 호출 시 `await`를 사용해야함. 그렇지 않으면, 데모와 API에서 동시 호출 시 `TypeError("'coroutine' object is not iterable")`에러가 발생함.
  - 대신, gradio 데모 페이지에서 queue 대기열이 얼마나 되는지 미리 확인할 수 없음.
  - 데모와 API 양쪽에서 동시 호출했을 때 API 호출이 더 늦었음에도 불구하고 데모보다 우선적으로 처리됨.
- `uvicorn`과 `gunicorn` 모두 프로세스 기반으로 동작한다.
  - `uvicorn test:app --workers 3`으로 **button2(연산)**을 수행한 결과, 모든 요청이 약 8초 소요되었음.
  - `gunicorn test:app --worker-class uvicorn.workers.UvicornWorker --workers 3`으로 **button2(연산)**을 수행한 결과, 모든 요청이 약 8초 소요되었음.
  - 단, `gunicorn`으로 동시요청 테스트 시, `[CRITICAL] WORKER TIMEOUT` 에러가 자주 발생함. (timeout 설정 default가 빡빡한듯)

### 최종 결론 : AI 서비스를 API로 배포할 때
- `concurrency_limit=1`
- 모든 함수에 `async def`를 적용
- `uvicorn test:app --workers 1`

## 참고
- 프로세스 및 쓰레드
- Python GIL