# coding=utf-8
from __future__ import print_function, unicode_literals

import datetime
from bgmi.script import ScriptBase


class Script(ScriptBase):

    class Model(ScriptBase.Model):
        bangumi_name = '三月的狮子 第二季'
        cover = 'COVER URL'
        update_time = 'Tue'
        due_date = datetime.datetime(2018, 1, 30)
        source = 'dmhy'
        _bangumi_id = '的獅子'
