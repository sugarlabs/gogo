# GoGoActivity/GoGoActivity.py

import os
import gtk
import time
import logging

from gettext import gettext as _

from sugar.activity import activity

from monitor import BoardMonitor


from power import power

def runningOnXO():
    return (os.uname()[2]).find("olpc") != -1
    

_logger = logging.getLogger('read-activity')



class GoGoActivity(activity.Activity):
    """GoGo Activity"""
    
    APM = None # Automatic Power Management
    
    def __init__(self, handle):
        """Set up the GoGo activity."""
        
        activity.Activity.__init__(self, handle)
        self.set_title(_('GoGo'))
        logging.info(_('GoGo'))
        
        # Show the toolbox elements
        toolbox = activity.ActivityToolbox(self)
        self.set_toolbox(toolbox)
        toolbox.show()

        self.monitor = BoardMonitor(self)
        
        # Display everything
        vb = gtk.VBox()
        self.monitor.notebookMain.reparent(vb)
        self.monitor.statusbar.reparent(vb)
        self.set_canvas(vb)
        self.show_all()
    
        if runningOnXO():
            try:
                self.APM = power.get_automatic_pm()
                power.set_automatic_pm(False)
            except:
                pass
        
    def can_close(self):
        if runningOnXO():
            if self.APM != None:
                try:
                    power.set_automatic_pm(self.APM)
                except:
                    pass
        return True
    
        
    def read_file(self, file_path):
        """Load a file from the datastore on activity start."""
        _logger.debug('GoGoActivity.read_file: %s', file_path)

        try:
            FILE = open(file_path,"r")
            self.monitor.proceduresTab.LogoProceduresBuffer.set_text(FILE.read())
            FILE.close()
        except Exception, e:
            _logger.error('read_file(): %s, error: %s', file_path, e)

    def write_file(self, file_path):
        _logger.debug('GoGoActivity.write_file: %s', file_path)
        
        try:
            FILE = open(file_path,"w")
            FILE.write(self.monitor.proceduresTab.LogoProceduresBuffer.get_text(self.LogoProceduresBuffer.get_start_iter(),self.LogoProceduresBuffer.get_end_iter()))
            FILE.close()
        except Exception, e:
            _logger.error('write_file(): %s, error: %s', file_path, e)
        

