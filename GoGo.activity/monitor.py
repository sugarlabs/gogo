#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Este arquivo é parte do programa Monitor
# Monitor é um software livre; você pode redistribui-lo e/ou 
# modifica-lo dentro dos termos da Licença Pública Geral GNU como 
# publicada pela Fundação do Software Livre (FSF); na versão 3 da 
# Licença, ou (na sua opinião) qualquer versão.
#
# Este programa é distribuido na esperança que possa ser  util, 
# mas SEM NENHUMA GARANTIA; sem uma garantia implicita de ADEQUAÇÂO a qualquer
# MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a
# Licença Pública Geral GNU para maiores detalhes.
#
# Você deve ter recebido uma cópia da Licença Pública Geral GNU
# junto com este programa, se não, escreva para a Fundação do Software
# Livre(FSF) Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

# Centro de Tecnologia da Informação Renato Archer, Campinas-SP, Brasil
# Projeto realizado com fundos do Conselho Nacional de Desenvolvimento Científico e Tecnológico (CNPQ)

# Esse código faz parte do projeto BR-Gogo, disponível em http://sourceforge.net/projects/br-gogo/


importerror=False

import pickle,sys
from time import sleep

from gettext import gettext as _

try:
    import pygtk
    pygtk.require('2.0')
    import gtk
    import gtk.glade
    assert gtk.gtk_version >= (2, 8, 0)
    assert gtk.pygtk_version >= (2, 8, 0)
except AssertionError:
    #print _("Você não tem a versão necessária do GTK+ e/ou PyGTK instalada.")
    print _("You do not have the required version of GTK + and / or PyGTK installed.")
    #print _('A versão instalada do GTK+ é: %s') % ('.'.join([str(n) for n in gtk.gtk_version]))
    print _('The installed version of GTK+ is: %s') % ('.'.join([str(n) for n in gtk.gtk_version]))
    #print _('A versão do GTK+ necessária é: 2.8.0 ou mais recente\n')
    print _('The version of GTK + is required: 2.8.0 or newer\n')
    print "http://downloads.sourceforge.net/gladewin32/gtk-2.12.9-win32-1.exe?modtime=1208401479&big_mirror=0"
    #print _('A versão do PyGTK instalada é: %s') % ('.'.join([str(n) for n in gtk.pygtk_version]))
    print _('The version of PyGTK installed is: %s') % ('.'.join([str(n) for n in gtk.pygtk_version]))
    #print _('A versão do PyGTK necessária é: 2.8.0 ou mais recente\n')
    print _('The version of PyGTK is required: 2.8.0 or newer\n')
    print "http://ftp.gnome.org/pub/GNOME/binaries/win32/pygtk/2.10/pygtk-2.10.6-1.win32-py2.5.exe"
    importerror=True
except:
    #print _('A versão do PyGTK necessária é: 2.8.0 ou mais recente, ela é necessária para a execução do programa.')
    print _('PyGTK 2.8.0 or newer is required.')
    #print _('Não foi encontrada nenhuma versão do PyGTK no seu sistema.')
    print _('There was no version of PyGTK found on your system.')
    print "http://ftp.gnome.org/pub/GNOME/binaries/win32/pygtk/2.10/pygtk-2.10.6-1.win32-py2.5.exe"
    importerror=True
    
#try:
#    import gtk.glade
#except:
#    #print _("Você não tem a versão necessária do python-glade2 instalada.")
#    print _("You do not have the required version of python-glade2 installed.")
#    importerror=True


try:
    import serial
except ImportError:
    #print _('pySerial precisa ser instalado:')
    print _('pySerial needs to be installed:')
    print "http://downloads.sourceforge.net/pyserial/pyserial-2.2.win32.exe?modtime=1122861377&big_mirror=0"
    importerror=True
    
    

#try:
#    import cairo
#except ImportError:
#    #print _('PyCairo precisa ser instalado:')
#    print _('PyCairo needs to be installed:')
#    print "http://ftp.gnome.org/pub/GNOME/binaries/win32/pycairo/1.2/pycairo-1.2.6-1.win32-py2.5.exe"
#    importerror=True

