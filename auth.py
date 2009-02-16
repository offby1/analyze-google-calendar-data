#!/usr/bin/env python

"""
Authenticate against Google's Calendar APIs.  This requires that you
download and install
http://gdata-python-client.googlecode.com/files/gdata.py-1.2.4.tar.gz
or something quite similar.
"""

from __future__ import with_statement
__author__ = ""
__version__ = "$Id$"

from xml.etree import ElementTree
import atom
import atom.service
import gdata.calendar
import gdata.calendar.service
import gdata.service
import getopt
import string
import sys
import time

def auth(email, password):
    calendar_service = gdata.calendar.service.CalendarService()
    calendar_service.email = email
    calendar_service.password = password
    calendar_service.source = "eric.hanchrow-gcaldeduplicator-version0"
    calendar_service.ProgrammaticLogin()

    return calendar_service
