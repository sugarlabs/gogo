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

import os
if os.name=='nt':
    import win32api
    import win32con

from gettext import gettext as _

import gi
gi.require_version('Pango', '1.0')

try:
    from gi.repository import Gtk
except ImportError:
    #print _('GTK+ Runtime Enviromnt precisa ser instalado:')
    print((_('GTK+ Runtime Enviroment needs to be installed:')))
    print("http://downloads.sourceforge.net/gladewin32/Gtk-2.12.9-win32-1.exe?modtime=1208401479&big_mirror=0")
    eval(input())
    
from .Tab import Tab

from pyLogoCompiler.Exceptions import ConnectionProblem

from gi.repository import Pango

from cairoplot import plots
from cairoplot.series import Series

# >>>>>>>>>>>>>>>>> temp

# For non-dev machines, quick hack at attempt to show traceback in in a msg dialog

import sys
import traceback

def logexception(type, value, tb):
    text = ' '.join(t for t in traceback.format_exception(type, value, tb))
    print(text)
    try:
        dialog = Gtk.MessageDialog(None, Gtk.DIALOG_MODAL, \
                                         Gtk.MESSAGE_INFO, \
                                         Gtk.BUTTONS_OK, \
                                         text)
        dialog.run()
        dialog.destroy()
    except:
        pass
    
sys.excepthook = logexception

# <<<<<<<<<<<<<<<<<<< temp



class UploadTab(Tab):
    
    LAST_DATA_FILENAME = '.last_data.txt'
    defaultTab = 9
    
    def __init__(self, gui, GoGo, liststoreSensorsTypes, sensorTypes, activity=None):    
        self.gui = gui
        self.GoGo = GoGo
        self.sensorTypes = sensorTypes
        self.activity = activity
        
        self.dataFilename = ""
        
        self.data = []
        self.colDataRaw = []
        self.colDataMapped = []
        
        self.textviewData = self.gui.get_object('textviewData')
        self.textviewData.modify_font(Pango.FontDescription('monospace'))
        self.textviewBuffer = Gtk.TextBuffer()
        self.textviewData.set_buffer(self.textviewBuffer)

        self.spinbuttonColumns = self.gui.get_object('spinbuttonColumns')

        self.checkbuttonShowHeaders   = self.gui.get_object('checkbuttonShowHeaders')
        self.checkbuttonTwoLineHeader = self.gui.get_object('checkbuttonTwoLineHeader')
        
        self.progressbar = self.gui.get_object('progressbarUpload')
        self.lblProgress = self.gui.get_object('labelValuesUploaded')
        self.uploadTotal = 0
        
        self.colSpec = []
        for c in range(8):
            w = self.gui.get_object('comboboxC%i' % c)
            w.set_active(0)
            w.set_sensitive(c == 0)
            w.set_model(liststoreSensorsTypes)
            self.colSpec.append(w)

        #if not self.activity:
        try:
            f=open(self.LAST_DATA_FILENAME,'r')
            self.textviewBuffer.set_text(f.read())
            f.close()
        except:
            pass
        
        self.graphContainer = None
        self.graphWidth  = 50
        self.graphHeight = 50
        self.graphData = None
        self.graph = None
        self.graphVisible = False
        self.graphUpdateRequired = False
        
        self.notebookDataView = self.gui.get_object('notebookDataView')
        #self.notebookDataView.set_current_page(0)
       

    def buttonStartUpload_clicked_cb(self,widget):
        print("uploading")
        try:
            self.progressbar.set_fraction(0.0)
            self.lblProgress.set_text(_('%i Values Uploaded' % 0))
            while Gtk.events_pending():
                Gtk.main_iteration(False)
            self.data = self.GoGo.autoUpload(self.uploadProgress_cb)
        except ConnectionProblem:
            self.showWarning(_("Check GoGo plugged in, turned on and connected"))
            return
        except:
            self.showError(_("Error communicating"))
            return
        else:
            self.lblProgress.set_text(_('%i Values Uploaded' % len(self.data)))
            self.refreshTextView()
            self.showInfo(_("Data successfully uploaded."), self.gui.get_object('mainWindow'))
        
    
    def buttonSaveData_clicked_cb(self,widget):
        if len(self.data) == 0:
            return
        