#try:
#    from cairoplot import plots
#    USE_CAIROPLOT = True
#except:
#    USE_CAIROPLOT = False
#print "USE_CAIROPLOT: ",USE_CAIROPLOT

#try:
#    import gobject
#except ImportError:
#    #print _('PyGObject precisa ser instalado:')
#    print _('PyGObject needs to be installed:')
#    print "http://ftp.gnome.org/pub/GNOME/binaries/win32/pygobject/2.12/pygobject-2.12.3-1.win32-py2.5.exe"
#    importerror=True

#try:
#    import kiwi
#except ImportError:
#    #print _('Kiwi precisa ser instalado:')
#    print _('Kiwi needs to be installed:')
#    print "http://ftp.gnome.org/pub/GNOME/binaries/win32/kiwi/kiwi-1.9.21.win32.exe"    
#    importerror=True

if importerror:
    #raw_input()
    sys.exit(1)

#from communication.Communication import Comm
from pyLogoCompiler import pyYacc
from pyLogoCompiler.Communication import GoGoComms

from tabs.Tab import Tab
from tabs.ConsoleTab import ConsoleTab
from tabs.ProceduresTab import ProceduresTab
from tabs.UploadTab import UploadTab
from tabs.SensorsTab import SensorsTab
from tabs.ConfigTab import ConfigTab



NAME=_("Board Monitor")
VERSION="0.3.1"
AUTHORS="Br-Gogo\nhttp://br-gogo.sourceforge.net\n\nFelipe Andrade Holanda\n\nFelipe Augusto Silva (revisor)\n"



class BoardMonitor(object):
    def __init__(self, activity=None):
        #Carrega a interface a partir do arquivo glade
        
        self.activity = activity
        
#        if gtk.gtk_version >= (2, 6, 0):
#            self.gui = gtk.glade.XML('gui/monitor.glade')
#        else:
#            self.gui = gtk.glade.XML('gui/monitor-alt.glade')
        self.gui = gtk.glade.XML('gui/monitor.glade')
        
        self.window    = self.gui.get_widget('mainWindow')    
        self.statusbar = self.gui.get_widget('statusbar')

        self.GoGo = GoGoComms()
        
        #self.gui.get_widget('statusbarVersion').push(0,'Versão '+VERSION)
        self.gui.get_widget('statusbarVersion').push(0,_('Version ') + VERSION)
        #self.statusbar.set_has_resize_grip(True)    

        self.notebookMain = self.gui.get_widget('notebookMain')    
        self.liststore    = gtk.ListStore(str, str, str) # Name, Unit, #Description
        
        self.sensorsTab    = SensorsTab(self.gui, self.liststore)
        self.sensorTypes   = self.sensorsTab.sensorTypes
        self.proceduresTab = ProceduresTab(self.gui, self.GoGo, self.statusbar, self.activity)
        self.uploadTab     = UploadTab(self.gui, self.GoGo, self.liststore, self.sensorTypes, self.activity)
        self.configTab     = ConfigTab(self.gui, self.GoGo, self.notebookMain, self.statusbar, self.activity)
        self.consoleTab    = ConsoleTab(self.gui, self.GoGo, self.statusbar, self.liststore, self.sensorTypes)
        
        self.notebookMain.reorder_child(self.gui.get_widget('vboxConfigurationTab'),-1)
        self.notebookMain.set_current_page(-1)    
        self.notebookMain.set_show_tabs(True)    
        
        #Conecta Sinais aos Callbacks:        
        dic = {"gtk_main_quit" : gtk.main_quit}
        self.gui.signal_autoconnect(dic)    
        self.gui.signal_autoconnect(self)
        

