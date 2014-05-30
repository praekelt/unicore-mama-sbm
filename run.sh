#!/bin/bash
cd /praekelt-unicore-mama-sbm/mamasbm && ../ve/bin/gunicorn --paste production.ini
