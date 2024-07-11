from __future__ import annotations

import uuid
import bs4
import itertools
import datetime

from typing import Union
from django.utils.safestring import mark_safe
from abc import ABC, abstractmethod

__all__ = ['CompositeHtml', 'LeafHtml', 'CompositeElement', 'LeafElement', 'DisPlayer']


class AbstractCompositeHtml(ABC):
    """
    Abstract Method used for MenuHtml Class
    """
    @abstractmethod
    def __init__(self, icon, title):
        self.icon = icon
        self.title = title

    @abstractmethod
    def base_html(self):
        pass

    @abstractmethod
    def insert(self, data):
        pass


class AbstractLeafHtml(ABC):
    """
    Abstract Method used for MenuHtml Class
    """
    @abstractmethod
    def __init__(self, icon, title):
        self.icon = icon
        self.title = title

    @abstractmethod
    def base_html(self):
        pass


class CompositeHtml(AbstractCompositeHtml):
    """
        Class which represents HTML for composite menu
        composite menu is defined as a menu which encapsulates other leaf menus.
        leaf menu is defined as a menu which being clicked redirect to a defined page
        example structure:
        < MENU >
           |
           |-- Tables                                     | COMPOSITE lvl menu  ( expand all below menus once pressed )
           |    |                                         |
           |    |-- Test results tables                   |   COMPOSITE lvl menu ( expand all below menus once pressed )
           |    |    |-- Sensors Test Results             |      | LEAF lvl menu ( redirect to link once pressed )
           |    |    |-- Hydraulic Test Results           |      | LEAF lvl menu ( redirect to link once pressed )
           |    |-- Test Specification tables             |   COMPOSITE lvl menu ( expand all below menus once pressed )
           |    |    |-- Sensors Test Specification       |      | LEAF lvl menu ( redirect to link once pressed )
           |    |    |-- Hydraulic Test Specification     |      | LEAF lvl menu ( redirect to link once pressed )

    """
    def __init__(self, icon='NA', title='NA'):
        """
        Constructor
        self.html represents html object which must contain html attribute pointing to html string
        :param icon: Icon string; e.g. 'fas fa-home'
        :param title: Menu title
        """
        self.icon = icon
        self.title = title
        self.html = self.base_html()

    def base_html(self):
        """
        Equivalent with:
        >>>identification = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
        >>>s = '<li class="nav-item">' \
                '<a data-toggle="collapse" href={hash_id} class="collapsed" aria-expanded="false">' \
                '<i class={icon}></i>' \
                '<p>{title}</p>' \
                '<span class="caret"></span>' \
                '</a>' \
                '<div class="collapse" id={id}>' \
                '<ul class="nav nav-collapse">' \
                '</ul>' \
                '</div>' \
                '</li>'.format(hash_id="#" + identification, id=identification, title=self.title)

        Method can be overwritten for custom html representation of menu
        :return: html as tag
        """
        id_ = str(uuid.uuid4())
        navigation = bs4.Tag(name='li')
        navigation['class'] = 'nav-item'
        link = bs4.Tag(name="a")
        link['data-toggle'] = 'collapse'
        link['href'] = "#" + id_
        link['class'] = 'collapsed'
        link['aria-expanded'] = 'false'
        icon = bs4.Tag(name='i')
        icon['class'] = self.icon
        title = bs4.Tag(name='p')
        title.insert(0, self.title)
        span = bs4.Tag(name='span')
        span['class'] = 'caret'
        link.insert(0, span)
        link.insert(0, title)
        link.insert(0, icon)
        main = bs4.Tag(name='div')
        main['class'] = 'collapse'
        main['id'] = id_
        ul = bs4.Tag(name='ul')
        ul['class'] = 'nav nav-collapse'
        main.insert(0, ul)

        navigation.insert(0, link)
        navigation.insert(1, main)

        return navigation

    def insert(self, data):
        """
        Method is designated to encapsulate HTML within HTML
        Method is used for adding sub menus to menu.

        If HTML representation os overwritten insert method overwriting is a must

        :param data: inserts data within html
        :return:
        """
        html = self.base_html()
        html.ul.insert(0, bs4.BeautifulSoup(data, features="html.parser"))
        return html.prettify()


