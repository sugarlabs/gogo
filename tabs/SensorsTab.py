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

from gettext import gettext as _

try:
    from gi.repository import Gtk
except ImportError:
    #print _('GTK+ Runtime Enviromnt precisa ser instalado:')
    print((_('GTK+ Runtime Enviroment needs to be installed:')))
    print("http://downloads.sourceforge.net/gladewin32/Gtk-2.12.9-win32-1.exe?modtime=1208401479&big_mirror=0")

from configparser import ConfigParser
import pickle
from .Tab import Tab


from cairoplot import plots


# import matplotlib
# from matplotlib.figure import Figure
# from matplotlib.backends.backend_Gtk import FigureCanvasGTK as FigureCanvas
# matplotlib.use('Cairo')
# from pylab import *
# from numpy import arange, sin, pi



SENSOR_TYPES_FILENAME="sensors/sensorTypes.dat"
#GRAPHIC_FILENAME="sensors/graphic.png"

class SensorsTab(Tab):

    def __init__(self,gui,liststore):
        self.gui = gui
        self.liststore = liststore
        
        try:
            self.sensorsFile = open(SENSOR_TYPES_FILENAME,"r")
            try:
                self.sensorTypes = pickle.load(self.sensorsFile)
            except:
                #print _("Arquivo de configuração de sensores corrompido ou vazio.")
                print((_("Sensor configuration file corrupted or empty.")))
                self.sensorTypes = []
                self.create_default_sensor()
            self.sensorsFile.close()
        except:
            #print _("Arquivo de configuração de sensores não existe.")
            print((_("Sensor configuration file does not exist.")))
            self.sensorTypes=[]
            self.create_default_sensor()
        
        self.labelSensorNameUnits    = self.gui.get_object("labelSensorNameUnits")
        self.labelSensorDescription = self.gui.get_object("labelSensorDescription")
        
        #self.vboxGraphic=self.gui.get_object("vboxGraphic")
        #f = Figure(figsize=(5,4), dpi=100)
        #self.ax= f.add_subplot(111)
        #t = arange(0.0,3.0,0.01)
        #s = sin(2*pi*t)
        #self.ax.plot(t,s)
        #canvas = FigureCanvas(f)
        #self.vboxGraphic.add(canvas)
        #self.drawingareaGraphic=self.gui.get_object("drawingareaGraphic")
            
        self.treeviewSensors=self.gui.get_object("treeviewSensors")
        
        for sensor in self.sensorTypes:
            self.liststore.append([sensor.name,sensor.unit,sensor.description])
                
        #self.treemodelsort = Gtk.TreeModelSort(self.liststore)
        #self.treemodelsort.set_sort_column_id(0, Gtk.SORT_ASCENDING)
        #self.treeviewSensors.set_model(self.treemodelsort)
        self.treeviewSensors.set_model(self.liststore)
        
        cellrendererName        = Gtk.CellRendererText()
        cellrendererUnit        = Gtk.CellRendererText()
        cellrendererDescription = Gtk.CellRendererText()
        
        cellrendererName.set_property('editable', True)        
        cellrendererUnit.set_property('editable', True)
        cellrendererDescription.set_property('editable', True)
        
        cellrendererName.connect('edited', self.treeviewSensors_edited_cb,0)
        cellrendererUnit.connect('edited', self.treeviewSensors_edited_cb,1)
        cellrendererDescription.connect('edited', self.treeviewSensors_edited_cb,2)
        
        columnName          = Gtk.TreeViewColumn(_("Name"), cellrendererName)
        columnUnit          = Gtk.TreeViewColumn(_("Unit"), cellrendererUnit)
        columnDescription   = Gtk.TreeViewColumn(_("Description"), cellrendererDescription)
        
        columnName.add_attribute(cellrendererName,"text",0)
        columnUnit.add_attribute(cellrendererUnit,"text",1)
        columnDescription.add_attribute(cellrendererDescription,"text",2)
        
        self.treeviewSensors.append_column(columnName)
        self.treeviewSensors.append_column(columnUnit)
        self.treeviewSensors.append_column(columnDescription)
        
        # Sensor Points:
        self.treeviewSensorPoints = self.gui.get_object("treeviewSensorPoints")
        self.liststoreSensors = Gtk.ListStore(str,str)        
        self.treeviewSensorPoints.set_model(self.liststoreSensors)
        cellrendererX = Gtk.CellRendererText()
        cellrendererY = Gtk.CellRendererText()
        cellrendererX.set_property('editable', True)
        cellrendererY.set_property('editable', True)
        cellrendererX.connect('edited', self.sensorPoint_edited_cb,0)
        cellrendererY.connect('edited', self.sensorPoint_edited_cb,1)
        columnX = Gtk.TreeViewColumn(_("X"), cellrendererX)
        columnY = Gtk.TreeViewColumn(_("Y"), cellrendererY)
        columnX.set_expand(True)
        columnY.set_expand(True)
        columnX.add_attribute(cellrendererX,"text",0)
        columnY.add_attribute(cellrendererY,"text",1)
        self.treeviewSensorPoints.append_column(columnX)
        self.treeviewSensorPoints.append_column(columnY)
        
        self.graphContainer = None
        self.graphWidth  = 50
        self.graphHeight = 50
        self.graphData = None
        self.graph = None
        
        
    def create_default_sensor(self):        
        self.sensorTypes.append(SensorType(_("Standard"),"None","Raw values",[[0,0.0],[1023,1023.0]]))
        self.writeSensorsConfig()
    
    def writeSensorsConfig(self):
        self.sensorsFile=open(SENSOR_TYPES_FILENAME,"wb")
        pickle.dump(self.sensorTypes,self.sensorsFile)
        self.sensorsFile.close()
    
    ### SensorLab Callbacks
    def sensorPoint_edited_cb(self,cell, path, new_text, column):
        treemodel,treeiter = self.treeviewSensors.get_selection().get_selected()
        if treeiter:
            sensorNumber = int(treemodel.get_path(treeiter)[0])
            pointNumber  = int(path)
            if column == 0:
                if int(new_text)<0 or int(new_text)>1023:
                    #print _("O valor lido pelo sensor deve estar entre 0 e 1023")
                    print((_("The light value should be between 0 and 1023")))
                    return
                if ([int(new_text),float(self.sensorTypes[sensorNumber].points[pointNumber][1])]) in self.sensorTypes[sensorNumber].points:
                    #print _("O ponto já existe.")
                    print((_("Point already exists.")))
                    return
                #self.sensorTypes[sensorNumber].points[pointNumber][column]=int(new_text)
                self.sensorTypes[sensorNumber].edit_point(pointNumber,0,int(new_text))
                    
            if column == 1:
                if ([self.sensorTypes[sensorNumber].points[pointNumber][0],float(new_text)]) in self.sensorTypes[sensorNumber].points:
                    #print _("O ponto já existe.")
                    print((_("Point already exists!")))
                    return
                self.sensorTypes[sensorNumber].edit_point(pointNumber,1,float(new_text))
            
            self.liststoreSensors[path][column] = new_text
            
            self.writeSensorsConfig()
            
            
    def treeviewSensors_edited_cb(self,cell, path, new_text, column):
        #path=self.treemodelsort.convert_child_path_to_path(path)
        self.liststore[path][column] = new_text
        if column == 0:
            self.sensorTypes[int(path[0])].name=new_text
        elif column == 1:
            self.sensorTypes[int(path[0])].unit=new_text
        elif column == 2:
            self.sensorTypes[int(path[0])].description=new_text
        self.writeSensorsConfig()
        
            
    def treeviewSensors_cursor_changed_cb(self,treeviewSensors):
        self.liststoreSensors.clear()
        treemodel,treeiter = treeviewSensors.get_selection().get_selected()
        if treeiter == None:
            return
        
        lbl = _('<b>Sensor Points: </b>%(name)s (%(units)s)')
        sensorName  = treemodel.get_value(treeiter,0)
        sensorUnits = treemodel.get_value(treeiter,1)
        if sensorUnits == '':
            sensorUnits = _('raw')
        self.labelSensorNameUnits.set_markup(lbl % {'name':sensorName, 'units':sensorUnits})
        #self.labelSensorName.set_text(treemodel.get_value(treeiter,0))
        #self.labelSensorUnit.set_text(treemodel.get_value(treeiter,1))
        self.labelSensorDescription.set_text(treemodel.get_value(treeiter,2))
        
        path = treemodel.get_path(treeiter)
        #sensorNumber=int(self.treemodelsort.convert_child_path_to_path(path)[0])
        sensorNumber = path[0]
        points = self.sensorTypes[sensorNumber].points
        
        for point in points:
            self.liststoreSensors.append([str(point[0]),str(point[1])])
        self.refreshGraph()
    
    
    def buttonAddSensor_clicked_cb(self,widget):
        #self.liststore.append([_("Nome"), _("Unidade"), _("Descrição")])
        self.liststore.append([_("Name"), _("Unit"), _("Description")])
        #self.sensorTypes.append(SensorType(_("Nome"), _("Unidade"), _("Descrição"),[[0,0],[1023,1023]]))
        self.sensorTypes.append(SensorType(_("Name"), _("Unit"), _("Description"),[[0,0],[1023,1023]]))
        self.writeSensorsConfig()
        
        
    def buttonRemoveSensor_clicked_cb(self,widget):
        treemodel,treeiter = self.treeviewSensors.get_selection().get_selected()
        if treeiter:
            self.liststoreSensors.clear()
            self.sensorTypes.pop(int(treemodel.get_path(treeiter)[0]))
            treemodel.remove(treeiter)
            self.writeSensorsConfig()
        self.refreshGraph()
    
    
    def buttonImportSensors_clicked_cb(self,widget):
        #dialog = Gtk.FileChooserDialog(_("Abrir.."), None, Gtk.FILE_CHOOSER_ACTION_OPEN,
        dialog = Gtk.FileChooserDialog(_("Open.."), None, Gtk.FILE_CHOOSER_ACTION_OPEN,
        (Gtk.STOCK_CANCEL,Gtk.RESPONSE_CANCEL,Gtk.STOCK_OPEN, Gtk.RESPONSE_OK))        
        dialog.set_default_response(Gtk.RESPONSE_OK)
        dialog.set_current_folder(dialog.get_current_folder()+"/sensors/")
        response = dialog.run()
        if response == Gtk.RESPONSE_OK:
            filename = dialog.get_filename()
            dialog.destroy()
            try:
                FILE = open(filename,"r")
            except Exception as e:
                self.showError(e.__str__())
                return
            
            filetype = filename.split('.')[-1].lower()
            if not (filetype in ['csv','sensor']):
                self.showError(_('Error: unrecognised file type: %s') % filename)
                return
            
            try:
                if filetype == 'sensor':
                    c = ConfigParser()
                    c.readfp(FILE)
                    name = c.get("SENSOR","name")
                    unit = c.get("SENSOR","unit")
                    description = c.get("SENSOR","description")
                    sensor = SensorType(name,unit,description,[])
                    
                    p = 0
                    while True:
                        try:
                            x = c.getint(  'POINT '+str(p), 'x')
                            y = c.getfloat('POINT '+str(p), 'y')
                            sensor.add_point([x,y])
                            p += 1
                        except:
                            break
                        
                else: # CSV
                    # Line 1: name, unit, description
                    name, unit, description = FILE.readline().replace('\r\n','').split(',')
                    sensor = SensorType(name,unit,description,[])
                    # Line 2: skip
                    FILE.readline()
                    # Line 3..<BLANK>: x,y
                    for line in FILE:
                        line = line.replace('\r\n','')
                        if line == '':
                            break
                        x,y = line.split(',')
                        sensor.add_point([int(x), float(y)])
                                                 
                self.liststore.append([name,unit,description])
                self.sensorTypes.append(sensor)
                self.writeSensorsConfig()
            
            except Exception as e:
                self.showError(e.__str__())
            
            FILE.close()
               
    
    def buttonExportSensors_clicked_cb(self,widget):
        treemodel,treeiter = self.treeviewSensors.get_selection().get_selected()
        if treeiter:
            sensorNumber = int(treemodel.get_path(treeiter)[0])
            
            #dialog = Gtk.FileChooserDialog(_("Salvar.."), None, Gtk.FILE_CHOOSER_ACTION_SAVE,
            dialog = Gtk.FileChooserDialog(_("Save.."), None, Gtk.FILE_CHOOSER_ACTION_SAVE,
            (Gtk.STOCK_CANCEL,Gtk.RESPONSE_CANCEL,Gtk.STOCK_SAVE, Gtk.RESPONSE_OK))        
            dialog.set_default_response(Gtk.RESPONSE_OK)
            dialog.set_current_folder(dialog.get_current_folder()+"/sensors/")
            dialog.set_current_name(self.sensorTypes[sensorNumber].name+".sensor")
            response = dialog.run()
            if response == Gtk.RESPONSE_OK:
                filename = dialog.get_filename()
                dialog.destroy()
                try:
                    FILE = open(filename,"w")
                    c=ConfigParser()
                    
                    for i in  range(len(self.sensorTypes[sensorNumber].points)-1,-1,-1):
                        c.add_section("POINT "+str(i))
                        c.set("POINT "+str(i),"x", self.sensorTypes[sensorNumber].points[i][0])
                        c.set("POINT "+str(i),"y", self.sensorTypes[sensorNumber].points[i][1])
                    
                    c.add_section("SENSOR")
                    c.set("SENSOR","name", self.sensorTypes[sensorNumber].name)
                    c.set("SENSOR","unit", self.sensorTypes[sensorNumber].unit)
                    c.set("SENSOR","description", self.sensorTypes[sensorNumber].description)
                    
                    c.write(FILE)
                    FILE.close()
                except Exception as e:
                    self.showError(e.__str__())
    
    
    def buttonExportSensorsCSV_clicked_cb(self,widget):
        treemodel,treeiter = self.treeviewSensors.get_selection().get_selected()
        if treeiter:
            sensorNumber = int(treemodel.get_path(treeiter)[0])
            
            #dialog = Gtk.FileChooserDialog(_("Salvar.."), None, Gtk.FILE_CHOOSER_ACTION_SAVE,
            dialog = Gtk.FileChooserDialog(_("Save.."), None, Gtk.FILE_CHOOSER_ACTION_SAVE,
            (Gtk.STOCK_CANCEL,Gtk.RESPONSE_CANCEL,Gtk.STOCK_SAVE, Gtk.RESPONSE_OK))        
            dialog.set_default_response(Gtk.RESPONSE_OK)
            dialog.set_current_folder(dialog.get_current_folder()+"/sensors/")
            dialog.set_current_name(self.sensorTypes[sensorNumber].name+".csv")
            response = dialog.run()
            if response == Gtk.RESPONSE_OK:
                filename = dialog.get_filename()
                dialog.destroy()
                try:
                    FILE = open(filename,"w")
                    FILE.writelines(','.join([
                                  self.sensorTypes[sensorNumber].name, 
                                  self.sensorTypes[sensorNumber].unit,
                                  self.sensorTypes[sensorNumber].description
                                  ]))
                    FILE.writelines('\r\nBegin Table\r\n')
                    for i in  range(len(self.sensorTypes[sensorNumber].points)):
                        FILE.writelines('%5i , %10.3f' % (
                                        self.sensorTypes[sensorNumber].points[i][0],
                                        self.sensorTypes[sensorNumber].points[i][1]
                                        ))
                        FILE.writelines('\r\n')
                    FILE.writelines('\r\nEnd Table\r\n')
                    FILE.close()
                except Exception as e:
                    self.showError(e.__str__())
            
            
    def buttonInsertPoint_clicked_cb(self,widget):
        treemodel,treeiter = self.treeviewSensors.get_selection().get_selected()
        
        if treeiter:
            sensorNumber = int(treemodel.get_path(treeiter)[0])
            z = len(self.sensorTypes[sensorNumber].points)            
            self.liststoreSensors.append([z,float(z)])            
            self.sensorTypes[sensorNumber].add_point([z,float(z)])
            #self.sensorTypes[sensorNumber].points.append([0,0])
            self.writeSensorsConfig()
    
    
    def buttonRemovePoint_clicked_cb(self,widget):
        treemodel,treeiter=self.treeviewSensors.get_selection().get_selected()
        
        if treeiter:
            sensorNumber = int(treemodel.get_path(treeiter)[0])            
            treemodelSensor,treeiterSensor=self.treeviewSensorPoints.get_selection().get_selected()
            if treeiterSensor:
                pointNumber = int(treemodelSensor.get_path(treeiterSensor)[0])
                
                if len(self.sensorTypes[sensorNumber].points)>2:
                    self.sensorTypes[sensorNumber].remove_point(pointNumber)                
                    treemodelSensor.remove(treeiterSensor)
                else:
                    #print _("São necessários ao menos 2 pontos.")
                    #print _("It takes at least two points!")
                    self.showInfo(_("At least two points required!"), self.gui.get_object('mainWindow'))
                self.writeSensorsConfig()
    
    
    def refreshGraph(self):
        treemodel,treeiter = self.treeviewSensors.get_selection().get_selected()
                
        if treeiter:
            sensorNumber = int(treemodel.get_path(treeiter)[0])
