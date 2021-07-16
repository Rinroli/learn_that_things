"""Date base commands."""

create_table_subjects = """
CREATE TABLE IF NOT EXISTS subjects (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  subject TEXT NOT NULL UNIQUE,
  nu_defs INTEGER DEFAULT 0
);
"""

create_table_defs = """
CREATE TABLE IF NOT EXISTS defs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  rel_index INTEGER NOT NULL,
  what TEXT NOT NULL,
  def_body TEXT NOT NULL,
  subject TEXT NOT NULL,
  lecture INTEGER,
  FOREIGN KEY (subject) REFERENCES subjects (subject)
);
"""

add_new_def = """
INSERT INTO
  defs (rel_index, what, def_body, subject, lecture)
VALUES
  ({rel_index},
  '{what}',
  '{def_body}',
  '{subject}',
  {lecture});
"""

add_one_to_subject = """
UPDATE subjects
SET nu_defs = nu_defs + 1
WHERE subject = '{subject}';
"""

new_subject = """
INSERT INTO
  subjects (subject)
VALUES
  ('{subject}');
"""

nu_defs_by_subj = """
SELECT nu_defs
FROM subjects
WHERE subject = '{subject}';
"""

get_def = """
SELECT what, def_body, lecture, id
FROM defs
WHERE rel_index = {rel_ind} AND subject = '{subj}';
"""

get_abs_def = """
SELECT what, def_body, lecture, subject, rel_index
FROM defs
WHERE id = {id};
"""

get_subj = """
SELECT subject
FROM subjects
WHERE id = {id};
"""

get_subj_id = """
SELECT id
FROM defs
WHERE subject = '{subj}';
"""

get_all_id = """
SELECT id
FROM defs;
"""

nu_subjects = """
SELECT COUNT(*) FROM subjects;
"""

nu_defs = """
SELECT COUNT(*) FROM defs;
"""