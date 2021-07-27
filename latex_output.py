"""Custom text output for latex."""


from pylatexenc import latexwalker, latex2text, macrospec


lw_context_db = latexwalker.get_default_latex_context_db()
lw_context_db.add_context_category(
    'my-quotes',
    prepend=True,
    macros=[
        macrospec.MacroSpec("dd", "{{"),
    ],
)


def _get_optional_arg(node, default, l2tobj):
    """Helper that returns the `node` converted to text, or `default`
    if the node is `None` (e.g. an optional argument that was not
    specified)"""
    if node is None:
        return default
    return l2tobj.nodelist_to_text([node])


def partial_derivative(n, l2tobj):
    """Get the text replacement for the macro \dd"""
    if not n.nodeargd:
        return ''

    first = _get_optional_arg(n.nodeargd.argnlist[0],"f", l2tobj)
    second = _get_optional_arg(n.nodeargd.argnlist[1], "x", l2tobj)

    result = " <\\frac{{\partial {f}}}{{\partial {s}}}> ".format(
        f=first, s=second)
    return custom_latex_to_text(result)


l2t_context_db = latex2text.get_default_latex_context_db()
l2t_context_db.add_context_category(
    'my-quotes',
    prepend=True,
    macros=[
        latex2text.MacroTextSpec("dd",
                                 simplify_repl=partial_derivative),
    ],
)


def custom_latex_to_text(input_latex):
    """The latex parser instance with custom latex_context"""
    lw_obj = latexwalker.LatexWalker(input_latex, latex_context=lw_context_db)
    nodelist, _, _ = lw_obj.get_latex_nodes()
    l2t_obj = latex2text.LatexNodes2Text(latex_context=l2t_context_db,
                                         keep_braced_groups=True,
                                         keep_braced_groups_minlen=2)
    return l2t_obj.nodelist_to_text(nodelist)
