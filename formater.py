#!/usr/bin/env python3
# -*- coding: Utf-8 -*


class MenuFormater:
    """This class formats the different menus of
    the application through the same structure."""

    def _init_(self, menu):
        self.menu = menu

    def format(self, menu):
        # Menu's title is displayed, and the different options related to it.
        lines = [f'--- {menu.title} ---']
        lines.extend(f'{k} => {v.label}' for k,
            v in menu.numeric_entries.items())
        lines.extend(f'{k} => {v.label}' for k,
            v in menu.keyword_entries.items())
        lines.append(menu.prompt)
        return '\n'.join(lines)
