import sys

import os
import cv2
import json
import math
import time
import string
import imutils
import datetime
import requests
import waitress
import threading
import collections
import numpy as np

from PIL import Image, ImageDraw, ImageFont

from pathlib import Path

# Flask
from flask import (
	Flask,
	request as FlaskRequest,
	Response as FlaskResponse,
	redirect as FlaskRedirect,
	abort as FlaskAbort,
	render_template as FlaskTemplate
)

# RFTLib
from RFTLib.Core.Object import *
from RFTLib.Core.Table import *
from RFTLib.Core.Buffer import *
from RFTLib.Core.Resource import *
from RFTLib.Core.Structure import *
from RFTLib.Core.Exception import *




# ~~~~~~~~~~~~~ Data ~~~~~~~~~~~~~
Data_Obj = RFT_Resource(
	"./res/data",
	{
		r"yaml": RFT_Resource_YAML
	}
)

Data = Data_Obj.load()
Data.lift("Data")
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~ Tables ~~~~~~~~~~~~
Tables_Obj = RFT_Table(
	"./res/tables"
)
Tables_Obj.indent = True

Tables_Obj.saveEvery(30)

Tables = Tables_Obj.data
Tables.lift("Tables")
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

