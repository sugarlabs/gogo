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


try:
    from gi.repository import Gtk
except ImportError:
    #print _('GTK+ Runtime Enviromnt precisa ser instalado:')
    print((_('GTK+ Runtime Enviroment needs to be installed:')))
    print("http://downloads.sourceforge.net/gladewin32/Gtk-2.12.9-win32-1.exe?modtime=1208401479&big_mirror=0")
    
from .Tab import Tab

from pyLogoCompiler.Exceptions import *

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


class ProceduresTab(Tab):
    
    LAST_CODE_FILENAME='.last_code.txt'
    
    compilerMessages = []

    def __init__(self, gui, GoGo, statusbar, activity=None):    
        self.gui = gui
        self.GoGo = GoGo
        self.statusbar = statusbar
        self.activity = activity
        
        self.logoFilename = ""
        self.tvLogoProcedures = self.gui.get_object('textviewLogoProcedures')
        self.LogoProceduresBuffer = Gtk.TextBuffer()
        self.tvLogoProcedures.set_buffer(self.LogoProceduresBuffer)
        
        self.tvCompilerMessages = self.gui.get_object('textviewCompilerMessages')
        self.compilerMessagesBuffer = Gtk.TextBuffer()
        self.tvCompilerMessages.set_buffer(self.compilerMessagesBuffer)

        #if not self.activity:
        try:
            f=open(self.LAST_CODE_FILENAME,'r')
            self.LogoProceduresBuffer.set_text(f.read())
            f.close()
        except:
            pass
        
    def textviewLogoProcedures_insert_at_cursor_cb(self,widget,s):
        pass
        #print 'AAA',s
        
    def buttonNew_clicked_cb(self,widget):
        self.LogoProceduresBuffer.set_text("")
        self.logoFilename=""
        
    def buttonOpen_clicked_cb(self,widget):
        #dialog = Gtk.FileChooserDialog(_("Abrir.."), None, Gtk.FILE_CHOOSER_ACTION_OPEN,
        dialog = Gtk.FileChooserDialog(_("Open.."), None, Gtk.FILE_CHOOSER_ACTION_OPEN,
        (Gtk.STOCK_CANCEL,Gtk.RESPONSE_CANCEL,Gtk.STOCK_OPEN, Gtk.RESPONSE_OK))        
        dialog.set_default_response(Gtk.RESPONSE_OK)
        response = dialog.run()
        if response == Gtk.RESPONSE_OK:
            try:
                self.logoFilename = dialog.get_filename()
                FILE = open(self.logoFilename,"r")
                self.LogoProceduresBuffer.set_text(FILE.read())
                FILE.close()
            except Exception as e:
                self.showError(e.__str__())
        
        dialog.destroy()    
        
    def buttonSave_clicked_cb(self,widget):
#        if self.activity:
#            self.activity.save()
#            return
        
        if self.logoFilename=="":
            #dialog = Gtk.FileChooserDialog(_("Salvar.."), None, Gtk.FILE_CHOOSER_ACTION_SAVE,
            dialog = Gtk.FileChooserDialog(_("Save.."), None, Gtk.FILE_CHOOSER_ACTION_SAVE,
            (Gtk.STOCK_CANCEL,Gtk.RESPONSE_CANCEL,Gtk.STOCK_SAVE, Gtk.RESPONSE_OK))        
            dialog.set_default_response(Gtk.RESPONSE_OK)
            response = dialog.run()
            if response == Gtk.RESPONSE_OK:
                self.logoFilename = dialog.get_filename()        
            dialog.destroy()
        
        try:
            FILE = open(self.logoFilename,"w")
            FILE.write(self.LogoProceduresBuffer.get_text(self.LogoProceduresBuffer.get_start_iter(),self.LogoProceduresBuffer.get_end_iter()))
            FILE.close()
        except Exception as e:
            self.showError(e.__str__())
        
    def buttonSaveAs_clicked_cb(self,widget):
        #dialog = Gtk.FileChooserDialog(_("Salvar Como.."), None, Gtk.FILE_CHOOSER_ACTION_SAVE,
        dialog = Gtk.FileChooserDialog(_("Save As.."), None, Gtk.FILE_CHOOSER_ACTION_SAVE,
        (Gtk.STOCK_CANCEL,Gtk.RESPONSE_CANCEL,Gtk.STOCK_SAVE, Gtk.RESPONSE_OK))        
        dialog.set_default_response(Gtk.RESPONSE_OK)
        response = dialog.run()
        if response == Gtk.RESPONSE_OK:
            self.logoFilename = dialog.get_filename()
            dialog.destroy()
            try:
                FILE = open(self.logoFilename,"w")
                FILE.write(self.LogoProceduresBuffer.get_text(self.LogoProceduresBuffer.get_start_iter(),self.LogoProceduresBuffer.get_end_iter()))
                FILE.close()
            except Exception as e:
                self.showError(e.__str__())
        
    def buttonDownload_clicked_cb(self,widget):        
        try:
            if os.name=='nt':
                win32api.SetFileAttributes(self.LAST_CODE_FILENAME,win32con.FILE_ATTRIBUTE_NORMAL)
        except:
            pass
        
        text = self.LogoProceduresBuffer.get_text(self.LogoProceduresBuffer.get_start_iter(),self.LogoProceduresBuffer.get_end_iter())
        
