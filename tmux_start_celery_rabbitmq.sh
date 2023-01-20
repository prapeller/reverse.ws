#!/bin/bash

session="celery"

tmux start-server

tmux new-session -d -s $session -n celery


tmux selectp -t 1
tmux send-keys "docker start rabbitmq" C-m
tmux send-keys "docker run --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq" C-m

#tmux splitw -h
#tmux send-keys "docker start redis_tmux" C-m
#tmux send-keys "docker run --name redis -p 6379:6379 redis" C-m

#tmux splitw -h
#tmux send-keys "source venv/bin/activate" C-m
#tmux send-keys "celery -A celery_app worker --loglevel=INFO --concurrency=1" C-m
#
#tmux splitw -h
#tmux send-keys "source venv/bin/activate" C-m
#tmux send-keys "celery -A celery_app flower --loglevel=INFO" C-m

#tmux select-layout even-horizontal

tmux attach-session -t $session
