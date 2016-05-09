#!/usr/bin/python3 -B

import gi, sqlite3, tempfile
gi.require_version('Gtk', '3.0')
import locale
import gettext
import ctypes

from config import *
from gi.repository import Gtk, Gio, GLib, Gdk

domain = 'semafor'
if os.path.exists('/usr/share/semafor'):  # We are installed system-wide
    localedir = '/usr/share/locale'  # so we should use system locale dir
else:
    localedir = programdir + '/locale'  # developing locally

# Loading the correct translation under Windows is a bit trickier than on Linux
if os.name == "nt":
    # TODO: Implement proper language switcher
    # On Windows we will default to the Serbian Cyrillic translation until a proper
    # language switcher isn't implemented.
    os.environ['LANG'] = 'sr_RS'
    libintl = ctypes.cdll.LoadLibrary(programdir + "/libintl-8.dll")
    libintl.bindtextdomain(domain, localedir)
    libintl.bind_textdomain_codeset(domain, "UTF-8")
    locale.setlocale(locale.LC_ALL, '')
    gettext.bindtextdomain(domain, localedir)
    gettext.textdomain(domain)
    _ = gettext.gettext
else:  # We are running a sane OS such as Linux.
    locale.setlocale(locale.LC_ALL, '')
    locale.bindtextdomain(domain, localedir)
    gettext.bindtextdomain(domain, localedir)
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
        icon = Gio.ThemedIcon(name="media-playlist-shuffle-symbolic")
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
        fix_untranslated_glade_in_win(self.hbbuilder)

        # category selection window
        self.selwinbuilder = Gtk.Builder()
        self.selwinbuilder.set_translation_domain(domain)
        self.selwinbuilder.add_from_file(programdir + '/ui/categoryselection.ui')
        self.selectionwindow = self.selwinbuilder.get_object("categorybox1")
        fix_untranslated_glade_in_win(self.selwinbuilder)

        # Setup an image for every category button
        self.category_am_image = self.selwinbuilder.get_object("image1")
        self.category_am_image.set_from_file(programdir + '/icon/categories/category-am.png')
        self.category_a1_image = self.selwinbuilder.get_object("image2")
        self.category_a1_image.set_from_file(programdir + '/icon/categories/category-a1.png')
        self.category_a2_image = self.selwinbuilder.get_object("image3")
        self.category_a2_image.set_from_file(programdir + '/icon/categories/category-a2.png')
        self.category_a_image = self.selwinbuilder.get_object("image4")
        self.category_a_image.set_from_file(programdir + '/icon/categories/category-a.png')
        self.category_b1_image = self.selwinbuilder.get_object("image5")
        self.category_b1_image.set_from_file(programdir + '/icon/categories/category-b1.png')
        self.category_b_image = self.selwinbuilder.get_object("image6")
        self.category_b_image.set_from_file(programdir + '/icon/categories/category-b.png')
        self.category_be_image = self.selwinbuilder.get_object("image7")
        self.category_be_image.set_from_file(programdir + '/icon/categories/category-be.png')
        self.category_c1_image = self.selwinbuilder.get_object("image8")
        self.category_c1_image.set_from_file(programdir + '/icon/categories/category-c1.png')
        self.category_c1e_image = self.selwinbuilder.get_object("image9")
        self.category_c1e_image.set_from_file(programdir + '/icon/categories/category-c1e.png')
        self.category_c_image = self.selwinbuilder.get_object("image10")
        self.category_c_image.set_from_file(programdir + '/icon/categories/category-c.png')
        self.category_ce_image = self.selwinbuilder.get_object("image11")
        self.category_ce_image.set_from_file(programdir + '/icon/categories/category-ce.png')
        self.category_d1_image = self.selwinbuilder.get_object("image12")
        self.category_d1_image.set_from_file(programdir + '/icon/categories/category-d1.png')
        self.category_d1e_image = self.selwinbuilder.get_object("image13")
        self.category_d1e_image.set_from_file(programdir + '/icon/categories/category-d1e.png')
        self.category_d_image = self.selwinbuilder.get_object("image14")
        self.category_d_image.set_from_file(programdir + '/icon/categories/category-d.png')
        self.category_de_image = self.selwinbuilder.get_object("image15")
        self.category_de_image.set_from_file(programdir + '/icon/categories/category-de.png')
        self.category_f_image = self.selwinbuilder.get_object("image16")
        self.category_f_image.set_from_file(programdir + '/icon/categories/category-f.png')
        self.category_m_image = self.selwinbuilder.get_object("image17")
        self.category_m_image.set_from_file(programdir + '/icon/categories/category-m.png')
        self.add(self.selectionwindow)

        # part selection window with small string
        partselectionwindow = Gtk.Builder()
        partselectionwindow.set_translation_domain(domain)
        partselectionwindow.add_from_file(programdir + '/ui/partselection.ui')
        self.partwindow = partselectionwindow.get_object("partbox1")
        fix_untranslated_glade_in_win(partselectionwindow)

        # no database window
        nodbselectionwindow = Gtk.Builder()
        nodbselectionwindow.set_translation_domain(domain)
        nodbselectionwindow.add_from_file(programdir + '/ui/nodb.ui')
        self.nodbwindow = nodbselectionwindow.get_object("grid1")
        self.nodbimage = nodbselectionwindow.get_object("imagenodb")
        self.nodbimage.set_from_file(programdir + '/icon/no-db.png')
        fix_untranslated_glade_in_win(nodbselectionwindow)

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
        fix_untranslated_glade_in_win(self.questionbuilder)

def fix_untranslated_glade_in_win(gtkbuilder):
    #TODO: remove this when upstream fixes translations with Python3+Windows
    # https://github.com/tobias47n9e/pygobject-locale/issues/1
    if os.name == "nt": 
        for obj in gtkbuilder.get_objects(): 
            if (not isinstance(obj, Gtk.SeparatorMenuItem)) and hasattr(obj, "get_label"): 
                label = obj.get_label() 
                if label is not None: 
                    obj.set_label(_(label)) 
            elif hasattr(obj, "get_title"):
                title = obj.get_title() 
                if title is not None: 
                    obj.set_title(_(title)) 
            if hasattr(obj, "get_tooltip_text"): 
                text = obj.get_tooltip_text() 
                if text is not None: 
                    obj.set_tooltip_text(_(text))
