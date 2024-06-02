# ai_analysis_log

```zsh
# prepare
$ docker-compose build
# start
$ docker-compose up -d
# request
curl -X POST -d '{"image_path": "/url/image001"}' -H "Content-Type: application/json" -H "Authorization: Bearer dummy_token" http://localhost/analyze-image
# end
$ docker-compose down
```

## etc

docker exec -it python_container bash

コマンドパレット: Dev-Containers: Open Folder In Container

コマンドパレット: Dev-Containers: Reopen Folder Locally

uvicorn main:app --reload
