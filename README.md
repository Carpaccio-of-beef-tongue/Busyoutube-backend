# busyoutube-backend

# how to use
```
docker-compose up -d
```
これでバックエンドサーバーは立ち上がる
結果を見たいときは下を実行(ブラウザでもよい)
```
curl localhost:5001
```
```
curl -X POST -H "Content-Type: application/json" -d '{"youtube_link": "<youtube_link>"}' "http://localhost:5001/process_youtube_link"
```