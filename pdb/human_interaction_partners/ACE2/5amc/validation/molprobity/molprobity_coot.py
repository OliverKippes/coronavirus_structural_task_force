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
data['rama'] = [('A', '  45 ', 'ASN', 0.02150627172393238, (-10.728000000000012, 22.36499999999999, -43.91000000000001)), ('B', '  45 ', 'ASN', 0.0150295665216109, (13.609000000000004, 51.469, 26.656))]
data['omega'] = [('A', ' 141 ', 'PRO', None, (4.073999999999991, 26.041, -40.41600000000001)), ('A', ' 608 ', 'PRO', None, (10.879999999999988, 47.697999999999986, -34.228)), ('B', ' 141 ', 'PRO', None, (9.122, 60.538999999999994, 14.5)), ('B', ' 608 ', 'PRO', None, (20.056999999999995, 59.946, -6.311000000000002))]
data['rota'] = [('A', '   9 ', 'GLN', 0.03594030686589249, (-38.58000000000001, 3.424999999999999, -20.501000000000005)), ('A', ' 133 ', 'THR', 0.15479646354247426, (4.6869999999999905, 43.55, -47.423)), ('A', ' 372 ', 'TYR', 0.06622863824650713, (-10.437000000000005, -0.4890000000000003, -26.187)), ('A', ' 388 ', 'HIS', 0.1152263832542189, (-3.7440000000000095, 8.567999999999998, -22.597)), ('B', ' 151 ', 'ARG', 0.13660419365715318, (4.818999999999994, 67.073, -2.202)), ('B', ' 368 ', 'TYR', 0.2633576216340826, (-12.117999999999995, 46.67000000000001, 26.819)), ('B', ' 372 ', 'TYR', 0.036636655686869725, (-13.601000000000004, 42.479, 31.202)), ('B', ' 388 ', 'HIS', 0.049551356471871325, (-10.793999999999999, 44.713999999999984, 20.031000000000006)), ('B', ' 421 ', 'ASP', 0.23355063044643312, (-21.207000000000004, 66.28299999999999, 2.871000000000001))]
data['cbeta'] = []
data['probe'] = [(' A 365  HIS  HD1', ' A 388  HIS  HD2', -0.743, (-4.201, 9.099, -26.485)), (' A 365  HIS  HD1', ' A 388  HIS  CD2', -0.706, (-4.676, 8.705, -26.246)), (' A 157  LEU HD11', ' A 477  VAL HG13', -0.69, (9.78, 41.951, -27.877)), (' B 350  ARG  H  ', ' B 355  GLN HE21', -0.638, (0.727, 61.885, 17.651)), (' B 124  THR HG22', ' B 327  GLU  CG ', -0.595, (15.81, 52.125, 19.105)), (' B 206  THR HG23', ' B 210  ASP  OD2', -0.56, (-17.874, 32.382, 6.487)), (' B 365  HIS  HD1', ' B 388  HIS  CD2', -0.554, (-8.357, 46.238, 21.716)), (' B 124  THR HG22', ' B 327  GLU  HG2', -0.546, (16.595, 51.769, 19.296)), (' A 467  ARG HH11', ' A 471  GLN HE22', -0.538, (5.422, 29.154, -20.355)), (' A  12  ALA  O  ', ' A2006  HOH  O  ', -0.507, (-35.953, 2.259, -8.831)), (' A  81  GLN  HB2', ' A  82  GLN HE22', -0.504, (-24.164, 6.421, -4.468)), (' A 157  LEU HD13', ' A 476  PRO  HB2', -0.499, (11.394, 39.908, -26.976)), (' B 157  LEU HD11', ' B 477  VAL HG13', -0.499, (12.149, 54.804, -6.096)), (' A 372  TYR  OH ', ' A 388  HIS  HE1', -0.494, (-8.989, 6.496, -25.682)), (' A 206  THR HG23', ' A 210  ASP  OD2', -0.482, (-3.751, 12.779, -3.761)), (' B 365  HIS  HD1', ' B 388  HIS  HD2', -0.475, (-8.84, 46.337, 22.062)), (' B  31  VAL  O  ', ' B  34  GLN  HG3', -0.474, (4.629, 36.253, 33.92)), (' B  99  GLY  HA2', ' B 186  TYR  CE1', -0.469, (1.483, 27.408, 19.599)), (' A 501  TYR  CD1', ' A 907  NIY  HB2', -0.464, (0.825, 17.221, -23.298)), (' A 270  PRO  HD3', ' A 426  LEU HD22', -0.45, (24.352, 19.42, -22.157)), (' A 270  PRO  HD3', ' A 426  LEU  CD2', -0.446, (23.764, 19.385, -22.242)), (' A  32  LEU HD12', ' A 377  VAL HG21', -0.444, (-19.926, 6.774, -28.028)), (' B  17  ALA  HB1', ' B  92  ILE HD11', -0.443, (-12.112, 21.562, 32.573)), (' A 274  LYS  HB3', ' A 275  PRO  CD ', -0.437, (29.645, 11.551, -28.197)), (' A  85  ASP  HB3', ' A  88  LEU  HB3', -0.436, (-23.105, -1.747, -13.198)), (' B  24  TYR  HD2', ' B  25  GLN  HG3', -0.425, (-6.961, 29.688, 34.095)), (' B 477  VAL HG12', ' B 603  LEU HD21', -0.417, (14.402, 54.379, -8.262)), (' B 501  TYR  CD1', ' B 907  NIY  HB2', -0.411, (-5.353, 47.718, 12.252)), (' B 157  LEU HD13', ' B 476  PRO  HB2', -0.408, (9.761, 56.166, -5.817)), (' B 124  THR HG22', ' B 327  GLU  HG3', -0.404, (15.624, 51.9, 19.301)), (' A  84  THR  HB ', ' A2007  HOH  O  ', -0.401, (-24.65, -5.597, -8.701))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