#            x = range(0.0, 1024.0, 1.0)
#            y = []
#            for i in x:
#                y += [self.sensorTypes[sensorNumber].get_new_value(i)]
#            self.graphTest(zip(x,y))
            
            self.drawGraph([tuple(v) for v in self.sensorTypes[sensorNumber].points])
        else:
            self.drawGraph([])
            
    
    def drawGraph(self, data=[]):
        if data == []: 
            if self.graph != None:
                self.graphContainer.remove(self.graph.handler)
            return
        
        if self.graphContainer == None:
            self.graphContainer = self.gui.get_object("sensorGraphContainer")
            if self.graphContainer == None: return
            r = self.graphContainer.get_allocation()
            self.graphWidth, self.graphHeight = (r.width,r.height)
            self.graph = None

        if self.graph != None:
            self.graphContainer.remove(self.graph.handler)

        self.graph = plots.ScatterPlot('Gtk', data=data,
                width=self.graphWidth, height=self.graphHeight, background="white",
                border=5, axis=True, grid=True, series_legend = False)
        
        self.graphContainer.add(self.graph.handler)
        self.graph.handler.show()
        
            
    
class SensorType(object):
    
    def __init__(self,name="",unit="",description="",points=[[0,0],[1023,1023]]):
        self.name = name
        self.unit = unit
        self.description = description
        self.points = points
        self.x = []
        self.y = []
        for i in points:
            self.x += [i[0]]
            self.y += [i[1]]        
