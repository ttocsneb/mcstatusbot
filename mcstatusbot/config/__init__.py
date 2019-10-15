import os
from . import schema
from ruamel import yaml

from os.path import dirname as d
path = os.path.join(d(d(d(__file__))), "config.yml")


def get_settings():
    print("Entering First Time Setup.\n")

    data = dict()
    fields = schema.ConfigSchema._declared_fields

    print("Minecraft Server info")
    data["ip"] = input("Enter the IP/address of the server ({}): ".format(
        fields["ip"].missing
    ))

    data["port"] = None
    while data["port"] is None:
        p = input("Enter the port of the server ({}):".format(
            fields["port"].missing
        ))
        if p == "":
            data["port"] = ""
            break
        try:
            data["port"] = int(p)
            if data["port"] < 0 or data["port"] > 65535:
                data["port"] = None
                raise ValueError
        except ValueError:
            print("{} is not a valid port".format(p))

    print("Discord Bot Info")
    data["token"] = \
        input("Enter the bot token (if not given, put in config file): ")

    data["prefix"] = input("Enter the prefix ({}): ".format(
        fields["prefix"].missing
    ))

    return dict([
        (k, v) for k, v in data.items() if v != ""
    ])


def load() -> schema.Config:
    config = schema.ConfigSchema()
    dump = False
    try:
        with open(path) as f:
            obj = yaml.round_trip_load(f)
    except IOError:
        obj = get_settings()
        dump = True

    conf = config.load(obj)

    if dump:
        data = config.dump(conf)
        print("Saving config to {}".format(path))
        with open(path, "w") as f:
            yaml.round_trip_dump(data, f)

    return conf


config = load()
