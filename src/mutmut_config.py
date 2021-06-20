# Config for the mutmut: https://mutmut.readthedocs.io/en/latest/#whitelisting


NO_MUTATIONS_FILES = ["test", "init"]


NO_MUTATIONS_LINES = ["log"]


def pre_mutation(context):
    for no_mutations_filename_prefix in NO_MUTATIONS_FILES:
        if context.filename.find(no_mutations_filename_prefix) != -1:
            context.skip = True

    if not context.skip:
        line = context.current_source_line.strip()
        for no_mutations_line_prefix in NO_MUTATIONS_LINES:
            if line.startswith(no_mutations_line_prefix):
                context.skip = True