#        if self.activity:
#            self.activity.save()
#            return
        
        dialog = Gtk.FileChooserDialog(_("Save As.."), None, Gtk.FILE_CHOOSER_ACTION_SAVE,
        (Gtk.STOCK_CANCEL,Gtk.RESPONSE_CANCEL,Gtk.STOCK_SAVE, Gtk.RESPONSE_OK))        
        dialog.set_default_response(Gtk.RESPONSE_OK)
        response = dialog.run()
        if response == Gtk.RESPONSE_OK:
            self.dataFilename = dialog.get_filename()
            try:
                FILE = open(self.dataFilename,"w")
                FILE.write(self.dataFormattedForSaving())
                FILE.close()
            except Exception as e:
                self.showError(e.__str__())
        dialog.destroy()
        
    def buttonClearData_clicked_cb(self,widget):
        self.data = []
        self.colDataRaw = []
        self.colDataMapped = []
        self.dataFilename = ""
        self.progressbar.set_fraction(0.0)
        self.lblProgress.set_text(_('%i Values Uploaded' % 0))
        self.refreshTextView()
    
    def spinbuttonColumns_changed_cb(self,widget):
        cc = self.spinbuttonColumns.get_value_as_int()
        for c in range(8):
            self.colSpec[c].set_sensitive(c < cc)
        self.refreshTextView()
        
    def colSpec_changed_cb(self,widget):
        self.refreshTextView()
        
    def checkbuttonShowHeaders_toggled_cb(self,widget):
        self.checkbuttonTwoLineHeader.set_sensitive(widget.get_active())
        self.refreshTextView()
        
    def checkbuttonTwoLineHeader_toggled_cb(self,widget):
        self.refreshTextView()
        
    def notebookDataView_switch_page_cb(self,widget,page,page_num):
        self.graphVisible = page_num == 1
        if self.graphVisible:
            self.refreshGraph()
            
        
    def getSelectedSensors(self):
        sensorIndexes = [w.get_active() for w in self.colSpec[:self.spinbuttonColumns.get_value_as_int()]]
        for i in [i for i,v in enumerate(sensorIndexes) if v == -1]:
            sensorIndexes[i] = 0 
        return [self.sensorTypes[n] for n in sensorIndexes]
        
        
    def calibrateData(self):
        self.colDataMapped = []
        
        maxRows = max([len(c) for c in self.colDataRaw])
        
        sensors = self.getSelectedSensors()
        
        for c,data in enumerate(self.colDataRaw):
            m = [round(sensors[c].get_new_value(v),3) for v in data]
            if len(m) < maxRows:
                m += [''] * (maxRows - len(m))
            self.colDataMapped += [m]
    
    
    def getSensorHeaders(self):
        self.useHdrs = False
        self.hdrs = []
        
        if not self.checkbuttonShowHeaders.get_active():
            return False
        
        sensors = self.getSelectedSensors()
        
        self.hdrs = [[s.name,s.unit] for s in sensors]
        for i in [i for i,h in enumerate(self.hdrs) if h[1] == None or h[1] == '']:
            self.hdrs[i][1] = 'None' 
        
        self.useHdrs = True
        return True
    

    def csvHeaders(self):
        if not self.useHdrs:
            return ''
        
        if not self.checkbuttonTwoLineHeader.get_active():
            t = ','.join([('%s (%s)' % (h[0],h[1])) for h in self.hdrs]) + '\n'
            return t
         
        t  = ','.join([h[0] for h in self.hdrs]) + '\n'
        t += ','.join([h[1] for h in self.hdrs]) + '\n'
        return t
    

    def displayHeaders(self):
        if not self.useHdrs:
            return ''
                
        t = ''
        
        if not self.checkbuttonTwoLineHeader.get_active():
            hdrs = [('%s (%s)' % (h[0],h[1])) for h in self.hdrs]
            hdrs = [h.rjust(max(len(h),self.defaultTab), ' ') for h in hdrs]
            self.hdrTabs = []
            for h in hdrs:
                t += h + ' '
                self.hdrTabs.extend([len(h)])
            return t + '\n' + ('-' * len(t)) + '\n'
        
        hdrs0 = []
        hdrs1 = []
        for h in self.hdrs:
            w = max(len(h[0]), len(h[1]), self.defaultTab)
            hdrs0 += [h[0].rjust(w, ' ')]
            hdrs1 += [h[1].rjust(w, ' ')]
            
        self.hdrTabs = []
        for h in hdrs0:
            t += h + ' '
            self.hdrTabs.extend([len(h)])
        w = len(t)
        t += '\n'
        for h in hdrs1:
            t += h + ' '
        return t + '\n' + ('-' * w) + '\n'
        
        
        
    def dataFormattedForSaving(self):
        t = self.csvHeaders()
        for line in self.colDataMapped:
            t = t + ','.join(map(str, line)) + '\n'
        return t
    
    
    def dataFormattedForDisplay(self):
        t = self.displayHeaders()
        
        if len(self.colDataMapped) == 1:
            d = list(zip(self.colDataMapped[0]))
        else:
            d = list(zip(*self.colDataMapped))

        for r,rowData in enumerate(d):
            for c,v in enumerate(rowData):
                if self.useHdrs:
                    t = t + str(v).rjust(self.hdrTabs[c], ' ') + ' '
                else:
                    t = t + str(v).rjust(self.defaultTab, ' ') + ' '
            t = t + '\n'
                    
        return t
    
    
    def refreshTextView(self):
        if len(self.data) == 0:
            self.textviewBuffer.set_text("")
            return
        
        self.getSensorHeaders()
        
        nCols = self.spinbuttonColumns.get_value_as_int()
        if nCols == 1:
            self.colDataRaw = [self.data]
        else:
            self.colDataRaw = list(self.data[i::nCols] for i in range(nCols))
        self.calibrateData()
        self.textviewBuffer.set_text(self.dataFormattedForDisplay())
        
        self.graphUpdateRequired = True
        self.refreshGraph()
        
    
    def refreshGraph(self):
        if not (self.graphVisible and self.graphUpdateRequired): return
        
        if self.graphContainer == None:
            self.graphContainer = self.gui.get_object("dataGraphContainer")
            if self.graphContainer == None: return
            r = self.graphContainer.get_allocation()
            self.graphWidth, self.graphHeight = (r.width,r.height)
            self.graph = None
            
        data = {}
        for c,t in enumerate(self.colDataMapped):
            lbl = '%(colNum)i-%(name)s (%(units)s)' % \
                {'colNum': c, 'name': self.hdrs[c][0], 'units': self.hdrs[c][1]}
            data[lbl] = t
        
        self.drawGraph(data,[str(x) for x in range(len(self.colDataMapped[0]))])
        self.graphUpdateRequired = False
        

    def drawGraph(self, data=[], xLabels=[]):
        if data == {}: return
        
        if self.graph != None:
            self.graphContainer.remove(self.graph.handler)
        
        self.graph = plots.DotLinePlot('Gtk', data=data, x_labels=xLabels,
                width=self.graphWidth, height=self.graphHeight, background="white",
                border=5, axis=True, grid=True, series_legend = True)
        
        self.graphContainer.add(self.graph.handler)
        self.graph.handler.show()
        
        
    def uploadProgress_cb(self, count, total):
        self.progressbar.set_fraction(float(count) / total)
        self.lblProgress.set_text(_('%i Values Uploaded' % count))
        while Gtk.events_pending():
            Gtk.main_iteration(False)
    
