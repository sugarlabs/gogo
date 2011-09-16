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

import sys

from gettext import gettext as _

#try:
#	import serial
#except ImportError:	
#    #print _('pySerial precisa ser instalado:')
#    print _('pySerial needs to be installed:')
#    print "http://downloads.sourceforge.net/pyserial/pyserial-2.2.win32.exe?modtime=1122861377&big_mirror=0"
#	#raw_input()
#	sys.exit(1)


from Tab import Tab
#from pyLogoCompiler.Exceptions import *
import os


class ConfigTab(Tab):

    #textConnected    = _("<b><span size='xx-large'>GoGo%(version)sConnected</span></b>")     
    #textDisconnected = _("<b><span size='xx-large'>Gogo%(version)sDisconnected</span></b>")
    
    def __init__(self,gui, GoGo, notebookMain, statusbar, activity=None):
        self.gui = gui
        self.GoGo = GoGo
        self.activity = activity

        self.notebookMain = notebookMain	
        self.statusbar = statusbar
        self.labelConnected = self.gui.get_widget("labelConnected")
        self.boardImage = self.gui.get_widget("imageMonitor")
        
        if self.activity:
            lbl = self.gui.get_widget("labelTitleVersion")
            lbl.set_markup(_('<b><span size="xx-large">GoGo Activity</span></b> (v %(version)s)' \
                                  % {"version": os.environ['SUGAR_BUNDLE_VERSION']}))        
            


    def buttonConnect_clicked_cb(self,widget):
        if self.GoGo.autoConnect():
            i = self.GoGo.getPort()
            if os.name=='nt':
                #self.statusbar.push(0,_("Gogo conectada na porta COM ") + str(i+1) + "")
                self.statusbar.push(0,_("Gogo connected to the COM port ") + str(i+1) + "")
            else:
                #self.statusbar.push(0,_("Gogo conectada na porta /dev/ttyS") + str(i) + "")
                self.statusbar.push(0,_("Gogo connected on port ") + str(i) + "")
                # Set board image depending on serial/usb (needs checking)
                if self.GoGo.isUSBVersion():
                    self.boardImage.set_from_file("gui/usb-board-tour.png")
                else:
                    self.boardImage.set_from_file("gui/serial.png")
                    
            #self.labelConnected.set_markup(_("<b><span size='xx-large'>Conectado</span></b>"))		
            self.labelConnected.set_markup(_("<b><span size='xx-large'>GoGo Connected</span></b>"))        
        else:
            print "Gogo not found"
            #self.showWarning(_("Houve algum problema com a conexão verifique se a gogoboard está conectada adequadamente e se está ligada"))	
            self.showWarning(_("There were problems with the connection. Make sure the GoGo Board is properly connected."))    
        

    def buttonDisconnect_clicked_cb(self,widget):
        self.GoGo.closePort()
        #self.notebookMain.set_show_tabs(False)
        #self.labelConnected.set_markup(_("<b><span size='xx-large'>Gogo Desconectada</span></b>"))
        self.labelConnected.set_markup(_("<b><span size='xx-large'>Gogo Disconnected</span></b>"))
        #self.statusbar.push(0,_("Gogo desconectada"))
        self.statusbar.push(0,_("Gogo disconnected"))
        
    def buttonSetLanguage_clicked_cb(self,widget):
        pass
