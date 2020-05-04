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
data['rama'] = [('A', '  24 ', 'MET', 0.0005651639999999999, (19.445, 62.192, -4.778)), ('A', '  27 ', 'THR', 0.013726688915426232, (17.068000000000005, 59.333, -12.226)), ('A', '  41 ', 'ASP', 0.002783762424697036, (7.524000000000003, 59.503, -18.705)), ('A', '  60 ', 'PRO', 0.029360889952396666, (5.366, 45.66299999999999, -11.44)), ('A', ' 193 ', 'CYS', 0.00022889357992272427, (-29.226000000000003, 14.591999999999999, -40.466)), ('A', ' 224 ', 'PRO', 0.08149660652451952, (-25.04700000000001, 25.811000000000007, -45.275)), ('B', ' 191 ', 'LYS', 0.01491192584498167, (3.011000000000001, 67.80199999999999, -44.488))]
data['omega'] = []
data['rota'] = [('A', '   5 ', 'THR', 0.053037411998957396, (17.203000000000007, 61.814, 1.15)), ('A', '   6 ', 'ILE', 0.015639707553856443, (13.709, 62.26100000000001, -0.354)), ('A', '  21 ', 'LEU', 0.042529860522041454, (13.325, 56.445, -0.501)), ('A', '  26 ', 'MET', 0.01217147267239633, (20.234, 58.909, -10.185)), ('A', '  30 ', 'GLN', 0.27937384805892324, (17.54, 52.70700000000001, -12.816)), ('A', '  52 ', 'GLU', 0.1193605051882708, (8.746, 64.997, -1.961)), ('A', '  54 ', 'LYS', 0.027242226170435327, (4.066, 62.778, -4.453)), ('A', '  81 ', 'LEU', 0.0, (0.392999999999998, 49.062, -18.072)), ('A', '  86 ', 'SER', 0.2687998264336934, (0.17900000000000205, 55.874999999999986, -23.59)), ('A', ' 171 ', 'THR', 0.07439978388975729, (-15.526000000000003, 40.345, -27.316)), ('A', ' 180 ', 'GLU', 0.27776671363732425, (-20.876, 33.83100000000002, -14.577)), ('A', ' 191 ', 'LYS', 0.008407878955904939, (-34.79500000000001, 17.45, -42.168)), ('A', ' 222 ', 'SER', 0.05271212529675254, (-30.43400000000001, 28.914, -41.491)), ('A', ' 223 ', 'ILE', 0.015733774850135482, (-26.913, 27.725000000000005, -42.415)), ('A', ' 236 ', 'VAL', 0.05671890578261572, (-34.57100000000001, 27.003, -26.743)), ('A', ' 294 ', 'MET', 0.020527152325818056, (-36.25600000000001, 60.044, -35.891)), ('B', '  58 ', 'VAL', 0.007351242675213143, (-12.836, 17.895, -12.128)), ('B', '  59 ', 'LEU', 0.14180918817109306, (-14.136000000000005, 21.45499999999999, -11.669000000000002)), ('B', '  81 ', 'LEU', 0.05972657548701086, (-13.254000000000005, 24.741000000000003, -18.027)), ('B', '  92 ', 'LYS', 0.20972429668704587, (-10.518000000000008, 13.995999999999997, -29.526)), ('B', ' 127 ', 'LYS', 0.024125886492597004, (6.147, 30.041, -26.474)), ('B', ' 180 ', 'GLU', 0.16251659893208079, (7.3, 40.758, -23.255)), ('B', ' 223 ', 'ILE', 0.11910280005292817, (-3.3369999999999997, 55.548, -43.858))]
data['cbeta'] = []
data['probe'] = [(' A   4  LYS  N  ', ' A  24  MET  SD ', -1.046, (21.852, 62.642, -2.127)), (' A 192  HIS  NE2', ' A1001  HOH  O  ', -0.872, (-36.144, 14.582, -46.207)), (' A 902  S88  O20', ' A 903  DMS  H22', -0.726, (-11.158, 47.691, -37.967)), (' A 241  SER  H  ', ' A 905  DMS  H23', -0.714, (-27.569, 38.637, -18.635)), (' A 171  THR HG21', ' B1089  HOH  O  ', -0.664, (-13.607, 38.578, -30.507)), (' A 192  HIS  O  ', ' A 194  GLY  N  ', -0.645, (-31.187, 14.157, -39.599)), (' A  40  ALA  O  ', ' A  42  VAL  N  ', -0.614, (7.392, 60.653, -16.951)), (' A 240  SER  HA ', ' A 905  DMS  C2 ', -0.585, (-27.728, 36.864, -18.595)), (' A   6  ILE HG23', ' A  22  VAL HG23', -0.58, (14.497, 61.563, -3.43)), (' A 902  S88  H6 ', ' A 903  DMS  C2 ', -0.575, (-9.172, 47.991, -38.06)), (' A 294  MET  HE2', ' A 294  MET  N  ', -0.562, (-34.538, 59.933, -35.145)), (' A 240  SER  HB2', ' A 905  DMS  H22', -0.558, (-26.673, 38.194, -19.883)), (' A 307  LYS  HD3', ' A 308  GLU  N  ', -0.556, (-33.477, 42.346, -21.399)), (' A 241  SER  N  ', ' A 905  DMS  H23', -0.556, (-28.381, 38.859, -18.511)), (' A 218  LYS  HE2', ' A 311  TYR  CE1', -0.554, (-37.879, 34.215, -27.194)), (' B  84  TYR  OH ', ' B 147  ASN  OD1', -0.544, (-6.759, 19.555, -22.66)), (' A 192  HIS  CD2', ' A1001  HOH  O  ', -0.539, (-35.681, 14.853, -45.163)), (' B 239  GLU  OE2', ' B 310  SER  OG ', -0.535, (16.786, 44.773, -33.306)), (' A 902  S88  H6 ', ' A 903  DMS  H22', -0.519, (-10.051, 48.297, -38.318)), (' A  27  THR HG22', ' A  30  GLN  OE1', -0.51, (19.134, 56.859, -14.002)), (' A 225  CYS  SG ', ' A 231  ALA  HB2', -0.498, (-27.313, 21.479, -41.227)), (' A  36  TYR  CE2', ' A  85  MET  HG3', -0.497, (3.013, 54.149, -17.708)), (' B 280  LYS  HD2', ' B1015  HOH  O  ', -0.494, (8.375, 20.518, -45.951)), (' B 225  CYS  HB2', ' B 229  ARG  O  ', -0.488, (-4.757, 62.097, -44.65)), (' B 294  MET  HG3', ' B 296  GLU  O  ', -0.484, (2.036, 27.926, -56.754)), (' A   4  LYS  C  ', ' A   4  LYS  HD2', -0.484, (17.907, 63.229, -1.063)), (' B 190  CYS  SG ', ' B 193  CYS  HB2', -0.481, (0.549, 65.442, -40.63)), (' A 190  CYS  CB ', ' A 193  CYS  HB3', -0.469, (-29.742, 17.319, -40.302)), (' B 283  LEU  HB2', ' B 294  MET  O  ', -0.469, (4.728, 26.771, -54.379)), (' A   4  LYS  HZ1', ' A  49  VAL HG22', -0.453, (16.268, 67.227, -3.802)), (' B 112  OCS  OD2', ' B 113  TYR  N  ', -0.451, (-11.021, 27.058, -41.364)), (' A 218  LYS  HE2', ' A 311  TYR  CD1', -0.442, (-37.43, 34.439, -26.324)), (' A 240  SER  CA ', ' A 905  DMS  C2 ', -0.439, (-27.9, 37.206, -18.823)), (' A  57  PHE  CD2', ' A  85  MET  HE3', -0.437, (0.544, 53.759, -14.317)), (' B 280  LYS  CD ', ' B1015  HOH  O  ', -0.437, (8.613, 20.639, -45.667)), (' A 281  GLU  OE2', ' A 284  TYR  OH ', -0.436, (-35.821, 62.133, -26.189)), (' A   4  LYS  NZ ', ' A  49  VAL HG22', -0.436, (16.214, 67.233, -3.552)), (' A  40  ALA  O  ', ' A  42  VAL HG13', -0.434, (7.623, 62.1, -15.954)), (' A  54  LYS  HA ', ' A  54  LYS  HD2', -0.433, (2.13, 62.693, -4.683)), (' B 903  DMS  H21', ' B1022  HOH  O  ', -0.433, (4.132, 54.383, -27.95)), (' A 158  LYS  NZ ', ' A 903  DMS  H21', -0.431, (-8.583, 48.092, -35.32)), (' A 902  S88  H1 ', ' B 210  GLY  HA2', -0.43, (-5.67, 47.049, -43.693)), (' A 192  HIS  O  ', ' A 193  CYS  C  ', -0.429, (-30.595, 14.148, -39.541)), (' A 240  SER  CB ', ' A 905  DMS  H22', -0.428, (-27.279, 37.505, -19.76)), (' A 241  SER  H  ', ' A 905  DMS  C2 ', -0.425, (-27.418, 38.849, -18.626)), (' B  62  ASP  C  ', ' B  62  ASP  OD1', -0.422, (-10.395, 24.759, -3.184)), (' B  95  LYS  HD2', ' B  95  LYS  N  ', -0.419, (-9.283, 12.319, -36.697)), (' A 193  CYS  HB2', ' A 227  CYS  SG ', -0.417, (-26.833, 16.409, -41.211)), (' A 112  OCS  OD2', ' A 113  TYR  N  ', -0.417, (-15.727, 54.419, -34.244)), (' B 180  GLU  CD ', ' B 180  GLU  H  ', -0.415, (7.068, 38.53, -23.339)), (' A  51  HIS  O  ', ' A  52  GLU  C  ', -0.41, (7.233, 64.752, -2.823)), (' A 189  VAL HG22', ' A 195  GLN  OE1', -0.404, (-34.312, 19.576, -33.858)), (' A 236  VAL  HA ', ' A 313  THR  HB ', -0.403, (-36.168, 27.471, -27.051)), (' A  27  THR  HA ', ' A  46  LYS  HA ', -0.401, (16.654, 61.01, -12.077))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
