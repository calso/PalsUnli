# -*- coding: utf-8 -*-
from lettuce import *

@step(u'I see the header "([^"]*)"')
def see_header(step, text):
    header = world.dom.cssselect('h2')[0]
    assert header.text == text

