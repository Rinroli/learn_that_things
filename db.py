#!/usr/bin/env python3
"""Add new definition to the base."""

from sqlite3 import connect as sql_connect
from sqlite3 import Error as sql_error
from termcolor import cprint
from random import choice

import logging as lg
import os

import db_commands as dbc


class dataAccess:
    """Provide access to DB."""
    def __init__(self, path: str = './db_commands.sqlite') -> None:
        self.logger = lg.getLogger("main.db")
        self.logger.info("Init dataAccess")
        self.con = None
        try:
            self.con = sql_connect(
                os.path.realpath(__file__).rpartition('/')[0] + \
                    "/db_commands.sqlite")
        except sql_error as e:
            print("Error {}".format(e))
        self._create_tables()

    def _execute_query(self, query):
        """Execute the query on SQL."""
        if __name__ == '__main__':
            cprint(query, color="blue")

        cursor = self.con.cursor()
        cursor.execute(query)
        self.con.commit()

    def _read_info(self, query):
        """Read info from db."""
        if __name__ == '__main__':
            cprint(query, color="green")

        cursor = self.con.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except sql_error as e:
            print("Error {}".format(e))

    def _create_tables(self):
        """Create the initial tables main and notes."""
        self._execute_query(dbc.create_table_subjects)
        self._execute_query(dbc.create_table_defs)
        self.logger.info("Tables created (if it was necessary)")

    def add_def(self, what: str, def_body: str, subject: str, lecture: int):
        """Create new def with given fields."""
        try:
            self._execute_query(dbc.new_subject.format(subject=subject))
            self.logger.info(f"New subject <{subject}>")
        except Exception as e:
            self.logger.debug(f"Already exists <{subject}>")

        rel_index = self.nu_by_subject(subject) + 1
        self._execute_query(
            dbc.add_new_def.format(what=what,
                                   def_body=def_body,
                                   subject=subject,
                                   lecture=lecture,
                                   rel_index=rel_index))
        self._execute_query(dbc.add_one_to_subject.format(subject=subject))
        self.logger.info(f"Add new def, relative index #{rel_index}")

    def nu_by_subject(self, subject: str) -> int:
        """Number of defs by subject."""
        result = self._read_info(dbc.nu_defs_by_subj.format(subject=subject))
        print(result)
        if result:
            return len(result)
        return 0

    def get_def(self, nu_def: int, subj: str) -> str:
        """Get def by number (relative) and subject."""
        result = self._read_info(dbc.get_def.format(rel_ind=nu_def, subj=subj))
        if result:
            return result[0]
        return ''

    def get_abs_def(self, nu_def: int) -> str:
        result = self._read_info(dbc.get_abs_def.format(id=nu_def))
        if result:
            return result[0]
        return ''

    def get_subj(self, subj_nu: int):
        """Get subject by number."""
        result = self._read_info(dbc.get_subj.format(id=subj_nu))
        if result:
            return result[0][0]
        return ''

    def get_random_def_id(self, subject="all"):
        """Return random def id by subject or not."""
        if subject == "all":
            indexes = self._read_info(dbc.get_all_id)
        else:
            indexes = self._read_info(dbc.get_subj_id.format(subject=subject))
        if not indexes:
            self.logger.info("There are no suitable defs")
            return -1

        picked = choice(indexes)[0]
        self.logger.info(f"Pick def#{picked} from <{subject}>")
        return picked

    def nu_subjects(self) -> int:
        """Return number of subjects in the db."""
        return self._read_info(dbc.nu_subjects)[0][0]

    def nu_defs(self) -> int:
        """Return number of defs in the db."""
        return self._read_info(dbc.nu_defs)[0][0]
