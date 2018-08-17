export SOCKS_HOSTNAME := localhost
export SOCKS_PORT := 1080
export DNS_HOSTNAME := google-public-dns-a.google.com
export DNS_PORT := 53
export LISTEN_HOSTNAME := localhost
export LISTEN_PORT := 53

all: start

install:
	@sudo apt-get -fy install sudo python-daemonize python-socks

dev:
	@sudo SOCKS_HOSTNAME=$(SOCKS_HOSTNAME) SOCKS_PORT=$(SOCKS_PORT) DNS_HOSTNAME=$(DNS_HOSTNAME) DNS_PORT=$(DNS_PORT) LISTEN_HOSTNAME=$(LISTEN_HOSTNAME) LISTEN_PORT=$(LISTEN_PORT) PYTHON_ENV=development python main.py

start:
	@sudo SOCKS_HOSTNAME=$(SOCKS_HOSTNAME) SOCKS_PORT=$(SOCKS_PORT) DNS_HOSTNAME=$(DNS_HOSTNAME) DNS_PORT=$(DNS_PORT) LISTEN_HOSTNAME=$(LISTEN_HOSTNAME) LISTEN_PORT=$(LISTEN_PORT) PYTHON_ENV=production python main.py
