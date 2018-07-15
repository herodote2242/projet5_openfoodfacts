#!/usr/bin/env python3
# -*- coding: Utf-8 -*

from formater import MenuFormater


class MenuEntry:
    """ This class supports the creation of a menu as an object.
    """

    def __init__(self, id, label, handler, menu, data={}):
        self.id = id
        self.label = label
        self.handler = handler
        self.menu = menu
        self.data = data


class MenuManager:
    """This class is responsible for the management of a menu.
    """

    def __init__(self, menu):
        self.menu = menu

    def _input(self):
        """ Asks the user for an input and repeat the request until
        the answer is correct.
        """
        while True:
            answer = input(self.menu.message).lower().strip()
            if self.menu.is_valid(answer):
                return self.menu.get(answer)

    def ask(self, entries={}):
        """ This function is used to ensure the user's answer is
        saved and the proper handler is called.
        """
        menu_entry = self._input()
        # The user's input is saved.
        entries[menu_entry.menu.name] = menu_entry
        # The app calls the handler method for the chosen input.
        menu_entry.handler(entries)


class Menu:
    """ This class is reprensenting a menu.
    """

    def __init__(self, name, title="", prompt='--> ',
            formater=None, manager=None):
        self.name = name
        self.counter = 1
        self.title = title
        self.prompt = prompt
        # Numeric entries are auto-incremented numeric numbers.
        self.numeric_entries = {}
        # Keyword entries are represented by an alphabetical letter.
        self.keyword_entries = {}
        # The two classes Formater and Manager can be customized if needed.
        self.formater = formater if formater else MenuFormater()
        self.manager = manager if manager else MenuManager(self)

    def add(self, label, handler, id=None, data={}):
        """ Appends a new entry to the menu. The new entry is numeric by
        default.
        """
        if id is None:
            # Gets the next value and increment the counter.
            id = self.counter
            self.counter += 1
            self.numeric_entries[str(id)] = MenuEntry(
                id, label, handler, self, data)
        else:
            # Or uses the right letter for each menu option.
            self.keyword_entries[id] = MenuEntry(
                id, label, handler, self, data)

    def get(self, answer):
        """ Returns the MenuEntry corresponding to a given answer of
        the user.
        """
        return {**self.numeric_entries, **self.keyword_entries}.get(
            answer, None)

    def is_valid(self, answer):
        """Returns True if the user answer is a valid one.
        A valid answer is one that is present either in
        self.numberic_entries or in the self.keyword_entries dictionaries.
        """
        return answer in {**self.numeric_entries, **self.keyword_entries}

    @property
    def message(self):
        """Formats the menu. The message is prepared by an external
        formater that can be replaced by any class implementing the
        same interface as formaters.MenuFormater.
        """
        return self.formater.format(self)
