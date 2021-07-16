# Learn that things

This small repository will try to help with this. Build your own *sqlite*-database of definitions.

For **Linux** (I do not know if the program works on **Windows**. But it is quite possible)

## **Usage**

At the moment, there are three modes of operation - two for writing, one for reading (and help).

```bash
usage: main.py [-h] {add_def,show_random,from_file,help}
```

Note: * means necessary

```txt
add_def:        Add note to the base:
        <string>        *what - concept, what should be defined
        <string>        *def_body - definition
        <string>        *subject - what subject
        <integer>       lecture - number of the lection
from_file       Add definitions from json-file
        <string>        file - file with definitions, 'example.json' by default
show_random     Show random def from the base.
        <string>        subject - subject of random def, 'all' by default
```

## TODO

* Tests

* **Export** to *LaTeX*, all and by subject

* Changing and deleting existing records (now you can do this, for example, through the *sqlitebrowser*)
