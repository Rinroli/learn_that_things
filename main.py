#!/usr/bin/env python3
"""Operate with db - add defs and read them.

version 1.0
"""

from db import dataAccess
from termcolor import cprint, colored
import logging as lg
from random import choice, randint
from argparse import ArgumentParser
from pylatexenc.latexwalker import LatexWalker, LatexEnvironmentNode
import latex_output
import json
import os


PHRASES = {
    "what": [
        "What* is it: ", "An empty concept - mm-m, too original",
        "Please, try again: "
    ],
    "def_body":
    ["Body*: ", "Concept without definition?", "Let's try again: "],
    "subject": ["Subject*: ", "Math?", "Subject: "]
}


HELP_MESSAGE = """The script has two modes - adding and showing
Note: * means necessary
All default files are in './examples'
{add_def}\tAdd note to the base. Will ask:
\t<string>\t*what - concept, what should be defined
\t<string>\t*def_body - definition
\t<string>\t*subject - what subject
\t<integer>\tlecture - number of the lection
{from_file}\tAdd defs from json-file
\t-f <string>\tfile - file with definitions, 'example.json' by default
{latex}\t\Import definitions from latex
\t-s <string>\tsubject - subject of defs, 'Жизнь' by default
\t-f <string>\tfile - file with definitions, 'example_latex.tex' by default
\t\t\t\tWill add extension '.tex' if necessary
{show_random}\tShow random def from the base.
\t-s <string>\tsubject - subject of random def, 'all' by default
{export}\t\tExport definitions to latex, result in './exported/'
\t-s <string>\tsubject - subject of defs, 'all' by default
\t-f <string>\tfile - file with definitions, 'exported.tex' by default
\t\t\t\tWill add extension '.tex' if necessary""".format(
    add_def=colored("add_def:", "green"),
    from_file=colored("from_file", "green"),
    latex=colored("latex", "green"),
    show_random=colored("show_random", "green"),
    export=colored("export", "green"))


tex_def = """\\begin{{definition}}[\\textbf{{{what}}}, №{lecture}]
    {def_body}
\\end{{definition}}

"""


tex_preamble = r"""\documentclass{article}
\usepackage[utf8x]{inputenc}
\usepackage[russian]{babel}
\usepackage{my_style} 
\pagestyle{plain}
\begin{document}
"""


def add_def() -> bool:
    """ Retrieves the definition from the user and
    enters it into the database.
    """
    logger.info("Start <add_def>")

    fields = ["what", "def_body", "subject"]
    fields_dict = {"what": '', "def_body": '', "subject": ''}

    for fi in fields:
        phrase = PHRASES[fi]
        fields_dict[fi] = input(colored(phrase[0], "green"))
        if not fields_dict[fi]:
            cprint(phrase[1], "green")
            fields_dict[fi] = input(colored(phrase[2], "green"))
            if not fields_dict[fi]:
                cprint("Mm-m, no - some help?..")
                return False

    lecture = input(colored("Lecture #", "green"))
    if (not lecture and lecture.isalnum()):
        cprint("Number of lecture must be integer, did you know that?",
               color="yellow")
        lecture = input(colored("Lecture #", "green"))
        if (not lecture and lecture.isalnum()):
            cprint("Mm-m, no - some help?..")
            return False

    # what = what.lower()
    lecture = int(lecture) if lecture else -1

    result = [
        fields_dict["what"], fields_dict["def_body"], fields_dict["subject"],
        lecture
    ]
    result[2] = result[2].capitalize()

    logger.info(f"Get what=<{result[0]}>")
    logger.debug(f"Get def_body=<{result[1]}>")
    logger.debug(f"Get subject=<{result[2]}>")
    logger.debug(f"Get lecture=<{result[3]}>")

    data_base.add_def(*result)
    cprint(f"All done! New definition of '{result[0]}' has been saved",
           color="green")

    return True


def read_from_file(file_name: str = "example.json"):
    """Read new defs from file."""
    logger.info(f"Start reading from the file <{file_name}>")
    if not file_name.endswith(".json"):
        file_name += ".json"
    with open(file_name, "r") as f_def:
        all_data = json.load(f_def)
        for fd in all_data:
            logger.info(f"Read def <{fd}>")
            info_def = all_data[fd]
            result = [fd, info_def["def_body"], info_def["subject"]]
            if "lecture" in all_data[fd]:
                result.append(all_data[fd]["lecture"])
            else:
                result.append(-1)

            logger.debug(f"Get def_body=<{result[1]}>")
            logger.debug(f"Get subject=<{result[2]}>")
            logger.debug(f"Get lecture=<{result[3]}>")

            data_base.add_def(*result)
            cprint(f"All done! New definition of '{fd}' has been saved",
                   color="green")


