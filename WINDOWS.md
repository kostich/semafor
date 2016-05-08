# Building on Windows

To freeze the program into exe, on Windows you will need to first install Python 3.4
(3.5 does not work, currently) and add python and pip executables to your system
PATH. These executables are usually located in the:

* `C:\Python34\` and

* `C:\Python34\Scripts` directories.

After doing that you will need to install pygi-aio-3.18.2_rev7-setup (can be found
on sourceforge, during the install just check the "Base packages","GDK-Pixbuf" and "GTK+"
items).

We will use `cx_freeze` to package the program into the exe so execute this command
into the cmd: `pip install cx_Freeze`.

Afterwards, `chdir` into the directory where the Semafor's source code is cloned
and execute `python setup.py build`. After that finishes, you need to copy over
the gnome .dll's from the root gnome folder of your Python 3.4 installation. For
example, if the Python install path is `C:\Python34\`, these .dll's are located in
the directory `C:\Python34\Lib\site-packages\gnome\`. Copy over all the dll's from this
directory but don't copy over any .dll from any subdirectory.

Now you can double-click semafor.exe and Semafor will launch on Windows.

If you get the error about the missing question database, follow the instructions
for acquiring the database listed in the README.
