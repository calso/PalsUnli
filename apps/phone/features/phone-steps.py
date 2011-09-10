# -*- coding: utf-8 -*-
from lettuce import *

@step(u'I see "([^"]*)" link')
def i_see_link(step, text):
    links = world.dom.cssselect('a.add-link')
    for link in links:
        assert link.text == text
        return
    assert False, 'Link not found'

