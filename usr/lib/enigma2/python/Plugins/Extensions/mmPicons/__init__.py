#!/usr/bin/python
# -*- coding: utf-8 -*-

from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
import gettext
from os import environ as os_environ
import os
import sys

PluginLanguageDomain = 'mmPicons'
PluginLanguagePath = 'Extensions/mmPicons/res/locale'


def trace_error():
    import traceback
    try:
        traceback.print_exc(file=sys.stdout)
        traceback.print_exc(file=open('/tmp/Error.log', 'a'))
    except Exception as e:
        print('error: ', str(e))
        pass


def logdata(name="", data=None):
    try:
        line = str(name) + ": " + str(data) + "\n"
        with open("/tmp/mmPicons.log", "a") as fp:
            fp.write(line)
    except BaseException:
        trace_error()


def getversioninfo():
    currversion = '1.4'
    version_file = '/usr/lib/enigma2/python/Plugins/Extensions/mmPicons/version'
    if os.path.exists(version_file):
        try:
            fp = open(version_file, 'r').readlines()
            for line in fp:
                if 'version' in line:
                    currversion = line.split('=')[1].strip()
        except BaseException:
            pass
    logdata("Version ", currversion)
    return (currversion)


def localeInit():
    if os.path.exists('/var/lib/dpkg/status'):
        lang = language.getLanguage()[:2]
        os_environ['LANGUAGE'] = lang
    gettext.bindtextdomain(
        PluginLanguageDomain,
        resolveFilename(
            SCOPE_PLUGINS,
            PluginLanguagePath))


if os.path.exists('/var/lib/dpkg/status'):
    def _(txt):
        return gettext.dgettext(PluginLanguageDomain, txt) if txt else ""

    localeInit()
    language.addCallback(localeInit)
else:
    def _(txt):
        if gettext.dgettext(PluginLanguageDomain, txt):
            return gettext.dgettext(PluginLanguageDomain, txt)
        else:
            print(("[%s] fallback to default translation for %s" %
                  (PluginLanguageDomain, txt)))
            return gettext.gettext(txt)
    language.addCallback(localeInit)
