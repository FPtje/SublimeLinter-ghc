#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Jon Surrell
# Copyright (c) 2013 Jon Surrell
#
# License: MIT
#
# Edited by FPtje

"""This module exports the Ghc plugin class."""

from SublimeLinter.lint import Linter, util
from os.path import basename
import re



class Ghc(Linter):
    """Provides an interface to ghc."""

    syntax = ('haskell', 'haskell-sublimehaskell', 'literate haskell')
    cmd = 'ghcLint.sh @'
    regex = (
        r'^(?P<filename>.+?):'
        r'(?P<line>\d+):(?P<col>\d+):'
        r'\s+((?P<warning>warning:)|(?P<error>error:))?[^\n]*\s+(?P<message>.+)$'
    )
    multiline = True
    # re_flags = re.DOTALL

    # No stdin
    # tempfile_suffix = {
    #     'haskell': 'hs',
    #     'haskell-sublimehaskell': 'hs',
    #     'literate haskell': 'lhs'
    # }

    # ghc writes errors to STDERR
    error_stream = util.STREAM_STDERR

    def split_match(self, match):
        """Override to ignore errors reported in imported files."""
        match, line, col, error, warning, message, near = (
            super().split_match(match)
        )

        match_filename = basename(match.groupdict()['filename'])
        linted_filename = basename(self.filename)

        if match_filename != linted_filename:
            return None, None, None, None, None, '', None

        return match, line, col, error, warning, message, near
