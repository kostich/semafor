#!/usr/bin/python3 -B

import gi, sqlite3, tempfile
gi.require_version('Gtk', '3.0')
from config import *
from gi.repository import Gtk, Gio, GLib, Gdk

class MainWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.Window.__init__(self, title="Бирање категорије", application=app)
        self.set_default_size(800, 575)
        self.set_icon_from_file(programdir + '/icon/icon.png')
        self.set_wmclass("Семафор", "Семафор")

        # headerbar
        self.hbbuilder = Gtk.Builder()
        self.hbbuilder.add_from_file(programdir + '/ui/headerbar.ui')
        self.hb = self.hbbuilder.get_object("programheaderbar")
        self.set_titlebar(self.hb)

        self.partbutton = self.hbbuilder.get_object("menu")
        icon = Gio.ThemedIcon(name="open-menu-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.partbutton.add(image)

        self.menumodel = Gio.Menu()
        self.partbutton.set_menu_model(self.menumodel)
        self.menumodel.append("Основе безбедности саобраћаја и појмови", "app.obsip")
        self.menumodel.append("Посебне мере и овлашћења", "app.pmio")
        self.menumodel.append("Последице непоштовања прописа", "app.pnp")
        self.menumodel.append("Правила саобраћаја", "app.ps")
        self.menumodel.append("Саобраћајна сигнализација", "app.ss")
        self.menumodel.append("Возачи", "app.vozaci")
        self.menumodel.append("Дужности у случају саобраћајне незгоде", "app.dussn")
        self.menumodel.append("Време управљања и одмори возача", "app.vuiov")
        self.menumodel.append("Начин употребе тахографа", "app.nut")
        self.menumodel.append("Возила", "app.vozila")
        self.menumodel.append("Технички услови за возила", "app.tuzv")
        self.menumodel.append("Превоз терета и лица возилима", "app.ptilv")
        self.menumodel.append("Бирање категорије", "app.categoryselect")

        self.arrowbox = self.hbbuilder.get_object("arrowbox")
        Gtk.StyleContext.add_class(self.arrowbox.get_style_context(), "linked")

        self.leftarrow = self.hbbuilder.get_object("leftarrow")
        self.leftarrow.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))

        self.rightarrow = self.hbbuilder.get_object("rightarrow")
        self.rightarrow.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))

        # category selection window
        self.selwinbuilder = Gtk.Builder()
        self.selwinbuilder.add_from_file(programdir + '/ui/categoryselection.ui')
        self.selectionwindow = self.selwinbuilder.get_object("categorybox1")
        self.add(self.selectionwindow)

        # part selectin window with small string
        partselectionwindow = Gtk.Builder()
        partselectionwindow.add_from_file(programdir + '/ui/partselection.ui')
        self.partwindow = partselectionwindow.get_object("partbox1")

        # question window
        self.questionbuilder = Gtk.Builder()
        self.questionbuilder.add_from_file(programdir + '/ui/questionwindow.ui')
        self.questionwindow = self.questionbuilder.get_object("scrolledwindow1")
        self.question = self.questionbuilder.get_object("question")
        self.picturegrid = self.questionbuilder.get_object("picturegrid")
        # Part where we set the variables containing images and solutions
        # has been moved into the loadquestion function so we could rearange
        # those elements depending on the number of images in the question.
        # This part is beneath the "Reflow the images" comment.
        self.answer1 = self.questionbuilder.get_object("answer1")
        self.label1 = self.questionbuilder.get_object("label1")
        self.answer2 = self.questionbuilder.get_object("answer2")
        self.label2 = self.questionbuilder.get_object("label2")
        self.answer3 = self.questionbuilder.get_object("answer3")
        self.label3 = self.questionbuilder.get_object("label3")
        self.answer4 = self.questionbuilder.get_object("answer4")
        self.label4 = self.questionbuilder.get_object("label4")
        self.answer5 = self.questionbuilder.get_object("answer5")
        self.label5 = self.questionbuilder.get_object("label5")
        self.answer6 = self.questionbuilder.get_object("answer6")
        self.label6 = self.questionbuilder.get_object("label6")
