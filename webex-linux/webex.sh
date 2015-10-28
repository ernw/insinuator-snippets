#!/bin/sh

webex() {
	FIREFOX_PATH="/opt/programs/firefox_x86" #Change this to actual path
	JRE_PATH="/opt/programs/jre_x86" #Change this to actual path

	if pgrep firefox > /dev/null; then
		echo "[-] Firefox seems to be running. Please exit first";
	else
		echo "[+] Placing link to x86 plugin into ~/.mozilla/plugins"
		if [ ! -d ~/.mozilla/plugins ]; then
			mkdir -p ~/.mozilla/plugins
		fi
		if [ -f ~/.mozilla/plugins/libnpjp2.so ]; then
			echo "[+] Backing up already existing plugin"
			mv ~/.mozilla/plugins/libnpjp2.so ~/.mozilla/plugins/libnpjp2.so.bak
		fi

		ln -s "${JRE_PATH}/lib/i386/libnpjp2.so" ~/.mozilla/plugins/;

		echo "[+] Starting x86 firefox"
		"${FIREFOX_PATH}/firefox";

		echo "[+] Removing link to x86 plugin"
		rm -f ~/.mozilla/plugins/libnpjp2.so;

		if [ -f ~/.mozilla/plugins/libnpjp2.so.bak ]; then
			echo "[+] Restoring plugin from backup"
			mv ~/.mozilla/plugins/libnpjp2.so.bak ~/.mozilla/plugins/libnpjp2.so
		fi
	fi;
}
