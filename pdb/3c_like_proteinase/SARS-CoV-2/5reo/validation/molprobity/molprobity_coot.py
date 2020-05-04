# script auto-generated by phenix.molprobity


from __future__ import absolute_import, division, print_function
from six.moves import cPickle as pickle
from six.moves import range
try :
  import gobject
except ImportError :
  gobject = None
import sys

class coot_extension_gui(object):
  def __init__(self, title):
    import gtk
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    scrolled_win = gtk.ScrolledWindow()
    self.outside_vbox = gtk.VBox(False, 2)
    self.inside_vbox = gtk.VBox(False, 0)
    self.window.set_title(title)
    self.inside_vbox.set_border_width(0)
    self.window.add(self.outside_vbox)
    self.outside_vbox.pack_start(scrolled_win, True, True, 0)
    scrolled_win.add_with_viewport(self.inside_vbox)
    scrolled_win.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

  def finish_window(self):
    import gtk
    self.outside_vbox.set_border_width(2)
    ok_button = gtk.Button("  Close  ")
    self.outside_vbox.pack_end(ok_button, False, False, 0)
    ok_button.connect("clicked", lambda b: self.destroy_window())
    self.window.connect("delete_event", lambda a, b: self.destroy_window())
    self.window.show_all()

  def destroy_window(self, *args):
    self.window.destroy()
    self.window = None

  def confirm_data(self, data):
    for data_key in self.data_keys :
      outlier_list = data.get(data_key)
      if outlier_list is not None and len(outlier_list) > 0 :
        return True
    return False

  def create_property_lists(self, data):
    import gtk
    for data_key in self.data_keys :
      outlier_list = data[data_key]
      if outlier_list is None or len(outlier_list) == 0 :
        continue
      else :
        frame = gtk.Frame(self.data_titles[data_key])
        vbox = gtk.VBox(False, 2)
        frame.set_border_width(6)
        frame.add(vbox)
        self.add_top_widgets(data_key, vbox)
        self.inside_vbox.pack_start(frame, False, False, 5)
        list_obj = residue_properties_list(
          columns=self.data_names[data_key],
          column_types=self.data_types[data_key],
          rows=outlier_list,
          box=vbox)

# Molprobity result viewer
class coot_molprobity_todo_list_gui(coot_extension_gui):
  data_keys = [ "rama", "rota", "cbeta", "probe" ]
  data_titles = { "rama"  : "Ramachandran outliers",
                  "rota"  : "Rotamer outliers",
                  "cbeta" : "C-beta outliers",
                  "probe" : "Severe clashes" }
  data_names = { "rama"  : ["Chain", "Residue", "Name", "Score"],
                 "rota"  : ["Chain", "Residue", "Name", "Score"],
                 "cbeta" : ["Chain", "Residue", "Name", "Conf.", "Deviation"],
                 "probe" : ["Atom 1", "Atom 2", "Overlap"] }
  if (gobject is not None):
    data_types = { "rama" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "rota" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "cbeta" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT],
                   "probe" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT] }
  else :
    data_types = dict([ (s, []) for s in ["rama","rota","cbeta","probe"] ])

  def __init__(self, data_file=None, data=None):
    assert ([data, data_file].count(None) == 1)
    if (data is None):
      data = load_pkl(data_file)
    if not self.confirm_data(data):
      return
    coot_extension_gui.__init__(self, "MolProbity to-do list")
    self.dots_btn = None
    self.dots2_btn = None
    self._overlaps_only = True
    self.window.set_default_size(420, 600)
    self.create_property_lists(data)
    self.finish_window()

  def add_top_widgets(self, data_key, box):
    import gtk
    if data_key == "probe" :
      hbox = gtk.HBox(False, 2)
      self.dots_btn = gtk.CheckButton("Show Probe dots")
      hbox.pack_start(self.dots_btn, False, False, 5)
      self.dots_btn.connect("toggled", self.toggle_probe_dots)
      self.dots2_btn = gtk.CheckButton("Overlaps only")
      hbox.pack_start(self.dots2_btn, False, False, 5)
      self.dots2_btn.connect("toggled", self.toggle_all_probe_dots)
      self.dots2_btn.set_active(True)
      self.toggle_probe_dots()
      box.pack_start(hbox, False, False, 0)

  def toggle_probe_dots(self, *args):
    if self.dots_btn is not None :
      show_dots = self.dots_btn.get_active()
      overlaps_only = self.dots2_btn.get_active()
      if show_dots :
        self.dots2_btn.set_sensitive(True)
      else :
        self.dots2_btn.set_sensitive(False)
      show_probe_dots(show_dots, overlaps_only)

  def toggle_all_probe_dots(self, *args):
    if self.dots2_btn is not None :
      self._overlaps_only = self.dots2_btn.get_active()
      self.toggle_probe_dots()

