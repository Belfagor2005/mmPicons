#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
****************************************
*           coded by Lululla           *
*         improve code by jbleyel      *
*             skin by MMark            *
*             09/05/2021               *
*          fixed by @jbleyel           *
****************************************
'''
#Info https://e2skin.blogspot.com/
from __future__ import print_function, unicode_literals
from . import _
from Components.ActionMap import ActionMap, NumberActionMap
from Components.AVSwitch import AVSwitch
from Components.Button import Button
from Components.ConfigList import ConfigListScreen
from Components.HTMLComponent import *
from Components.Input import Input
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.PluginComponent import plugins
from Components.PluginList import *
from Components.ProgressBar import ProgressBar
from Components.ScrollLabel import ScrollLabel
from Components.Pixmap import Pixmap
from Components.Sources.List import List
from Components.Sources.Progress import Progress
from Components.Sources.StaticText import StaticText
from Components.Sources.Source import Source
from Components.config import *
from Plugins.Plugin import PluginDescriptor
from Screens.ChoiceBox import ChoiceBox
from Screens.Console import Console
from Screens.LocationBox import LocationBox
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.Standby import *
from Screens.Standby import TryQuitMainloop
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Tools.Directories import SCOPE_SKIN_IMAGE, SCOPE_PLUGINS, SCOPE_LANGUAGE
from Tools.Directories import pathExists, resolveFilename, fileExists, copyfile
from Tools.Downloader import downloadWithProgress
from Tools.LoadPixmap import LoadPixmap
from enigma import *
from enigma import ePicLoad, loadPic
from enigma import RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_HALIGN_CENTER
from enigma import getDesktop, loadPNG, gFont
from enigma import eListbox, eTimer, eListboxPythonMultiContent, eConsoleAppContainer
from os import path, listdir, remove, mkdir, access, X_OK, chmod
from twisted.web.client import downloadPage, getPage
from xml.dom import Node, minidom
import base64
import os
import re
import sys
import shutil
import ssl
import socket
import subprocess
import glob
import six
from sys import version_info
global skin_path, mmkpicon, mpdDreamOs, pngs, pngl, pngx, XStreamity


def logdata(name='', data=None):
    try:
        data = str(data)
        fp = open('/tmp/mmPicons.log', 'a')
        fp.write(str(name) + ': ' + data + "\n")
        fp.seek(0)
        fp.close()
    except:
        trace_error()
        pass


def getversioninfo():
    currversion = '1.2'
    version_file = '/usr/lib/enigma2/python/Plugins/Extensions/mmPicons/version'
    if os.path.exists(version_file):
        try:
            fp = open(version_file, 'r').readlines()
            for line in fp:
                if 'version' in line:
                    currversion = line.split('=')[1].strip()
        except:
            pass
    logdata("Version ", currversion)
    return (currversion)


mpdDreamOs = False
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
PY3 = sys.version_info[0] == 3
if PY3:
    from urllib.request import urlopen, Request
    from urllib.error import URLError, HTTPError
    from urllib.request import urlretrieve
else:
    from urllib2 import urlopen, Request, URLError
    from urllib import urlretrieve

try:
    from enigma import eMediaDatabase
    mpdDreamOs = True
except:
    mpdDreamOs = False

try:
    from enigma import eDVBDB
except ImportError:
    eDVBDB = None

try:
    import zipfile
except:
    pass

def checkStr(txt):
    if PY3:
        if isinstance(txt, type(bytes())):
            txt = txt.decode('utf-8')
    else:
        if isinstance(txt, type(six.text_type())):
            txt = txt.encode('utf-8')
    return txt

def checkInternet():
    try:
        response = checkStr(urlopen("http://google.com", None, 5))
        response.close()
    except HTTPError:
        return False
    except URLError:
        return False
    except socket.timeout:
        return False
    else:
        return True


try:
    from OpenSSL import SSL
    from twisted.internet import ssl
    from twisted.internet._sslverify import ClientTLSOptions
    sslverify = True
except:
    sslverify = False

if sslverify:
    try:
        from urlparse import urlparse
    except:
        from urllib.parse import urlparse

    class SNIFactory(ssl.ClientContextFactory):
        def __init__(self, hostname=None):
            self.hostname = hostname

        def getContext(self):
            ctx = self._contextFactory(self.method)
            if self.hostname:
                ClientTLSOptions(self.hostname, ctx)
            return ctx

#for download on ATV 6.5
#CHECK THI ISSUE
#https://github.com/openatv/enigma2/commit/3974e84a59be2a8eb4d2250a876713d38e8f56b4

def checkMyFile(url):
    # FIXME urlopen will cause a full download of file and this is not what you want //thank's @jbleyel
    return []
    try:
        dest = "/tmp/download.zip"
        req = Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        req.add_header('Referer', 'https://www.mediafire.com/')
        req.add_header('X-Requested-With', 'XMLHttpRequest')
        page = urlopen(req)
        r = page.read()
        n1 = r.find('"Download file"', 0)
        n2 = r.find('Repair your download', n1)
        r2 = r[n1:n2]
        myfile = re.findall('href="http://download(.*?)">', r2)
        return myfile
    except:
        e = URLError #, e:
        print('We failed to open "%s".' % url)
        if hasattr(e, 'code'):
            print('We failed with error code - %s.' % e.code)
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        return ''
    return

def make_request(url):
    try:
        req = Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0')
        response = urlopen(req)
        link = response.read()
        response.close()
        return link
    except:
        e = URLError #, e:
        print('We failed to open "%s".' % url)
        if hasattr(e, 'code'):
            print('We failed with error code - %s.' % e.code)
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)

def trace_error():
    import traceback
    try:
        traceback.print_exc(file=sys.stdout)
        traceback.print_exc(file=open('/tmp/traceback.log', 'a'))
    except:
        pass

def freespace():
    try:
        diskSpace = os.statvfs('/')
        capacity = float(diskSpace.f_bsize * diskSpace.f_blocks)
        available = float(diskSpace.f_bsize * diskSpace.f_bavail)
        fspace = round(float(available / 1048576.0), 2)
        tspace = round(float(capacity / 1048576.0), 1)
        spacestr = 'Free space(' + str(fspace) + 'MB)\nTotal space(' + str(tspace) + 'MB)'
        return spacestr
    except:
        return ''


def deletetmp():
    os.system('rm -rf /tmp/unzipped;rm -f /tmp/*.ipk;rm -f /tmp/*.tar;rm -f /tmp/*.zip;rm -f /tmp/*.tar.gz;rm -f /tmp/*.tar.bz2;rm -f /tmp/*.tar.tbz2;rm -f /tmp/*.tar.tbz')
    return

pblk = 'aHR0cHM6Ly93d3cubWVkaWFmaXJlLmNvbS9hcGkvMS41L2ZvbGRlci9nZXRfY29udGVudC5waHA/Zm9sZGVyX2tleT1vdnowNG1ycHpvOXB3JmNvbnRlbnRfdHlwZT1mb2xkZXJzJmNodW5rX3NpemU9MTAwMCZyZXNwb25zZV9mb3JtYXQ9anNvbg=='
ptrs = 'aHR0cHM6Ly93d3cubWVkaWFmaXJlLmNvbS9hcGkvMS41L2ZvbGRlci9nZXRfY29udGVudC5waHA/Zm9sZGVyX2tleT10dmJkczU5eTlocjE5JmNvbnRlbnRfdHlwZT1mb2xkZXJzJmNodW5rX3NpemU9MTAwMCZyZXNwb25zZV9mb3JtYXQ9anNvbg=='
ptmov = 'aHR0cHM6Ly93d3cubWVkaWFmaXJlLmNvbS9hcGkvMS41L2ZvbGRlci9nZXRfY29udGVudC5waHA/Zm9sZGVyX2tleT1uazh0NTIyYnY0OTA5JmNvbnRlbnRfdHlwZT1maWxlcyZjaHVua19zaXplPTEwMDAmcmVzcG9uc2VfZm9ybWF0PWpzb24='
ecskins = 'aHR0cHM6Ly93d3cubWVkaWFmaXJlLmNvbS9hcGkvMS41L2ZvbGRlci9nZXRfY29udGVudC5waHA/Zm9sZGVyX2tleT1jOHN3MGFoc3Mzc2kwJmNvbnRlbnRfdHlwZT1maWxlcyZjaHVua19zaXplPTEwMDAmcmVzcG9uc2VfZm9ybWF0PWpzb24='
openskins = 'aHR0cHM6Ly93d3cubWVkaWFmaXJlLmNvbS9hcGkvMS41L2ZvbGRlci9nZXRfY29udGVudC5waHA/Zm9sZGVyX2tleT0wd3o0M3l2OG5zeDc5JmNvbnRlbnRfdHlwZT1maWxlcyZjaHVua19zaXplPTEwMDAmcmVzcG9uc2VfZm9ybWF0PWpzb24='
host_trs = base64.b64decode(ptrs)
host_blk = base64.b64decode(pblk)
host_mov = base64.b64decode(ptmov)
host_skin = base64.b64decode(ecskins)
host_skinz = base64.b64decode(openskins)
config.plugins.mmPicons = ConfigSubsection()
config.plugins.mmPicons.mmkpicon = ConfigDirectory(default='/media/hdd/picon/')
HD = getDesktop(0).size()
plugin_path = os.path.dirname(sys.modules[__name__].__file__)
currversion = getversioninfo()
desc_plug = '..:: mMark Picons & Skins V. %s ::..' % currversion
title_plug = 'mMark Blog - www.e2skin.blogspot.com'
XStreamity = False
skin_path = plugin_path
ico_path = plugin_path + '/logo.png'
no_cover = plugin_path + '/no_coverArt.png'
res_plugin_path = plugin_path + '/res/'
ico1_path = res_plugin_path + 'pics/plugin.png'
ico3_path = res_plugin_path + 'pics/setting.png'
res_picon_plugin_path = res_plugin_path + 'picons/'
piconstrs = res_picon_plugin_path + 'picon_trs.png'
piconsblk = res_picon_plugin_path + 'picon_blk.png'
piconszeta = res_picon_plugin_path + 'picon_z.png'
piconsmovie = res_picon_plugin_path + 'picon_mv.png'
pixmaps = res_picon_plugin_path + 'backg.png'
mmkpicon = config.plugins.mmPicons.mmkpicon.value.strip()

if mmkpicon.endswith('/'):
    mmkpicon = mmkpicon[:-1]
if not os.path.exists(mmkpicon):
    try:
        os.makedirs(mmkpicon)
    except OSError as e:
        print(('Error creating directory %s:\n%s') % (mmkpicon, str(e)))

logdata("path picons: ", str(mmkpicon))


if HD.width() > 1280:
    skin_path = res_plugin_path + 'skins/fhd/'
else:
    skin_path = res_plugin_path + 'skins/hd/'
if mpdDreamOs:
    skin_path = skin_path + 'dreamOs/'


class mmList(MenuList):
    def __init__(self, list):
        MenuList.__init__(self, list, False, eListboxPythonMultiContent)
        self.l.setFont(0, gFont('Regular', 20))
        self.l.setFont(1, gFont('Regular', 22))
        self.l.setFont(2, gFont('Regular', 24))
        self.l.setFont(3, gFont('Regular', 26))
        self.l.setFont(4, gFont('Regular', 28))
        self.l.setFont(5, gFont('Regular', 30))
        self.l.setFont(6, gFont('Regular', 32))
        self.l.setFont(7, gFont('Regular', 34))
        self.l.setFont(8, gFont('Regular', 36))
        self.l.setFont(9, gFont('Regular', 40))
        if HD.width() > 1280:
            self.l.setItemHeight(50)
        else:
            self.l.setItemHeight(40)


def OnclearMem():
    try:
        os.system("sync")
        os.system("echo 1 > /proc/sys/vm/drop_caches")
        os.system("echo 2 > /proc/sys/vm/drop_caches")
        os.system("echo 3 > /proc/sys/vm/drop_caches")
    except:
        pass


def DailyListEntry(name, idx):
    pngs = ico1_path
    res = [name]
    if fileExists(pngs):
        if HD.width() > 1280:
            res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 12), size=(34, 25), png=loadPNG(pngs)))
            res.append(MultiContentEntryText(pos=(60, 0), size=(1900, 50), font=7, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
        else:
            res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 6), size=(34, 25), png=loadPNG(pngs)))
            res.append(MultiContentEntryText(pos=(60, 0), size=(1000, 50), font=2, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT))
        return res


def oneListEntry(name):
    pngx = ico1_path
    res = [name]
    if HD.width() > 1280:
        res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 12), size=(34, 25), png=loadPNG(pngx)))
        res.append(MultiContentEntryText(pos=(60, 0), size=(1900, 50), font=7, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    else:
        res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 6), size=(34, 25), png=loadPNG(pngx)))
        res.append(MultiContentEntryText(pos=(60, 0), size=(1000, 50), font=2, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT))
    return res


def showlist(data, list):
    icount = 0
    plist = []
    for line in data:
        name = data[icount]
        plist.append(oneListEntry(name))
        icount = icount + 1
        list.setList(plist)


Panel_list3 = [
 ('PICONS BLACK'),
 ('PICONS TRANSPARENT'),
 ('PICONS MOVIE'),
 ('SKIN DMM ZETA'),
 ('SKIN OPEN ZETA')]


class SelectPicons(Screen):

    def __init__(self, session):
        self.session = session
        skin = skin_path + 'mmall.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('Select Picons')
        Screen.__init__(self, session)
        self.setTitle(title_plug)
        self['text'] = mmList([])
        self.working = False
        self.selection = 'all'
        self['pth'] = Label('')
        self['pth'].setText(_('Picons folder ') + mmkpicon)
        self['poster'] = Pixmap()
        self['space'] = Label('')
        self['info'] = Label('')
        self['info'].setText(_('Please select ...'))
        self['key_green'] = Button(_('Remove'))
        self['key_red'] = Button(_('Exit'))
        self['key_yellow'] = Button(_('Preview'))
        self["key_blue"] = Button(_('Restart'))
        self['progress'] = ProgressBar()
        self['progresstext'] = StaticText()
        self["progress"].hide()
        self['progresstext'].text = ''
        self.currentList = 'text'
        self.menulist = []
        self['title'] = Label(title_plug)
        self['actions'] = NumberActionMap(['SetupActions', 'DirectionActions', 'ColorActions', "MenuActions"], {'ok': self.okRun,
         'green': self.remove,
         'back': self.closerm,
         'red': self.closerm,
         'yellow': self.zoom,
         'blue': self.msgtqm,
         'up': self.up,
         'down': self.down,
         'left': self.left,
         'right': self.right,
         'menu': self.goConfig,
         'cancel': self.closerm}, -1)
        self.onLayoutFinish.append(self.updateMenuList)

    def zoom(self):
        self.session.open(PiconsPreview, pixmaps)

    def getfreespace(self):
        fspace = freespace()
        self['space'].setText(fspace)
        logdata("freespace ", fspace)

    def closerm(self):
        self.close()

    def msgtqm(self):
        self.mbox = self.session.openWithCallback(self.restartenigma, MessageBox, _("Do you want to restart Enigma?"), MessageBox.TYPE_YESNO)

    def restartenigma(self, result):
        if result:
            self.session.open(TryQuitMainloop, 3)
        else:
            return

    def updateMenuList(self):
        self.menu_list = []
        for x in self.menu_list:
            del self.menu_list[0]
        list = []
        idx = 0
        for x in Panel_list3:
            list.append(DailyListEntry(x, idx))
            self.menu_list.append(x)
            idx += 1
        self['text'].setList(list)
        self.getfreespace()
        self.load_poster()

    def okRun(self):
        self.keyNumberGlobalCB(self['text'].getSelectedIndex())

    def keyNumberGlobalCB(self, idx):
        sel = self.menu_list[idx]
        if sel == ('PICONS BLACK'):
            self.session.open(MMarkFolderScreen, host_blk, piconsblk)
        elif sel == 'PICONS TRANSPARENT':
            self.session.open(MMarkFolderScreen, host_trs, piconstrs)
        elif sel == ('PICONS MOVIE'):
            self.session.open(MMarkPiconScreen, 'MMark-Picons', host_mov, piconsmovie, True)
        elif sel == ('SKIN DMM ZETA'):
            self.session.open(MMarkFolderSkinZeta, host_skin)
        elif sel == ('SKIN OPEN ZETA'):
            self.session.open(MMarkFolderSkinZeta, host_skinz)
        else:
            self.mbox = self.session.open(MessageBox, _(':P  COMING SOON!!!'), MessageBox.TYPE_INFO, timeout=4)

    def remove(self):
        self.session.openWithCallback(self.okRemove, MessageBox, (_("Do you want to remove all picons in folder?\n%s\nIt could take a few minutes, wait .." % mmkpicon)), MessageBox.TYPE_YESNO)

    def okRemove(self, result):
        if result:
            self['info'].setText(_('Erase %s... please wait' % mmkpicon))
            print("Picons folder : ", mmkpicon)
            piconsx = glob.glob(str(mmkpicon) + '/*.png')
            logdata("piconsx ", piconsx)
            for f in piconsx:
                try:
                    print("processing file: " + f)
                    os.remove(f)
                except OSError as e:
                    print("Error: %s : %s" % (f, e.strerror))
                    logdata("Error ", e.strerror)
        self.mbox = self.session.open(MessageBox, _('%s it has been cleaned' % mmkpicon), MessageBox.TYPE_INFO, timeout=4)
        self['info'].setText(_('Please select ...'))

    def goConfig(self):
        self.session.open(mmConfig)

    def up(self):
        self[self.currentList].up()
        self.load_poster()

    def down(self):
        self[self.currentList].down()
        self.load_poster()

    def left(self):
        self[self.currentList].pageUp()
        self.load_poster()

    def right(self):
        self[self.currentList].pageDown()
        self.load_poster()

    def load_poster(self):
        global pixmaps
        sel = self['text'].getSelectedIndex()
        if sel == 0:
            pixmaps = piconsblk
        elif sel == 1:
            pixmaps = piconstrs
        elif sel == 2:
            pixmaps = piconsmovie
        else:
            pixmaps = piconszeta
        if mpdDreamOs:
            self['poster'].instance.setPixmap(gPixmapPtr())
        else:
            self['poster'].instance.setPixmap(None)
        self['poster'].hide()
        sc = AVSwitch().getFramebufferScale()
        self.picload = ePicLoad()
        size = self['poster'].instance.size()
        self.picload.setPara((size.width(),
         size.height(),
         sc[0],
         sc[1],
         False,
         1,
         '#FF000000'))
        ptr = self.picload.getData()
        if mpdDreamOs:
            if self.picload.startDecode(pixmaps, False) == 0:
                ptr = self.picload.getData()
        else:
            if self.picload.startDecode(pixmaps, 0, 0, False) == 0:
                ptr = self.picload.getData()
        if ptr != None:
            self['poster'].instance.setPixmap(ptr)
            self['poster'].show()
        else:
            print('no cover.. error')
        return


class MMarkPiconScreen(Screen):

    def __init__(self, session, name, url, pixmaps, movie=False):
        self.session = session
        skin = skin_path + 'mmall.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('Picons & Skins')
        Screen.__init__(self, session)
        self.setTitle(title_plug)
        self.list = []
        self['text'] = mmList([])
        self.icount = 0
        self['info'] = Label(_('Load selected filter list, please wait ...'))
        self['pth'] = Label('')
        self['pth'].setText(_('Picons folder ') + mmkpicon)
        self['poster'] = Pixmap()
        self['progress'] = ProgressBar()
        self['progresstext'] = StaticText()
        self["progress"].hide()
        self['progresstext'].text = ''
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_('Preview'))
        self["key_blue"] = Button(_(''))
        self['key_blue'].hide()
        self['space'] = Label('')
        self.currentList = 'text'
        self.menulist = []
        self.getfreespace()
        self.downloading = False
        self.url = url
        self.name = name
        self.timer = eTimer()
        self.timer.start(500, 1)
        self.pixmaps = pixmaps
        self.movie = movie
        if mpdDreamOs:
            self.timer_conn = self.timer.timeout.connect(self.downxmlpage)
        else:
            self.timer.callback.append(self.downxmlpage)
        self['title'] = Label(title_plug)
        self['actions'] = ActionMap(['SetupActions', 'DirectionActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         "yellow": self.zoom,
         'up': self.up,
         'down': self.down,
         'left': self.left,
         'right': self.right,
         'cancel': self.close}, -2)

    def zoom(self):
        self.session.open(PiconsPreview, self.pixmaps)

    def getfreespace(self):
        fspace = freespace()
        self['space'].setText(fspace)

    def downxmlpage(self):
        url = six.ensure_binary(self.url)
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)

    def errorLoad(self, error):
        print(str(error))
        self['info'].setText(_('Try again later ...'))
        logdata("errorLoad ", error)
        self.downloading = False

    def _gotPageLoad(self, data):
        r = six.ensure_str(data)
        self.names = []
        self.urls = []
        try:
            n1 = r.find('"quickkey":', 0)
            n2 = r.find('more_chunks', n1)
            data2 = r[n1:n2]
            regex = 'filename":"(.*?)".*?"created":"(.*?)".*?"downloads":"(.*?)".*?"normal_download":"(.*?)"'
            match = re.compile(regex, re.DOTALL).findall(data2)
            for name, data, download, url in match:
                if 'zip' in url:
                    url = url.replace('\\', '')
                    if self.movie:
                        name = name.replace('_', ' ').replace('-', ' ').replace('mmk', '').replace('.zip', '')
                        name = name + ' ' + data[0:10] + ' ' + 'Down: ' + download
                    else:
                        name = name.replace('_', ' ').replace('mmk', 'MMark').replace('.zip', '')
                        name = name + ' ' + data[0:10] + ' ' + 'Down:' + download
                    self.urls.append(url)
                    self.names.append(name)
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])
            self.downloading = True
        except:
            self.downloading = False
        if self.movie:
            self.load_poster()

    def okRun(self):
        self.session.openWithCallback(self.okInstall, MessageBox, (_("Do you want to install?\nIt could take a few minutes, wait ..")), MessageBox.TYPE_YESNO)

    def okInstall(self, result):
        self['info'].setText(_('... please wait'))
        if result:
            if self.downloading == True:

                idx = self["text"].getSelectionIndex()
                self.name = self.names[idx]
                url = self.urls[idx]
                dest = "/tmp/download.zip"
                if os.path.exists(dest):
                    os.remove(dest)
                myfile = checkMyFile(url)
                for url in myfile:
                    img = no_cover
                    url = 'http://download' + url
                self.download = downloadWithProgress(url, dest)
                self.download.addProgress(self.downloadProgress)
                self.download.start().addCallback(self.install).addErrback(self.showError)
            else:
                self['info'].setText(_('Picons Not Installed ...'))

    def install(self, fplug):
        if os.path.exists('/tmp/download.zip'):
            self['info'].setText(_('Install ...'))
            myCmd = "unzip -o -q '/tmp/download.zip' -d %s/" % str(mmkpicon)
            logdata("install2 ", myCmd)
            subprocess.Popen(myCmd, shell=True, executable='/bin/bash')
            self.mbox = self.session.open(MessageBox, _('Successfully Picons Installed'), MessageBox.TYPE_INFO, timeout=5)
        self['info'].setText(_('Please select ...'))
        self['progresstext'].text = ''
        self.progclear = 0
        self['progress'].setValue(self.progclear)
        self["progress"].hide()
        self.downloading = False                                

    def downloadProgress(self, recvbytes, totalbytes):
        self["progress"].show()
        self['progress'].value = int(100 * recvbytes / float(totalbytes))
        self['progresstext'].text = '%d of %d kBytes (%.2f%%)' % (recvbytes / 1024, totalbytes / 1024, 100 * recvbytes / float(totalbytes))

    def showError(self, error):
        print("download error =", error)
        logdata("showerror ", error)
        self.close()

    def cancel(self, result=None):
        self.close(None)
        return

    def up(self):
        self[self.currentList].up()
        self.load_poster()

    def down(self):
        self[self.currentList].down()
        self.load_poster()

    def left(self):
        self[self.currentList].pageUp()
        self.load_poster()

    def right(self):
        self[self.currentList].pageDown()
        self.load_poster()

    def load_poster(self):
        if mpdDreamOs:
            self['poster'].instance.setPixmap(gPixmapPtr())
        else:
            self['poster'].instance.setPixmap(None)
        self['poster'].hide()
        sc = AVSwitch().getFramebufferScale()
        self.picload = ePicLoad()
        size = self['poster'].instance.size()
        self.picload.setPara((size.width(),
         size.height(),
         sc[0],
         sc[1],
         False,
         1,
         '#FF000000'))
        ptr = self.picload.getData()
        if mpdDreamOs:
            if self.picload.startDecode(self.pixmaps, False) == 0:
                ptr = self.picload.getData()
        else:
            if self.picload.startDecode(self.pixmaps, 0, 0, False) == 0:
                ptr = self.picload.getData()
        if ptr != None:
            self['poster'].instance.setPixmap(ptr)
            self['poster'].show()
        else:
            print('no cover.. error')
        return


class MMarkFolderScreen(Screen):

    def __init__(self, session, url, pixmaps):
        self.session = session
        skin = skin_path + 'mmall.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('Picons & Skins')
        Screen.__init__(self, session)
        self.setTitle(title_plug)
        self.list = []
        self['text'] = mmList([])
        self.icount = 0
        self['info'] = Label(_('Load selected filter list, please wait ...'))
        self['pth'] = Label('')
        self['pth'].setText(_('Picons folder ') + mmkpicon)
        self['poster'] = Pixmap()
        self['progress'] = ProgressBar()
        self['progresstext'] = StaticText()
        self["progress"].hide()
        self['progresstext'].text = ''
        self['key_green'] = Button(_('Select'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_('Preview'))
        self["key_blue"] = Button(_(''))
        self['key_blue'].hide()
        self['space'] = Label('')
        self.currentList = 'text'
        self.menulist = []
        self.getfreespace()
        self.downloading = False
        self.timer = eTimer()
        self.timer.start(500, 1)
        self.url = url
        self.pixmaps = pixmaps
        if mpdDreamOs:
            self.timer_conn = self.timer.timeout.connect(self.downxmlpage)
        else:
            self.timer.callback.append(self.downxmlpage)
        self['title'] = Label(title_plug)
        self['actions'] = ActionMap(['SetupActions', 'DirectionActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         "yellow": self.zoom,
         'up': self.up,
         'down': self.down,
         'left': self.left,
         'right': self.right,
         'cancel': self.close}, -2)

    def zoom(self):
        self.session.open(PiconsPreview, pixmaps)

    def getfreespace(self):
        fspace = freespace()
        self['space'].setText(fspace)

    def downxmlpage(self):
        url = six.ensure_binary(self.url)
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)

    def errorLoad(self, error):
        print(str(error))
        self['info'].setText(_('Try again later ...'))
        logdata("errorLoad ", error)
        self.downloading = False

    def _gotPageLoad(self, data):
        r = six.ensure_str(data)
        self.names = []
        self.urls = []
        try:
            n1 = r.find('"folderkey"', 0)
            n2 = r.find('more_chunks', n1)
            data2 = r[n1:n2]
            regex = '{"folderkey":"(.*?)".*?"name":"(.*?)".*?"created":"(.*?)"'
            match = re.compile(regex, re.DOTALL).findall(data2)
            for url, name, data in match:
                url = 'https://www.mediafire.com/api/1.5/folder/get_content.php?folder_key=' + url + '&content_type=files&chunk_size=1000&response_format=json'
                url = url.replace('\\', '')
                pic = no_cover
                name = 'Picons-' + name
                self.urls.append(url)
                self.names.append(name)
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])
            self.downloading = True
        except:
            self.downloading = False
        self.load_poster()

    def okRun(self):
        idx = self['text'].getSelectionIndex()
        if idx == -1 or None:
            return
        name = self.names[idx]
        url = self.urls[idx]
        self.session.open(MMarkPiconScreen, name, url, self.pixmaps)

    def cancel(self, result=None):
        self.close(None)
        return

    def goConfig(self):
            self.session.open(mmConfig)

    def up(self):
        self[self.currentList].up()
        self.load_poster()

    def down(self):
        self[self.currentList].down()
        self.load_poster()

    def left(self):
        self[self.currentList].pageUp()
        self.load_poster()

    def right(self):
        self[self.currentList].pageDown()
        self.load_poster()

    def load_poster(self):
        if mpdDreamOs:
            self['poster'].instance.setPixmap(gPixmapPtr())
        else:
            self['poster'].instance.setPixmap(None)
        self['poster'].hide()
        sc = AVSwitch().getFramebufferScale()
        self.picload = ePicLoad()
        size = self['poster'].instance.size()
        self.picload.setPara((size.width(),
         size.height(),
         sc[0],
         sc[1],
         False,
         1,
         '#FF000000'))
        ptr = self.picload.getData()
        if mpdDreamOs:
            if self.picload.startDecode(self.pixmaps, False) == 0:
                ptr = self.picload.getData()
        else:
            if self.picload.startDecode(self.pixmaps, 0, 0, False) == 0:
                ptr = self.picload.getData()
        if ptr != None:
            self['poster'].instance.setPixmap(ptr)
            self['poster'].show()
        else:
            print('no cover.. error')
        return

class MMarkFolderSkinZeta(Screen):

    def __init__(self, session, url):
        self.session = session
        skin = skin_path + 'mmall.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('Picons & Skins')
        Screen.__init__(self, session)
        self.setTitle(title_plug)
        self.list = []
        self['text'] = mmList([])

        self.icount = 0
        self['info'] = Label(_('Load selected filter list, please wait ...'))
        self['pth'] = Label('')
        self['pth'].setText(_('Picons folder ') + mmkpicon)
        self['poster'] = Pixmap()
        self['progress'] = ProgressBar()
        self['progresstext'] = StaticText()
        self["progress"].hide()
        self['progresstext'].text = ''
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_('Preview'))
        self["key_blue"] = Button(_(''))
        self['key_blue'].hide()
        self['space'] = Label('')
        self.currentList = 'text'
        self.menulist = []
        self.getfreespace()
        self.downloading = False
        self.url = url
        self.name = 'MMark-Skins'
        self.timer = eTimer()
        self.timer.start(500, 1)
        if mpdDreamOs:
            self.timer_conn = self.timer.timeout.connect(self.downxmlpage)
        else:
            self.timer.callback.append(self.downxmlpage)
        self['title'] = Label(title_plug)
        self['actions'] = ActionMap(['SetupActions', 'DirectionActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         "yellow": self.zoom,
         'up': self.up,
         'down': self.down,
         'left': self.left,
         'right': self.right,
         'cancel': self.close}, -2)

    def zoom(self):
        self.session.open(PiconsPreview, pixmaps)

    def GetPicturePath(self):
        ActiveZoom = False
        realpng = pixmaps
        if path.isfile(realpng):
            ActiveZoom = True
        return realpng

    def getfreespace(self):
        fspace = freespace()
        self['space'].setText(fspace)

    def downxmlpage(self):
        url = six.ensure_binary(self.url)
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)

    def errorLoad(self, error):
        print(str(error))
        self['info'].setText(_('Try again later ...'))
        logdata("errorLoad ", error)
        self.downloading = False

    def _gotPageLoad(self, data):
        r = six.ensure_str(data)
        self.names = []
        self.urls = []
        try:
            n1 = r.find('"quickkey":', 0)
            n2 = r.find('more_chunks', n1)
            data2 = r[n1:n2]
            regex = 'filename":"(.*?)".*?"created":"(.*?)".*?"downloads":"(.*?)".*?"normal_download":"(.*?)"'
            match = re.compile(regex, re.DOTALL).findall(data2)
            for name, data, download, url in match:
                if 'zip' in url:
                    url = url.replace('\\', '')
                    name = name.replace('_', ' ').replace('-', ' ').replace('mmk', '').replace('.zip', '')
                    name = name + ' ' + data[0:10] + ' ' + 'Down: ' + download
                    self.urls.append(url)
                    self.names.append(name)
            self['info'].setText(_('Please select ...'))
            showlist(self.names, self['text'])
            self.downloading = True
        except:
            self.downloading = False
        self.load_poster()

    def okRun(self):
        self.session.openWithCallback(self.okInstall, MessageBox, (_("Do you want to install?\nIt could take a few minutes, wait ..")), MessageBox.TYPE_YESNO)

    def okInstall(self, result):
        self['info'].setText(_('... please wait'))
        if result:
            if self.downloading == True:
                if not os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/XStreamity/plugin.pyo') and 'xstreamity' in self.name:
                    self.mbox = self.session.open(MessageBox, _('Xstreamity Player not installed'), MessageBox.TYPE_INFO, timeout=4)
                    return
                idx = self["text"].getSelectionIndex()
                self.name = self.names[idx]
                url = self.urls[idx]
                dest = "/tmp/download.zip"
                if os.path.exists(dest):
                    os.remove(dest)
                myfile = checkMyFile(url)
                for url in myfile:
                    img = no_cover
                    url = 'http://download' + url
                self.download = downloadWithProgress(url, dest)
                self.download.addProgress(self.downloadProgress)
                self.download.start().addCallback(self.install).addErrback(self.showError)
            else:
                self['info'].setText(_('Picons Not Installed ...'))

    def downloadProgress(self, recvbytes, totalbytes):
        self["progress"].show()
        self['progress'].value = int(100 * recvbytes / float(totalbytes))
        self['progresstext'].text = '%d of %d kBytes (%.2f%%)' % (recvbytes / 1024, totalbytes / 1024, 100 * recvbytes / float(totalbytes))

    def install(self, fplug):
        if os.path.exists('/tmp/download.zip'):
            if os.path.exists('/etc/enigma2/skin_user.xml'):
                os.rename('/etc/enigma2/skin_user.xml', '/etc/enigma2/skin_user-bak.xml')
            self['info'].setText(_('Install ...'))
            myCmd = "unzip -o -q '/tmp/download.zip' -d /"
            logdata("install4 ", myCmd)
            subprocess.Popen(myCmd, shell=True, executable='/bin/bash')
            self.mbox = self.session.open(MessageBox, _('Successfully Skin Installed'), MessageBox.TYPE_INFO, timeout=5)
        self['info'].setText(_('Please select ...'))
        self['progresstext'].text = ''
        self.progclear = 0
        self['progress'].setValue(self.progclear)
        self["progress"].hide()
        self.downloading = False
            
    def showError(self, error):
        print("download error =", error)
        logdata("errorLoad ", error)
        self.close()

    def cancel(self, result=None):
        self.close(None)
        return

    def up(self):
        self[self.currentList].up()
        self.load_poster()

    def down(self):
        self[self.currentList].down()
        self.load_poster()

    def left(self):
        self[self.currentList].pageUp()
        self.load_poster()

    def right(self):
        self[self.currentList].pageDown()
        self.load_poster()

    def load_poster(self):
        global pixmaps
        pixmaps = piconszeta
        if mpdDreamOs:
            self['poster'].instance.setPixmap(gPixmapPtr())
        else:
            self['poster'].instance.setPixmap(None)
        self['poster'].hide()
        sc = AVSwitch().getFramebufferScale()
        self.picload = ePicLoad()
        size = self['poster'].instance.size()
        self.picload.setPara((size.width(),
         size.height(),
         sc[0],
         sc[1],
         False,
         1,
         '#FF000000'))
        ptr = self.picload.getData()
        if mpdDreamOs:
            if self.picload.startDecode(pixmaps, False) == 0:
                ptr = self.picload.getData()
        else:
            if self.picload.startDecode(pixmaps, 0, 0, False) == 0:
                ptr = self.picload.getData()
        if ptr != None:
            self['poster'].instance.setPixmap(ptr)
            self['poster'].show()
        else:
            print('no cover.. error')
        return

class mmConfig(Screen, ConfigListScreen):

    def __init__(self, session):
        skin = skin_path + 'mmConfig.xml'
        f = open(skin, 'r')
        self.skin = f.read()
        f.close()
        Screen.__init__(self, session)
        self.setup_title = _("Config")
        self.onChangedEntry = []
        self.session = session
        self.setTitle(title_plug)
        self['description'] = Label('')
        info = ''
        self['info'] = Label(_('Config Panel Addon'))
        self['key_yellow'] = Button(_('Choice'))
        self['key_green'] = Button(_('Save'))
        self['key_red'] = Button(_('Back'))
        self["key_blue"] = Button(_(''))
        self['key_blue'].hide()
        self['title'] = Label(title_plug)
        self["setupActions"] = ActionMap(['OkCancelActions', 'DirectionActions', 'ColorActions', 'VirtualKeyboardActions', 'ActiveCodeActions'], {'cancel': self.extnok,
         'red': self.extnok,
         'back': self.close,
         'left': self.keyLeft,
         'right': self.keyRight,
         'yellow': self.Ok_edit,
         'ok': self.Ok_edit,
         'green': self.msgok}, -1)
        self.list = []
        ConfigListScreen.__init__(self, self.list, session=self.session, on_change=self.changedEntry)
        self.createSetup()
        self.onLayoutFinish.append(self.layoutFinished)

    def layoutFinished(self):
        self.setTitle(self.setup_title)
        if not os.path.exists('/tmp/currentip'):
            os.system('wget -qO- http://ipecho.net/plain > /tmp/currentip')
        currentip1 = open('/tmp/currentip', 'r')
        currentip = currentip1.read()
        self['info'].setText(_('Config Panel Addon\nYour current IP is %s') % currentip)

    def createSetup(self):
        self.editListEntry = None
        self.list = []
        self.list.append(getConfigListEntry(_("Set the path to the Picons folder"), config.plugins.mmPicons.mmkpicon, _("Press Ok to select the folder containing the picons files")))
        self["config"].list = self.list
        self["config"].setList(self.list)

    def changedEntry(self):
        for x in self.onChangedEntry:
            x()

    def getCurrentEntry(self):
            return self["config"].getCurrent()[0]

    def getCurrentValue(self):
        return str(self["config"].getCurrent()[1].getText())

    def createSummary(self):
        from Screens.Setup import SetupSummary
        return SetupSummary

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        print("current selection:", self["config"].l.getCurrentSelection())
        self.createSetup()

    def keyRight(self):
        ConfigListScreen.keyRight(self)
        print("current selection:", self["config"].l.getCurrentSelection())
        self.createSetup()

    def msgok(self):
        if self['config'].isChanged():
            for x in self["config"].list:
                x[1].save()

            self.mbox = self.session.openWithCallback(self.restartenigma, MessageBox, _("Restart Enigma is Required. Do you want to continue?"), MessageBox.TYPE_YESNO)
        else:
            self.close(True)

    def Ok_edit(self):
        ConfigListScreen.keyOK(self)
        sel = self['config'].getCurrent()[1]
        if sel and sel == config.plugins.mmPicons.mmkpicon:
            self.setting = 'mmkpicon'
            mmkpth = config.plugins.mmPicons.mmkpicon.value
            self.openDirectoryBrowser(mmkpth)
        else:
            pass

    def openDirectoryBrowser(self, path):
        try:
            self.session.openWithCallback(
             self.openDirectoryBrowserCB,
             LocationBox,
             windowTitle=_('Choose Directory:'),
             text=_('Choose directory'),
             currDir=str(path),
             bookmarks=config.movielist.videodirs,
             autoAdd=False,
             editDir=True,
             inhibitDirs=['/bin', '/boot', '/dev', '/home', '/lib', '/proc', '/run', '/sbin', '/sys', '/var'],
             minFree=15)
        except Exception as e:
            print(('openDirectoryBrowser get failed: ', str(e)))

    def openDirectoryBrowserCB(self, path):
        if path is not None:
            if self.setting == 'mmkpicon':
                config.plugins.mmPicons.mmkpicon.setValue(path)
        return

    def KeyText(self):
        sel = self['config'].getCurrent()
        if sel:
            self.session.openWithCallback(self.VirtualKeyBoardCallback, VirtualKeyBoard, title=self['config'].getCurrent()[0], text=self['config'].getCurrent()[1].value)

    def VirtualKeyBoardCallback(self, callback=None):
        if callback is not None and len(callback):
            self['config'].getCurrent()[1].value = callback
            self['config'].invalidate(self['config'].getCurrent())
        return

    def cancelConfirm(self, result):
        if not result:
            return
        for x in self['config'].list:
            x[1].cancel()
        self.close()

    def restartenigma(self, result):
        if result:
            self.session.open(TryQuitMainloop, 3)
        else:
            self.close(True)

    def extnok(self):
        if self['config'].isChanged():
            self.session.openWithCallback(self.cancelConfirm, MessageBox, _('Really close without saving the settings?'), MessageBox.TYPE_YESNO)
        else:
            self.close()

class PiconsPreview(Screen):
    x = getDesktop(0).size().width()
    y = getDesktop(0).size().height()
    skin = '<screen flags="wfNoBorder" position="0,0" size="%d,%d" title="PiconsPreview" backgroundColor="#00000000">' % (x, y)
    skin += '<widget name="pixmap" position="0,0" size="%d,%d" zPosition="1" alphatest="on" />' % (x, y)
    skin += '</screen>'

    def __init__(self, session, previewPng=None):
        self.skin = PiconsPreview.skin
        Screen.__init__(self, session)
        self.session = session
        self.Scale = AVSwitch().getFramebufferScale()
        self.PicLoad = ePicLoad()
        self['pixmap'] = Pixmap()
        try:
            self.PicLoad.PictureData.get().append(self.DecodePicture)
        except:
            self.PicLoad_conn = self.PicLoad.PictureData.connect(self.DecodePicture)
        self.previewPng = previewPng
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'], {'ok': self.close,
         'cancel': self.close,
         'blue': self.close}, -1)

        self.onLayoutFinish.append(self.ShowPicture)

    def ShowPicture(self):
        myicon = self.previewPng
        if HD.width() > 1280:
            png = loadPic(myicon, 1920, 1080, 0, 0, 0, 1)
        else:
            png = loadPic(myicon, 1280, 720, 0, 0, 0, 1)
        self["pixmap"].instance.setPixmap(png)

    def DecodePicture(self, PicInfo=''):
        ptr = self.picload.getData()
        self['pixmap'].instance.setPixmap(ptr)


def main(session, **kwargs):
    if checkInternet():
        session.open(SelectPicons)
    else:
        logdata("noInternet ", 'norete')
        session.open(MessageBox, "No Internet", MessageBox.TYPE_INFO)

def menu(menuid, **kwargs):
    if menuid == 'mainmenu':
        return [('mMark Picons & Skins',
          main,
          'mMark Picons & Skins',
          44)]
    return []

def mainmenu(session, **kwargs):
    main(session, **kwargs)


def Plugins(**kwargs):
    ico_path = 'logo.png'
    if not mpdDreamOs:
        ico_path = plugin_path + '/res/pics/logo.png'
    result = [PluginDescriptor(name=desc_plug, description=(title_plug), where=[PluginDescriptor.WHERE_PLUGINMENU], icon=ico_path, fnc=main)]
    return result

'''======================================================'''
