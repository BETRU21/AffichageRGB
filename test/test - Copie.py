import pandas as pd
from tkinter.filedialog import askopenfile
import csv
import os
import fnmatch
import time
import re

from collections import namedtuple

point = namedtuple(("x", "y"), "data")
point = (2, 4, [6,7,8,9])
print(point.x)
