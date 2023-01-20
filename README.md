# Run docker services
- install docker, docker-compose
- rename .envs/.example to .local
- > make build

# Run test scripts locally
- > python3.10 -m venv venv
- > source venv/bin/activate
- > pip install -r requirements.txt
- > python listen_results.py
- > python queue_reverse_text.py 123
