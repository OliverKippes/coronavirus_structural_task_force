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
data['rama'] = [('B', '  46 ', 'SER', 0.03944574920221736, (-47.013999999999974, 11.129, -10.186))]
data['omega'] = []
data['rota'] = [('A', '   5 ', 'LYS', 0.0802776064514134, (-32.30099999999999, -37.47299999999999, 45.244)), ('A', '  92 ', 'ASP', 0.2612581152964046, (-60.237999999999964, -64.475, 45.613)), ('A', ' 128 ', 'CYS', 0.10329543602539916, (-33.25499999999999, -44.97099999999999, 40.44)), ('A', ' 167 ', 'LEU', 0.0, (-25.89699999999999, -59.251999999999995, 37.628)), ('B', '   5 ', 'LYS', 0.0, (-55.37499999999997, -23.561999999999994, 3.5799999999999996)), ('B', '  57 ', 'LEU', 0.0, (-34.66599999999998, 10.206, -7.014)), ('B', ' 186 ', 'VAL', 0.0091742508832259, (-39.49899999999999, -4.568, -12.582999999999998)), ('B', ' 187 ', 'ASP', 0.28863291529272384, (-39.966, -1.374, -10.541)), ('C', '  43 ', 'ILE', 0.2773660140132727, (-49.98899999999998, -17.033000000000005, 62.983)), ('C', '  61 ', 'LYS', 0.0, (-57.796999999999976, -15.316, 67.418)), ('C', ' 181 ', 'PHE', 0.29765282749520805, (-35.65699999999997, -25.721000000000004, 68.291)), ('C', ' 196 ', 'THR', 0.2677552502862714, (-19.334999999999997, -23.559999999999995, 61.012)), ('C', ' 303 ', 'VAL', 0.21762269478298935, (-34.664999999999985, -55.267999999999994, 57.967)), ('D', '  48 ', 'ASP', 0.15432125001568864, (-64.88, -41.968, 33.079)), ('D', '  59 ', 'ILE', 0.04925208892353265, (-65.47299999999998, -31.533, 43.646)), ('D', '  63 ', 'ASN', 0.004043205745650573, (-56.44299999999997, -26.067999999999998, 42.701)), ('D', '  69 ', 'GLN', 0.17012807724347098, (-48.55999999999999, -23.144, 31.696999999999996)), ('D', '  73 ', 'VAL', 0.11700924391160375, (-43.80999999999999, -19.778, 33.464)), ('D', '  74 ', 'GLN', 0.029114478350706782, (-46.37999999999998, -21.807, 35.39)), ('D', ' 130 ', 'MET', 0.18074894191336938, (-70.63399999999997, -22.041, 11.227)), ('D', ' 131 ', 'ARG', 0.05010203241984726, (-72.68099999999997, -24.522, 9.226)), ('D', ' 190 ', 'THR', 0.0013599335943581536, (-71.65099999999997, -41.373, 22.573)), ('D', ' 253 ', 'LEU', 0.0, (-73.15599999999998, -5.112, -2.217))]
data['cbeta'] = []
data['probe'] = [(' C  41  HIS  HB2', ' C 401  3WL  H2 ', -0.781, (-43.49, -17.723, 61.377)), (' A 165  MET  HE1', ' A 187  ASP  HA ', -0.749, (-33.481, -64.019, 34.082)), (' A 109  GLY  HA2', ' A 200  ILE HD13', -0.695, (-30.7, -42.389, 31.665)), (' B 292  THR HG22', ' B 294  PHE  H  ', -0.691, (-43.54, -29.596, 1.846)), (' B  86  VAL HG13', ' B 179  GLY  HA2', -0.684, (-35.738, -5.245, -2.721)), (' C 129  ALA  HB3', ' C 131  ARG HH21', -0.673, (-26.123, -35.568, 57.055)), (' C  43  ILE HD11', ' C  66  PHE  CE1', -0.662, (-53.299, -20.003, 63.885)), (' C  45  THR HG23', ' C  47  GLU  H  ', -0.645, (-47.815, -8.28, 58.441)), (' D  56  ASP  OD2', ' D  60  ARG  NH1', -0.635, (-67.55, -38.869, 41.662)), (' D 247  VAL HG13', ' D 261  VAL HG21', -0.626, (-82.85, -8.176, -1.981)), (' A  86  VAL HG13', ' A 179  GLY  HA2', -0.625, (-43.077, -59.874, 33.026)), (' D  95  ASN  HB3', ' D  98  THR  OG1', -0.619, (-54.515, -11.211, 30.07)), (' D  63  ASN  N  ', ' D  63  ASN  OD1', -0.618, (-57.839, -26.304, 43.679)), (' C  43  ILE HD11', ' C  66  PHE  HE1', -0.612, (-52.914, -20.282, 63.667)), (' C 298  ARG  HG3', ' C 303  VAL HG22', -0.61, (-33.355, -52.451, 57.888)), (' B 213  ILE  HA ', ' B 304  THR HG23', -0.588, (-53.658, -41.745, 5.377)), (' C  86  VAL HG13', ' C 179  GLY  HA2', -0.581, (-42.106, -27.29, 67.941)), (' D 109  GLY  HA2', ' D 200  ILE HD13', -0.58, (-73.426, -19.652, 6.537)), (' B  40  ARG  NE ', ' B 187  ASP  OD2', -0.579, (-36.413, -0.492, -7.577)), (' C  58  LEU HD22', ' C  82  MET  HE3', -0.578, (-50.293, -19.952, 70.212)), (' B 126  TYR  HE1', ' B 128  CYS  HG ', -0.569, (-52.016, -14.496, -0.614)), (' D 175  THR HG22', ' D 181  PHE  HA ', -0.568, (-71.185, -26.014, 22.932)), (' D  86  VAL HG13', ' D 179  GLY  HA2', -0.563, (-68.504, -23.844, 27.382)), (' A 126  TYR  HE1', ' A 128  CYS  HG ', -0.552, (-32.928, -47.714, 42.817)), (' B 131  ARG HH22', ' B 289  ASP  CG ', -0.548, (-50.967, -24.594, -7.98)), (' B 137  LYS  O  ', ' D   4  ARG  NH1', -0.547, (-53.63, -16.602, -4.289)), (' C  41  HIS  CG ', ' C 401  3WL  H1 ', -0.546, (-42.933, -19.241, 60.301)), (' D   8  PHE  HD2', ' D 113  SER  HG ', -0.544, (-61.279, -13.699, 11.631)), (' B 292  THR HG22', ' B 294  PHE  N  ', -0.542, (-44.249, -29.602, 2.079)), (' B  22  CYS  SG ', ' B  61  LYS  HE3', -0.537, (-39.289, 11.177, -1.205)), (' A  30  LEU HD22', ' A 148  VAL HG11', -0.533, (-45.222, -54.206, 40.86)), (' D  67  LEU  HB2', ' D  74  GLN  OE1', -0.532, (-48.662, -26.634, 35.46)), (' B  45  THR HG22', ' B  47  GLU  H  ', -0.531, (-44.508, 12.935, -10.464)), (' C 233  VAL HG21', ' C 269  LYS  HE2', -0.531, (-4.039, -39.743, 61.656)), (' B 131  ARG  HD2', ' B 197  ASP  OD2', -0.53, (-50.094, -19.744, -11.536)), (' C 226  THR HG23', ' C 229  ASP  H  ', -0.527, (-4.016, -41.5, 68.743)), (' C 219  PHE  O  ', ' C 267  SER  OG ', -0.523, (-8.352, -47.594, 53.767)), (' C  95  ASN  HB3', ' C  98  THR  OG1', -0.52, (-54.866, -39.848, 63.537)), (' A  76  ARG  HB3', ' A  92  ASP  OD2', -0.511, (-59.129, -67.662, 47.725)), (' D 108  PRO  HA ', ' D 130  MET  HG2', -0.507, (-73.372, -21.226, 12.272)), (' D  27  LEU HD21', ' D  42  VAL  HB ', -0.505, (-59.782, -29.861, 29.174)), (' C  27  LEU HD21', ' C  42  VAL  HB ', -0.5, (-47.757, -22.033, 59.708)), (' D  48  ASP  N  ', ' D  48  ASP  OD1', -0.492, (-63.067, -42.023, 32.85)), (' C  67  LEU HD11', ' C  74  GLN  NE2', -0.491, (-61.575, -25.625, 55.024)), (' B  30  LEU HD22', ' B 148  VAL HG11', -0.491, (-41.294, -7.845, 5.541)), (' A 146  GLY  HA2', ' A 162  MET  HE2', -0.489, (-42.271, -58.451, 41.348)), (' A  41  HIS  HA ', ' A  54  TYR  HE1', -0.476, (-39.059, -68.669, 36.966)), (' D 108  PRO  HB3', ' D 132  PRO  HA ', -0.475, (-76.218, -23.061, 10.253)), (' C 233  VAL HG11', ' C 269  LYS  HG3', -0.475, (-4.83, -38.926, 59.578)), (' D 234  ALA  HB1', ' D 239  TYR  HB2', -0.475, (-81.39, -22.828, -2.347)), (' D  69  GLN  HG3', ' D  74  GLN  HG2', -0.472, (-46.647, -24.383, 33.49)), (' D 201  THR  O  ', ' D 205  LEU HD12', -0.471, (-77.19, -16.506, -1.372)), (' A   5  LYS  HE3', ' A 290  GLU  HB2', -0.471, (-30.18, -40.256, 40.463)), (' D 140  PHE  HB2', ' D 172  HIS  CE1', -0.469, (-60.764, -30.843, 14.012)), (' A 213  ILE  HA ', ' A 304  THR HG23', -0.469, (-31.732, -20.254, 38.981)), (' B  87  LEU HD21', ' B  89  LEU HD21', -0.467, (-36.27, 5.592, 2.784)), (' C 140  PHE  HB3', ' C 144  SER  OG ', -0.467, (-39.353, -26.458, 52.488)), (' B 189  GLN  HG2', ' B 401  3WL  C4 ', -0.466, (-45.741, 0.964, -11.284)), (' B 163  HIS  CE1', ' B 172  HIS  HB3', -0.466, (-48.912, -8.343, -5.608)), (' B 121  SER  HB2', ' D 304  THR  OG1', -0.463, (-54.684, -1.478, 9.821)), (' A  87  LEU HD21', ' A  89  LEU HD21', -0.461, (-48.151, -68.042, 39.983)), (' D 228  ASN  O  ', ' D 232  LEU  HG ', -0.461, (-90.419, -19.973, -4.375)), (' D 187  ASP  N  ', ' D 187  ASP  OD1', -0.456, (-70.672, -33.042, 26.73)), (' B   5  LYS  NZ ', ' B 502  HOH  O  ', -0.456, (-52.299, -21.071, -0.727)), (' B 276  MET  HE2', ' B 281  ILE HD12', -0.45, (-59.638, -34.929, -6.459)), (' C 130  MET  HA ', ' C 136  ILE HG22', -0.45, (-30.1, -32.468, 60.031)), (' C 225  THR HG22', ' C 226  THR  O  ', -0.45, (-5.305, -43.415, 66.642)), (' B   7  ALA  HA ', ' B 127  GLN  HG2', -0.45, (-50.964, -19.667, 5.575)), (' B  31  TRP  CE2', ' B  95  ASN  HB2', -0.45, (-38.677, -1.237, 15.276)), (' C  43  ILE HD11', ' C  66  PHE  CZ ', -0.447, (-53.449, -19.915, 64.877)), (' C 186  VAL HG23', ' C 188  ARG  HB2', -0.447, (-36.764, -15.044, 65.792)), (' D 131  ARG  NH2', ' D 290  GLU  OE2', -0.447, (-68.513, -23.538, 5.194)), (' C   5  LYS  HG2', ' C 291  PHE  CZ ', -0.446, (-26.724, -42.689, 51.441)), (' A   8  PHE  HB3', ' A 152  ILE HD12', -0.446, (-44.431, -41.356, 44.439)), (' B  45  THR  H  ', ' B  48  ASP  HB2', -0.444, (-42.278, 9.66, -8.937)), (' D 232  LEU  HA ', ' D 235  MET  HE3', -0.443, (-88.782, -24.25, -2.776)), (' C  82  MET  HB2', ' C  82  MET  HE3', -0.442, (-49.905, -20.902, 71.243)), (' C  21  THR  HB ', ' C  67  LEU  HB3', -0.442, (-57.172, -22.257, 56.497)), (' A 165  MET  HB3', ' A 165  MET  HE2', -0.44, (-33.052, -62.558, 37.618)), (' A  76  ARG  HB2', ' A  76  ARG  HE ', -0.439, (-57.875, -69.326, 49.812)), (' B 233  VAL HG21', ' B 269  LYS  HE3', -0.437, (-49.673, -40.787, -18.43)), (' C 109  GLY  HA2', ' C 200  ILE HD13', -0.437, (-24.357, -36.931, 61.95)), (' D  53  ASN  CG ', ' D  56  ASP  HB2', -0.436, (-70.681, -36.482, 39.435)), (' D 167  LEU  HB3', ' D 168  PRO  HD2', -0.435, (-69.307, -37.193, 14.445)), (' B 163  HIS  HE1', ' B 172  HIS  HB3', -0.431, (-48.943, -7.751, -5.856)), (' A 240  GLU  HG3', ' A 241  PRO  HD2', -0.43, (-25.782, -41.489, 23.723)), (' A 187  ASP  N  ', ' A 187  ASP  OD1', -0.43, (-35.066, -65.426, 32.233)), (' D  58  LEU HD11', ' D  80  HIS  HD2', -0.429, (-63.168, -27.924, 39.429)), (' A 114  VAL  O  ', ' A 125  VAL  HA ', -0.428, (-37.578, -47.557, 47.343)), (' B  10  SER  O  ', ' B  14  GLU  HG3', -0.426, (-48.572, -10.859, 13.114)), (' A 286  LEU  HG ', ' C 285  ALA  HB2', -0.426, (-16.849, -38.05, 42.501)), (' C  45  THR HG22', ' C  48  ASP  CG ', -0.425, (-48.497, -9.729, 61.421)), (' C 114  VAL  O  ', ' C 125  VAL  HA ', -0.424, (-39.117, -37.13, 52.355)), (' B 126  TYR  HE1', ' B 128  CYS  SG ', -0.422, (-51.428, -14.607, -0.784)), (' D  87  LEU HD21', ' D  89  LEU HD21', -0.42, (-60.129, -25.971, 35.858)), (' A  31  TRP  CE2', ' A  95  ASN  HB2', -0.419, (-55.355, -56.768, 46.408)), (' A 245  ASP  O  ', ' A 249  ILE HG12', -0.419, (-36.228, -33.476, 24.289)), (' D   7  ALA  HA ', ' D 127  GLN  HG2', -0.418, (-59.779, -15.612, 8.597)), (' A 167  LEU  HA ', ' A 167  LEU HD12', -0.417, (-26.444, -60.47, 36.558)), (' B  21  THR  HB ', ' B  67  LEU  HB2', -0.417, (-44.348, 9.921, 5.87)), (' C 175  THR HG22', ' C 181  PHE  HA ', -0.417, (-36.881, -25.848, 67.185)), (' C 262  LEU  HA ', ' C 265  CYS  HB2', -0.416, (-9.17, -46.535, 63.637)), (' C  41  HIS  HB2', ' C 401  3WL  C5 ', -0.413, (-43.154, -17.376, 61.137)), (' B 292  THR HG23', ' B 293  PRO  HD2', -0.412, (-43.618, -28.954, -0.461)), (' C  92  ASP  N  ', ' C  92  ASP  OD1', -0.412, (-62.459, -32.081, 65.002)), (' C 108  PRO  HB3', ' C 132  PRO  HA ', -0.409, (-24.571, -31.932, 64.939)), (' D  31  TRP  CZ3', ' D  75  LEU HD11', -0.409, (-50.509, -16.928, 32.35)), (' C 131  ARG  NH2', ' C 290  GLU  HG2', -0.408, (-25.0, -35.926, 56.706)), (' B 200  ILE  O  ', ' B 204  VAL HG23', -0.406, (-49.276, -29.541, -8.175)), (' C 229  ASP  O  ', ' C 233  VAL HG23', -0.406, (-4.321, -38.17, 63.977)), (' B  52  PRO  HD2', ' B 188  ARG  HG2', -0.405, (-39.306, 2.661, -14.044)), (' B 301  SER  HB2', ' D 141  LEU HD22', -0.404, (-53.983, -36.027, 12.566)), (' D 102  LYS  HE2', ' D 156  CYS  SG ', -0.403, (-65.62, -6.186, 21.49)), (' C  45  THR HG23', ' C  47  GLU  N  ', -0.4, (-47.278, -8.726, 58.862))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
