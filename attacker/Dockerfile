FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends nmap curl iputils-ping dnsutils && rm -rf /var/lib/apt/lists/*

CMD ["sleep", "infinity"]
