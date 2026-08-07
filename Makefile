# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jpedra-v <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/7/05 16:08:31 by jpedra-v          #+#    #+#              #
#    Updated: 2026/08/05 16:47:09 by jpedra-v         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #
PYTHON = python3
PIP = pip
MAIN = main.py
SRC_DIR = src

.PHONY: install lint clean fclean run debug

install:
	python3 -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt
	rm -rf maps
	rm -f maps.tar.gz
	venv/bin/python3 -m wget https://cdn.intra.42.fr/document/document/55886/maps.tar.gz
	tar -xvf maps.tar.gz
	rm -rf maps.tar.gz

lint:
	venv/bin/flake8 . --exclude=venv && venv/bin/mypy . --exclude venv --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .mypy_cache .pytest_cache

fclean: clean
	rm -rf maps
	rm -rf venv

run:
	./venv/bin/python3 main.py

debug:
	venv/bin/python3 -m pdb main.py
