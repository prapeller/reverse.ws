#!/bin/bash

session="rabbitmq"

tmux start-server

tmux new-session -d -s $session -n rabbitmq


tmux selectp -t 1
tmux send-keys "docker start rabbitmq" C-m
tmux send-keys "docker run --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq" C-m

tmux attach-session -t $session
