#!/usr/bin/env python3.10
import sys
import os

path = '/home/lanxin488/breast-cancer-prediction'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
