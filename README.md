DASBiT - A Python-based IRC bot
===============================

Quick Start
-----------
Start the bot by typing "./dasbit <data path>", where data path is a writable
directory. It will prompt your for connection information, which will then be
stored in the data path.

By default, only the two master plugins "users" and "plugins" are enabled. To
enable further plugins, call "!plugin enable <plugin-name>".

Available Plugins
-----------------
The following core plugins are shipped with DASBiT:

- users: user access management
- plugins: plugin management
- channels: joining and parting channels

Additional helpful plugins are also provided. See the [wiki](https://github.com/DASPRiD/DASBiT/wiki/Plugins) for a full list and help.

License
-------
The files in this archive are released under the new BSD license that is
bundled with this package in the file LICENSE.

Init script
-----------
You can set up the init script by:

```bash
$ cp init.d/dasbit /etc/init.d/dasbit
```

Then you can use the following commands to control the bot:

```bash
$ sudo service dasbit start
$ sudo service dasbit status
$ sudo service dasbit stop
```

