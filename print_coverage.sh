#!/bin/bash

(source venv/bin/activate;coverage run --omit 'venv/*,test/*' -m pytest;coverage report;deactivate)
