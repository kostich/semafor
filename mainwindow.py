#!/usr/bin/python3 -B

import gi, sqlite3, tempfile
gi.require_version('Gtk', '3.0')
import locale
import gettext

from config import *
from gi.repository import Gtk, Gio, GLib, Gdk

domain = 'semafor'
gettextdir = 'locale'
localedir = programdir + '/' + gettextdir

locale.setlocale(locale.LC_ALL, '')
locale.bindtextdomain(domain, localedir)
gettext.bindtextdomain(domain, gettextdir)
gettext.textdomain(domain)
_ = gettext.gettext

class MainWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.Window.__init__(self, title=_('Category choosing'), application=app)
        self.set_default_size(800, 575)
        self.set_icon_from_file(programdir + '/icon/icon.png')
        self.set_wmclass(_('Semafor'), _('Semafor'))

        # headerbar
        self.hbbuilder = Gtk.Builder()
        self.hbbuilder.set_translation_domain(domain)
        self.hbbuilder.add_from_file(programdir + '/ui/headerbar.ui')
        self.hb = self.hbbuilder.get_object("programheaderbar")
        self.set_titlebar(self.hb)

        self.partbutton = self.hbbuilder.get_object("menu")
        icon = Gio.ThemedIcon(name="open-menu-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.partbutton.add(image)

        self.randombutton = self.hbbuilder.get_object("random")
        icon = Gio.ThemedIcon(name="media-playlist-shuffle-symbolic.symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.randombutton.add(image)

        self.menumodel = Gio.Menu()
        self.partbutton.set_menu_model(self.menumodel)
        self.menumodel.append(_('The basics of the traffic safety and traffic terms'), "app.obsip")
        self.menumodel.append(_('Special regulations and permissions'), "app.pmio")
        self.menumodel.append(_('The consequences of the violation of traffic rules'), "app.pnp")
        self.menumodel.append(_('Traffic rules'), "app.ps")
        self.menumodel.append(_('Traffic signals'), "app.ss")
        self.menumodel.append(_('Drivers'), "app.vozaci")
        self.menumodel.append(_('Duties in the case of the traffic accident'), "app.dussn")
        self.menumodel.append(_('Driving period driver resting'), "app.vuiov")
        self.menumodel.append(_('Tachograph usage'), "app.nut")
        self.menumodel.append(_('Vehicles'), "app.vozila")
        self.menumodel.append(_('Vehicle technical conditions'), "app.tuzv")
        self.menumodel.append(_('Cargo and passenger transport'), "app.ptilv")
        self.menumodel.append(_('Category choosing'), "app.categoryselect")

        self.arrowbox = self.hbbuilder.get_object("arrowbox")
        Gtk.StyleContext.add_class(self.arrowbox.get_style_context(), "linked")

        self.leftarrow = self.hbbuilder.get_object("leftarrow")
        self.leftarrow.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))

        self.rightarrow = self.hbbuilder.get_object("rightarrow")
        self.rightarrow.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))

        # category selection window
        self.selwinbuilder = Gtk.Builder()
        self.selwinbuilder.set_translation_domain(domain)
        self.selwinbuilder.add_from_file(programdir + '/ui/categoryselection.ui')
        self.selectionwindow = self.selwinbuilder.get_object("categorybox1")
        self.add(self.selectionwindow)

        # part selection window with small string
        partselectionwindow = Gtk.Builder()
        partselectionwindow.set_translation_domain(domain)
        partselectionwindow.add_from_file(programdir + '/ui/partselection.ui')
        self.partwindow = partselectionwindow.get_object("partbox1")

        # no database window
        nodbselectionwindow = Gtk.Builder()
        nodbselectionwindow.set_translation_domain(domain)
        nodbselectionwindow.add_from_file(programdir + '/ui/nodb.ui')
        self.nodbwindow = nodbselectionwindow.get_object("grid1")
        self.nodbimage = nodbselectionwindow.get_object("imagenodb")
        self.nodbimage.set_from_file(programdir + '/icon/no-db.png')

        # question window
        self.questionbuilder = Gtk.Builder()
        self.questionbuilder.set_translation_domain(domain)
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
