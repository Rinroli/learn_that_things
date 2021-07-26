# Learn that things

This small repository will try to help with this. Build your own *sqlite*-database of definitions.

Now you can also easily export definitions to the *LaTeX*-file.

For **Linux** (I do not know if the program works on **Windows**. But it is quite possible)

## **Usage**

At the moment, there are **four** modes of operation - two for writing, one for reading and export to *LaTeX* (and help).

```bash
usage: main.py [-h] [-f FILE] [-s SUBJECT] [-d DATA]
               {add_def,show_random,from_file,export,help}
```

Note: * means necessary

```txt
add_def:        Add note to the base:
        <string>        *what - concept, what should be defined
        <string>        *def_body - definition
        <string>        *subject - what subject
        <integer>       lecture - number of the lection
from_file       Add definitions from json-file
        -f <string>        file - file with definitions, 'example.json' by default
show_random     Show random def from the base.
        -s <string>        subject - subject of random def, 'all' by default
export          Export definitions to latex, result in './exported'
        -s <string>        subject - subject of defs, 'all' by default
        -f <string>     file - file with definitions, 'exported.tex' by default
                                Will add extension '.tex' if necessary
```

## TODO

* Tests

* ***DONE*** Export to *LaTeX*, all and by subject

* Changing and deleting existing records (now you can do this, for example, through the *sqlitebrowser*)

* Searching by name and tags

* References
