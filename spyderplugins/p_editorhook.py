"""
EditorHook Plugin

    - Basic implementation of Hello World plugin
    - Shows example of how to add Hello World to the menu, e.g.
        Run -> Hello World
    - Also adds a EditorHook item to theConfiguration Page, e.g.
        Tools -> Preferences
"""

from spyderlib.qt.QtGui import QVBoxLayout, QGroupBox, QLabel
from spyderlib.qt.QtCore import SIGNAL

# Local imports
from spyderlib.baseconfig import get_translation
_ = get_translation("p_editorhook", dirname="spyderplugins")
from spyderlib.utils.qthelpers import get_icon, create_action
from spyderlib.plugins import SpyderPluginMixin, PluginConfigPage

from spyderplugins.widgets.editorhookgui import EditorHookWidget


class EditorHookConfigPage(PluginConfigPage):
    """
    The Configuration Page that can be found under Tools -> Preferences. This
    only displays a label.
    """

    def setup_page(self):
        """ Setup of the configuration page. All widgets need to be added here"""

        setup_group = QGroupBox(_("EditorHook Plugin Configuration"))
        setup_label = QLabel(_("EditorHook plugin configuration needs to be "\
                               "implemented here.\n"))
        setup_label.setWordWrap(True)

        # Warning: do not try to regroup the following QLabel contents with
        # widgets above -- this string was isolated here in a single QLabel
        # on purpose: to fix Issue 863
        setup_layout = QVBoxLayout()
        setup_layout.addWidget(setup_label)
        setup_group.setLayout(setup_layout)

        vlayout = QVBoxLayout()
        vlayout.addWidget(setup_group)
        vlayout.addStretch(1)
        self.setLayout(vlayout)

class EditorHook(EditorHookWidget, SpyderPluginMixin):
    """EditorHook class that implements all the SpyderPluginMixin methods"""
    CONF_SECTION = 'editorhook'
    CONFIGWIDGET_CLASS = EditorHookConfigPage

    def __init__(self, parent=None):
        EditorHookWidget.__init__(self, parent=parent,
                              max_entries=self.get_option('max_entries', 50))
        SpyderPluginMixin.__init__(self, parent)

        # Initialize plugin
        self.initialize_plugin()

    #------ SpyderPluginWidget API ---------------------------------------------
    def get_plugin_title(self):
        """Return widget title"""
        return _("EditorHook")

    def get_plugin_icon(self):
        """Return widget icon"""
        return get_icon('editorhook.png')

    def get_focus_widget(self):
        """
        Return the widget to give focus to when
        this plugin's dockwidget is raised on top-level
        """
        #return self.datatree\
        pass

    def get_plugin_actions(self):
        """Return a list of actions related to plugin"""
        return []

    def on_first_registration(self):
        """Action to be performed on first plugin registration"""
        self.main.tabify_plugins(self.main.inspector, self)
        self.dockwidget.hide()
        #pass

    def register_plugin(self):
        """Register plugin in Spyder's main window"""
        self.connect(self, SIGNAL("edit_goto(QString,int,QString)"),
                     self.main.editor.load)
        self.connect(self, SIGNAL('redirect_stdio(bool)'),
                     self.main.redirect_internalshell_stdio)
        self.main.add_dockwidget(self)

        editorhook_act = create_action(self, _("Hello World"),
                                     icon=get_icon('editorhook.png'),
                                     triggered=self.show)
        editorhook_act.setEnabled(True)
        self.register_shortcut(editorhook_act, context="EditorHook",
                               name="Run editorhook", default="F10")

        self.main.run_menu_actions += [editorhook_act]
        self.main.editor.pythonfile_dependent_actions += [editorhook_act]

    def refresh_plugin(self):
        """Refresh editorhook widget"""
        #self.remove_obsolete_items()  # FIXME: not implemented yet
        pass

    def closing_plugin(self, cancelable=False):
        """Perform actions before parent main window is closed"""
        return True

    def apply_plugin_settings(self, options):
        """Apply configuration file's plugin settings"""
        # The history depth option will be applied at
        # next Spyder startup, which is soon enough
        pass

    def show(self):
        """Show the editorhook dockwidget"""
        if self.dockwidget and not self.ismaximized:
            self.dockwidget.setVisible(True)
            self.dockwidget.setFocus()
            self.dockwidget.raise_()

    #------ Public API ---------------------------------------------------------

    # Insert text into the editor window
    def insertText(self, text):
      print(self.main.editor)


#===============================================================================
# The following statements are required to register this 3rd party plugin:
#===============================================================================
PLUGIN_CLASS = EditorHook