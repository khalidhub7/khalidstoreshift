#!/usr/bin/env python3
""" initializing blueprint """
from flask import Blueprint
app_views = Blueprint("app_views", __name__, url_prefix='/khalid_store_shift')


from .cart import *
from .login import *
from .orders import *
from .checkout import *
from .register import *
from .products import *