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

try:
    from kiwi import tasklet
except ImportError:
    #print _('Kiwi precisa ser instalado:')
    print _('Kiwi needs to be installed:')
    print "http://ftp.gnome.org/pub/GNOME/binaries/win32/kiwi/kiwi-1.9.21.win32.exe"
    raw_input()
    sys.exit(1)
    
from Tab import Tab
#from tabs.ConfigTab import ConfigTab


class ConsoleTab(Tab):
    
    def __init__(self, gui, GoGo, statusbar, liststoreSensorsTypes, sensorTypes):
        ### Board Console
        self.gui = gui
        self.GoGo = GoGo
        self.statusbar = statusbar
        self.labelConnected = self.gui.get_widget("labelConnected")
        self.sensorTypes = sensorTypes
        
        self.motorA=gui.get_widget("checkbuttonMotorA")
        self.motorB=gui.get_widget("checkbuttonMotorB")
        self.motorC=gui.get_widget("checkbuttonMotorC")
        self.motorD=gui.get_widget("checkbuttonMotorD")    
        self.motorPowerWidget=gui.get_widget("spinbuttonMotorPower")
        
        self.entryMinPwmDuty=gui.get_widget("entryMinPwmDuty")
        self.entryMaxPwmDuty=gui.get_widget("entryMaxPwmDuty")
        self.hscalePwmDuty=gui.get_widget("hscalePwmDuty")
        # Good limits for servos
        self.minDuty=20
        self.maxDuty=45
        self.hscalePwmDuty.set_range(self.minDuty,self.maxDuty)
        self.motorsActivated=""
        self.buttonSetPwmDuty=gui.get_widget("buttonSetPwmDuty")
        
        self.radiobuttonBurstFast=gui.get_widget("radiobuttonBurstFast")
        self.radiobuttonBurstSlow=gui.get_widget("radiobuttonBurstSlow")
        self.entryRefreshRate=gui.get_widget("entryRefreshRate")
        
        self.sensorBars=(
        gui.get_widget("progressbar1"),
        gui.get_widget("progressbar2"),
        gui.get_widget("progressbar3"),
        gui.get_widget("progressbar4"),
        gui.get_widget("progressbar5"),
        gui.get_widget("progressbar6"),
        gui.get_widget("progressbar7"),
        gui.get_widget("progressbar8"),
        )
        
        self.entrySensors=(
        gui.get_widget("entrySensor1"),
        gui.get_widget("entrySensor2"),
        gui.get_widget("entrySensor3"),
        gui.get_widget("entrySensor4"),
        gui.get_widget("entrySensor5"),
        gui.get_widget("entrySensor6"),
        gui.get_widget("entrySensor7"),
        gui.get_widget("entrySensor8"),
        )
        self.checkbuttonSensors=(
        gui.get_widget("checkbuttonSensor1"),
        gui.get_widget("checkbuttonSensor2"),
        gui.get_widget("checkbuttonSensor3"),
        gui.get_widget("checkbuttonSensor4"),
        gui.get_widget("checkbuttonSensor5"),
        gui.get_widget("checkbuttonSensor6"),
        gui.get_widget("checkbuttonSensor7"),
        gui.get_widget("checkbuttonSensor8")
        )
        
        self.comboboxSensors=(
        gui.get_widget("comboboxSensor1"),
        gui.get_widget("comboboxSensor2"),
        gui.get_widget("comboboxSensor3"),
        gui.get_widget("comboboxSensor4"),
        gui.get_widget("comboboxSensor5"),
        gui.get_widget("comboboxSensor6"),
        gui.get_widget("comboboxSensor7"),
        gui.get_widget("comboboxSensor8")    
        )
        for i in self.comboboxSensors:
            i.set_model(liststoreSensorsTypes)
        
        self.sensorValues=[0]*8    
            
        self.burstModeOnOff=False
        self.refreshMode=False
        self.refreshRate=1000
        
        ###/Board Console
            
    def taskleted(func):
        def new(*args,**kwargs):
            tasklet.Tasklet(func(*args,**kwargs))
        return new
    
    
    @taskleted
    def showStatusMsg(self,context,msg):        
        context_id=self.statusbar.get_context_id(context)        
        msg_id=self.statusbar.push(context_id,msg)
        timeout=tasklet.WaitForTimeout(1000)
        yield timeout
        self.statusbar.remove(context_id,msg_id) # See >>>
        # "remove" depreciated in later GTK version, so in future use >>> 
        #self.statusbar.remove_message(context_id,msg_id)
        tasklet.get_event()
        
    def setDisconnected(self):
            #self.showWarning(_("Gogo desconectada"))
            self.showWarning(_("Gogo disconnected"))
            #self.statusbar.push(0,_("Gogo desconectada"))
            self.statusbar.push(0,_("Gogo disconnected"))
            #self.labelConnected.set_markup(_("<b><span size='xx-large'>Gogo Desconectada</span></b>"))
            self.labelConnected.set_markup(_("<b><span size='xx-large'>Gogo Disconnected</span></b>"))


    def runCommand(self,command,context,msg):
        try:
            print ">>> runCommand(" + msg + ")"
            command()
            self.showStatusMsg(context,msg)
        except:
            self.setDisconnected()
        
    

    def buttonBeep_clicked_cb(self, widget):
            self.runCommand(self.GoGo.beep,_("Misc"),_("Beep"))

    def buttonLedOn_clicked_cb(self, widget):
        try:
            self.GoGo.ledOn()
            self.showStatusMsg(_("Misc"),_("LED On"))
        except:
            self.setDisconnected()
        
    def buttonLedOff_clicked_cb(self, widget):
        try:
            self.GoGo.ledOff()
            self.showStatusMsg(_("Misc"),_("LED Off"))
        except:
            self.setDisconnected()
        
        
    def checkbuttonMotor_toggled_cb(self,widget):
        m=""
        if self.motorA.get_active():
            m=m+'a'
        if self.motorB.get_active():
            m=m+'b'
        if self.motorC.get_active():
            m=m+'c'
        if self.motorD.get_active():
            m=m+'d'
        try:
            self.GoGo.talkToMotor(m)
            self.motorsActivated=m
            #self.showStatusMsg(_("Motor"), _("Controlar motores: ") + m)
            self.showStatusMsg(_("Motor"), _("Controlling motors: ") + m)
        except:
            #self.showStatusMsg(_("Motor"), _("Controlar motores: ") + m)
            self.showStatusMsg(_("Motor"), _("Controlling motors: ") + m)
        
        
        
    def buttonMotorControlOn_clicked_cb(self, widget):        
        try:
            self.GoGo.motorOn()
            #self.showStatusMsg(_("Motor"), _("Motores ") + self.motorsActivated + _(" Ligados"))
            self.showStatusMsg(_("Motor"), _("Motors ") + self.motorsActivated + _(" On"))
        except:
            self.setDisconnected()
    
    def buttonMotorControlOff_clicked_cb(self, widget):
        try:
            self.GoGo.motorOff()
            #self.showStatusMsg(_("Motor"), _("Motores ") + self.motorsActivated + _(" Desligados"))
            self.showStatusMsg(_("Motor"), _("Motors ") + self.motorsActivated + _(" Off"))
        except:
            self.setDisconnected()
    
    def buttonMotorControlBreak_clicked_cb(self, widget):
        try:
            self.GoGo.motorBreak()
            #self.showStatusMsg(_("Motor"), _("Motores ") + self.motorsActivated + _(" Brecados"))
            self.showStatusMsg(_("Motor"), _("Motors ") + self.motorsActivated + _(" Brake"))
        except:
            self.setDisconnected()
        
    def buttonMotorControlCoast_clicked_cb(self, widget):
        try:
            self.GoGo.motorCoast()
            #self.showStatusMsg(_("Motor"), _("Motores ") + self.motorsActivated + _(" Parados"))
            self.showStatusMsg(_("Motor"), _("Motors ") + self.motorsActivated + _(" Coast"))
        except:
            self.setDisconnected()
    
    def buttonPowerSet_clicked_cb(self, widget):
        try:
            power=self.motorPowerWidget.get_value_as_int()
            self.GoGo.setMotorPower(power)
            #self.showStatusMsg(_("Motor"), _("Pontência dos Motores ") + self.motorsActivated + _(" definida para ") + str(power))
            self.showStatusMsg(_("Motor"), _("Power of Motors ") + self.motorsActivated + _(" set to ") + str(power))
        except:
            self.setDisconnected()
    
    def buttonMotorControlThisway_clicked_cb(self, widget):
        try:
            self.GoGo.motorThisway()
            #self.showStatusMsg(_("Motor"), _("Motores ") + self.motorsActivated + _(" para lá"))
            self.showStatusMsg(_("Motor"), _("Motors ") + self.motorsActivated + _(" this way"))
        except:
            self.setDisconnected()
        
    def buttonMotorControlThatway_clicked_cb(self, widget):
        try:
            self.GoGo.motorThatway()
            #self.showStatusMsg(_("Motor"), _("Motores ") + self.motorsActivated + _(" para cá"))
            self.showStatusMsg(_("Motor"), _("Motors ") + self.motorsActivated + _(" that way"))
        except:
            self.setDisconnected()
        
    def buttonMotorControlReverse_clicked_cb(self, widget):
        try:
            self.GoGo.motorReverse()
            #self.showStatusMsg(_("Motor"), _("Motores ") + self.motorsActivated + _(" revertidos"))
            self.showStatusMsg(_("Motor"), _("Motors ") + self.motorsActivated + _(" reversed"))
        except:
            self.setDisconnected()
    
    
    
    def entryMinPwmDuty_changed_cb(self,widget):
        try:
            self.minDuty=int(widget.get_text())
        except:
            return
        else:
            if self.minDuty>self.maxDuty:
                self.minDuty=self.maxDuty-1
            if self.minDuty<0:
                self.minDuty=0
            try:
                self.hscalePwmDuty.set_range(self.minDuty,self.maxDuty)
            except:
                print self.minDuty,self.maxDuty            
        
    def entryMaxPwmDuty_changed_cb(self,widget):
        try:
            self.maxDuty=int(widget.get_text())
        except:
            return
        else:
            if self.maxDuty<self.minDuty:
                self.maxDuty=self.minDuty+1
            if self.maxDuty>255:
                self.maxDuty=255            
            try:
                self.hscalePwmDuty.set_range(self.minDuty,self.maxDuty)
            except:
                print self.minDuty,self.maxDuty
    
    def buttonSetPwmDuty_clicked_cb(self,widget):
        try:
            duty=int(self.hscalePwmDuty.get_value())
            self.GoGo.setPwmDuty(duty)
            #self.showStatusMsg(_("Motor"), _("Motores ") + self.motorsActivated + _(" de passo: ") +str(duty))
            self.showStatusMsg(_("Motor"), _("Motors ") + self.motorsActivated + _(" PwmDuty: ") +str(duty))
        except:
            self.setDisconnected()
    
    def get_sensor_value(self,sensorNumber):
        #print 'get_sensor_value'
        try:
            return self.GoGo.readSensor(sensorNumber)
        except:
            self.burstModeOnOff = False
            self.refreshMode =  False
            #self.showWarning("Gogo desconectada##")
            #self.statusbar.push(0,"Gogo desconectada")
        #return sensorNumber*100
    
    def get_sensor_text(self,sensorNumber,value):        
        stype=self.comboboxSensors[sensorNumber].get_active()    
        if stype>=0:
            return self.sensorTypes[stype].get_text(value)            
        else:
            return str(value)
        
    
    
    def buttonRefreshAll_clicked_cb(self,widget):
        self.refreshMode = True
        for i in range(8):
            if self.refreshMode:
                value=self.get_sensor_value(i)
                if value>-1:
                    self.sensorValues[i]=value
                    self.entrySensors[i].set_text(self.get_sensor_text(i,value))
                    self.sensorBars[i].set_fraction(self.sensorValues[i]/1023.0)
        #self.showStatusMsg(_("Sensor"), _("Valor dos sensores atualizado"))    
        self.showStatusMsg(_("Sensor"), _("All sensor readings refreshed"))    
        
        #print self.GoGo.readSensor(0)
    
    def refreshSensors(self):
        while self.burstModeOnOff:
            timeout = tasklet.WaitForTimeout(self.refreshRate)
            for i in range(8):
                if self.checkbuttonSensors[i].get_active() and self.burstModeOnOff:
                    value=self.get_sensor_value(i)
                    if value>-1:
                        self.sensorValues[i]=value
                        self.entrySensors[i].set_text(self.get_sensor_text(i,value))
                        self.sensorBars[i].set_fraction(self.sensorValues[i]/1023.0)
            yield timeout
            tasklet.get_event()
    
    
    def burstMode(self):
        if self.radiobuttonBurstFast.get_active():
            self.entryRefreshRate.set_text("20 hz")
            self.refreshRate=50
            #self.showStatusMsg(_("Sensor"), _("Leitura de sensores a 20hz"))
            self.showStatusMsg(_("Sensor"), _("Reading sensors at 20hz"))
        if self.radiobuttonBurstSlow.get_active():
            self.entryRefreshRate.set_text("5 hz")
            self.refreshRate=200
            #self.showStatusMsg(_("Sensor"), _("Leitura de sensores a 5hz"))
            self.showStatusMsg(_("Sensor"), _("Reading sensors at a 5hz"))


    def buttonSensorBurstOn_clicked_cb(self,widget):
        self.burstMode()
        self.burstModeOnOff=True
        tasklet.run(self.refreshSensors())
        
    def radiobuttonBurstFast_toggled_cb(self,widget):
        self.burstMode()
            
    def radiobuttonBurstSlow_toggled_cb(self,widget):
        self.burstMode()
    
    def buttonSensorBurstOff_clicked_cb(self,widget):    
        
        self.entryRefreshRate.set_text("0")
        self.burstModeOnOff=False
        #self.showStatusMsg(_("Sensor"), _("Leitura de sensores desligada"))
        self.showStatusMsg(_("Sensor"), _("Burst mode off"))
        