### Main Window Callbacks:

    def imagemenuitemAbout_activate_cb(self,widget):    
        about = gtk.AboutDialog()        
        about.set_name(NAME)
        about.set_version(VERSION)
        #about.set_copyright(copyright)
        #about.set_comments(comments)
        #about.set_license(license)
        #about.set_wrap_license(license)
        #about.set_website(website)
        #about.set_website_label(website_label)
        about.set_authors(AUTHORS)
        #about.set_documenters(documenters)
        #about.set_artists(artists)
        #about.set_translator_credits(translator_credits)    
        #about.set_logo(gtk.gdk.pixbuf_new_from_file("gui/gogo.png"))
        about.set_logo(self.gui.get_widget('imageMonitor').get_pixbuf())
        #about.set_logo_icon_name(icon_name)
        
        about.run()
        about.destroy()
        
    def imagemenuitemHelp_activate_cb(self,widget):
        pass
### Board Console Callbacks:    
    def buttonBeep_clicked_cb(self, widget):
        self.consoleTab.buttonBeep_clicked_cb(widget)        
        
    def buttonLedOn_clicked_cb(self, widget):
        self.consoleTab.buttonLedOn_clicked_cb(widget)        
        
    def buttonLedOff_clicked_cb(self, widget):
        self.consoleTab.buttonLedOff_clicked_cb(widget)        
        
    def checkbuttonMotor_toggled_cb(self,widget):
        self.consoleTab.checkbuttonMotor_toggled_cb(widget)        
        
    def buttonMotorControlOn_clicked_cb(self, widget):
        self.consoleTab.buttonMotorControlOn_clicked_cb(widget)        
    
    def buttonMotorControlOff_clicked_cb(self, widget):        
        self.consoleTab.buttonMotorControlOff_clicked_cb(widget)
    
    def buttonMotorControlBreak_clicked_cb(self, widget):
        self.consoleTab.buttonMotorControlBreak_clicked_cb(widget)
        
    def buttonMotorControlCoast_clicked_cb(self, widget):
        self.consoleTab.buttonMotorControlCoast_clicked_cb(widget)
    
    def buttonPowerSet_clicked_cb(self, widget):
        self.consoleTab.buttonPowerSet_clicked_cb(widget)
    
    def buttonMotorControlThisway_clicked_cb(self, widget):
        self.consoleTab.buttonMotorControlThisway_clicked_cb(widget)
        
    def buttonMotorControlThatway_clicked_cb(self, widget):
        self.consoleTab.buttonMotorControlThatway_clicked_cb(widget)
        
    def buttonMotorControlReverse_clicked_cb(self, widget):
        self.consoleTab.buttonMotorControlReverse_clicked_cb(widget)
        
    
    # def entryMinPwmDuty_changed_cb(self,widget):
        # print "entryMinPwmDuty_changed_cb"
        # #self.consoleTab.entryMaxPwmDuty_changed_cb(widget)
            
    # def entryMaxPwmDuty_changed_cb(self,widget):
        # print "entryMaxPwmDuty_changed_cb"
        # #self.consoleTab.entryMaxPwmDuty_changed_cb(widget)
    
    def entryMinPwmDuty_changed_cb(self,widget):
        self.consoleTab.entryMinPwmDuty_changed_cb(widget)
        
    def entryMaxPwmDuty_changed_cb(self,widget):
        self.consoleTab.entryMaxPwmDuty_changed_cb(widget)
        
    def buttonSetPwmDuty_clicked_cb(self,widget):
        print "buttonSetPwmDuty_clicked_cb"
        self.consoleTab.buttonSetPwmDuty_clicked_cb(widget)
    
    def buttonRefreshAll_clicked_cb(self,widget):
        self.consoleTab.buttonRefreshAll_clicked_cb(widget)
    
    def buttonSensorBurstOn_clicked_cb(self,widget):
        self.consoleTab.buttonSensorBurstOn_clicked_cb(widget)
        
    def radiobuttonBurstFast_toggled_cb(self,widget):
        self.consoleTab.radiobuttonBurstFast_toggled_cb(widget)
            
    def radiobuttonBurstSlow_toggled_cb(self,widget):
        self.consoleTab.radiobuttonBurstSlow_toggled_cb(widget)
    
    def buttonSensorBurstOff_clicked_cb(self,widget):
        self.consoleTab.buttonSensorBurstOff_clicked_cb(widget)    
    
        
