#!/bin/bash

# case of ButtonMac in header
curl http://ifttt-line.appspot.com/dash-receive-text -H 'Content-Type: text/plain' -H 'ButtonMac: ac:63:be:00:2e:d2' --data-binary '{}'

# case of DashId in body
#curl http://ifttt-line.appspot.com/dash-receive-text -H 'Content-Type: text/plain' --data-binary '{"title":"hoge", "description":"fuga", "dash":"butada_all-free", "text":""}'

#curl http://helloworld-153914.appspot.com/dash-receive-text -H 'Content-Type: text/plain' --data-binary '{"title":"hoge", "description":"fuga", "dash":"butada_all-free", "text":""}'

