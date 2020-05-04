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
data['rama'] = []
data['omega'] = []
data['rota'] = [('A', '   4 ', 'SER', 0.14985483750595746, (-22.314, -8.697, -11.1)), ('A', '  63 ', 'GLU', 0.0007401075673568776, (11.623000000000005, 4.072, -10.28)), ('A', ' 118 ', 'GLN', 0.1276309342716607, (-14.820999999999998, 4.415, -1.055)), ('A', ' 124 ', 'LYS', 0.18746525882256723, (-19.819000000000003, 2.308, -10.347)), ('A', ' 156 ', 'CYS', 0.1959417521824297, (-4.865, -6.046, 6.345)), ('A', ' 159 ', 'GLU', 0.03038855277781889, (-4.096000000000001, 2.539, 4.535)), ('A', ' 176 ', 'GLU', 0.03387686606565943, (-21.07, -19.587, 6.023999999999999)), ('A', ' 179 ', 'ASN', 0.15333810375345994, (-20.103, -12.046, 3.851)), ('A', ' 192 ', 'GLU', 0.0, (-0.19400000000000012, -20.63, -11.226)), ('A', ' 195 ', 'MET', 0.10387040217990627, (-7.256, -18.86199999999999, -9.587)), ('A', ' 199 ', 'VAL', 0.08621687225798355, (-7.935999999999999, -13.291, -6.561)), ('B', '   3 ', 'ARG', 0.0, (-45.671000000000014, -18.865999999999996, -33.043)), ('B', '  47 ', 'SER', 0.054144874777055416, (-21.938999999999997, -20.076, -17.16)), ('B', '  87 ', 'GLU', 0.2745015210226747, (-15.379000000000005, -19.058, -12.721)), ('B', '  94 ', 'THR', 0.00804527490691628, (-5.86, -19.601, -26.15)), ('B', ' 118 ', 'GLN', 0.003179017771128272, (-35.478, -29.885000000000005, -41.447)), ('B', ' 120 ', 'LYS', 2.0447493343559526e-06, (-39.926000000000016, -27.981, -39.013)), ('B', ' 124 ', 'LYS', 0.20190044965987183, (-40.33100000000001, -28.307, -32.503)), ('B', ' 129 ', 'VAL', 0.1747719634473414, (-36.20600000000001, -28.637999999999998, -25.284)), ('B', ' 156 ', 'CYS', 0.12157603440677497, (-25.703000000000003, -18.822999999999993, -48.55299999999999)), ('B', ' 158 ', 'SER', 0.004019992775283754, (-27.248000000000008, -25.027, -46.41599999999999)), ('B', ' 192 ', 'GLU', 0.13163211106746103, (-21.081000000000003, -4.813999999999998, -30.218999999999994))]
data['cbeta'] = [('A', '  87 ', 'GLU', ' ', 0.2648713028889561, (4.736000000000001, -8.534000000000002, -29.864)), ('A', ' 109 ', 'ASP', ' ', 0.29008494163745335, (-4.081, 7.680999999999998, -21.814)), ('A', ' 155 ', 'ASP', ' ', 0.2594415720959218, (-3.498000000000001, -7.609, 10.858999999999998)), ('B', '  57 ', 'SER', ' ', 0.36848856416665965, (-12.901, -31.834999999999997, -26.043)), ('B', ' 168 ', 'VAL', ' ', 0.2762620081353161, (-31.741000000000014, -18.212999999999997, -27.625999999999994))]
data['probe'] = [(' A 173  GLU  O  ', ' A 180  ASN  HB2', -0.899, (-21.065, -15.381, -1.67)), (' B   3  ARG  H  ', ' B   3  ARG  NE ', -0.822, (-47.074, -19.441, -31.835)), (' B 173  GLU  OE1', ' B 200  LYS  NZ ', -0.715, (-36.03, -7.799, -35.879)), (' A 173  GLU  O  ', ' A 180  ASN  CB ', -0.711, (-21.59, -14.56, -0.749)), (' B 117  LYS  HD2', ' B 213  SER  O  ', -0.66, (-28.139, -31.993, -40.656)), (' A 148  GLU  OE1', ' B 104  TYR  OH ', -0.618, (-10.166, -24.255, -5.176)), (' B   3  ARG  H  ', ' B   3  ARG  HE ', -0.605, (-47.7, -20.13, -31.743)), (' B  70  MET  O  ', ' B  73  ALA  HB3', -0.593, (-19.939, -30.492, -28.702)), (' A   1  ALA  N  ', ' A 401  HOH  O  ', -0.593, (-27.349, 1.193, -10.45)), (' A 157  SER  HB3', ' A 160  ASP  HB2', -0.577, (-2.173, -1.721, 5.74)), (' B 163  HIS  CD2', ' B 165  VAL HG13', -0.558, (-22.304, -19.234, -35.386)), (' B   7  TRP  CE2', ' B 130  GLY  HA2', -0.556, (-36.357, -23.885, -25.129)), (' B   3  ARG  CZ ', ' B   3  ARG  H  ', -0.52, (-47.551, -18.846, -31.188)), (' B   2  PRO  HA ', ' B   3  ARG HH21', -0.518, (-47.136, -20.82, -30.276)), (' A 192  GLU  CD ', ' A 192  GLU  H  ', -0.514, (1.077, -19.37, -12.811)), (' B 185  VAL  HB ', ' B 199  VAL HG13', -0.507, (-28.484, -15.65, -35.022)), (' B   5  VAL HG23', ' B 170  TYR  CZ ', -0.503, (-40.961, -20.643, -30.852)), (' B   3  ARG  N  ', ' B   3  ARG  NE ', -0.5, (-47.095, -19.177, -32.076)), (' B 136  ILE  CG2', ' B 211  ILE HD12', -0.493, (-28.125, -21.24, -38.33)), (' A  52  ASN  C  ', ' A  52  ASN HD22', -0.489, (8.188, 2.294, -21.748)), (' B 118  GLN  HG2', ' B 121  ALA  H  ', -0.489, (-37.793, -30.057, -39.466)), (' B   5  VAL HG23', ' B 170  TYR  CE2', -0.488, (-40.45, -21.031, -31.226)), (' B 158  SER  HA ', ' B 210  GLY  N  ', -0.469, (-27.263, -23.885, -45.06)), (' A   7  TRP  CE2', ' A 130  GLY  HA2', -0.468, (-15.341, -2.348, -17.521)), (' A 175  THR  OG1', ' A 180  ASN  HB3', -0.463, (-20.471, -15.663, 1.657)), (' A 183  TRP  CD1', ' A 203  LYS  HB2', -0.461, (-14.781, -5.681, -3.363)), (' B  69  LEU HD12', ' B  72  TYR  CZ ', -0.451, (-16.485, -33.791, -34.91)), (' A 173  GLU  OE1', ' A 200  LYS  NZ ', -0.447, (-16.122, -17.302, -6.025)), (' B   7  TRP  NE1', ' B 130  GLY  HA2', -0.444, (-35.906, -23.684, -25.56)), (' B  25  CYS  SG ', ' B 301  C7T  N30', -0.443, (-16.063, -21.301, -34.846)), (' B   3  ARG  HE ', ' B   3  ARG  N  ', -0.442, (-47.217, -19.971, -31.931)), (' A  17  LYS  HD2', ' A 447  HOH  O  ', -0.441, (2.976, -9.544, -20.561)), (' A 179  ASN  HA ', ' A 179  ASN HD22', -0.437, (-20.753, -10.492, 3.584)), (' A 301  C7T  C28', ' A 301  C7T  C4 ', -0.432, (0.515, 3.479, -2.846)), (' B  35  GLU  HG3', ' B  48  LEU  HG ', -0.431, (-22.897, -23.735, -18.976)), (' B 153  GLU  H  ', ' B 208  HIS  CE1', -0.428, (-29.437, -15.828, -46.703)), (' B 101  ASN  HA ', ' B 102  PRO  HD2', -0.426, (-9.761, -31.932, -11.739)), (' A   9  GLU  HB2', ' B  17  LYS  HD2', -0.426, (-18.536, -14.058, -21.44)), (' B  70  MET  HG2', ' B 133  SER  HB3', -0.425, (-23.49, -26.617, -30.938)), (' A 195  MET  HB3', ' A 195  MET  HE2', -0.41, (-9.922, -19.762, -9.606)), (' B 158  SER  HA ', ' B 210  GLY  CA ', -0.407, (-27.471, -24.507, -44.441)), (' B 115  ILE HD12', ' B 132  ILE HG21', -0.401, (-31.348, -28.443, -32.356)), (' B 163  HIS  CD2', ' B 165  VAL  CG1', -0.4, (-22.656, -18.639, -35.596))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
