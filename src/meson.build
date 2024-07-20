pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'cute_script'
gnome = import('gnome')

blueprints = custom_target('blueprints',
  input: files(
    'gtk/help-overlay.blp',
    'window.blp',
    'script_row.blp',
  ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)
gnome.compile_resources('cute-script',
  'cute-script.gresource.xml',
  gresource_bundle: true,
  install: true,
  dependencies: blueprints,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'cute-script.in',
  output: 'cute-script',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr-xr-x'
)

cute_script_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'metadata.py',
  'script_row.py',
  'script_monitor.py',
]

install_data(cute_script_sources, install_dir: moduledir)
