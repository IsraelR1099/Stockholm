NAME := stockholm.py
DIR := infection

all:
	@echo "Usage ./$(NAME)"

setup:
	mkdir -p ~/$(DIR)

fclean:
	rm -rf ~/$(DIR)
