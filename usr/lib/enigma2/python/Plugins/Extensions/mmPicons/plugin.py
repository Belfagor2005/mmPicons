#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
****************************************
*           coded by Lululla           *
*         improve code by jbleyel      *
*             skin by MMark            *
*             28/08/2023               *
*         thank's fix by @jbleyel      *
****************************************
'''
# Info https://e2skin.blogspot.com/
from __future__ import print_function
from . import _, logdata, getversioninfo
from . import Utils
from .Downloader import downloadWithProgress
from .Console import Console as xConsole

from Components.AVSwitch import AVSwitch
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import (MultiContentEntryPixmapAlphaTest, MultiContentEntryText)
from Components.Pixmap import Pixmap
from Components.ProgressBar import ProgressBar
from Components.Sources.Progress import Progress
from Components.Sources.StaticText import StaticText
from Components.config import (
    config,
    getConfigListEntry,
    ConfigSubsection,
    ConfigDirectory,
    configfile,
    # ConfigSelection,
)
from Plugins.Plugin import PluginDescriptor
from Screens.LocationBox import LocationBox
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.Standby import TryQuitMainloop
from Screens.VirtualKeyBoard import VirtualKeyBoard
# from Tools.Downloader import downloadWithProgress
from enigma import (
    RT_VALIGN_CENTER,
    RT_HALIGN_LEFT,
    eTimer,
    eListboxPythonMultiContent,
    gFont,
    ePicLoad,
    loadPic,
    loadPNG,
    getDesktop,
)
from twisted.web.client import getPage
from datetime import datetime
import codecs
import glob
import json
import os
import re
import six
import ssl
import subprocess
import sys

global skin_path, mmkpicon, XStreamity
PY3 = sys.version_info.major >= 3


sslverify = False
try:
    from twisted.internet import ssl
    from twisted.internet._sslverify import ClientTLSOptions
    sslverify = True
except:
    sslverify = False


if sslverify:
    class SNIFactory(ssl.ClientContextFactory):
        def __init__(self, hostname=None):
            self.hostname = hostname

        def getContext(self):
            ctx = self._contextFactory(self.method)
            if self.hostname:
                ClientTLSOptions(self.hostname, ctx)
            return ctx


dirpics = '/media/hdd/picon/'
piconpathss = Utils.mountipkpth()
config.plugins.mmPicons = ConfigSubsection()
cfg = config.plugins.mmPicons
cfg.mmkpicon = ConfigDirectory(default=dirpics)
plugin_path = '/usr/lib/enigma2/python/Plugins/Extensions/mmPicons'
currversion = getversioninfo()
title_plug = 'mMark Picons & Skins'
desc_plugin = 'V.%s - e2skin.blogspot.com' % str(currversion)
XStreamity = False
ico_path = os.path.join(plugin_path, 'logo.png')
no_cover = os.path.join(plugin_path, 'no_coverArt.png')
res_plugin_path = os.path.join(plugin_path, 'res/')
ico1_path = os.path.join(res_plugin_path, 'pics/4logo.png')
# ico3_path = os.path.join(res_plugin_path, 'pics/setting.png')
res_picon_plugin_path = os.path.join(res_plugin_path, 'picons/')
piconstrs = os.path.join(res_picon_plugin_path, 'picon_trs.png')
piconsblk = os.path.join(res_picon_plugin_path, 'picon_blk.png')
piconszeta = os.path.join(res_picon_plugin_path, 'picon_z.png')
piconsmovie = os.path.join(res_picon_plugin_path, 'picon_mv.png')
pixmaps = os.path.join(res_picon_plugin_path, 'backg.png')
# mmkpicon = cfg.mmkpicon.value.strip()
pblk = 'aHR0cHM6Ly93d3cubWVkaWFmaXJlLmNvbS9hcGkvMS41L2ZvbGRlci9nZXRfY29udGVudC5waHA/Zm9sZGVyX2tleT1vdnowNG1ycHpvOXB3JmNvbnRlbnRfdHlwZT1mb2xkZXJzJmNodW5rX3NpemU9MTAwMCZyZXNwb25zZV9mb3JtYXQ9anNvbg=='
ptrs = 'aHR0cHM6Ly93d3cubWVkaWFmaXJlLmNvbS9hcGkvMS41L2ZvbGRlci9nZXRfY29udGVudC5waHA/Zm9sZGVyX2tleT10dmJkczU5eTlocjE5JmNvbnRlbnRfdHlwZT1mb2xkZXJzJmNodW5rX3NpemU9MTAwMCZyZXNwb25zZV9mb3JtYXQ9anNvbg=='
ptmov = 'aHR0cHM6Ly93d3cubWVkaWFmaXJlLmNvbS9hcGkvMS41L2ZvbGRlci9nZXRfY29udGVudC5waHA/Zm9sZGVyX2tleT1uazh0NTIyYnY0OTA5JmNvbnRlbnRfdHlwZT1maWxlcyZjaHVua19zaXplPTEwMDAmcmVzcG9uc2VfZm9ybWF0PWpzb24='
ecskins = 'aHR0cHM6Ly93d3cubWVkaWFmaXJlLmNvbS9hcGkvMS41L2ZvbGRlci9nZXRfY29udGVudC5waHA/Zm9sZGVyX2tleT1jOHN3MGFoc3Mzc2kwJmNvbnRlbnRfdHlwZT1maWxlcyZjaHVua19zaXplPTEwMDAmcmVzcG9uc2VfZm9ybWF0PWpzb24='
openskins = 'aHR0cHM6Ly93d3cubWVkaWFmaXJlLmNvbS9hcGkvMS41L2ZvbGRlci9nZXRfY29udGVudC5waHA/Zm9sZGVyX2tleT0wd3o0M3l2OG5zeDc5JmNvbnRlbnRfdHlwZT1maWxlcyZjaHVua19zaXplPTEwMDAmcmVzcG9uc2VfZm9ybWF0PWpzb24='
installer_url = 'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL0JlbGZhZ29yMjAwNS9tbVBpY29ucy9tYWluL2luc3RhbGxlci5zaA=='
developer_url = 'aHR0cHM6Ly9hcGkuZ2l0aHViLmNvbS9yZXBvcy9CZWxmYWdvcjIwMDUvbW1QaWNvbnM='

mmkpicon = str(cfg.mmkpicon.value)
if mmkpicon.endswith('/'):
    mmkpicon = mmkpicon[:-1]
if not os.path.exists(mmkpicon):
    try:
        os.makedirs(mmkpicon)
    except OSError as e:
        print(('Error creating directory %s:\n%s') % (mmkpicon, str(e)))


logdata("path picons: ", str(mmkpicon))
screenwidth = getDesktop(0).size()
if screenwidth.width() == 2560:
    skin_path = plugin_path + '/res/skins/uhd/'
elif screenwidth.width() == 1920:
    skin_path = plugin_path + '/res/skins/fhd/'
else:
    skin_path = plugin_path + '/res/skins/hd/'

if os.path.exists('/var/lib/dpkg/info'):
    skin_path = skin_path + 'dreamOs/'


class mmList(MenuList):
    def __init__(self, list):
        MenuList.__init__(self, list, True, eListboxPythonMultiContent)
        if screenwidth.width() == 2560:
            self.l.setItemHeight(60)
            textfont = int(44)
            self.l.setFont(0, gFont('Regular', textfont))
        elif screenwidth.width() == 1920:
            self.l.setItemHeight(50)
            textfont = int(32)
            self.l.setFont(0, gFont('Regular', textfont))
        else:
            self.l.setItemHeight(45)
            textfont = int(24)
            self.l.setFont(0, gFont('Regular', textfont))


def zxListEntry(name, idx):
    res = [name]
    pngs = ico1_path
    if screenwidth.width() == 2560:
        res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 10), size=(40, 40), png=loadPNG(pngs)))
        res.append(MultiContentEntryText(pos=(90, 0), size=(1200, 50), font=0, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    elif screenwidth.width() == 1920:
        res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 5), size=(40, 40), png=loadPNG(pngs)))
        res.append(MultiContentEntryText(pos=(70, 0), size=(1000, 50), font=0, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    else:
        res.append(MultiContentEntryPixmapAlphaTest(pos=(3, 10), size=(40, 40), png=loadPNG(pngs)))
        res.append(MultiContentEntryText(pos=(50, 0), size=(500, 50), font=0, text=name, color=0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    return res


def showlist(data, list):
    icount = 0
    plist = []
    for line in data:
        name = data[icount]
        plist.append(zxListEntry(name, icount))
        icount += 1
        list.setList(plist)


Panel_list3 = [('PICONS TRANSPARENT'),
               ('PICONS BLACK'),
               ('PICONS MOVIE'),
               ('SKIN DMM ZETA'),
               ('SKIN OPEN ZETA')]


class SelectPicons(Screen):
    def __init__(self, session):
        self.session = session
        skin = os.path.join(skin_path, 'mmall.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.setup_title = ('Select zPicons')
        Screen.__init__(self, session)
        self.setTitle(desc_plugin)
        self.working = False
        self.icount = 0
        self.menulist = []
        self.list = []
        self['title'] = Label(desc_plugin)
        self['pth'] = Label('')
        self['pth'].setText(_('Picons folder ') + mmkpicon)
        self['poster'] = Pixmap()
        self['pform'] = Label('n/a')
        self['info'] = Label(_('Loading data... Please wait'))
        self['key_red'] = Button(_('Exit'))
        self['key_green'] = Button(_('Remove'))
        self['key_yellow'] = Button(_('Preview'))
        self["key_blue"] = Button(_('Restart'))
        self['progress'] = ProgressBar()
        self['progresstext'] = StaticText()
        self["progress"].hide()
        self['progresstext'].text = ''
        self['text'] = mmList([])
        self.currentList = 'text'
        self.Update = False
        self['actions'] = ActionMap(['OkCancelActions',
                                     'HotkeyActions',
                                     'InfobarEPGActions',
                                     'MenuActions',
                                     'ChannelSelectBaseActions',
                                     'DirectionActions'], {'ok': self.okRun,
                                                           'menu': self.goConfig,
                                                           'blue': self.msgtqm,
                                                           'up': self.up,
                                                           'down': self.down,
                                                           'left': self.left,
                                                           'right': self.right,
                                                           'yellow': self.zoom,  # update_me,
                                                           'yellow_long': self.update_dev,
                                                           'info_long': self.update_dev,
                                                           'infolong': self.update_dev,
                                                           'showEventInfoPlugin': self.update_dev,
                                                           'green': self.remove,
                                                           'cancel': self.closerm,
                                                           'red': self.closerm}, -1)
        self.timer = eTimer()
        if os.path.exists('/var/lib/dpkg/status'):
            self.timer_conn = self.timer.timeout.connect(self.check_vers)
        else:
            self.timer.callback.append(self.check_vers)
        self.timer.start(500, 1)
        self.onLayoutFinish.append(self.updateMenuList)

    def check_vers(self):
        remote_version = '0.0'
        remote_changelog = ''
        req = Utils.Request(Utils.b64decoder(installer_url), headers={'User-Agent': 'Mozilla/5.0'})
        page = Utils.urlopen(req).read()
        if PY3:
            data = page.decode("utf-8")
        else:
            data = page.encode("utf-8")
        if data:
            lines = data.split("\n")
            for line in lines:
                if line.startswith("version"):
                    remote_version = line.split("=")
                    remote_version = line.split("'")[1]
                if line.startswith("changelog"):
                    remote_changelog = line.split("=")
                    remote_changelog = line.split("'")[1]
                    break
        self.new_version = remote_version
        self.new_changelog = remote_changelog
        # if currversion < remote_version:
        if float(currversion) < float(remote_version):
            self.Update = True
            # self['key_yellow'].show()
            # self['key_green'].show()
            self.session.open(MessageBox, _('New version %s is available\n\nChangelog: %s\n\nPress info_long or yellow_long button to start force updating.') % (self.new_version, self.new_changelog), MessageBox.TYPE_INFO, timeout=5)
        # self.update_me()

    def update_me(self):
        if self.Update is True:
            self.session.openWithCallback(self.install_update, MessageBox, _("New version %s is available.\n\nChangelog: %s \n\nDo you want to install it now?") % (self.new_version, self.new_changelog), MessageBox.TYPE_YESNO)
        else:
            self.session.open(MessageBox, _("Congrats! You already have the latest version..."),  MessageBox.TYPE_INFO, timeout=4)

    def update_dev(self):
        try:
            req = Utils.Request(Utils.b64decoder(developer_url), headers={'User-Agent': 'Mozilla/5.0'})
            page = Utils.urlopen(req).read()
            data = json.loads(page)
            remote_date = data['pushed_at']
            strp_remote_date = datetime.strptime(remote_date, '%Y-%m-%dT%H:%M:%SZ')
            remote_date = strp_remote_date.strftime('%Y-%m-%d')
            self.session.openWithCallback(self.install_update, MessageBox, _("Do you want to install update ( %s ) now?") % (remote_date), MessageBox.TYPE_YESNO)
        except Exception as e:
            print('error xcons:', e)

    def install_update(self, answer=False):
        if answer:
            cmd1 = 'wget -q "--no-check-certificate" ' + Utils.b64decoder(installer_url) + ' -O - | /bin/sh'
            self.session.open(xConsole, 'Upgrading...', cmdlist=[cmd1], finishedCallback=self.myCallback, closeOnSuccess=False)
        else:
            self.session.open(MessageBox, _("Update Aborted!"),  MessageBox.TYPE_INFO, timeout=3)

    def myCallback(self, result=None):
        print('result:', result)
        return

    def zoom(self):
        self.session.open(PiconsPreview, pixmaps)

    def getfreespace(self):
        try:
            fspace = Utils.freespace()
            self['pform'].setText(str(fspace))
        except Exception as e:
            print(e)

    def closerm(self):
        Utils.deletetmp()
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
        self.list = []
        idx = 0
        for x in Panel_list3:
            self.list.append(zxListEntry(x, idx))
            self.menu_list.append(x)
            idx += 1
            print('idx x  ', idx)
        self['text'].list = self.list
        self['text'].setList(self.list)
        self['info'].setText('Please select ...')
        logdata("updateMenuList ")
        self.getfreespace()
        self.load_poster()

    def okRun(self):
        self.keyNumberGlobalCB(self['text'].getSelectedIndex())

    def keyNumberGlobalCB(self, idx):
        sel = self.menu_list[idx]
        print('selll ', sel)
        if sel == ('PICONS BLACK'):
            self.session.open(MMarkFolderScreen, Utils.b64decoder(pblk), piconsblk)
        elif sel == 'PICONS TRANSPARENT':
            self.session.open(MMarkFolderScreen, Utils.b64decoder(ptrs), piconstrs)
        elif sel == ('PICONS MOVIE'):
            self.session.open(MMarkPiconScreen, 'MMark-Picons', Utils.b64decoder(ptmov), piconsmovie, True)
        elif sel == ('SKIN DMM ZETA'):
            self.session.open(MMarkFolderSkinZeta, Utils.b64decoder(ecskins))
        elif sel == ('SKIN OPEN ZETA'):
            self.session.open(MMarkFolderSkinZeta, Utils.b64decoder(openskins))
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
                    logdata("process ", f)
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
        self["poster"].show()
        if os.path.exists(pixmaps):
            size = self['poster'].instance.size()
            self.picload = ePicLoad()
            sc = AVSwitch().getFramebufferScale()
            self.picload.setPara([size.width(), size.height(), sc[0], sc[1], False, 1, '#00000000'])
            if os.path.exists('/var/lib/dpkg/info'):
                self.picload.startDecode(pixmaps, False)
            else:
                self.picload.startDecode(pixmaps, 0, 0, False)
            ptr = self.picload.getData()
            if ptr is not None:
                self['poster'].instance.setPixmap(ptr)
                self['poster'].show()


class MMarkPiconScreen(Screen):
    def __init__(self, session, name, url, pixmaps, movie=False):
        self.session = session
        skin = os.path.join(skin_path, 'mmall.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.setup_title = ('zPicons & Skins')
        Screen.__init__(self, session)
        self.setTitle(desc_plugin)
        self['title'] = Label(desc_plugin)
        self.list = []
        self.menulist = []
        self.icount = 0
        self.downloading = False
        self.url = url
        self.name = name
        self.error_message = ""
        self.last_recvbytes = 0
        self.error_message = None
        self.download = None
        self.aborted = False
        self.timer = eTimer()
        self.pixmaps = pixmaps
        self.movie = movie
        self['text'] = mmList([])
        self['info'] = Label(_('Loading data... Please wait'))
        self['pth'] = Label('')
        self['pth'].setText(_('Picons folder ') + mmkpicon)
        self['poster'] = Pixmap()
        self['progress'] = ProgressBar()
        self['progresstext'] = StaticText()
        self["progress"].hide()
        self['progresstext'].text = ''
        self['key_red'] = Button(_('Back'))
        self['key_green'] = Button(_('Install'))
        self['key_yellow'] = Button(_('Preview'))
        self["key_blue"] = Button()
        self['key_blue'].hide()
        self['key_green'].hide()
        self['pform'] = Label('')
        self.currentList = 'text'
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions',
                                     'ButtonSetupActions',
                                     'DirectionActions'], {'ok': self.okRun,
                                                           'green': self.okRun,
                                                           'red': self.close,
                                                           'yellow': self.zoom,
                                                           'up': self.up,
                                                           'down': self.down,
                                                           'left': self.left,
                                                           'right': self.right,
                                                           'cancel': self.close}, -2)
        if os.path.exists('/var/lib/dpkg/info'):
            self.timer_conn = self.timer.timeout.connect(self.downxmlpage)
        else:
            self.timer.callback.append(self.downxmlpage)
        self.timer.start(500, 1)
        self.onLayoutFinish.append(self.getfreespace)

    def zoom(self):
        self.session.open(PiconsPreview, self.pixmaps)

    def getfreespace(self):
        try:
            fspace = Utils.freespace()
            self['pform'].setText(str(fspace))
        except Exception as e:
            print(e)

    def downxmlpage(self):
        url = six.ensure_binary(self.url)
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)

    def errorLoad(self):
        self['info'].setText(_('Try again later ...'))
        logdata("errorLoad ")
        self.downloading = False

    def _gotPageLoad(self, data):
        r = data
        if six.PY3:
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
            self['key_green'].show()
            showlist(self.names, self['text'])
            self.downloading = True
        except:
            self.downloading = False
        self.load_poster()

    def okRun(self):
        i = len(self.names)
        print('iiiiii= ', i)
        if i < 1:
            return
        self.session.openWithCallback(self.okInstall, MessageBox, (_("Do you want to install?\nIt could take a few minutes, wait ..")), MessageBox.TYPE_YESNO)

    def okInstall(self, result):
        self['info'].setText(_('... please wait'))
        if result:
            if self.downloading is True:
                idx = self["text"].getSelectionIndex()
                self.name = self.names[idx]
                url = self.urls[idx]
                dest = "/tmp/download.zip"
                print('url333: ', url)
                if os.path.exists(dest):
                    os.remove(dest)
                try:
                    myfile = Utils.ReadUrl(url)
                    regexcat = 'href="https://download(.*?)"'
                    match = re.compile(regexcat, re.DOTALL).findall(myfile)
                    url = 'https://download' + str(match[0])
                    print("url final =", url)
                    if os.path.exists('/var/lib/dpkg/info'):
                        cmd = ["wget --no-check-certificate -U '%s' -c '%s' -O '%s' --post-data='action=purge' > /dev/null" % (Utils.RequestAgent(), str(url), dest)]
                        print('command:', cmd)
                        subprocess.Popen(cmd[0], shell=True, executable='/bin/bash')
                        self.session.openWithCallback(self.install, MessageBox, _('Download file in /tmp successful!'), MessageBox.TYPE_INFO, timeout=5)
                        return
                    self.download = downloadWithProgress(url, dest)
                    self.download.addProgress(self.downloadProgress2)
                    self.download.start().addCallback(self.install).addErrback(self.showError)
                except Exception as e:
                    print('error: ', str(e))
                    print("Error: can't find file or read data")
            else:
                self['info'].setText(_('Picons Not Installed ...'))

    def install(self, fplug):
        self.progclear = 0
        if os.path.exists('/tmp/download.zip'):
            self['info'].setText(_('Install ...'))
            myCmd = "unzip -o -q '/tmp/download.zip' -d %s/" % str(mmkpicon)
            logdata("install2 ", myCmd)
            subprocess.Popen(myCmd, shell=True, executable='/bin/bash')
            self.mbox = self.session.open(MessageBox, _('Successfully Picons Installed'), MessageBox.TYPE_INFO, timeout=5)
        self['info'].setText(_('Please select ...'))
        self['progresstext'].text = ''
        self['progress'].setValue(self.progclear)
        self["progress"].hide()

    def downloadProgress2(self, recvbytes, totalbytes):
        try:
            self['info'].setText(_('Download in progress...'))
            self["progress"].show()
            self['progress'].value = int(100 * self.last_recvbytes / float(totalbytes))
            self['progresstext'].text = '%d of %d kBytes (%.2f%%)' % (self.last_recvbytes / 1024, totalbytes / 1024, 100 * self.last_recvbytes / float(totalbytes))
            self.last_recvbytes = recvbytes
            # if self.last_recvbytes == recvbytes:
                # self.getfreespace()
        except ZeroDivisionError:
            self['info'].setText(_('Download Failed!'))
            self["progress"].hide()
            self['progress'].setRange((0, 100))
            self['progress'].setValue(0)

    def showError(self):
        print("download error ")
        self.downloading = False
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
        self["poster"].show()
        if os.path.exists(self.pixmaps):
            size = self['poster'].instance.size()
            self.picload = ePicLoad()
            sc = AVSwitch().getFramebufferScale()
            self.picload.setPara([size.width(), size.height(), sc[0], sc[1], False, 1, '#00000000'])
            if os.path.exists('/var/lib/dpkg/info'):
                self.picload.startDecode(self.pixmaps, False)
            else:
                self.picload.startDecode(self.pixmaps, 0, 0, False)
            ptr = self.picload.getData()
            if ptr is not None:
                self['poster'].instance.setPixmap(ptr)
                self['poster'].show()


class MMarkFolderScreen(Screen):
    def __init__(self, session, url, pixmaps):
        self.session = session
        skin = os.path.join(skin_path, 'mmall.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.setup_title = ('zPicons & Skins')
        self['title'] = Label(desc_plugin)
        Screen.__init__(self, session)
        self.setTitle(desc_plugin)
        self.list = []
        self.menulist = []
        self.icount = 0
        self.downloading = False
        self.timer = eTimer()
        self.url = url
        self.pixmaps = pixmaps
        self['text'] = mmList([])
        self['info'] = Label(_('Loading data... Please wait'))
        self['pth'] = Label('')
        self['pth'].setText(_('Picons folder ') + mmkpicon)
        self['poster'] = Pixmap()
        self['progress'] = ProgressBar()
        self['progresstext'] = StaticText()
        self["progress"].hide()
        self['progresstext'].text = ''
        self['key_red'] = Button(_('Back'))
        self['key_green'] = Button(_('Select'))
        self['key_yellow'] = Button(_('Preview'))
        self["key_blue"] = Button()
        self['key_blue'].hide()
        self['key_green'].hide()
        self['pform'] = Label('')
        self.currentList = 'text'
        if os.path.exists('/var/lib/dpkg/info'):
            self.timer_conn = self.timer.timeout.connect(self.downxmlpage)
        else:
            self.timer.callback.append(self.downxmlpage)
        self.timer.start(500, 1)
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions',
                                     'ButtonSetupActions',
                                     'DirectionActions'], {'ok': self.okRun,
                                                           'green': self.okRun,
                                                           'red': self.close,
                                                           "yellow": self.zoom,
                                                           'up': self.up,
                                                           'down': self.down,
                                                           'left': self.left,
                                                           'right': self.right,
                                                           'cancel': self.close}, -2)
        self.onLayoutFinish.append(self.getfreespace)

    def zoom(self):
        self.session.open(PiconsPreview, self.pixmaps)

    def getfreespace(self):
        try:
            fspace = Utils.freespace()
            self['pform'].setText(str(fspace))
        except Exception as e:
            print(e)

    def downxmlpage(self):
        url = six.ensure_binary(self.url)
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)

    def errorLoad(self):
        self['info'].setText(_('Try again later ...'))
        logdata("errorLoad ")
        self.downloading = False

    def _gotPageLoad(self, data):
        r = data
        if six.PY3:
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
                name = 'Picons-' + name
                self.urls.append(url)
                self.names.append(name)
            self['info'].setText(_('Please select ...'))
            self['key_green'].show()
            showlist(self.names, self['text'])
            self.downloading = True
        except:
            self.downloading = False
        self.load_poster()

    def okRun(self):
        i = len(self.names)
        print('iiiiii= ', i)
        if i < 1:
            return
        idx = self['text'].getSelectionIndex()
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
        self["poster"].show()
        if os.path.exists(self.pixmaps):
            size = self['poster'].instance.size()
            self.picload = ePicLoad()
            sc = AVSwitch().getFramebufferScale()
            self.picload.setPara([size.width(), size.height(), sc[0], sc[1], False, 1, '#00000000'])
            if os.path.exists('/var/lib/dpkg/info'):
                self.picload.startDecode(self.pixmaps, False)
            else:
                self.picload.startDecode(self.pixmaps, 0, 0, False)
            ptr = self.picload.getData()
            if ptr is not None:
                self['poster'].instance.setPixmap(ptr)
                self['poster'].show()

    def abort(self):
        print("aborting", self.url)
        if self.download:
            self.download.stop()
        self.downloading = False
        self.aborted = True

    def download_finished(self, string=""):
        if self.aborted:
            self.finish(aborted=True)

    def download_failed(self, failure_instance=None, error_message=""):
        self.error_message = error_message
        if error_message == "" and failure_instance is not None:
            self.error_message = failure_instance.getErrorMessage()
        self.downloading = False
        info = _('Download Failed! ') + self.error_message
        self['info'].setText(info)
        self.session.open(MessageBox, _(info), MessageBox.TYPE_INFO, timeout=5)


class MMarkFolderSkinZeta(Screen):
    def __init__(self, session, url):
        self.session = session
        skin = os.path.join(skin_path, 'mmall.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.setup_title = ('zPicons & Skins')
        Screen.__init__(self, session)
        self.setTitle(desc_plugin)
        self['title'] = Label(desc_plugin)
        self.list = []
        self.menulist = []
        self.icount = 0
        self.downloading = False
        self.url = url
        self.name = 'MMark-Skins'
        self['text'] = mmList([])
        self['info'] = Label(_('Loading data... Please wait'))
        self['pth'] = Label('')
        self['pth'].setText(_('Picons folder ') + mmkpicon)
        self['poster'] = Pixmap()
        self['progress'] = ProgressBar()
        self['progresstext'] = StaticText()
        self["progress"].hide()
        self['progresstext'].text = ''
        self['key_red'] = Button(_('Back'))
        self['key_green'] = Button(_('Install'))
        self['key_yellow'] = Button(_('Preview'))
        self["key_blue"] = Button()
        self['key_blue'].hide()
        self['key_green'].hide()
        self['pform'] = Label('')
        self.currentList = 'text'
        self.timer = eTimer()
        if os.path.exists('/var/lib/dpkg/info'):
            self.timer_conn = self.timer.timeout.connect(self.downxmlpage)
        else:
            self.timer.callback.append(self.downxmlpage)
        self.timer.start(500, 1)

        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions',
                                     'ButtonSetupActions',
                                     'DirectionActions'], {'ok': self.okRun,
                                                           'green': self.okRun,
                                                           'red': self.close,
                                                           "yellow": self.zoom,
                                                           'up': self.up,
                                                           'down': self.down,
                                                           'left': self.left,
                                                           'right': self.right,
                                                           'cancel': self.close}, -2)
        self.onLayoutFinish.append(self.getfreespace)

    def zoom(self):
        self.session.open(PiconsPreview, pixmaps)

    def GetPicturePath(self):
        realpng = pixmaps
        if os.path.isfile(realpng):
            print(realpng)
        return realpng

    def getfreespace(self):
        try:
            fspace = Utils.freespace()
            self['pform'].setText(str(fspace))
        except Exception as e:
            print(e)

    def downxmlpage(self):
        url = six.ensure_binary(self.url)
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)

    def errorLoad(self):
        self.downloading = False
        pass

    def _gotPageLoad(self, data):
        r = data
        if six.PY3:
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
                if '.jpg' or '.png' in str(url):
                    continue
                if '.sh' or '.txt' in str(url):
                    continue
                if '.zip' or '.ipk' or '.deb' in str(url):
                    url = url.replace('\\', '')
                    name = name.replace('enigma2-plugin-skins-', '')
                    name = name.replace('_', ' ').replace('-', ' ').replace('mmk', '')
                    name = name.replace('.zip', '').replace('.ipk', '').replace('.deb', '')
                    name = name + ' ' + data[0:10] + ' ' + 'Down: ' + download
                    self.urls.append(url)
                    self.names.append(name)
            self['info'].setText(_('Please select ...'))
            self['key_green'].show()
            showlist(self.names, self['text'])
            self.downloading = True
        except:
            self.downloading = False
        self.load_poster()

    def okRun(self):
        i = len(self.names)
        if i < 1:
            return
        self.session.openWithCallback(self.okInstall, MessageBox, (_("Do you want to install?\nIt could take a few minutes, wait ..")), MessageBox.TYPE_YESNO)

    def okInstall(self, result):
        self['info'].setText(_('... please wait'))
        if result:
            if self.downloading is True:
                if not os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/XStreamity') and 'xstreamity' in self.name:
                    self.mbox = self.session.open(MessageBox, _('Xstreamity Player not installed'), MessageBox.TYPE_INFO, timeout=4)
                    return
                idx = self["text"].getSelectionIndex()
                self.name = self.names[idx]
                url = self.urls[idx]
                dest = "/tmp/download.zip"
                if os.path.exists(dest):
                    os.remove(dest)
                try:
                    myfile = Utils.ReadUrl(url)
                    regexcat = 'href="https://download(.*?)"'
                    match = re.compile(regexcat, re.DOTALL).findall(myfile)
                    url = 'https://download' + str(match[0])
                    print("url final =", url)
                    if os.path.exists('/var/lib/dpkg/info'):
                        cmd = ["wget --no-check-certificate -U '%s' -c '%s' -O '%s' --post-data='action=purge' > /dev/null" % (Utils.RequestAgent(), str(url), dest)]
                        print('command:', cmd)
                        subprocess.Popen(cmd[0], shell=True, executable='/bin/bash')
                        self.session.openWithCallback(self.install, MessageBox, _('Download file in /tmp successful!'), MessageBox.TYPE_INFO, timeout=5)
                        return
                    self.download = downloadWithProgress(url, dest)
                    self.download.addProgress(self.downloadProgress2)
                    self.download.start().addCallback(self.install).addErrback(self.showError)
                except Exception as e:
                    print('error: ', str(e))
                    print("Error: can't find file or read data")
            else:
                self['info'].setText(_('Picons Not Installed ...'))

    def downloadProgress2(self, recvbytes, totalbytes):
        try:
            self['info'].setText(_('Download in progress...'))
            self["progress"].show()
            self['progress'].value = int(100 * self.last_recvbytes / float(totalbytes))
            self['progresstext'].text = '%d of %d kBytes (%.2f%%)' % (self.last_recvbytes / 1024, totalbytes / 1024, 100 * self.last_recvbytes / float(totalbytes))
            self.last_recvbytes = recvbytes
            # if self.last_recvbytes == recvbytes:
                # self.getfreespace()
        except ZeroDivisionError:
            self['info'].setText(_('Download Failed! '))
            self["progress"].hide()
            self['progress'].setRange((0, 100))
            self['progress'].setValue(0)

    def install(self, fplug):
        self.progclear = 0
        if os.path.exists('/tmp/download.zip'):
            if os.path.exists('/etc/enigma2/skin_user.xml'):
                os.rename('/etc/enigma2/skin_user.xml', '/etc/enigma2/skin_user-bak.xml')
            self['info'].setText(_('Install ...'))
            myCmd = "unzip -o -q '/tmp/download.zip' -d /"
            logdata("install1 ", myCmd)
            subprocess.Popen(myCmd, shell=True, executable='/bin/bash')
            self.mbox = self.session.open(MessageBox, _('Successfully Skin Installed'), MessageBox.TYPE_INFO, timeout=5)

        elif os.path.exists('/tmp/download.deb'):
            if os.path.exists('/etc/enigma2/skin_user.xml'):
                os.rename('/etc/enigma2/skin_user.xml', '/etc/enigma2/skin_user-bak.xml')
            self['info'].setText(_('Install ...'))
            myCmd = 'apt-get install --reinstall /tmp/download.deb -y'
            if os.path.exists('/var/lib/dpkg/info'):
                logdata("install2 ", myCmd)
                subprocess.Popen(myCmd, shell=True, executable='/bin/bash')
                self.mbox = self.session.open(MessageBox, _('Successfully Skin Installed'), MessageBox.TYPE_INFO, timeout=5)

        elif os.path.exists('/tmp/download.ipk'):
            if os.path.exists('/etc/enigma2/skin_user.xml'):
                os.rename('/etc/enigma2/skin_user.xml', '/etc/enigma2/skin_user-bak.xml')
            self['info'].setText(_('Install ...'))
            myCmd = 'opkg install --force-reinstall --force-overwrite /tmp/download.ipk > /dev/null'
            logdata("install3 ", myCmd)
            subprocess.Popen(myCmd, shell=True, executable='/bin/bash')
            self.mbox = self.session.open(MessageBox, _('Successfully Skin Installed'), MessageBox.TYPE_INFO, timeout=5)

        self['info'].setText(_('Please select ...'))
        self['progresstext'].text = ''
        self['progress'].setValue(self.progclear)
        self["progress"].hide()

    def showError(self):
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
        self["poster"].show()
        if os.path.exists(pixmaps):
            size = self['poster'].instance.size()
            self.picload = ePicLoad()
            sc = AVSwitch().getFramebufferScale()
            self.picload.setPara([size.width(), size.height(), sc[0], sc[1], False, 1, '#00000000'])
            if os.path.exists('/var/lib/dpkg/info'):
                self.picload.startDecode(pixmaps, False)
            else:
                self.picload.startDecode(pixmaps, 0, 0, False)
            ptr = self.picload.getData()
            if ptr is not None:
                self['poster'].instance.setPixmap(ptr)
                self['poster'].show()


class mmConfig(Screen, ConfigListScreen):
    def __init__(self, session):
        self.session = session
        skin = os.path.join(skin_path, 'mmConfig.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        Screen.__init__(self, session)
        self.setup_title = _("Config")
        self.onChangedEntry = []
        self.list = []
        ConfigListScreen.__init__(self, self.list, session=self.session, on_change=self.changedEntry)
        self.setTitle(desc_plugin)
        self['description'] = Label('Config mmPicons Panel')
        self['info'] = Label(_('SELECT YOUR CHOICE'))
        self["paypal"] = Label()
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_('Choice'))
        self['key_green'] = Button(_('- - - -'))
        # self["key_blue"] = Button()
        # self['key_blue'].hide()
        self["setupActions"] = ActionMap(['OkCancelActions',
                                          'DirectionActions',
                                          'ColorActions',
                                          'ButtonSetupActions',
                                          'VirtualKeyboardActions',
                                          'ActiveCodeActions'], {'cancel': self.extnok,
                                                                 'red': self.extnok,
                                                                 'back': self.close,
                                                                 'left': self.keyLeft,
                                                                 'right': self.keyRight,
                                                                 'yellow': self.Ok_edit,
                                                                 'showVirtualKeyboard': self.KeyText,
                                                                 'ok': self.Ok_edit,
                                                                 'green': self.msgok}, -1)
        self.createSetup()
        self.onLayoutFinish.append(self.layoutFinished)
        if self.setInfo not in self['config'].onSelectionChanged:
            self['config'].onSelectionChanged.append(self.setInfo)

    def paypal2(self):
        conthelp = "If you like what I do you\n"
        conthelp += "can contribute with a coffee\n\n"
        conthelp += "scan the qr code and donate € 1.00"
        return conthelp

    def layoutFinished(self):
        self.setTitle(self.setup_title)
        paypal = self.paypal2()
        self["paypal"].setText(paypal)
        if not os.path.exists('/tmp/currentip'):
            os.system('wget -qO- http://ipecho.net/plain > /tmp/currentip')
        currentip1 = open('/tmp/currentip', 'r')
        currentip = currentip1.read()
        self['description'].setText(_('Config Panel Addon\nYour current IP is %s') % currentip)
        logdata("Showpicture ", currentip)

    def createSetup(self):
        self.editListEntry = None
        self.list = []
        self.list.append(getConfigListEntry(_("Set the path to the Picons folder"), cfg.mmkpicon, _("Press Ok to select the folder containing the picons files")))
        self["config"].list = self.list
        self["config"].l.setList(self.list)

    def setInfo(self):
        try:
            sel = self['config'].getCurrent()[2]
            if sel:
                self['info'].setText(str(sel))
            else:
                self['info'].setText(_('SELECT YOUR CHOICE'))
            return
        except Exception as e:
            print("Error ", e)

    def changedEntry(self):
        self['key_green'].instance.setText(_('Save') if self['config'].isChanged() else '- - - -')
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
        if os.path.exists(cfg.mmkpicon.value) is False:
            self.session.open(MessageBox, _('Device not detected!'), MessageBox.TYPE_INFO, timeout=4)

        if self['config'].isChanged():
            for x in self["config"].list:
                x[1].save()
            cfg.save()
            configfile.save()
            # self.mbox = self.session.openWithCallback(self.restartenigma, MessageBox, _("Restart Enigma is Required. Do you want to continue?"), MessageBox.TYPE_YESNO)
            self.session.open(MessageBox, _('Successfully saved configuration'), MessageBox.TYPE_INFO, timeout=4)
            self.close(True)
        else:
            self.close()

    def Ok_edit(self):
        sel = self['config'].getCurrent()[1]
        if sel:
            if sel == cfg.mmkpicon:
                self.setting = 'mmkpicon'
                mmkpth = cfg.mmkpicon.value
                self.openDirectoryBrowser(mmkpth, 'pthpicon')
        else:
            pass

    def openDirectoryBrowser(self, path, itemcfg):
        try:
            callback_map = {
                "pthpicon": self.openDirectoryBrowserCB(cfg.mmkpicon)
            }

            if itemcfg in callback_map:
                self.session.openWithCallback(
                    callback_map[itemcfg],
                    LocationBox,
                    windowTitle=_("Choose Directory:"),
                    text=_("Choose directory"),
                    currDir=str(path),
                    bookmarks=config.movielist.videodirs,
                    autoAdd=True,
                    editDir=True,
                    inhibitDirs=["/bin", "/boot", "/dev", "/home", "/lib", "/proc", "/run", "/sbin", "/sys", "/usr", "/var"]
                )
        except Exception as e:
            print(e)

    def openDirectoryBrowserCB(self, config_entry):
        def callback(path):
            if path is not None:
                config_entry.setValue(path)
        return callback

    def KeyText(self):
        sel = self['config'].getCurrent()
        if sel:
            self.session.openWithCallback(self.VirtualKeyBoardCallback, VirtualKeyBoard, title=self['config'].getCurrent()[0], text=self['config'].getCurrent()[1].value)

    def VirtualKeyBoardCallback(self, callback=None):
        if callback is not None and len(callback):
            self['config'].getCurrent()[1].value = callback
            self['config'].invalidate(self['config'].getCurrent())

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
    from enigma import getDesktop
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
        self.previewPng = previewPng
        self['pixmap'] = Pixmap()
        try:
            self.PicLoad.PictureData.get().append(self.DecodePicture)
        except:
            self.PicLoad_conn = self.PicLoad.PictureData.connect(self.DecodePicture)
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions'], {'ok': self.close,
                                                       'cancel': self.close,
                                                       'blue': self.close}, -1)
        self.onLayoutFinish.append(self.ShowPicture)

    def ShowPicture(self):
        logdata("Showpicture ", 'Show')
        myicon = self.previewPng
        if screenwidth.width() == 2560:
            png = loadPic(myicon, 2560, 1440, 0, 0, 0, 1)
        elif screenwidth.width() == 1920:
            png = loadPic(myicon, 1920, 1080, 0, 0, 0, 1)
        else:
            png = loadPic(myicon, 1280, 720, 0, 0, 0, 1)
        self["pixmap"].instance.setPixmap(png)

    def DecodePicture(self, PicInfo=''):
        ptr = self.picload.getData()
        self['pixmap'].instance.setPixmap(ptr)


def main(session, **kwargs):
    try:
        session.open(SelectPicons)
    except Exception as e:
        print('error open plugin', e)


def menu(menuid, **kwargs):
    return [(title_plug, main(), 'mmPicons by mMark', 44)] if menuid == "mainmenu" else []
    # if menuid == 'mainmenu':
        # from Tools.BoundFunction import boundFunction
        # return [(title_plug,
                 # boundFunction(main, showExtentionMenuOption=True),
                 # 'mmPicons',
                 # -1)]
    # else:
        # return []


def systemmenu(menuid, **kwargs):
    if menuid == 'system':
        return [(title_plug, main, 'mmPicons', 44)]
    else:
        return []


def Plugins(**kwargs):
    ico_path = 'logo.png'
    if not Utils.DreamOS():
        ico_path = plugin_path + '/res/pics/logo.png'
    result = [PluginDescriptor(name=title_plug, description=desc_plugin, where=PluginDescriptor.WHERE_PLUGINMENU, icon=ico_path, fnc=main)]
    return result
