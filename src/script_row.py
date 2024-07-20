from os import system
from gi.repository import Adw, GObject, Gtk, GLib
from .metadata import ScriptMetadata
from .script_monitor import ScriptMonitor
import subprocess


@Gtk.Template(resource_path="/io/github/cute_lights/CuteScript/script_row.ui")
class ScriptRow(Adw.PreferencesGroup):
    __gtype_name__ = "ScriptRow"

    name: str = GObject.Property(type=str, default="")
    description: str = GObject.Property(type=str, default="")
    script_name: str = GObject.Property(type=str, default="")
    is_active: bool = GObject.Property(type=bool, default=False)

    play_button: Gtk.Button = Gtk.Template.Child()
    edit_button: Gtk.Button = Gtk.Template.Child()

    def is_script_active(self):
        """Check if the script is active."""
        
        return ScriptMonitor.instance().is_script_active(self.script_name)

    def __init__(self, metadata: ScriptMetadata):
        super().__init__()
        self.name = metadata["name"]
        self.description = metadata["description"]
        self.script_name = metadata["script_name"]

        monitor = ScriptMonitor.instance()
        monitor.connect_script_change(self.on_active_script_changed)
        self.play_button.connect("clicked", self.on_play_button_clicked)
        self.edit_button.connect("clicked", self.on_edit_button_clicked)

    def on_play_button_clicked(self, button):
        monitor = ScriptMonitor.instance()
        if self.is_active:
            monitor.stop_script()
        else:
            monitor.start_script(self.script_name)

    def on_edit_button_clicked(self, button):
        GLib.spawn_command_line_async(
            f"xdg-open {GLib.get_user_config_dir()}/cute_lights/scripts/{self.script_name}"
        )

    def on_active_script_changed(self, app, _):
        if self.is_script_active() and not self.is_active:
            self.play_button.set_icon_name("media-playback-stop-symbolic")
            self.play_button.add_css_class("error")
            self.is_active = True
        else:
            self.play_button.set_icon_name("media-playback-start-symbolic")
            self.play_button.remove_css_class("error")
            self.is_active = False
