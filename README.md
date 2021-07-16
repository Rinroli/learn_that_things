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
add_def:      You should enter:
    <string>   *what - concept, what should be defined
    <string>   *def_body - definition
    <string>   *subject - what subject
    <integer>  lecture - number of the lection
        This will add note to the base
from_file:    Add several defs from json-file, see example.json.
show_random:  Show random def from all the base.
```

## TODO

* Flexible file selection for adding from file - already done, it remains to configure the *cli-input*

* Random def from subject - already done, it remains to configure the *cli-input*

* Tests

* **Export** to *LaTeX*, all and by subject

* Changing and deleting existing records (now you can do this, for example, through the *sqlitebrowser*)
