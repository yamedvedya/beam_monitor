import tango
import os
import configparser

from pathlib import Path


# ----------------------------------------------------------------------
def get_tango_host():
    db = tango.Database()
    return db.get_db_host()

# ----------------------------------------------------------------------
def get_server_name_by_class(tango_host):

    if tango_host is None:
        db = tango.Database()
    else:
        if tango_host.find('tango://') == 0:
            raise RuntimeError(f"Bad TANGO_HOST syntax {tango_host}")

        lst = tango_host.split(':')
        try:
            if len(lst) == 2:
                db = tango.Database(*lst)
            elif len(lst) == 1:
                db = tango.Database(lst[0], "10000")
        except:
            raise RuntimeError(f"Failed to return Database, {tango_host}")

    devices_in_db = dict.fromkeys(db.get_server_list("*").value_string)

    existing_servers = []

    for srv in devices_in_db.keys():
        if devices_in_db[srv] is None:
            devices_in_db[srv] = db.get_server_class_list(srv).value_string
        for clss in devices_in_db[srv]:
            if clss == "TelegramBot":
                existing_servers.extend(db.get_device_name(srv, "TelegramBot").value_string)
                break

    return existing_servers


# ----------------------------------------------------------------------
def check_settings():
    file_name = os.path.join(os.path.join(str(Path.home()), '.beamline_monitor'), 'settings.ini')
    if not os.path.exists(file_name):
        return

    parser = configparser.ConfigParser()
    parser.read(file_name)

    if "TELEGRAMBOT" not in parser:
        parser.add_section("TELEGRAMBOT")
        tango_host = get_tango_host()
        servers = get_server_name_by_class(tango_host)
        if len(servers):
            parser.set("TELEGRAMBOT", "enabled", "true")
            parser.set("TELEGRAMBOT", "host", tango_host)
            parser.set("TELEGRAMBOT", "server", servers[0])
            parser.set("TELEGRAMBOT", "specific_server", "")
        else:
            parser.set("TELEGRAMBOT", "enabled", "false")

        with open(file_name, 'w') as f:
            parser.write(f)


# ----------------------------------------------------------------------
def refresh_combo_box(combo_box, text):
    """Auxiliary function refreshing combo box with a given text.
    """
    idx = combo_box.findText(text)
    if idx != -1:
        combo_box.setCurrentIndex(idx)
        return True
    else:
        combo_box.setCurrentIndex(0)
        return False