#        if self.activity:
#            self.activity.save()
#        else:
        f = open(self.LAST_CODE_FILENAME,'w')
        f.write(text)
        f.close()
        try:
            if os.name=='nt':
                win32api.SetFileAttributes(self.LAST_CODE_FILENAME,win32con.FILE_ATTRIBUTE_HIDDEN)
        except:
            pass

        # DMOC: splitting next chunk into two distinct steps, "compiling" and "downloading",
        #       each with own exception handling (less brain ache ;-) )
        
        try: # COMPILE
            self.GoGo.compile(text, self.logCompilerMessages)
#        except UnknowSymbol:
#            #self.showError(_("Função ou variavel não definida sendo usada"))
#            self.showError(_("Undefined function or variable being used"))
#        except BracketError:
#            #self.showError(_("Erro nos colchetes"))
#            self.showError(_("Error in brackets"))
#        except BlockTooLong:
#            #self.showError(_("Bloco de codigos muito longo"))
#            self.showError(_("Block too long"))
#        except CodeTooLong:
#            #self.showError(_("Código muito longo."))
#            self.showError(_("Code too long"))
#        except TooManyGlobals:
#            #self.showError(_("Muitas vaiaveis sendo usadas"))
#            self.showError(_("Too many globals"))
#        except DuplicatedSymbol:
#            #self.showError(_("Multiplas declarações de funções ou variáveis"))
#            self.showError(_("Multiple declarations of functions or variables"))
#        except ParentesisError:
#            #self.showError(_("Erro nos parentesis"))
#            self.showError(_("Error in parentheses"))
#        except AttributeError as detail:
#            print "AttErr"
#            self.showError(detail.__str__())
#        except TypeError:
#            self.showError("Type Error (argh!)")
#        except SyntaxError as detail:
#            self.showError("Syntax Error: "+detail.__str__())
#            #pass
        except Exception as e:
            #self.showError(_("Error compiling"))
            self.logCompilerMessages('***END***')
            #self.showError(e.__str__())
            self.showError(_('Error/s: Check Messages'))
        else:
            if self.compilerMessages != []: # Unresolved symbols
                self.logCompilerMessages('***END***')
                self.showError(_('Error/s: Check Messages'))
            else:
                #self.showError("Erro no carregamento do código.",self.gui.get_object('mainWindow'))
                self.statusbar.push(0,_("Code successfully compiled."))
    
                try: # DOWNLOAD
                    self.GoGo.download()
                except ConnectionProblem:
                    self.showWarning(_("Check GoGo plugged in, turned on and connected"))
                except:
                    self.showError(_("Error communicating"))
                else:
                    self.showInfo(_("Code successfully downloaded."), self.gui.get_object('mainWindow'))
                    #self.statusbar.push(0,_("Code successfully downloaded."))
        
    
    def logCompilerMessages(self, msg, unresolvedSymbolError=False):
        if msg == '***BEGIN***':
            self.compilerMessages = []
            self.compilerMessagesBuffer.set_text("")
            return
        
        if msg == '***END***':
            if self.compilerMessages != []:
                self.compilerMessagesBuffer.set_text('\n'.join([m for m in self.compilerMessages]))
            return
            
        self.compilerMessages.append(msg)
    
    
