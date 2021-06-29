from django.shortcuts import render,redirect
from django.contrib import messages
import datetime
# from bs4 import BeautifulSoup
import requests

import os
# import smtplib
import time
import random

# Create your views here.
def home(request):
    return render(request,'app/index.html')



