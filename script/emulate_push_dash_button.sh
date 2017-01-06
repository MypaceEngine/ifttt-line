#!/bin/bash

curl http://ifttt-line.appspot.com/dash-receive-text -H 'Content-Type: text/plain' --data-binary '{"title":"hoge", "description":"fuga", "dash":"butada_all-free", "text":""}'
#curl http://helloworld-153914.appspot.com/dash-receive-text -H 'Content-Type: text/plain' --data-binary '{"title":"hoge", "description":"fuga", "dash":"butada_all-free", "text":""}'

