install:
	mkdir -p /usr/share/semafor
	cp -r ./* /usr/share/semafor/
	ln -s /usr/share/semafor/semafor.py /usr/bin/semafor
	mv /usr/share/semafor/semafor.desktop /usr/share/applications/
	msgfmt po/sr.po -o /usr/share/locale/sr/LC_MESSAGES/semafor.mo
	msgfmt po/sr@latin.po -o /usr/share/locale/sr@latin/LC_MESSAGES/semafor.mo

uninstall:
	rm -rf /usr/share/semafor/
	rm -f /usr/share/applications/semafor.desktop
	unlink /usr/bin/semafor

translations:
	mkdir -p ./locale/sr/LC_MESSAGES/
	mkdir -p ./locale/sr@latin/LC_MESSAGES/
	msgfmt po/sr.po -o ./locale/sr/LC_MESSAGES/semafor.mo
	msgfmt po/sr@latin.po -o ./locale/sr@latin/LC_MESSAGES/semafor.mo

clean:
	rm -rf ./locale
