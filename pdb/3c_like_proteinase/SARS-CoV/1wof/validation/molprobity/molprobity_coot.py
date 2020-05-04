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
data['rama'] = [('A', '   1 ', 'SER', 0.027670642235976584, (83.612, -17.27, 24.379)), ('A', ' 154 ', 'TYR', 0.016957709943516454, (100.10899999999998, 0.626, 36.013))]
data['omega'] = []
data['rota'] = [('A', '   3 ', 'PHE', 0.060032440303909015, (89.703, -13.821999999999997, 23.683)), ('A', '  30 ', 'LEU', 0.0, (96.78800000000003, 16.168, 22.582)), ('A', '  47 ', 'GLU', 0.2512284374963912, (97.16300000000003, 21.975, -2.445)), ('A', '  60 ', 'ARG', 0.14826612320619958, (103.889, 32.582, 7.945)), ('A', '  75 ', 'LEU', 0.08454631778953366, (92.473, 27.734, 24.593)), ('A', ' 268 ', 'LEU', 0.01261824865963815, (102.075, -24.14099999999999, 16.278)), ('B', '  55 ', 'GLU', 0.05382718275733229, (62.952000000000005, -10.603000000000003, 49.675)), ('B', '  88 ', 'ARG', 0.2052280828413881, (69.34200000000001, 0.747, 44.437)), ('B', ' 127 ', 'GLN', 0.21218931872309282, (82.45000000000002, -4.069, 21.894)), ('B', ' 142 ', 'ASN', 0.11547549558852924, (84.818, -13.602, 38.94)), ('B', ' 228 ', 'ASN', 0.023840157141951614, (61.693000000000005, -16.278000000000002, 0.917)), ('B', ' 245 ', 'ASP', 0.136927207466705, (61.99700000000002, -4.765000000000001, 8.168)), ('B', ' 268 ', 'LEU', 0.005462524138209556, (75.64199999999998, -14.102, 1.145))]
data['cbeta'] = []
data['probe'] = [(' A   6  MET  HE2', ' A 299  GLN  HG3', -1.049, (90.254, -8.771, 28.163)), (' B   4  ARG  H  ', ' B 299  GLN HE22', -0.922, (86.368, -0.721, 11.441)), (' A 186  VAL  H  ', ' A 192  GLN HE22', -0.88, (106.062, 9.524, 3.901)), (' A   1  SER  HB3', ' B2216  HOH  O  ', -0.852, (81.925, -16.634, 25.989)), (' A 191  ALA  HA ', ' A1145  I12  N1 ', -0.769, (101.501, 7.073, -4.273)), (' B   4  ARG  H  ', ' B 299  GLN  NE2', -0.747, (86.538, -0.53, 11.45)), (' A 222  ARG  HG2', ' A 222  ARG HH11', -0.746, (106.223, -36.529, 23.543)), (' B 231  ASN  HB3', ' B 235  MET  HE3', -0.733, (63.79, -18.493, 5.414)), (' B 277  ASN HD22', ' B 279  ARG HH12', -0.731, (86.147, -18.669, -3.418)), (' A  75  LEU HD22', ' A  91  VAL  HB ', -0.715, (95.72, 26.566, 25.638)), (' B 244  GLN  O  ', ' B 247  VAL HG22', -0.714, (62.714, -5.058, 4.136)), (' A  86  LEU HD22', ' A 162  MET  CE ', -0.713, (102.207, 15.094, 15.707)), (' A 276  MET  HE3', ' A 281  ILE HG13', -0.708, (92.523, -23.386, 17.307)), (' A  39  PRO  HG3', ' A 162  MET  HE3', -0.704, (99.867, 14.254, 14.378)), (' A  86  LEU  HG ', ' A 179  GLY  CA ', -0.693, (105.9, 14.747, 15.763)), (' A  48  ASP  O  ', ' A  52  PRO  HB3', -0.69, (102.572, 21.051, 1.692)), (' A  51  ASN  ND2', ' A 188  ARG  HE ', -0.684, (107.386, 16.924, -0.354)), (' A 127  GLN  HG2', ' A1163  HOH  O  ', -0.679, (95.546, -5.567, 21.411)), (' A  60  ARG  HB2', ' A  60  ARG  NH1', -0.674, (103.03, 31.167, 5.679)), (' A  60  ARG  HB2', ' A  60  ARG HH11', -0.669, (103.271, 30.958, 5.898)), (' B   4  ARG  N  ', ' B 299  GLN HE22', -0.648, (86.483, -1.396, 12.321)), (' A  51  ASN HD22', ' A 188  ARG  HE ', -0.643, (107.134, 17.458, 0.227)), (' A  86  LEU HD22', ' A 162  MET  HE2', -0.639, (101.833, 14.138, 16.094)), (' A   4  ARG  H  ', ' A 299  GLN HE22', -0.637, (89.54, -11.977, 25.297)), (' B 243  THR  H  ', ' B 246  HIS  CD2', -0.636, (64.792, -9.917, 8.332)), (' B  19  GLN  NE2', ' B 119  ASN HD22', -0.634, (87.204, -4.17, 45.394)), (' B 276  MET  HE3', ' B 281  ILE HG13', -0.633, (85.493, -13.426, 2.496)), (' A 286  ILE HD11', ' A 288  GLU  OE2', -0.629, (91.251, -13.786, 14.416)), (' B 142 AASN  HA ', ' B2145  I12 H282', -0.623, (83.488, -14.393, 37.897)), (' A  19  GLN HE22', ' A 119  ASN HD22', -0.621, (85.383, 20.453, 14.594)), (' B 142 BASN  HA ', ' B2145  I12 H282', -0.621, (83.486, -14.399, 37.917)), (' B  48  ASP  O  ', ' B  52  PRO  HB3', -0.62, (70.252, -17.389, 47.171)), (' A  40  ARG  HA ', ' A  87  LEU  HG ', -0.619, (102.385, 21.227, 12.93)), (' A 276  MET  CE ', ' A 281  ILE HG13', -0.611, (92.185, -23.728, 16.785)), (' B 209  TYR  O  ', ' B 213  ILE HG23', -0.602, (79.815, -0.726, 1.915)), (' B 231  ASN  HB3', ' B 235  MET  CE ', -0.598, (63.351, -18.42, 6.175)), (' B  51  ASN  ND2', ' B 188  ARG HH12', -0.592, (65.181, -20.915, 44.966)), (' A 222  ARG  HG2', ' A 222  ARG  NH1', -0.588, (106.719, -37.019, 23.972)), (' B 169  THR HG23', ' B 171  VAL HG22', -0.586, (76.791, -19.822, 27.377)), (' B  51  ASN HD22', ' B 188  ARG HH12', -0.585, (65.192, -20.233, 44.631)), (' A  25  THR HG23', ' A1145  I12 H253', -0.58, (93.226, 20.148, 7.609)), (' B 163  HIS  HE1', ' B 172  HIS  HB3', -0.578, (78.392, -12.849, 31.739)), (' A  84  ASN  OD1', ' A 180  LYS  HE3', -0.572, (111.926, 13.923, 15.504)), (' A 163  HIS  HE1', ' A 172  HIS  HB3', -0.57, (96.506, 6.105, 9.737)), (' B 277  ASN HD22', ' B 279  ARG  NH1', -0.566, (86.325, -17.739, -3.39)), (' B 213  ILE  C  ', ' B 213  ILE HD12', -0.565, (83.826, 1.68, 1.691)), (' B 131  ARG  HD3', ' B 197  ASP  OD1', -0.558, (74.392, -16.076, 19.239)), (' B  47  GLU  N  ', ' B  47  GLU  OE1', -0.555, (76.71, -19.441, 52.562)), (' A  86  LEU  CD2', ' A 162  MET  HE2', -0.554, (102.432, 14.492, 15.567)), (' B 233  VAL HG21', ' B 269  LYS  HE2', -0.552, (69.267, -20.161, -1.511)), (' A  31  TRP  CE2', ' A  75  LEU HD11', -0.551, (94.291, 23.053, 26.66)), (' A  19  GLN HE21', ' A 119  ASN  HA ', -0.551, (86.996, 19.498, 15.131)), (' A  86  LEU  HG ', ' A 179  GLY  HA2', -0.548, (105.848, 13.835, 16.256)), (' A 222  ARG  HG2', ' A 222  ARG  O  ', -0.546, (106.216, -35.864, 23.473)), (' A  55  GLU  CD ', ' A  55  GLU  H  ', -0.544, (110.118, 23.083, 6.475)), (' A 118  TYR  CE1', ' A 144  SER  HB3', -0.543, (88.611, 10.244, 11.65)), (' B 169  THR  CG2', ' B 171  VAL HG22', -0.54, (76.496, -20.418, 27.242)), (' B  19  GLN HE22', ' B 119  ASN HD22', -0.537, (87.7, -3.858, 45.907)), (' B  31  TRP  CE2', ' B  95  ASN  HB2', -0.536, (78.695, 9.122, 42.682)), (' A  86  LEU HD22', ' A 162  MET  HE1', -0.534, (101.556, 15.357, 16.147)), (' B  51  ASN HD22', ' B 188  ARG  NH1', -0.533, (65.436, -20.65, 44.492)), (' B 210  ALA  O  ', ' B 213  ILE HG13', -0.532, (82.518, -0.694, 3.14)), (' A 186  VAL  H  ', ' A 192  GLN  NE2', -0.532, (106.246, 9.102, 3.251)), (' B 163  HIS  CE1', ' B 172  HIS  HB3', -0.528, (78.145, -12.146, 31.981)), (' B  40  ARG  O  ', ' B  43  ILE HG12', -0.528, (71.261, -9.807, 47.306)), (' A  19  GLN  NE2', ' A 119  ASN HD22', -0.526, (85.828, 20.624, 14.895)), (' B   2  GLY  H  ', ' B 214  ASN HD21', -0.521, (88.285, 0.993, 5.535)), (' B  86  LEU  HG ', ' B 179  GLY  HA2', -0.516, (68.62, -5.098, 37.332)), (' B 243  THR  H  ', ' B 246  HIS  HD2', -0.515, (65.092, -10.012, 8.795)), (' B  31  TRP  CD2', ' B  95  ASN  HB2', -0.512, (78.666, 9.078, 41.867)), (' A  49  MET  HE2', ' A1145  I12 H183', -0.509, (98.428, 16.628, 4.058)), (' B 133  ASN  O  ', ' B 134  HIS  HB2', -0.507, (69.271, -14.954, 25.471)), (' A 163  HIS  CE1', ' A 172  HIS  HB3', -0.505, (96.444, 6.008, 9.982)), (' B 227  LEU HD21', ' B 242  LEU  O  ', -0.5, (63.116, -12.201, 5.493)), (' A 165  MET  HB3', ' A1145  I12  H14', -0.497, (98.323, 11.653, 5.594)), (' A 235  MET  HE3', ' A 241  PRO  HG3', -0.494, (111.855, -15.004, 8.672)), (' A 115  LEU HD11', ' A 122  PRO  HB3', -0.492, (88.135, 8.838, 22.54)), (' B  40  ARG  HA ', ' B  87  LEU  HG ', -0.491, (70.74, -6.189, 44.955)), (' B 186  VAL HG23', ' B 188  ARG  HG2', -0.491, (68.191, -18.791, 38.903)), (' B 118  TYR  CE1', ' B 144  SER  HB3', -0.49, (85.303, -9.356, 36.046)), (' A  39  PRO  CG ', ' A 162  MET  HE3', -0.486, (99.225, 15.055, 14.26)), (' A 276  MET  HE1', ' A 281  ILE  N  ', -0.485, (90.329, -22.801, 17.182)), (' A 132  PRO  HD2', ' A 197  ASP  OD1', -0.484, (103.57, -6.937, 9.402)), (' A   6  MET  HE2', ' A 299  GLN  CG ', -0.484, (90.987, -9.278, 28.069)), (' A 286  ILE  C  ', ' A 286  ILE HD12', -0.482, (92.395, -16.82, 13.903)), (' A 243  THR  H  ', ' A 246  HIS  CD2', -0.481, (112.065, -14.078, 17.477)), (' B 142 BASN  N  ', ' B 142 BASN  OD1', -0.477, (85.371, -14.882, 37.814)), (' A 228  ASN  O  ', ' A 232  LEU  HG ', -0.477, (114.048, -23.726, 10.335)), (' B 191  ALA  HB2', ' B2145  I12  H42', -0.47, (72.507, -27.572, 37.402)), (' B 175  THR HG22', ' B 181  PHE  HA ', -0.469, (68.38, -9.213, 34.102)), (' B 244  GLN  NE2', ' B 247  VAL  CG2', -0.467, (62.249, -5.09, 2.371)), (' B 131  ARG  HD2', ' B 137  LYS  HE3', -0.465, (77.016, -16.178, 20.256)), (' B 198  THR  OG1', ' B 240  GLU  HG2', -0.461, (69.542, -15.847, 14.543)), (' A 167  LEU  HB3', ' A 168  PRO  HD2', -0.461, (99.777, 3.5, 1.09)), (' A 106  ILE HG13', ' A 110  GLN  HB2', -0.458, (104.733, -1.978, 20.19)), (' B 131  ARG HH22', ' B 289  ASP  CG ', -0.456, (76.746, -12.577, 15.915)), (' A  45  THR  H  ', ' A  48  ASP  HB2', -0.453, (98.535, 23.475, 2.36)), (' B   6  MET  HE3', ' B 299  GLN  HG3', -0.452, (85.031, 2.345, 13.037)), (' B 228  ASN  HA ', ' B 228  ASN HD22', -0.452, (61.334, -16.517, 2.566)), (' B 168  PRO  HG3', ' B2145  I12  C5 ', -0.45, (75.818, -24.04, 34.796)), (' B 109  GLY  HA2', ' B 200  ILE HD13', -0.449, (72.947, -9.575, 16.9)), (' B   2  GLY  H  ', ' B 214  ASN  ND2', -0.445, (88.078, 0.606, 5.222)), (' A  38  CYS  C  ', ' A 162  MET  HE1', -0.44, (100.424, 16.544, 15.571)), (' B   8  PHE  HD1', ' B 113  SER  HG ', -0.438, (80.212, 1.119, 22.789)), (' B 142 BASN  OD1', ' B2145  I12 H292', -0.438, (84.381, -16.326, 37.099)), (' A 109  GLY  HA2', ' A 200  ILE HD13', -0.436, (103.025, -7.468, 15.829)), (' B 131  ARG  CD ', ' B 197  ASP  OD1', -0.436, (74.807, -15.714, 19.834)), (' B 277  ASN  HB2', ' B 279  ARG  NH1', -0.433, (87.524, -18.288, -2.803)), (' B 277  ASN  ND2', ' B 279  ARG HH12', -0.432, (86.327, -18.858, -3.426)), (' B  10  SER  O  ', ' B  14  GLU  HG3', -0.431, (85.171, 4.709, 31.308)), (' A 243  THR  H  ', ' A 246  HIS  HD2', -0.43, (111.407, -14.065, 17.368)), (' B  81  SER  OG ', ' B  88  ARG  NH1', -0.43, (65.217, 1.354, 45.239)), (' B 153  ASP  O  ', ' B 154  TYR  HB2', -0.428, (74.899, 12.314, 22.009)), (' B 269  LYS  O  ', ' B 273  GLN  HG3', -0.426, (74.557, -20.031, -0.277)), (' B 213  ILE HG22', ' B 257  THR HG22', -0.426, (79.078, 0.998, 0.062)), (' A 301  SER  OG ', ' A 303  VAL HG23', -0.424, (96.115, -9.184, 34.89)), (' A 115  LEU HD13', ' A 125  VAL  CG1', -0.423, (88.982, 5.696, 23.005)), (' A 188  ARG  HG2', ' A 188  ARG HH11', -0.422, (106.7, 14.415, 3.183)), (' A  86  LEU  HG ', ' A 179  GLY  HA3', -0.422, (106.646, 14.754, 16.046)), (' A 153  ASP  O  ', ' A 154  TYR  HB3', -0.421, (101.907, 1.702, 35.834)), (' B 167  LEU HD21', ' B 185  PHE  CE2', -0.421, (71.111, -18.837, 29.773)), (' A 286  ILE HG21', ' B 285  THR HG21', -0.421, (91.232, -16.858, 9.034)), (' B   3  PHE  HA ', ' B 299  GLN  NE2', -0.416, (86.637, -0.509, 10.692)), (' A  52  PRO  HG2', ' A  54  TYR  CE1', -0.416, (104.772, 18.836, 4.217)), (' A 270  GLU  HA ', ' A 270  GLU  OE1', -0.415, (102.351, -30.393, 12.502)), (' A  -2  LEU HD22', ' B 139  SER  OG ', -0.414, (87.873, -12.357, 29.301)), (' B 244  GLN  NE2', ' B 247  VAL HG21', -0.41, (62.194, -5.184, 2.374)), (' A 222  ARG  CG ', ' A 222  ARG  NH1', -0.407, (106.05, -36.986, 24.305)), (' B 262  LEU  HA ', ' B 262  LEU HD23', -0.406, (67.73, -9.765, -0.986)), (' B 227  LEU HD23', ' B 231  ASN  ND2', -0.406, (63.003, -13.933, 3.981)), (' B 276  MET  CE ', ' B 281  ILE HG13', -0.401, (85.745, -13.252, 3.242)), (' A  31  TRP  CZ2', ' A  75  LEU HD11', -0.401, (94.152, 23.528, 27.516))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