#        self.tck = splrep(self.x,self.y,s=0,k=1) 
    
    
    def lagrange(self,x,i):
        s = 1.0
        for k in range(len(self.points)):
            if k != i:
                s *= float(x-self.points[k][0])
        for k in range(len(self.points)):
            if k != i:
                #print self.points[i][0],self.points[k][0]
                s /= float(self.points[i][0]-self.points[k][0])
        return s
    
    
    def get_new_value(self,x):
        s = 0
        for i in range(len(self.points)):
            s += self.points[i][1] * self.lagrange(x,i)
        return s
    
#    def get_new_value3(self,x):
#        print splev(x,self.tck,der=0)
#        return splev(x,self.tck,der=0)
    
    def add_point(self,point):
        self.points.append(point)
        
        self.x = []
        self.y = []
        p = self.points[:]
        p.sort()
        for i in p:
            self.x.append(i[0])
            self.y.append(i[1])
            
        kk = len(self.points)-1
        if kk > 3:
            kk = 3
        #print self.x,self.y
#        self.tck = splrep(self.x,self.y,s=0,k=kk)
        
    def remove_point(self,pointIndex):
        self.points.pop(pointIndex)
        
        self.x = []
        self.y = []
        p = self.points[:]
        p.sort()
        for i in p:
            self.x.append(i[0])
            self.y.append(i[1])
            
        kk = len(self.points)-1
        if kk > 3:
            kk = 3
        
        #print self.x,self.y
#        self.tck = splrep(self.x,self.y,s=0,k=kk)
    
    def edit_point(self,pointIndex,x_or_y,new_value):
        self.points[pointIndex][x_or_y]=new_value
        
        self.x = []
        self.y = []
        p = self.points[:]
        p.sort()
        for i in p:
            self.x.append(i[0])
            self.y.append(i[1])
            
        kk = len(self.points)-1
        if kk > 3:
            kk = 3
        
        #print self.x,self.y
#        self.tck = splrep(self.x,self.y,s=0,k=kk)
    
    def get_text(self,old_value):
        return "%.4f" % self.get_new_value(old_value) + str(self.unit)
        
    def get_points(self):
        for i in self.points:
            yield i
    
    def get_x(self,point):
        return self.points[point][0]
        
    def get_y(self,point):
        return self.points[point][1]
    
