# DELETE ME?

# -*- coding: utf-8 -*-
#
# pip install git+https://github.com/Tallisado/pyrofactory.git#egg=PyroFactory

from pyro_factory import PyroFactory
import pyrobot_config as config

# mandatory: PAYLOAD
# opt: TYPOLOGY
# opt: BASE_URL
# opt: DISPLAY

pyrofactory = PyroFactory().run(config)
 