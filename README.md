# Semafor

Semafor (read as Semaphore) is a new GNOME program for testing the knowledge of driving regulations
in Serbia.

**Early Alpha**.

![Alt text](screenshot.png?raw=true "Semafor interface")

## Depends on
- gtk3 >= 3.16
- python3
- python-sqlite
- make

## Installation
  * Clone this repo,
  * cd into the directory where you cloned this repo,
  * issue the command `sudo make install` to install it.

If you already installed the program earlier, you'll need to uninstall it first,
as described in the "Removal" section and then execute `sudo make install` again.

## Usage
After doing this, you can start Semafor by:
  * Searching for Semafor or Семафор in Gnome Overview (if using Gnome Shell),
  * executing command `semafor` in the Terminal,
  * executing command `/usr/share/semafor/semafor.py` in the Terminal.

If you wish to run it locally, without installing it to your system /usr, you can
do that by first generating the translations with `make translations` and then
by executing `./semafor.py` while in the directory where you cloned the code.

After staring it up for the first time, you'll receive an error about missing question database.

The program is currently in early alpha. The program requires data and assets released from the
Serbian Ministry of Internal Affairs under the terms which deny commercial usage. Because of the
restrictions and because I didn't had the time to figure out the correct license under which
these assets can be distributed, you will need to download the question database separately.

To see how this program works, download database with questions into the folder where the program
is located. If you have installed the program as described in the Installation section, download
the assets with `sudo curl http://костић.срб/data.db -o /usr/share/semafor/data.db` and restart
the program.

If running the program locally, just do `curl http://костић.срб/data.db -o ./data.db` while
in the directory where you cloned the code and restart the program.

## Usage on Windows

Described in the WINDOWS file.

## Uninstallation
To remove your system-wide installed Semafor, just execute `sudo make uninstall`
in the directory where you cloned this repo.