### /Board Console
    
    
### Logo Procedures Callbacks:    
    def buttonNew_clicked_cb(self,widget):
        self.proceduresTab.buttonNew_clicked_cb(widget)
        
    def buttonOpen_clicked_cb(self,widget):
        self.proceduresTab.buttonOpen_clicked_cb(widget)
        
    def buttonSave_clicked_cb(self,widget):
        self.proceduresTab.buttonSave_clicked_cb(widget)
        
    def buttonSaveAs_clicked_cb(self,widget):
        self.proceduresTab.buttonSaveAs_clicked_cb(widget)
        
    def buttonDownload_clicked_cb(self,widget):        
        self.proceduresTab.buttonDownload_clicked_cb(widget)        
### /Logo Procedures
    
    
### Recorded Data Callbacks:    
    def buttonStartUpload_clicked_cb(self,widget):
        self.uploadTab.buttonStartUpload_clicked_cb(widget)
        
    def buttonSaveData_clicked_cb(self,widget):
        self.uploadTab.buttonSaveData_clicked_cb(widget)
        
    def buttonClearData_clicked_cb(self,widget):
        self.uploadTab.buttonClearData_clicked_cb(widget)
        
    def spinbuttonColumns_changed_cb(self,widget):
        self.uploadTab.spinbuttonColumns_changed_cb(widget)
        
    def colSpec_changed_cb(self,widget):
        self.uploadTab.colSpec_changed_cb(widget)
        
    def checkbuttonShowHeaders_toggled_cb(self,widget):
        self.uploadTab.checkbuttonShowHeaders_toggled_cb(widget)
        
    def checkbuttonTwoLineHeader_toggled_cb(self,widget):
        self.uploadTab.checkbuttonTwoLineHeader_toggled_cb(widget)
            
    def notebookDataView_switch_page_cb(self,widget,page,page_num):
        self.uploadTab.notebookDataView_switch_page_cb(widget,page,page_num)
        
### /Recorded Data
    
    
### SensorLab Callbacks:
    def sensorPoint_edited_cb(self,cell, path, new_text, column):
        self.sensorsTab.sensorPoint_edited_cb(cell, path, new_text, column)    
        
    def edited_cb(self,cell, path, new_text, column):        
        self.sensorsTab.edited_cb(cell, path, new_text, column)        
            
    def treeviewSensors_cursor_changed_cb(self,treeviewSensors):
        self.sensorsTab.treeviewSensors_cursor_changed_cb(treeviewSensors)    
    
    def buttonAddSensor_clicked_cb(self,widget):
        self.sensorsTab.buttonAddSensor_clicked_cb(widget)        
        
    def buttonRemoveSensor_clicked_cb(self,widget):
        self.sensorsTab.buttonRemoveSensor_clicked_cb(widget)
    
    def buttonImportSensors_clicked_cb(self,widget):
        self.sensorsTab.buttonImportSensors_clicked_cb(widget)
        
    def buttonExportSensors_clicked_cb(self,widget):
        self.sensorsTab.buttonExportSensors_clicked_cb(widget)
    
    def buttonExportSensorsCSV_clicked_cb(self,widget):
        self.sensorsTab.buttonExportSensorsCSV_clicked_cb(widget)
    
    def buttonInsertPoint_clicked_cb(self,widget):
        self.sensorsTab.buttonInsertPoint_clicked_cb(widget)
            
    def buttonRemovePoint_clicked_cb(self,widget):
        self.sensorsTab.buttonRemovePoint_clicked_cb(widget)    
###/Sensors
    
    
### Configuration Callbacks:
    def buttonConnect_clicked_cb(self,widget):
        self.configTab.buttonConnect_clicked_cb(widget)        
    
    def buttonDisconnect_clicked_cb(self,widget):
        self.configTab.buttonDisconnect_clicked_cb(widget)
        
    def buttonSetLanguage_clicked_cb(self,widget):
        self.configTab.buttonSetLanguage_clicked_cb(widget)    
### /Configuration
    
    
    


    

if __name__ == '__main__':
        m = BoardMonitor()
        
        #Exibe toda interface:
        m.window.show_all()
        
        #Inicia o loop principal de eventos (GTK MainLoop):
        gtk.main()

        
