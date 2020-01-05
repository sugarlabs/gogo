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

try:
	from gi.repository import Gtk
except ImportError:
	#print _('GTK+ Runtime Enviromnt precisa ser instalado:')
	print((_('GTK+ Runtime Enviroment needs to be installed:')))
	print("http://downloads.sourceforge.net/gladewin32/Gtk-2.12.9-win32-1.exe?modtime=1208401479&big_mirror=0")
	eval(input())
	

class Tab(object):
	def __init__(self):
		pass
		
	def showDialog(self,text,dialog_type,parent):
		dialog = Gtk.MessageDialog(parent, Gtk.DIALOG_MODAL, dialog_type, Gtk.BUTTONS_OK, text)
		dialog.run()
		dialog.destroy()
	def showInfo(self,text,parent=None):
		self.showDialog(text,Gtk.MESSAGE_INFO,parent)
	def showWarning(self,text,parent=None):
		self.showDialog(text,Gtk.MESSAGE_WARNING,parent)
	def showError(self,text,parent=None):
		self.showDialog(text,Gtk.MESSAGE_ERROR,parent)
		
#Gtk.MESSAGE_INFO
#Gtk.MESSAGE_WARNING	
#Gtk.MESSAGE_QUESTION
#Gtk.MESSAGE_ERROR
