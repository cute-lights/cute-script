from gi.repository import GObject, Adw, GLib
from subprocess import Popen

class ScriptMonitor(GObject.Object):
    __gtype_name__ = "ScriptMonitor"
    proc = None
    script_name = GObject.Property(type=str, default="")


    def __init__(self):
        super().__init__()

    def connect_script_change(self, cb: callable):
        self.connect("notify::script-name", cb)

    def start_script(self, script_name):
        self.stop_script()
        self.script_name = script_name
        self.proc = Popen(["python3", f"{GLib.get_user_config_dir()}/cute_lights/scripts/{script_name}"])
    
    def stop_script(self):
        if self.proc:
            self.proc.kill()
            self.proc = None
            self.script_name = ""

    def is_script_active(self, script_name):
        return self.script_name == script_name
    
    def get_active_script(self):
        return self.script_name

    @staticmethod
    def instance() -> 'ScriptMonitor':
        app = Adw.Application.get_default()
        if not app:
            return None
        return app.script_monitor