def read_from_latex(file_name: str = "example.tex", subject: str = "all"):
    """Read defs from latex file."""
    logger.info(f"Start parsing latex file <file_name>")
    if subject == "all":
        subject = "Жизнь"
    if not file_name.endswith(".tex"):
        file_name += ".tex"
        logger.info(f"Output file changed to <{file_name}>")

    with open(file_name, "r") as f_in:
        read_data = f_in.read()
        parsed = LatexWalker(read_data)
        nodelist, _, _ = parsed.get_latex_nodes(pos=0)
        main_nodes = nodelist[11].nodelist
        logger.debug("Parsed latex file")
        for m_node in main_nodes:
            if m_node.isNodeType(LatexEnvironmentNode) and \
                    m_node.environmentname == "definition":
                what, b, e, lecture = _proccess_one_latex_def(m_node)
                def_body = "\n".join(
                    map(lambda x: x.strip(),
                        read_data[b:e].split(sep="\n")[1:-1]))
                data_base.add_def(what, def_body, subject, lecture)

                cprint(f"All done! New definition of '{what}' has been saved",
                       color="green")
                logger.info(f"Read def <{what}>")
                logger.debug(f"Get def_body=<{def_body}>")
                logger.debug(f"Get subject=<{subject}>")
                logger.debug(f"Get lecture=<{lecture}>")


def _proccess_one_latex_def(env_node: LatexEnvironmentNode):
    """Proccess one def from latex, add to db."""
    what = env_node.nodeargd.argnlist[0].nodelist[0]
    what = what.nodeargd.argnlist[0].nodelist[0].chars
    lecture = int(env_node.nodeargd.argnlist[0].nodelist[1].chars[3:])
    def_begin, def_len = env_node.pos, env_node.len
    return what, def_begin, def_begin + def_len, lecture


def random_subject() -> str:
    """Choose random subject."""
    logger.info("Choose random subject")
    nu_subjects = data_base.nu_subjects()
    subj_nu = randint(1, nu_subjects)
    subject = data_base.get_subj(subj_nu)
    logger.info(f"Get <{subject}>")
    return subject


def random_def(subject: str = 'all'):
    """Choose random def from subject. ''=all"""
    logger.info(f"Let's choose random def from <{subject}>")
    nu_def = data_base.get_random_def_id(subject)
    logger.debug(f"<{nu_def}> was picked")

    res = data_base.get_abs_def(nu_def)
    if subject == 'all':
        subject = res[3]

    logger.info(f"Get <{res}>")

    de = latex_output.custom_latex_to_text(res[1])

    return f"{de}\n\t{res[0].capitalize()}, курс \"{subject}\"" + (
        f"#{res[2]}" if res[2] != -1 else '')


def export_latex(subject: str="all", to_exp: str="exported.tex"):
    """Export defs to latex  file."""
    logger.info(f"Begin export_latex to file <{to_exp}>")
    if not to_exp.endswith(".tex"):
        to_exp = to_exp + ".tex"
        logger.info(f"Output file changed to <{to_exp}>")
    all_data = data_base.get_defs(subject)
    with open("exported/" + to_exp, "w") as exp_file:
        exp_file.write(tex_preamble)
        section_subj = ""
        for one_def in all_data:
            what, def_body, cur_s, lecture = one_def
            if section_subj != cur_s:
                exp_file.write(f"\\section{{{cur_s}}}\n")
                section_subj = cur_s
            exp_file.write(tex_def.format(what=what,
                                          def_body=def_body,
                                          lecture=lecture))
            logger.debug(f"Export <{one_def}>")
        logger.info(f"Export all from <{subject}>")
        exp_file.write(r"\end{document}")
    print(f"Export all from <{subject}>")


def parse_arguments():
    """Parse arguments from terminal."""
    parser = ArgumentParser()
    parser.add_argument("command",
                        help="In what way",
                        choices=[
                            "add_def", "show_random", "from_file", "export",
                            "latex", "help"
                        ])
    parser.add_argument("-f",
                        "--file",
                        help="The file where to get the data from")
    parser.add_argument("-s", "--subject", help="Choose the subject if needed")
    parser.add_argument("-d",
                        "--data",
                        default=script_path + '/db_commands.sqlite',
                        help="Choose the data-base")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    logger = lg.getLogger("main")
    logger.setLevel(lg.DEBUG)
    script_path = os.path.realpath(__file__).rpartition('/')[0]
    fh = lg.FileHandler(script_path + "/logs.log")
    formatter = lg.Formatter(
        datefmt="%Y-%m-%d|%H:%M:%S",
        fmt='%(asctime)s: %(levelname)s - %(name)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    logger.info("Start session.")

    args_parsed = parse_arguments()
    command = args_parsed.command
    subject = args_parsed.subject if args_parsed.subject else "all"
    given_file = args_parsed.file

    data_base = dataAccess(args_parsed.data)

    if command == 'add_def':
        add_def()
    elif command == "show_random":
        cprint(random_def(subject), "yellow")
    elif command == "from_file":
        file_json = given_file if given_file else "examples/example.json"
        read_from_file(file_json)
    elif command == "export":
        file_exp = given_file if given_file else "exported.tex"
        export_latex(subject, file_exp)
    elif command == "latex":
        file_latex = given_file if given_file else "examples/example_latex.tex"
        read_from_latex(file_latex, subject)
    else:
        print(HELP_MESSAGE)

    logger.info("End session.")
