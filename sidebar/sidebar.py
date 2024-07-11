from .sidebar_constructor import CompositeElement, LeafElement, CompositeHtml, LeafHtml
from .icons import Icons

menu = CompositeElement(CompositeHtml(title='Composite Menu', icon=Icons.fa_play_circle))

submenu_1 = LeafElement(LeafHtml(title="Leaf Menu", link='http://google.com'))

menu.add(submenu_1)