class rsc_todo_list_gui(coot_extension_gui):
  data_keys = ["by_res", "by_atom"]
  data_titles = ["Real-space correlation by residue",
                 "Real-space correlation by atom"]
  data_names = {}
  data_types = {}

class residue_properties_list(object):
  def __init__(self, columns, column_types, rows, box,
      default_size=(380,200)):
    assert len(columns) == (len(column_types) - 1)
    if (len(rows) > 0) and (len(rows[0]) != len(column_types)):
      raise RuntimeError("Wrong number of rows:\n%s" % str(rows[0]))
    import gtk
    self.liststore = gtk.ListStore(*column_types)
    self.listmodel = gtk.TreeModelSort(self.liststore)
    self.listctrl = gtk.TreeView(self.listmodel)
    self.listctrl.column = [None]*len(columns)
    self.listctrl.cell = [None]*len(columns)
    for i, column_label in enumerate(columns):
      cell = gtk.CellRendererText()
      column = gtk.TreeViewColumn(column_label)
      self.listctrl.append_column(column)
      column.set_sort_column_id(i)
      column.pack_start(cell, True)
      column.set_attributes(cell, text=i)
    self.listctrl.get_selection().set_mode(gtk.SELECTION_SINGLE)
    for row in rows :
      self.listmodel.get_model().append(row)
    self.listctrl.connect("cursor-changed", self.OnChange)
    sw = gtk.ScrolledWindow()
    w, h = default_size
    if len(rows) > 10 :
      sw.set_size_request(w, h)
    else :
      sw.set_size_request(w, 30 + (20 * len(rows)))
    sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    box.pack_start(sw, False, False, 5)
    inside_vbox = gtk.VBox(False, 0)
    sw.add(self.listctrl)

  def OnChange(self, treeview):
    import coot # import dependency
    selection = self.listctrl.get_selection()
    (model, tree_iter) = selection.get_selected()
    if tree_iter is not None :
      row = model[tree_iter]
      xyz = row[-1]
      if isinstance(xyz, tuple) and len(xyz) == 3 :
        set_rotation_centre(*xyz)
        set_zoom(30)
        graphics_draw()

def show_probe_dots(show_dots, overlaps_only):
  import coot # import dependency
  n_objects = number_of_generic_objects()
  sys.stdout.flush()
  if show_dots :
    for object_number in range(n_objects):
      obj_name = generic_object_name(object_number)
      if overlaps_only and not obj_name in ["small overlap", "bad overlap"] :
        sys.stdout.flush()
        set_display_generic_object(object_number, 0)
      else :
        set_display_generic_object(object_number, 1)
  else :
    sys.stdout.flush()
    for object_number in range(n_objects):
      set_display_generic_object(object_number, 0)

def load_pkl(file_name):
  pkl = open(file_name, "rb")
  data = pickle.load(pkl)
  pkl.close()
  return data