class LeafHtml(AbstractLeafHtml):
    """
        Class which represents HTML for LEAF menu
        LEAF menu is defined as a menu which being clicked redirect to a defined page
    """
    def __init__(self, link='NA', title='NA'):
        """
        constructor shall remain unchanged.
        self.html represents html object which must contain html attribute pointing to html string
        :param link: link to page to be displayed when menu is clicked
        :param title: title of menu
        """
        self.link = link
        self.title = title
        self.html = self.base_html()

    def base_html(self):
        """
        Equivalent with:
        >>> s = '<li>' \
                '<a href={link}>' \
                '<span class="sub-item">{title}</span>' \
                '</a>' \
                '</li>'.format(link=self.link, title=self.title)

        Method can be overwritten for custom html representation of menu
        :return: html tag as string
        """
        item = bs4.Tag(name='li')
        link = bs4.Tag(name='a')
        link['href'] = self.link
        title = bs4.Tag(name='span')
        title['class'] = 'sub-item'
        title.insert(0, self.title)
        link.insert(0, title)
        item.insert(0, link)
        return item.prettify()


class LeafElement:
    """
        Class representing objects at the bottom or Leaf of the hierarchy tree.
    """

    def __init__(self, html: LeafHtml):
        """

        :param html: EndMenuHtml object or Custom object that has attribute
            - html -> pointing to html string
        """
        self.precedent = None
        self.html = html

    def menu_options(self):
        """
        :return: yield menu object
        """
        yield self

    @property
    def level(self):
        """
            return menu deep level
        :return: deep level
        """
        count = 0
        _ = self.precedent
        while hasattr(_, 'precedent'):
            _ = _.precedent
            count += 1
        return count

    def get_html(self):
        """

        :return: return leaf element as html
        """
        return self.html.html

    def print_title(self):
        """
            prints object title attribute
        :return: None
        """

        print(str(self), "\n")


class CompositeElement:
    """
        Class representing objects at any level of the hierarchy
        tree except for the bottom or leaf level. Maintains the child
        objects by adding and removing them from the tree structure.
    """

    def __init__(self, html: CompositeHtml):
        """
            Takes the first positional argument and assigns to member
            variable "position".
            Initializes a list of children elements.
            :param html: MenuHtml object or Custom object that has attribute
                - html -> pointing to html string
                - insert -> method designated to add Leaf or Composite element in current element
        """
        self.html = html
        self.children = list()
        self.precedent = None

    @property
    def level(self):
        """
            return menu deep level
            :return: deep level
        """

        count = 0
        _ = self.precedent
        while hasattr(_, 'precedent'):
            _ = _.precedent
            count += 1
        return count

    def add(self, child: Union[CompositeElement, LeafElement]):
        """
            Adds the supplied child element to the list of children
            elements "children"
        :param child:
        :return:
        """
        self.children.append(child)
        child.precedent = self

    def remove(self, child):
        """
            Removes the supplied child element from the list of
            children elements "children".'''
        :param child:
        :return:
        """
        self.children.remove(child)

    def menu_options(self):
        """
            Yield menu object; if children -> then yields their object too
        :return:
        """
        yield self
        for child in self.children:
            yield from child.menu_options()

    def print_title(self):
        """
            Traverse object tree and print objects title
            :return: None
        """
        print(str(self))
        for child in self.children:
            print("\t", end="")
            child.print_title()

    def get_html(self):
        result = ""
        for child in self.children:
            result += child.get_html() + "\n"
        result = self.html.insert(result)
        return result


class DisPlayer(list):
    """
        class which create HTML list and offer iterator for it
    """
    def __init__(self, other=None):
        super(DisPlayer, self).__init__()
        self.other = other or []
        if self.other:
            self.other = [mark_safe(item.get_html()) for item in self.other]

    def __len__(self):
        return list.__len__(self) + len(self.other)

    def __iter__(self):
        return itertools.chain(list.__iter__(self), iter(self.other))

    def __getitem__(self, index):
        length = list.__len__(self)

        if index > length:
            return self.other[index - length]
        else:
            return list.__getitem__(self, index)

    def append(self, value):
        """ Append object to the end of the list. """
        self.other.append(mark_safe(value.get_html()))
