#!/usr/bin/python3 -B

import signal
import gi
gi.require_version('Gtk', '3.0')
import mainwindow

from gi.repository import Gtk, Gio
from loadquestion import *
from random import randint

currentobsip = 0
currentpmio = 0
currentpnp = 0
currentps = 0
currentss = 0
currentvozaci = 0
currentdussn = 0
currentvuiov = 0
currentnut = 0
currentvozila = 0
currenttuzv = 0
currentptilv = 0
category = ""
part = ""


class Semafor(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        self.win = mainwindow.MainWindow(self)
        self.app = app
        # set appmenu
        builder = Gtk.Builder()
        builder.add_from_file(programdir + '/ui/appmenu.ui')
        self.app.set_app_menu(builder.get_object("app-menu"))

        # handlers for buttons on category selection window
        handlersselwin = {
            "on_category_activate": self.buttoncategory_pressed
        }
        self.win.selwinbuilder.connect_signals(handlersselwin)

        # handlers for arrows in headerbar
        handlersquestions = {
            "on_leftarrow_clicked": self.previousquestion,
            "on_rightarrow_clicked": self.nextquestion,
            "on_random_toggled": self.random_toggled
        }
        self.win.hbbuilder.connect_signals(handlersquestions)

        # handlers for answer checkbuttons in questionwindow
        handlersanswers = {
            "on_answer1_toggled": self.check_answer1,
            "on_answer2_toggled": self.check_answer2,
            "on_answer3_toggled": self.check_answer3,
            "on_answer4_toggled": self.check_answer4,
            "on_answer5_toggled": self.check_answer5,
            "on_answer6_toggled": self.check_answer6
        }
        self.win.questionbuilder.connect_signals(handlersanswers)

        self.win.show_all()
        self.win.arrowbox.hide()
        self.win.randombutton.hide()

    def do_startup(self):
        Gtk.Application.do_startup(self)

        # connect all the menu items with functions

        self.obsip_action = Gio.SimpleAction.new("obsip", None)
        self.obsip_action.connect("activate", self.obsip_callback)
        self.add_action(self.obsip_action)

        self.pmio_action = Gio.SimpleAction.new("pmio", None)
        self.pmio_action.connect("activate", self.pmio_callback)
        self.add_action(self.pmio_action)

        self.pnp_action = Gio.SimpleAction.new("pnp", None)
        self.pnp_action.connect("activate", self.pnp_callback)
        self.add_action(self.pnp_action)

        self.ps_action = Gio.SimpleAction.new("ps", None)
        self.ps_action.connect("activate", self.ps_callback)
        self.add_action(self.ps_action)

        self.ss_action = Gio.SimpleAction.new("ss", None)
        self.ss_action.connect("activate", self.ss_callback)
        self.add_action(self.ss_action)

        self.vozaci_action = Gio.SimpleAction.new("vozaci", None)
        self.vozaci_action.connect("activate", self.vozaci_callback)
        self.add_action(self.vozaci_action)

        self.dussn_action = Gio.SimpleAction.new("dussn", None)
        self.dussn_action.connect("activate", self.dussn_callback)
        self.add_action(self.dussn_action)

        self.vuiov_action = Gio.SimpleAction.new("vuiov", None)
        self.vuiov_action.connect("activate", self.vuiov_callback)
        self.add_action(self.vuiov_action)

        self.nut_action = Gio.SimpleAction.new("nut", None)
        self.nut_action.connect("activate", self.nut_callback)
        self.add_action(self.nut_action)

        self.vozila_action = Gio.SimpleAction.new("vozila", None)
        self.vozila_action.connect("activate", self.vozila_callback)
        self.add_action(self.vozila_action)

        self.tuzv_action = Gio.SimpleAction.new("tuzv", None)
        self.tuzv_action.connect("activate", self.tuzv_callback)
        self.add_action(self.tuzv_action)

        self.ptilv_action = Gio.SimpleAction.new("ptilv", None)
        self.ptilv_action.connect("activate", self.ptilv_callback)
        self.add_action(self.ptilv_action)

        self.categoryselect_action = Gio.SimpleAction.new("categoryselect", None)
        self.categoryselect_action.connect("activate", self.categoryselect_callback)
        self.add_action(self.categoryselect_action)

        self.menu_enabled(False)  # gray out menu button

        # Cannot use add_action_entries()
        # see https://bugzilla.gnome.org/show_bug.cgi?id=678655

        action = Gio.SimpleAction(name="quit")
        action.connect("activate", lambda a, b: self.quit())
        self.add_action(action)

        # fullscreen_action = Gio.SimpleAction.new("fullscreen", None)
        # fullscreen_action.connect("activate", self.change_fullscreen_state)
        # self.add_action(fullscreen_action)

        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.about_callback)
        self.add_action(about_action)

    def buttoncategory_pressed(self, listbox, listboxrow):
        pressed = listboxrow.get_index()
        global category

        if pressed == 0:
            self.win.remove(self.win.selectionwindow)
            self.win.add(self.win.partwindow)
            self.win.hb.props.title = "Семафор - AM"
            self.win.hb.props.subtitle = "Бирање области"
            self.menu_enabled(True)
            self.win.set_focus(self.win.rightarrow)
            category = "am"
        elif pressed == 1:
            self.win.remove(self.win.selectionwindow)
            self.win.add(self.win.partwindow)
            self.win.hb.props.title = "Семафор - A1"
            self.win.hb.props.subtitle = "Бирање области"
            self.menu_enabled(True)
            self.win.set_focus(self.win.rightarrow)
            category = "a1"
        elif pressed == 2:
            self.win.remove(self.win.selectionwindow)
            self.win.add(self.win.partwindow)
            self.win.hb.props.title = "Семафор - A2"
            self.win.hb.props.subtitle = "Бирање области"
            self.menu_enabled(True)
            self.win.set_focus(self.win.rightarrow)
            category = "a2"
        elif pressed == 3:
            self.win.remove(self.win.selectionwindow)
            self.win.add(self.win.partwindow)
            self.win.hb.props.title = "Семафор - A"
            self.win.hb.props.subtitle = "Бирање области"
            self.menu_enabled(True)
            self.win.set_focus(self.win.rightarrow)
            category = "a"
        elif pressed == 4:
            self.win.remove(self.win.selectionwindow)
            self.win.add(self.win.partwindow)
            self.win.hb.props.title = "Семафор - B1"
            self.win.hb.props.subtitle = "Бирање области"
            self.menu_enabled(True)
            self.win.set_focus(self.win.rightarrow)
            category = "b1"
        elif pressed == 5:
            self.win.remove(self.win.selectionwindow)
            self.win.add(self.win.partwindow)
            self.win.hb.props.title = "Семафор - B"
            self.win.hb.props.subtitle = "Бирање области"
            self.menu_enabled(True)
            self.win.set_focus(self.win.rightarrow)
            category = "b"
        elif pressed == 6:
            self.win.remove(self.win.selectionwindow)
            self.win.add(self.win.partwindow)
            self.win.hb.props.title = "Семафор - BE"
            self.win.hb.props.subtitle = "Бирање области"
            self.menu_enabled(True)
            self.win.set_focus(self.win.rightarrow)
            category = "be"
        elif pressed == 7:
            self.win.remove(self.win.selectionwindow)
            self.win.add(self.win.partwindow)
            self.win.hb.props.title = "Семафор - C1"
            self.win.hb.props.subtitle = "Бирање области"
            self.menu_enabled(True)
            self.win.set_focus(self.win.rightarrow)
            category = "c1"
        elif pressed == 8:
            self.win.remove(self.win.selectionwindow)
            self.win.add(self.win.partwindow)
            self.win.hb.props.title = "Семафор - C1E"
            self.win.hb.props.subtitle = "Бирање области"
            self.menu_enabled(True)
            self.win.set_focus(self.win.rightarrow)
            category = "c1e"
        elif pressed == 9:
            self.win.remove(self.win.selectionwindow)
            self.win.add(self.win.partwindow)
            self.win.hb.props.title = "Семафор - C"
            self.win.hb.props.subtitle = "Бирање области"
            self.menu_enabled(True)
            self.win.set_focus(self.win.rightarrow)
            category = "c"
        elif pressed == 10:
            self.win.remove(self.win.selectionwindow)
            self.win.add(self.win.partwindow)
            self.win.hb.props.title = "Семафор - CE"
            self.win.hb.props.subtitle = "Бирање области"
            self.menu_enabled(True)
            self.win.set_focus(self.win.rightarrow)
            category = "ce"
        elif pressed == 11:
            self.win.remove(self.win.selectionwindow)
            self.win.add(self.win.partwindow)
            self.win.hb.props.title = "Семафор - D1"
            self.win.hb.props.subtitle = "Бирање области"
            self.menu_enabled(True)
            self.win.set_focus(self.win.rightarrow)
            category = "d1"
        elif pressed == 12:
            self.win.remove(self.win.selectionwindow)
            self.win.add(self.win.partwindow)
            self.win.hb.props.title = "Семафор - D1E"
            self.win.hb.props.subtitle = "Бирање области"
            self.menu_enabled(True)
            self.win.set_focus(self.win.rightarrow)
            category = "d1e"
        elif pressed == 13:
            self.win.remove(self.win.selectionwindow)
            self.win.add(self.win.partwindow)
            self.win.hb.props.title = "Семафор - D"
            self.win.hb.props.subtitle = "Бирање области"
            self.menu_enabled(True)
            self.win.set_focus(self.win.rightarrow)
            category = "d"
        elif pressed == 14:
            self.win.remove(self.win.selectionwindow)
            self.win.add(self.win.partwindow)
            self.win.hb.props.title = "Семафор - DE"
            self.win.hb.props.subtitle = "Бирање области"
            self.menu_enabled(True)
            self.win.set_focus(self.win.rightarrow)
            category = "de"
        elif pressed == 15:
            self.win.remove(self.win.selectionwindow)
            self.win.add(self.win.partwindow)
            self.win.hb.props.title = "Семафор - F"
            self.win.hb.props.subtitle = "Бирање области"
            self.menu_enabled(True)
            self.win.set_focus(self.win.rightarrow)
            category = "f"
        elif pressed == 16:
            self.win.remove(self.win.selectionwindow)
            self.win.add(self.win.partwindow)
            self.win.hb.props.title = "Семафор - M"
            self.win.hb.props.subtitle = "Бирање области"
            self.menu_enabled(True)
            self.win.set_focus(self.win.rightarrow)
            category = "m"

    def menu_enabled(self, state):
        if state == True:
            self.obsip_action.set_enabled(True)
            self.pmio_action.set_enabled(True)
            self.pnp_action.set_enabled(True)
            self.ps_action.set_enabled(True)
            self.ss_action.set_enabled(True)
            self.vozaci_action.set_enabled(True)
            self.dussn_action.set_enabled(True)
            self.vuiov_action.set_enabled(True)
            self.nut_action.set_enabled(True)
            self.vozila_action.set_enabled(True)
            self.tuzv_action.set_enabled(True)
            self.ptilv_action.set_enabled(True)
            self.categoryselect_action.set_enabled(True)
        else:
            self.obsip_action.set_enabled(False)
            self.pmio_action.set_enabled(False)
            self.pnp_action.set_enabled(False)
            self.ps_action.set_enabled(False)
            self.ss_action.set_enabled(False)
            self.vozaci_action.set_enabled(False)
            self.dussn_action.set_enabled(False)
            self.vuiov_action.set_enabled(False)
            self.nut_action.set_enabled(False)
            self.vozila_action.set_enabled(False)
            self.tuzv_action.set_enabled(False)
            self.ptilv_action.set_enabled(False)
            self.categoryselect_action.set_enabled(False)

    def random_toggled(self, button):
        if self.win.randombutton.get_active() == True:
            self.win.leftarrow.set_sensitive(False)
            self.win.rightarrow.set_sensitive(True)
        else:
            currentps = 1
            currentss = 1
            currentnut = 1
            currentpnp = 1
            currentpmio = 1
            currenttuzv = 1
            currentdussn = 1
            currentobsip = 1
            currentptilv = 1
            currentvuiov = 1
            currentvozaci = 1
            currentvozila = 1

    def nextquestion(self, button):
        global currentobsip, currentpmio, currentpnp, currentps, currentss
        global currentvozaci, currentdussn, currentvuiov, currentnut
        global currentvozila, currenttuzv, currentptilv, category, part

        conn = sqlite3.connect(programdir + '/data.db')
        c = conn.cursor()

        query = 'SELECT `id` FROM ' + part + ' ORDER BY `id` DESC LIMIT 1;'
        c.execute(query)
        total = c.fetchone()[0]

        if part == "obsip":
            # if the random toggle is on, load a random question
            # if not, recalculate current question number for this part
            # and then load the question.
            # also check if we are on the first or last question and set
            # the left and right arrow accordingly
            if self.win.randombutton.get_active() == True:
                currentobsip = randint(1, total)
                loadquestion(str(currentobsip), part, self.win)
            else:
                if currentobsip <= total:
                    currentobsip = currentobsip + 1
                    loadquestion(str(currentobsip), part, self.win)
                if currentobsip >= 2 and currentobsip <= total:
                    self.win.leftarrow.set_sensitive(True)
                if currentobsip >= total:
                    self.win.rightarrow.set_sensitive(False)
        elif part == "pmio":
            if self.win.randombutton.get_active() == True:
                currentpmio = randint(1, total)
                loadquestion(str(currentpmio), part, self.win)
            else:
                if currentpmio <= total:
                    currentpmio = currentpmio + 1
                    loadquestion(str(currentpmio), part, self.win)
                if currentpmio >= 2 and currentpmio <= total:
                    self.win.leftarrow.set_sensitive(True)
                if currentpmio >= total:
                    self.win.rightarrow.set_sensitive(False)
        elif part == "pnp":
            if self.win.randombutton.get_active() == True:
                currentpnp = randint(1, total)
                loadquestion(str(currentpnp), part, self.win)
            else:
                if currentpnp <= total:
                    currentpnp = currentpnp + 1
                    loadquestion(str(currentpnp), part, self.win)
                if currentpnp >= 2 and currentpnp <= total:
                    self.win.leftarrow.set_sensitive(True)
                if currentpnp >= total:
                    self.win.rightarrow.set_sensitive(False)
        elif part == "ps":
            if self.win.randombutton.get_active() == True:
                currentps = randint(1, total)
                loadquestion(str(currentps), part, self.win)
            else:
                if currentps <= total:
                    currentps = currentps + 1
                    loadquestion(str(currentps), part, self.win)
                if currentps >= 2 and currentps <= total:
                    self.win.leftarrow.set_sensitive(True)
                if currentps >= total:
                    self.win.rightarrow.set_sensitive(False)
        elif part == "ss":
            if self.win.randombutton.get_active() == True:
                currentss = randint(1, total)
                loadquestion(str(currentss), part, self.win)
            else:
                if currentss <= total:
                    currentss = currentss + 1
                    loadquestion(str(currentss), part, self.win)
                if currentss >= 2 and currentss <= total:
                    self.win.leftarrow.set_sensitive(True)
                if currentss >= total:
                    self.win.rightarrow.set_sensitive(False)
        elif part == "vozaci":
            if self.win.randombutton.get_active() == True:
                currentvozaci = randint(1, total)
                loadquestion(str(currentvozaci), part, self.win)
            else:
                if currentvozaci <= total:
                    currentvozaci = currentvozaci + 1
                    loadquestion(str(currentvozaci), part, self.win)
                if currentvozaci >= 2 and currentvozaci <= total:
                    self.win.leftarrow.set_sensitive(True)
                if currentvozaci >= total:
                    self.win.rightarrow.set_sensitive(False)
        elif part == "dussn":
            if self.win.randombutton.get_active() == True:
                currentdussn = randint(1, total)
                loadquestion(str(currentdussn), part, self.win)
            else:
                if currentdussn <= total:
                    currentdussn = currentdussn + 1
                    loadquestion(str(currentdussn), part, self.win)
                if currentdussn >= 2 and currentdussn <= total:
                    self.win.leftarrow.set_sensitive(True)
                if currentdussn >= total:
                    self.win.rightarrow.set_sensitive(False)
        elif part == "vuiov":
            if self.win.randombutton.get_active() == True:
                currentvuiov = randint(1, total)
                loadquestion(str(currentvuiov), part, self.win)
            else:
                if currentvuiov <= total:
                    currentvuiov = currentvuiov + 1
                    loadquestion(str(currentvuiov), part, self.win)
                if currentvuiov >= 2 and currentvuiov <= total:
                    self.win.leftarrow.set_sensitive(True)
                if currentvuiov >= total:
                    self.win.rightarrow.set_sensitive(False)
        elif part == "nut":
            if self.win.randombutton.get_active() == True:
                currentnut = randint(1, total)
                loadquestion(str(currentnut), part, self.win)
            else:
                if currentnut <= total:
                    currentnut = currentnut + 1
                    loadquestion(str(currentnut), part, self.win)
                if currentnut >= 2 and currentnut <= total:
                    self.win.leftarrow.set_sensitive(True)
                if currentnut >= total:
                    self.win.rightarrow.set_sensitive(False)
        elif part == "vozila":
            if self.win.randombutton.get_active() == True:
                currentvozila = randint(1, total)
                loadquestion(str(currentvozila), part, self.win)
            else:
                if currentvozila <= total:
                    currentvozila = currentvozila + 1
                    loadquestion(str(currentvozila), part, self.win)
                if currentvozila >= 2 and currentvozila <= total:
                    self.win.leftarrow.set_sensitive(True)
                if currentvozila >= total:
                    self.win.rightarrow.set_sensitive(False)
        elif part == "tuzv":
            if self.win.randombutton.get_active() == True:
                currenttuzv = randint(1, total)
                loadquestion(str(currenttuzv), part, self.win)
            else:
                if currenttuzv <= total:
                    currenttuzv = currenttuzv + 1
                    loadquestion(str(currenttuzv), part, self.win)
                if currenttuzv >= 2 and currenttuzv <= total:
                    self.win.leftarrow.set_sensitive(True)
                if currenttuzv >= total:
                    self.win.rightarrow.set_sensitive(False)
        elif part == "ptilv":
            if self.win.randombutton.get_active() == True:
                currentptilv = randint(1, total)
                loadquestion(str(currentptilv), part, self.win)
            else:
                if currentptilv <= total:
                    currentptilv = currentptilv + 1
                    loadquestion(str(currentptilv), part, self.win)
                if currentptilv >= 2 and currentptilv <= total:
                    self.win.leftarrow.set_sensitive(True)
                if currentptilv >= total:
                    self.win.rightarrow.set_sensitive(False)

        conn.close()

    def previousquestion(self, button):
        global currentobsip, currentpmio, currentpnp, currentps, currentss
        global currentvozaci, currentdussn, currentvuiov, currentnut
        global currentvozila, currenttuzv, currentptilv, category, part

        conn = sqlite3.connect(programdir + '/data.db')
        c = conn.cursor()

        query = 'SELECT `id` FROM ' + part + ' ORDER BY `id` DESC LIMIT 1;'
        c.execute(query)
        total = c.fetchone()[0]

        if part == "obsip":
            if currentobsip <= total:
                currentobsip = currentobsip - 1
                loadquestion(str(currentobsip), part, self.win)
            if currentobsip == 1:
                self.win.leftarrow.set_sensitive(False)
            elif currentobsip < total:
                self.win.rightarrow.set_sensitive(True)
        elif part == "pmio":
            if currentpmio <= total:
                currentpmio = currentpmio - 1
                loadquestion(str(currentpmio), part, self.win)
            if currentpmio == 1:
                self.win.leftarrow.set_sensitive(False)
            elif currentpmio < total:
                self.win.rightarrow.set_sensitive(True)
        elif part == "pnp":
            if currentpnp <= total:
                currentpnp = currentpnp - 1
                loadquestion(str(currentpnp), part, self.win)
            if currentpnp == 1:
                self.win.leftarrow.set_sensitive(False)
            elif currentpnp < total:
                self.win.rightarrow.set_sensitive(True)
        elif part == "ps":
            if currentps <= total:
                currentps = currentps - 1
                loadquestion(str(currentps), part, self.win)
            if currentps == 1:
                self.win.leftarrow.set_sensitive(False)
            elif currentps < total:
                self.win.rightarrow.set_sensitive(True)
        elif part == "ss":
            if currentss <= total:
                currentss = currentss - 1
                loadquestion(str(currentss), part, self.win)
            if currentss == 1:
                self.win.leftarrow.set_sensitive(False)
            elif currentss < total:
                self.win.rightarrow.set_sensitive(True)
        elif part == "vozaci":
            if currentvozaci <= total:
                currentvozaci = currentvozaci - 1
                loadquestion(str(currentvozaci), part, self.win)
            if currentvozaci == 1:
                self.win.leftarrow.set_sensitive(False)
            elif currentvozaci < total:
                self.win.rightarrow.set_sensitive(True)
        elif part == "dussn":
            if currentdussn <= total:
                currentdussn = currentdussn - 1
                loadquestion(str(currentdussn), part, self.win)
            if currentdussn == 1:
                self.win.leftarrow.set_sensitive(False)
            elif currentdussn < total:
                self.win.rightarrow.set_sensitive(True)
        elif part == "vuiov":
            if currentvuiov <= total:
                currentvuiov = currentvuiov - 1
                loadquestion(str(currentvuiov), part, self.win)
            if currentvuiov == 1:
                self.win.leftarrow.set_sensitive(False)
            elif currentvuiov < total:
                self.win.rightarrow.set_sensitive(True)
        elif part == "nut":
            if currentnut <= total:
                currentnut = currentnut - 1
                loadquestion(str(currentnut), part, self.win)
            if currentnut == 1:
                self.win.leftarrow.set_sensitive(False)
            elif currentnut < total:
                self.win.rightarrow.set_sensitive(True)
        elif part == "vozila":
            if currentvozila <= total:
                currentvozila = currentvozila - 1
                loadquestion(str(currentvozila), part, self.win)
            if currentvozila == 1:
                self.win.leftarrow.set_sensitive(False)
            elif currentvozila < total:
                self.win.rightarrow.set_sensitive(True)
        elif part == "tuzv":
            if currenttuzv <= total:
                currenttuzv = currenttuzv - 1
                loadquestion(str(currenttuzv), part, self.win)
            if currenttuzv == 1:
                self.win.leftarrow.set_sensitive(False)
            elif currenttuzv < total:
                self.win.rightarrow.set_sensitive(True)
        elif part == "ptilv":
            if currentptilv <= total:
                currentptilv = currentptilv - 1
                loadquestion(str(currentptilv), part, self.win)
            if currentptilv == 1:
                self.win.leftarrow.set_sensitive(False)
            elif currentptilv < total:
                self.win.rightarrow.set_sensitive(True)

        conn.close()

    def categoryselect_callback(self, action, parameter):
        self.win.hb.props.title = "Семафор"
        self.win.arrowbox.hide()
        self.win.randombutton.hide()
        if self.win.hb.props.subtitle == "Бирање области":
            self.win.remove(self.win.partwindow)
            self.win.add(self.win.selectionwindow)
            self.win.hb.props.subtitle = "Бирање категорије"
            self.menu_enabled(False)
            self.win.leftarrow.set_sensitive(False)
            self.win.rightarrow.set_sensitive(False)
        elif self.win.hb.props.subtitle == "Основе безбедности саобраћаја и појмови":
            self.win.remove(self.win.questionwindow)
            self.win.add(self.win.selectionwindow)
            self.win.hb.props.subtitle = "Бирање категорије"
            self.menu_enabled(False)
            self.win.leftarrow.set_sensitive(False)
            self.win.rightarrow.set_sensitive(False)
        elif self.win.hb.props.subtitle == "Посебне мере и овлашћења":
            self.win.remove(self.win.questionwindow)
            self.win.add(self.win.selectionwindow)
            self.win.hb.props.subtitle = "Бирање категорије"
            self.menu_enabled(False)
            self.win.leftarrow.set_sensitive(False)
            self.win.rightarrow.set_sensitive(False)
        elif self.win.hb.props.subtitle == "Последице непоштовања прописа":
            self.win.remove(self.win.questionwindow)
            self.win.add(self.win.selectionwindow)
            self.win.hb.props.subtitle = "Бирање категорије"
            self.menu_enabled(False)
            self.win.leftarrow.set_sensitive(False)
            self.win.rightarrow.set_sensitive(False)
        elif self.win.hb.props.subtitle == "Правила саобраћаја":
            self.win.remove(self.win.questionwindow)
            self.win.add(self.win.selectionwindow)
            self.win.hb.props.subtitle = "Бирање категорије"
            self.menu_enabled(False)
            self.win.leftarrow.set_sensitive(False)
            self.win.rightarrow.set_sensitive(False)
        elif self.win.hb.props.subtitle == "Саобраћајна сигнализација":
            self.win.remove(self.win.questionwindow)
            self.win.add(self.win.selectionwindow)
            self.win.hb.props.subtitle = "Бирање категорије"
            self.menu_enabled(False)
            self.win.leftarrow.set_sensitive(False)
            self.win.rightarrow.set_sensitive(False)
        elif self.win.hb.props.subtitle == "Возачи":
            self.win.remove(self.win.questionwindow)
            self.win.add(self.win.selectionwindow)
            self.win.hb.props.subtitle = "Бирање категорије"
            self.menu_enabled(False)
            self.win.leftarrow.set_sensitive(False)
            self.win.rightarrow.set_sensitive(False)
        elif self.win.hb.props.subtitle == "Дужности у случају саобраћајне незгоде":
            self.win.remove(self.win.questionwindow)
            self.win.add(self.win.selectionwindow)
            self.win.hb.props.subtitle = "Бирање категорије"
            self.menu_enabled(False)
            self.win.leftarrow.set_sensitive(False)
            self.win.rightarrow.set_sensitive(False)
        elif self.win.hb.props.subtitle == "Време управљања и одмори возача":
            self.win.remove(self.win.questionwindow)
            self.win.add(self.win.selectionwindow)
            self.win.hb.props.subtitle = "Бирање категорије"
            self.menu_enabled(False)
            self.win.leftarrow.set_sensitive(False)
            self.win.rightarrow.set_sensitive(False)
        elif self.win.hb.props.subtitle == "Начин употребе тахографа":
            self.win.remove(self.win.questionwindow)
            self.win.add(self.win.selectionwindow)
            self.win.hb.props.subtitle = "Бирање категорије"
            self.menu_enabled(False)
            self.win.leftarrow.set_sensitive(False)
            self.win.rightarrow.set_sensitive(False)
        elif self.win.hb.props.subtitle == "Возила":
            self.win.remove(self.win.questionwindow)
            self.win.add(self.win.selectionwindow)
            self.win.hb.props.subtitle = "Бирање категорије"
            self.menu_enabled(False)
            self.win.leftarrow.set_sensitive(False)
            self.win.rightarrow.set_sensitive(False)
        elif self.win.hb.props.subtitle == "Технички услови за возила":
            self.win.remove(self.win.questionwindow)
            self.win.add(self.win.selectionwindow)
            self.win.hb.props.subtitle = "Бирање категорије"
            self.menu_enabled(False)
            self.win.leftarrow.set_sensitive(False)
            self.win.rightarrow.set_sensitive(False)
        elif self.win.hb.props.subtitle == "Превоз терета и лица возилима":
            self.win.remove(self.win.questionwindow)
            self.win.add(self.win.selectionwindow)
            self.win.hb.props.subtitle = "Бирање категорије"
            self.menu_enabled(False)
            self.win.leftarrow.set_sensitive(False)
            self.win.rightarrow.set_sensitive(False)

    def obsip_callback(self, action, parameter):
        global part, currentobsip
        part = "obsip"
        currentobsip = 1
        if self.win.hb.props.subtitle == "Бирање области":
            self.win.remove(self.win.partwindow)
        elif self.win.hb.props.subtitle == "Посебне мере и овлашћења":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Последице непоштовања прописа":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Правила саобраћаја":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Саобраћајна сигнализација":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Возачи":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Дужности у случају саобраћајне незгоде":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Начин употребе тахографа":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Време управљања и одмори возача":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Возила":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Технички услови за возила":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Превоз терета и лица возилима":
            self.win.remove(self.win.questionwindow)
        self.win.hb.props.subtitle = "Основе безбедности саобраћаја и појмови"
        self.win.arrowbox.show()
        self.win.randombutton.show()
        self.win.leftarrow.set_sensitive(False)
        self.win.rightarrow.set_sensitive(True)
        self.win.add(self.win.questionwindow)
        loadquestion("1", part, self.win)
        self.menu_enabled(True)
        self.obsip_action.set_enabled(False)

    def pmio_callback(self, action, parameter):
        global part, currentpmio
        part = "pmio"
        currentpmio = 1
        if self.win.hb.props.subtitle == "Бирање области":
            self.win.remove(self.win.partwindow)
        elif self.win.hb.props.subtitle == "Основе безбедности саобраћаја и појмови":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Последице непоштовања прописа":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Правила саобраћаја":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Саобраћајна сигнализација":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Возачи":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Дужности у случају саобраћајне незгоде":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Начин употребе тахографа":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Време управљања и одмори возача":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Возила":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Технички услови за возила":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Превоз терета и лица возилима":
            self.win.remove(self.win.questionwindow)
        self.win.hb.props.subtitle = "Посебне мере и овлашћења"
        self.win.arrowbox.show()
        self.win.randombutton.show()
        self.win.leftarrow.set_sensitive(False)
        self.win.rightarrow.set_sensitive(True)
        self.win.add(self.win.questionwindow)
        loadquestion("1", part, self.win)
        self.menu_enabled(True)
        self.pmio_action.set_enabled(False)

    def pnp_callback(self, action, parameter):
        global part, currentpnp
        part = "pnp"
        currentpnp = 1
        if self.win.hb.props.subtitle == "Бирање области":
            self.win.remove(self.win.partwindow)
        elif self.win.hb.props.subtitle == "Основе безбедности саобраћаја и појмови":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Посебне мере и овлашћења":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Правила саобраћаја":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Саобраћајна сигнализација":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Возачи":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Дужности у случају саобраћајне незгоде":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Начин употребе тахографа":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Време управљања и одмори возача":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Возила":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Технички услови за возила":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Превоз терета и лица возилима":
            self.win.remove(self.win.questionwindow)
        self.win.hb.props.subtitle = "Последице непоштовања прописа"
        self.win.arrowbox.show()
        self.win.randombutton.show()
        self.win.leftarrow.set_sensitive(False)
        self.win.rightarrow.set_sensitive(True)
        self.win.add(self.win.questionwindow)
        loadquestion("1", part, self.win)
        self.menu_enabled(True)
        self.pnp_action.set_enabled(False)

    def ps_callback(self, action, parameter):
        global part, currentps
        part = "ps"
        currentps = 1
        if self.win.hb.props.subtitle == "Бирање области":
            self.win.remove(self.win.partwindow)
        elif self.win.hb.props.subtitle == "Основе безбедности саобраћаја и појмови":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Посебне мере и овлашћења":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Последице непоштовања прописа":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Саобраћајна сигнализација":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Возачи":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Дужности у случају саобраћајне незгоде":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Начин употребе тахографа":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Време управљања и одмори возача":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Возила":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Технички услови за возила":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Превоз терета и лица возилима":
            self.win.remove(self.win.questionwindow)
        self.win.hb.props.subtitle = "Правила саобраћаја"
        self.win.arrowbox.show()
        self.win.randombutton.show()
        self.win.leftarrow.set_sensitive(False)
        self.win.rightarrow.set_sensitive(True)
        self.win.add(self.win.questionwindow)
        loadquestion("1", part, self.win)
        self.menu_enabled(True)
        self.ps_action.set_enabled(False)

    def ss_callback(self, action, parameter):
        global part, currentss
        part = "ss"
        currentss = 1
        if self.win.hb.props.subtitle == "Бирање области":
            self.win.remove(self.win.partwindow)
        elif self.win.hb.props.subtitle == "Основе безбедности саобраћаја и појмови":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Посебне мере и овлашћења":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Последице непоштовања прописа":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Правила саобраћаја":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Возачи":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Дужности у случају саобраћајне незгоде":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Начин употребе тахографа":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Време управљања и одмори возача":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Возила":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Технички услови за возила":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Превоз терета и лица возилима":
            self.win.remove(self.win.questionwindow)
        self.win.hb.props.subtitle = "Саобраћајна сигнализација"
        self.win.arrowbox.show()
        self.win.randombutton.show()
        self.win.leftarrow.set_sensitive(False)
        self.win.rightarrow.set_sensitive(True)
        self.win.add(self.win.questionwindow)
        loadquestion("1", part, self.win)
        self.menu_enabled(True)
        self.ss_action.set_enabled(False)

    def vozaci_callback(self, action, parameter):
        global part, currentvozaci
        part = "vozaci"
        currentvozaci = 1
        if self.win.hb.props.subtitle == "Бирање области":
            self.win.remove(self.win.partwindow)
        elif self.win.hb.props.subtitle == "Основе безбедности саобраћаја и појмови":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Посебне мере и овлашћења":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Последице непоштовања прописа":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Правила саобраћаја":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Саобраћајна сигнализација":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Дужности у случају саобраћајне незгоде":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Начин употребе тахографа":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Време управљања и одмори возача":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Возила":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Технички услови за возила":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Превоз терета и лица возилима":
            self.win.remove(self.win.questionwindow)
        self.win.hb.props.subtitle = "Возачи"
        self.win.arrowbox.show()
        self.win.randombutton.show()
        self.win.leftarrow.set_sensitive(False)
        self.win.rightarrow.set_sensitive(True)
        self.win.add(self.win.questionwindow)
        loadquestion("1", part, self.win)
        self.menu_enabled(True)
        self.vozaci_action.set_enabled(False)

    def dussn_callback(self, action, parameter):
        global part, currentdussn
        part = "dussn"
        currentdussn = 1
        if self.win.hb.props.subtitle == "Бирање области":
            self.win.remove(self.win.partwindow)
        elif self.win.hb.props.subtitle == "Основе безбедности саобраћаја и појмови":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Посебне мере и овлашћења":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Последице непоштовања прописа":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Правила саобраћаја":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Саобраћајна сигнализација":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Возачи":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Начин употребе тахографа":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Време управљања и одмори возача":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Возила":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Технички услови за возила":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Превоз терета и лица возилима":
            self.win.remove(self.win.questionwindow)
        self.win.hb.props.subtitle = "Дужности у случају саобраћајне незгоде"
        self.win.arrowbox.show()
        self.win.randombutton.show()
        self.win.leftarrow.set_sensitive(False)
        self.win.rightarrow.set_sensitive(True)
        self.win.add(self.win.questionwindow)
        loadquestion("1", part, self.win)
        self.menu_enabled(True)
        self.dussn_action.set_enabled(False)

    def vuiov_callback(self, action, parameter):
        global part, currentvuiov
        part = "vuiov"
        currentvuiov = 1
        if self.win.hb.props.subtitle == "Бирање области":
            self.win.remove(self.win.partwindow)
        elif self.win.hb.props.subtitle == "Основе безбедности саобраћаја и појмови":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Посебне мере и овлашћења":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Последице непоштовања прописа":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Правила саобраћаја":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Саобраћајна сигнализација":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Возачи":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Начин употребе тахографа":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Возила":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Технички услови за возила":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Превоз терета и лица возилима":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Дужности у случају саобраћајне незгоде":
            self.win.remove(self.win.questionwindow)
        self.win.hb.props.subtitle = "Време управљања и одмори возача"
        self.win.arrowbox.show()
        self.win.randombutton.show()
        self.win.leftarrow.set_sensitive(False)
        self.win.rightarrow.set_sensitive(True)
        self.win.add(self.win.questionwindow)
        loadquestion("1", part, self.win)
        self.menu_enabled(True)
        self.vuiov_action.set_enabled(False)

    def nut_callback(self, action, parameter):
        global part, currentnut
        part = "nut"
        currentnut = 1
        if self.win.hb.props.subtitle == "Бирање области":
            self.win.remove(self.win.partwindow)
        elif self.win.hb.props.subtitle == "Основе безбедности саобраћаја и појмови":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Посебне мере и овлашћења":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Последице непоштовања прописа":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Правила саобраћаја":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Саобраћајна сигнализација":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Возачи":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Дужности у случају саобраћајне незгоде":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Време управљања и одмори возача":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Возила":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Технички услови за возила":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Превоз терета и лица возилима":
            self.win.remove(self.win.questionwindow)
        self.win.hb.props.subtitle = "Начин употребе тахографа"
        self.win.arrowbox.show()
        self.win.randombutton.show()
        self.win.leftarrow.set_sensitive(False)
        self.win.rightarrow.set_sensitive(True)
        self.win.add(self.win.questionwindow)
        loadquestion("1", part, self.win)
        self.menu_enabled(True)
        self.nut_action.set_enabled(False)

    def vozila_callback(self, action, parameter):
        global part, currentvozila
        part = "vozila"
        currentvozila = 1
        if self.win.hb.props.subtitle == "Бирање области":
            self.win.remove(self.win.partwindow)
        elif self.win.hb.props.subtitle == "Основе безбедности саобраћаја и појмови":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Посебне мере и овлашћења":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Последице непоштовања прописа":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Правила саобраћаја":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Саобраћајна сигнализација":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Возачи":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Дужности у случају саобраћајне незгоде":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Начин употребе тахографа":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Време управљања и одмори возача":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Технички услови за возила":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Превоз терета и лица возилима":
            self.win.remove(self.win.questionwindow)
        self.win.hb.props.subtitle = "Возила"
        self.win.arrowbox.show()
        self.win.randombutton.show()
        self.win.leftarrow.set_sensitive(False)
        self.win.rightarrow.set_sensitive(True)
        self.win.add(self.win.questionwindow)
        loadquestion("1", part, self.win)
        self.menu_enabled(True)
        self.vozila_action.set_enabled(False)

    def tuzv_callback(self, action, parameter):
        global part, currenttuzv
        part = "tuzv"
        currenttuzv = 1
        if self.win.hb.props.subtitle == "Бирање области":
            self.win.remove(self.win.partwindow)
        elif self.win.hb.props.subtitle == "Основе безбедности саобраћаја и појмови":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Посебне мере и овлашћења":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Последице непоштовања прописа":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Правила саобраћаја":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Саобраћајна сигнализација":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Возачи":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Дужности у случају саобраћајне незгоде":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Начин употребе тахографа":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Време управљања и одмори возача":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Возила":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Превоз терета и лица возилима":
            self.win.remove(self.win.questionwindow)
        self.win.hb.props.subtitle = "Технички услови за возила"
        self.win.arrowbox.show()
        self.win.randombutton.show()
        self.win.leftarrow.set_sensitive(False)
        self.win.rightarrow.set_sensitive(True)
        self.win.add(self.win.questionwindow)
        loadquestion("1", part, self.win)
        self.menu_enabled(True)
        self.tuzv_action.set_enabled(False)

    def ptilv_callback(self, action, parameter):
        global part, currentptilv
        part = "ptilv"
        currentptilv = 1
        if self.win.hb.props.subtitle == "Бирање области":
            self.win.remove(self.win.partwindow)
        elif self.win.hb.props.subtitle == "Основе безбедности саобраћаја и појмови":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Посебне мере и овлашћења":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Последице непоштовања прописа":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Правила саобраћаја":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Саобраћајна сигнализација":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Возачи":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Дужности у случају саобраћајне незгоде":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Начин употребе тахографа":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Време управљања и одмори возача":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Возила":
            self.win.remove(self.win.questionwindow)
        elif self.win.hb.props.subtitle == "Технички услови за возила":
            self.win.remove(self.win.questionwindow)
        self.win.hb.props.subtitle = "Превоз терета и лица возилима"
        self.win.arrowbox.show()
        self.win.randombutton.show()
        self.win.leftarrow.set_sensitive(False)
        self.win.rightarrow.set_sensitive(True)
        self.win.add(self.win.questionwindow)
        loadquestion("1", part, self.win)
        self.menu_enabled(True)
        self.ptilv_action.set_enabled(False)

    def about_callback(self, action, parameter):
        dialog = Gtk.AboutDialog()
        dialog.set_default_size(430, 390)
        dialog.set_transient_for(self.win)
        dialog.set_program_name('Семафор')
        dialog.set_version('1.0')
        dialog.set_website('http://sourceforge.net/projects/semafor/')
        dialog.set_website_label("Веб страница Семафора.")
        dialog.set_comments("Програм за обуку возача.")
        dialog.set_translator_credits(('translator-credits'))
        dialog.set_artists([
            'Петар „mamuz” Милојевић <trenatre@mail.com>',
        ])
        dialog.set_authors([
            'Марко М. Костић <marko.m.kostic@gmail.com>',
        ])
        dialog.set_license(license)
        dialog.set_wrap_license(True)
        dialog.set_copyright("© 2011-2016 Марко М. Костић")
        image = Gtk.Image()
        image.set_from_file(programdir + '/icon/icon.png')
        pixbuf = image.get_pixbuf()
        dialog.set_logo(pixbuf)
        dialog.run()
        dialog.destroy()

    # functions bellow are called from the semafor.py, when a checkbutton is selected in
    # program. These functions just forward data to the main function above (checkanswer.py)
    # which is the one which acts and tests if the answer is correct.

    def check_answer1(window, checkbutton):
        answer = window.win.label1.get_label()
        label = window.win.label1
        if part == "obsip":
            checkanswer(str(currentobsip), part, answer, window, checkbutton, label)
        elif part == "pmio":
            checkanswer(str(currentpmio), part, answer, window, checkbutton, label)
        elif part == "pnp":
            checkanswer(str(currentpnp), part, answer, window, checkbutton, label)
        elif part == "ps":
            checkanswer(str(currentps), part, answer, window, checkbutton, label)
        elif part == "ss":
            checkanswer(str(currentss), part, answer, window, checkbutton, label)
        elif part == "vozaci":
            checkanswer(str(currentvozaci), part, answer, window, checkbutton, label)
        elif part == "dussn":
            checkanswer(str(currentdussn), part, answer, window, checkbutton, label)
        elif part == "vuiov":
            checkanswer(str(currentvuiov), part, answer, window, checkbutton, label)
        elif part == "nut":
            checkanswer(str(currentnut), part, answer, window, checkbutton, label)
        elif part == "vozila":
            checkanswer(str(currentvozila), part, answer, window, checkbutton, label)
        elif part == "tuzv":
            checkanswer(str(currenttuzv), part, answer, window, checkbutton, label)
        elif part == "ptilv":
            checkanswer(str(currentptilv), part, answer, window, checkbutton, label)

    def check_answer2(window, checkbutton):
        answer = window.win.label2.get_label()
        label = window.win.label2
        if part == "obsip":
            checkanswer(str(currentobsip), part, answer, window, checkbutton, label)
        elif part == "pmio":
            checkanswer(str(currentpmio), part, answer, window, checkbutton, label)
        elif part == "pnp":
            checkanswer(str(currentpnp), part, answer, window, checkbutton, label)
        elif part == "ps":
            checkanswer(str(currentps), part, answer, window, checkbutton, label)
        elif part == "ss":
            checkanswer(str(currentss), part, answer, window, checkbutton, label)
        elif part == "vozaci":
            checkanswer(str(currentvozaci), part, answer, window, checkbutton, label)
        elif part == "dussn":
            checkanswer(str(currentdussn), part, answer, window, checkbutton, label)
        elif part == "vuiov":
            checkanswer(str(currentvuiov), part, answer, window, checkbutton, label)
        elif part == "nut":
            checkanswer(str(currentnut), part, answer, window, checkbutton, label)
        elif part == "vozila":
            checkanswer(str(currentvozila), part, answer, window, checkbutton, label)
        elif part == "tuzv":
            checkanswer(str(currenttuzv), part, answer, window, checkbutton, label)
        elif part == "ptilv":
            checkanswer(str(currentptilv), part, answer, window, checkbutton, label)

    def check_answer3(window, checkbutton):
        answer = window.win.label3.get_label()
        label = window.win.label3
        if part == "obsip":
            checkanswer(str(currentobsip), part, answer, window, checkbutton, label)
        elif part == "pmio":
            checkanswer(str(currentpmio), part, answer, window, checkbutton, label)
        elif part == "pnp":
            checkanswer(str(currentpnp), part, answer, window, checkbutton, label)
        elif part == "ps":
            checkanswer(str(currentps), part, answer, window, checkbutton, label)
        elif part == "ss":
            checkanswer(str(currentss), part, answer, window, checkbutton, label)
        elif part == "vozaci":
            checkanswer(str(currentvozaci), part, answer, window, checkbutton, label)
        elif part == "dussn":
            checkanswer(str(currentdussn), part, answer, window, checkbutton, label)
        elif part == "vuiov":
            checkanswer(str(currentvuiov), part, answer, window, checkbutton, label)
        elif part == "nut":
            checkanswer(str(currentnut), part, answer, window, checkbutton, label)
        elif part == "vozila":
            checkanswer(str(currentvozila), part, answer, window, checkbutton, label)
        elif part == "tuzv":
            checkanswer(str(currenttuzv), part, answer, window, checkbutton, label)
        elif part == "ptilv":
            checkanswer(str(currentptilv), part, answer, window, checkbutton, label)

    def check_answer4(window, checkbutton):
        answer = window.win.label4.get_label()
        label = window.win.label4
        if part == "obsip":
            checkanswer(str(currentobsip), part, answer, window, checkbutton, label)
        elif part == "pmio":
            checkanswer(str(currentpmio), part, answer, window, checkbutton, label)
        elif part == "pnp":
            checkanswer(str(currentpnp), part, answer, window, checkbutton, label)
        elif part == "ps":
            checkanswer(str(currentps), part, answer, window, checkbutton, label)
        elif part == "ss":
            checkanswer(str(currentss), part, answer, window, checkbutton, label)
        elif part == "vozaci":
            checkanswer(str(currentvozaci), part, answer, window, checkbutton, label)
        elif part == "dussn":
            checkanswer(str(currentdussn), part, answer, window, checkbutton, label)
        elif part == "vuiov":
            checkanswer(str(currentvuiov), part, answer, window, checkbutton, label)
        elif part == "nut":
            checkanswer(str(currentnut), part, answer, window, checkbutton, label)
        elif part == "vozila":
            checkanswer(str(currentvozila), part, answer, window, checkbutton, label)
        elif part == "tuzv":
            checkanswer(str(currenttuzv), part, answer, window, checkbutton, label)
        elif part == "ptilv":
            checkanswer(str(currentptilv), part, answer, window, checkbutton, label)

    def check_answer5(window, checkbutton):
        answer = window.win.label5.get_label()
        label = window.win.label5
        if part == "obsip":
            checkanswer(str(currentobsip), part, answer, window, checkbutton, label)
        elif part == "pmio":
            checkanswer(str(currentpmio), part, answer, window, checkbutton, label)
        elif part == "pnp":
            checkanswer(str(currentpnp), part, answer, window, checkbutton, label)
        elif part == "ps":
            checkanswer(str(currentps), part, answer, window, checkbutton, label)
        elif part == "ss":
            checkanswer(str(currentss), part, answer, window, checkbutton, label)
        elif part == "vozaci":
            checkanswer(str(currentvozaci), part, answer, window, checkbutton, label)
        elif part == "dussn":
            checkanswer(str(currentdussn), part, answer, window, checkbutton, label)
        elif part == "vuiov":
            checkanswer(str(currentvuiov), part, answer, window, checkbutton, label)
        elif part == "nut":
            checkanswer(str(currentnut), part, answer, window, checkbutton, label)
        elif part == "vozila":
            checkanswer(str(currentvozila), part, answer, window, checkbutton, label)
        elif part == "tuzv":
            checkanswer(str(currenttuzv), part, answer, window, checkbutton, label)
        elif part == "ptilv":
            checkanswer(str(currentptilv), part, answer, window, checkbutton, label)

    def check_answer6(window, checkbutton):
        answer = window.win.label6.get_label()
        label = window.win.label6
        if part == "obsip":
            checkanswer(str(currentobsip), part, answer, window, checkbutton, label)
        elif part == "pmio":
            checkanswer(str(currentpmio), part, answer, window, checkbutton, label)
        elif part == "pnp":
            checkanswer(str(currentpnp), part, answer, window, checkbutton, label)
        elif part == "ps":
            checkanswer(str(currentps), part, answer, window, checkbutton, label)
        elif part == "ss":
            checkanswer(str(currentss), part, answer, window, checkbutton, label)
        elif part == "vozaci":
            checkanswer(str(currentvozaci), part, answer, window, checkbutton, label)
        elif part == "dussn":
            checkanswer(str(currentdussn), part, answer, window, checkbutton, label)
        elif part == "vuiov":
            checkanswer(str(currentvuiov), part, answer, window, checkbutton, label)
        elif part == "nut":
            checkanswer(str(currentnut), part, answer, window, checkbutton, label)
        elif part == "vozila":
            checkanswer(str(currentvozila), part, answer, window, checkbutton, label)
        elif part == "tuzv":
            checkanswer(str(currenttuzv), part, answer, window, checkbutton, label)
        elif part == "ptilv":
            checkanswer(str(currentptilv), part, answer, window, checkbutton, label)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = Semafor()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)