data = {}
data['rama'] = [('A', ' 154 ', 'TYR', 0.023852335676374112, (10.407, -11.497, -9.307))]
data['omega'] = []
data['rota'] = [('A', '   1 ', 'SER', 0.1865010235379422, (-2.011, 5.605, -16.399)), ('A', '  27 ', 'LEU', 0.22899980456906932, (5.755, -9.79, 19.126)), ('A', ' 217 ', 'ARG', 0.07462376691811758, (3.269000000000001, 18.68, -16.678))]
data['cbeta'] = []
data['probe'] = [(' A 110  GLN  HG3', ' A 689  HOH  O  ', -1.111, (19.237, 0.808, -1.694)), (' A 236  LYS  NZ ', ' A 501  HOH  O  ', -0.9, (14.8, 31.713, -0.304)), (' A 294  PHE  CD2', ' A 663  HOH  O  ', -0.854, (16.006, 3.09, -8.494)), (' A 217  ARG  NH2', ' A 502  HOH  O  ', -0.841, (3.694, 12.441, -22.026)), (' A 236  LYS  HD3', ' A 795  HOH  O  ', -0.654, (18.413, 29.036, -1.46)), (' A 288  GLU  OE1', ' A 503  HOH  O  ', -0.639, (5.652, 10.625, -1.469)), (' A 221 AASN  ND2', ' A 267  SER  HA ', -0.632, (11.374, 24.396, -13.456)), (' A 109  GLY  HA2', ' A 200  ILE HD13', -0.624, (14.781, 8.127, 0.048)), (' A 403  DMS  H23', ' A 654  HOH  O  ', -0.613, (3.341, -21.404, 7.118)), (' A 118  TYR  CE1', ' A 144  SER  HB3', -0.6, (1.772, -3.803, 15.424)), (' A  70  ALA  O  ', ' A  73 AVAL HG12', -0.6, (0.846, -22.84, 12.754)), (' A  19  GLN  NE2', ' A 119  ASN  HB3', -0.59, (0.057, -13.596, 18.503)), (' A 298  ARG  HG3', ' A 303  VAL  HB ', -0.554, (8.511, -3.662, -12.136)), (' A  69  GLN HE21', ' A  72  ASN  HA ', -0.543, (-1.766, -20.319, 16.904)), (' A 191  ALA  HA ', ' A 624  HOH  O  ', -0.535, (14.156, 9.737, 25.433)), (' A  19  GLN HE21', ' A 119  ASN  HB3', -0.517, (0.168, -13.152, 18.756)), (' A 191  ALA  CA ', ' A 624  HOH  O  ', -0.502, (14.52, 9.801, 25.76)), (' A 199  THR HG21', ' A 239  TYR  CZ ', -0.474, (12.165, 17.565, -1.6)), (' A 101  TYR  HA ', ' A 157  VAL  O  ', -0.466, (14.488, -13.259, -0.506)), (' A 104  VAL  O  ', ' A 160  CYS  HA ', -0.46, (17.914, -5.212, 4.213)), (' A  40  ARG  HA ', ' A  87  LEU  HG ', -0.457, (16.317, -11.52, 20.525)), (' A 236  LYS  HE3', ' A 237  TYR  CE2', -0.453, (15.027, 27.985, -0.777)), (' A  86  VAL HG13', ' A 179  GLY  HA2', -0.452, (18.651, -7.648, 14.14)), (' A 221 AASN HD21', ' A 267  SER  HA ', -0.436, (12.006, 24.525, -13.011)), (' A  19  GLN HE21', ' A 119  ASN  CB ', -0.434, (-0.126, -12.716, 18.557)), (' A 110  GLN  NE2', ' A 511  HOH  O  ', -0.422, (15.356, 1.097, -3.077)), (' A 294  PHE  HD2', ' A 663  HOH  O  ', -0.418, (15.893, 2.519, -7.186)), (' A  31  TRP  CD2', ' A  95  ASN  HB2', -0.414, (8.994, -21.355, 8.638)), (' A 114  VAL  O  ', ' A 125  VAL  HA ', -0.406, (2.49, -3.578, 4.69)), (' A  95  ASN  HB3', ' A  98  THR  OG1', -0.406, (10.265, -21.387, 5.746))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
