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
data['rama'] = [('A', ' 176 ', 'GLU', 0.0, (19.824, -12.961, 8.733)), ('A', ' 177 ', 'SER', 0.0011303300000000001, (17.531, -15.794, 9.408)), ('A', ' 179 ', 'ASN', 0.0017902806844281637, (13.798, -17.794000000000008, 10.615)), ('B', ' 177 ', 'SER', 0.045082684934437386, (-21.856, -3.662, -20.592))]
data['omega'] = [('A', ' 174 ', 'SER', None, (14.616, -11.794, 7.03)), ('A', ' 177 ', 'SER', None, (18.762, -15.008, 9.496)), ('A', ' 179 ', 'ASN', None, (14.676, -18.782000000000007, 9.988)), ('A', ' 180 ', 'ASN', None, (13.357999999999997, -15.788999999999993, 9.332)), ('B', ' 174 ', 'SER', None, (-17.217000000000006, -9.072, -17.224))]
data['rota'] = [('A', '   4 ', 'SER', 0.07446418806499766, (17.889, -17.129, -2.287)), ('A', '  95 ', 'GLU', 0.010437060081190927, (-12.880000000000008, -33.676, -18.437)), ('A', ' 109 ', 'ASP', 0.2263434122266714, (10.181999999999993, -36.173999999999985, -21.04)), ('A', ' 110 ', 'THR', 0.008159601566148922, (12.236999999999997, -39.18799999999999, -20.244)), ('A', ' 124 ', 'LYS', 0.0, (19.172000000000008, -28.756, -2.991)), ('A', ' 128 ', 'THR', 0.12068315474468291, (20.234000000000005, -27.503999999999998, -8.828)), ('A', ' 144 ', 'LEU', 0.0, (-7.907, -19.879, 1.074)), ('A', ' 156 ', 'CYS', 0.15870329342905726, (-1.2120000000000029, -28.264999999999997, 8.776)), ('A', ' 175 ', 'THR', 0.009519535524304956, (18.532, -9.867, 6.9270000000000005)), ('A', ' 180 ', 'ASN', 0.037408110250381786, (12.191999999999995, -16.487999999999996, 8.803)), ('A', ' 184 ', 'LEU', 0.0, (8.325999999999997, -19.591, -3.035)), ('B', '  40 ', 'ARG', 0.09119902412669473, (8.27, -9.968000000000004, -31.091)), ('B', '  95 ', 'GLU', 0.0008020707602051432, (22.757, 6.952, -10.124)), ('B', '  96 ', 'GLU', 0.2872997519215138, (26.262999999999998, 5.941999999999999, -11.247)), ('B', ' 109 ', 'ASP', 0.28698693372916945, (15.672000000000004, -0.18899999999999997, -31.277)), ('B', ' 110 ', 'THR', 0.01495926990173757, (14.952000000000007, 1.6249999999999996, -34.51)), ('B', ' 118 ', 'GLN', 0.14393564275372417, (-7.007999999999998, 8.956, -26.756)), ('B', ' 144 ', 'LEU', 0.1413301608495103, (-0.2509999999999996, 3.269999999999999, -2.784)), ('B', ' 156 ', 'CYS', 0.1297470327712684, (-6.925999999999998, 11.576999999999996, -10.561)), ('B', ' 174 ', 'SER', 0.09490767937981189, (-18.606, -8.713, -16.969)), ('B', ' 175 ', 'THR', 0.07162002260314806, (-19.966, -10.543, -20.02)), ('B', ' 178 ', 'ASP', 0.010760961188703289, (-19.592999999999993, -0.9909999999999999, -21.977)), ('B', ' 184 ', 'LEU', 0.010578918452449721, (-3.97, -4.192, -17.32)), ('C', ' 110 ', 'LEU', 0.03029923093962503, (8.179, 10.831000000000001, -14.539000000000001))]
data['cbeta'] = []
data['probe'] = [(' B 225  BMA  H62', ' B 226  NDG  N2 ', -1.027, (37.747, -12.01, -37.971)), (' B 225  BMA  H62', ' B 226  NDG  HA ', -1.013, (36.99, -12.548, -38.045)), (' A   1  ALA  H3 ', ' A   2  PRO  HD3', -1.011, (23.868, -22.724, -4.817)), (' A 175  THR  O  ', ' A 175  THR HG23', -0.999, (20.09, -8.766, 8.779)), (' A 175  THR  CG2', ' A 175  THR  O  ', -0.957, (19.761, -8.811, 8.523)), (' B 223  MAN  O3 ', ' B 224  MAN  C1 ', -0.954, (34.87, -3.413, -35.506)), (' A   1  ALA  N  ', ' A   2  PRO  HD3', -0.946, (23.671, -23.432, -3.993)), (' A 110  THR HG22', ' A 219  THR  OG1', -0.908, (13.904, -37.671, -17.802)), (' A   1  ALA  N  ', ' A   2  PRO  CD ', -0.897, (22.964, -22.859, -4.311)), (' A 178  ASP  HB2', ' A 179  ASN  HB2', -0.885, (15.171, -18.514, 12.201)), (' B 185  VAL HG21', ' B 201  MET  HE3', -0.885, (-2.332, 1.495, -16.062)), (' A 176  GLU  HG2', ' A 177  SER  H  ', -0.823, (19.884, -14.301, 10.431)), (' B 183  TRP  CE2', ' B 203  LYS  HG3', -0.82, (-8.014, 1.068, -21.918)), (' A 148  GLU  HG2', ' A 149  GLY  N  ', -0.816, (2.769, -11.049, 2.452)), (' A 148  GLU  HG2', ' A 149  GLY  H  ', -0.808, (3.461, -11.577, 2.163)), (' B 173  GLU  HB3', ' B 174  SER  CB ', -0.789, (-17.835, -7.235, -16.727)), (' A 110  THR  O  ', ' A 110  THR HG23', -0.782, (14.012, -39.965, -19.413)), (' B 203  LYS  HE2', ' B 204  ASP  OD2', -0.778, (-11.759, 0.931, -23.905)), (' B 174  SER  O  ', ' B 175  THR HG22', -0.739, (-21.107, -9.839, -18.144)), (' B   1  ALA  N  ', ' B   2  PRO  CD ', -0.7, (-9.017, -6.16, -31.82)), (' A   1  ALA  H2 ', ' A   2  PRO  CD ', -0.699, (22.694, -23.513, -3.946)), (' B 110  THR HG22', ' B 219  THR  OG1', -0.692, (11.696, 1.885, -35.583)), (' B 225  BMA  C6 ', ' B 226  NDG  HA ', -0.676, (37.101, -12.097, -38.496)), (' A 176  GLU  O  ', ' A 177  SER  HB3', -0.669, (17.931, -15.292, 7.149)), (' A 185  VAL HG21', ' A 201  MET  HE2', -0.665, (4.413, -23.465, -1.603)), (' B 173  GLU  HB3', ' B 174  SER  HB2', -0.664, (-17.587, -6.801, -16.814)), (' A 205  ARG  HG3', ' A 205  ARG HH11', -0.663, (8.516, -21.637, 9.692)), (' B 109  ASP  C  ', ' B 109  ASP  OD1', -0.644, (15.612, 2.112, -31.662)), (' A 201  MET  HE3', ' A 211  ILE HD12', -0.641, (5.237, -25.031, 0.094)), (' B  52  ASN HD22', ' B  84  ASP  H  ', -0.64, (22.254, -1.64, -21.455)), (' B  28  PHE  CE2', ' B  50  GLU  HG2', -0.635, (13.955, -1.289, -14.027)), (' B 136  ILE HD13', ' B 201  MET  HE1', -0.633, (-1.117, 3.166, -14.31)), (' A  52  ASN  ND2', ' A  84  ASP  H  ', -0.633, (-0.095, -32.192, -25.657)), (' A 178  ASP  CB ', ' A 179  ASN  HB2', -0.626, (15.725, -18.695, 12.292)), (' B 177  SER  HB3', ' B 179  ASN  H  ', -0.617, (-20.381, -2.618, -19.437)), (' A 137  ASP  OD2', ' A 140  HIS  HE1', -0.616, (-3.436, -29.281, 6.329)), (' A 161  MET  HE3', ' A 213  SER  HB2', -0.608, (4.567, -34.834, 1.293)), (' A  52  ASN HD22', ' A  84  ASP  H  ', -0.606, (-0.635, -32.047, -25.203)), (' A 115  ILE  H  ', ' A 115  ILE HD12', -0.592, (12.268, -35.116, -6.431)), (' A 110  THR  CG2', ' A 110  THR  O  ', -0.592, (13.923, -39.783, -19.164)), (' A 161  MET  CE ', ' A 213  SER  HB2', -0.589, (4.419, -34.989, 1.425)), (' B   1  ALA  H2 ', ' B   2  PRO  CD ', -0.589, (-8.453, -5.679, -30.979)), (' A 175  THR  O  ', ' A 176  GLU  HB2', -0.588, (19.896, -11.309, 9.642)), (' B   1  ALA  N  ', ' B   2  PRO  HD3', -0.587, (-9.133, -5.689, -32.175)), (' A 176  GLU  HG2', ' A 177  SER  N  ', -0.587, (19.731, -14.632, 9.983)), (' B 137  ASP  OD2', ' B 140  HIS  HE1', -0.586, (-3.887, 12.161, -9.852)), (' B 225  BMA  C6 ', ' B 226  NDG  N2 ', -0.584, (37.907, -11.743, -38.454)), (' B 183  TRP  NE1', ' B 203  LYS  HG3', -0.573, (-8.254, 2.214, -21.129)), (' B 202  ALA  HB1', ' B 205  ARG  HG3', -0.57, (-12.36, 3.968, -15.502)), (' A 201  MET  CE ', ' A 211  ILE HD12', -0.564, (4.62, -24.946, 0.003)), (' A 126  VAL HG11', ' A 169  GLY  HA2', -0.559, (13.696, -22.892, -5.518)), (' A 176  GLU  O  ', ' A 177  SER  CB ', -0.559, (18.05, -15.541, 7.397)), (' B   1  ALA  H3 ', ' B   2  PRO  HD3', -0.557, (-8.533, -6.091, -32.397)), (' B  28  PHE  CD2', ' B  50  GLU  HG2', -0.556, (13.212, -1.254, -14.231)), (' B  52  ASN  ND2', ' B  84  ASP  H  ', -0.551, (22.511, -1.42, -21.916)), (' B 131  PRO  HA ', ' B 167  VAL  O  ', -0.55, (1.683, -3.249, -23.213)), (' B 176  GLU  O  ', ' B 177  SER  HB2', -0.549, (-20.728, -4.686, -19.549)), (' A 177  SER  HA ', ' A 179  ASN  O  ', -0.538, (16.113, -15.433, 10.012)), (' A 168  VAL HG23', ' A 184  LEU HD13', -0.537, (8.888, -18.255, -7.068)), (' A 109  ASP  C  ', ' A 109  ASP  OD1', -0.535, (9.488, -37.776, -20.693)), (' B 176  GLU  HG2', ' B 177  SER  N  ', -0.528, (-23.616, -5.338, -20.57)), (' A 205  ARG  HG3', ' A 205  ARG  NH1', -0.523, (7.85, -21.543, 10.197)), (' A 168  VAL  CG2', ' A 184  LEU HD13', -0.517, (8.649, -18.284, -7.008)), (' A   1  ALA  H2 ', ' A   2  PRO  HD2', -0.517, (22.206, -22.948, -3.5)), (' B 110  THR  O  ', ' B 110  THR HG23', -0.51, (13.861, 2.776, -36.477)), (' A  77  VAL  HB ', ' A 109  ASP  OD2', -0.503, (6.758, -36.412, -19.684)), (' B  28  PHE  CZ ', ' B  50  GLU  HG2', -0.502, (13.928, -0.669, -13.218)), (' B   1  ALA  H2 ', ' B   2  PRO  HD2', -0.502, (-8.325, -5.509, -30.725)), (' A 115  ILE HG22', ' A 116  PRO  O  ', -0.502, (13.224, -35.141, -1.381)), (' A 186  LYS  HB2', ' A 198  TYR  CE2', -0.501, (4.922, -19.151, -9.064)), (' A 115  ILE  N  ', ' A 115  ILE HD12', -0.493, (12.778, -35.587, -5.832)), (' A   8  ARG  HD3', ' A 198  TYR  CZ ', -0.489, (6.436, -16.609, -9.705)), (' B 223  MAN  HO3', ' B 224  MAN  C1 ', -0.483, (35.206, -3.672, -35.0)), (' B  27  ALA  O  ', ' B  31  THR HG23', -0.482, (13.964, 0.408, -18.903)), (' B 150  ILE HD12', ' B 180  ASN HD22', -0.481, (-14.775, -2.399, -13.303)), (' A 148  GLU  CG ', ' A 149  GLY  H  ', -0.478, (2.867, -11.19, 2.088)), (' A  52  ASN HD21', ' A 100  TYR  HD1', -0.477, (-1.026, -33.766, -26.161)), (' A   3  ARG  NH2', ' A 176  GLU  O  ', -0.477, (20.037, -15.239, 6.245)), (' A  70  MET  HG2', ' A 133  SER  HB3', -0.476, (3.999, -31.826, -9.785)), (' B 225  BMA  C6 ', ' B 226  NDG  H3 ', -0.461, (38.201, -12.092, -36.54)), (' A 185  VAL  HB ', ' A 199  VAL HG13', -0.461, (3.26, -20.936, -2.168)), (' B 173  GLU  HB3', ' B 174  SER  OG ', -0.457, (-18.747, -6.838, -15.972)), (' B 225  BMA  H62', ' B 226  NDG  H3 ', -0.449, (37.975, -12.305, -37.072)), (' B 176  GLU  CG ', ' B 177  SER  N  ', -0.445, (-23.435, -5.827, -20.591)), (' A 174  SER  O  ', ' A 175  THR  C  ', -0.444, (18.316, -10.829, 8.544)), (' A 173  GLU  HG2', ' A 174  SER  HB3', -0.437, (12.832, -11.286, 8.359)), (' B 122  LEU  O  ', ' B 126  VAL HG23', -0.436, (-3.034, 0.029, -26.324)), (' A 144  LEU  HA ', ' A 144  LEU HD12', -0.435, (-8.021, -20.563, -0.499)), (' B 173  GLU  CB ', ' B 174  SER  HB2', -0.434, (-17.327, -6.551, -16.323)), (' A 131  PRO  O  ', ' A 132  ILE HD13', -0.431, (11.435, -28.499, -10.306)), (' A 191  GLU  O  ', ' A 196  GLY  HA2', -0.43, (-2.574, -12.387, -8.08)), (' B 153  GLU  H  ', ' B 208  HIS  CE1', -0.424, (-9.825, 7.008, -10.889)), (' B 153  GLU  O  ', ' B 156  CYS  HB2', -0.424, (-8.825, 9.54, -10.014)), (' A   8  ARG  HD3', ' A 198  TYR  CE2', -0.423, (6.389, -17.363, -9.038)), (' A 151  TYR  HB3', ' A 201  MET  HG2', -0.422, (2.598, -20.532, 3.319)), (' A 175  THR  O  ', ' A 175  THR HG22', -0.421, (19.079, -9.158, 9.275)), (' B 120  LYS  HE3', ' B 124  LYS  NZ ', -0.415, (-9.55, 4.131, -34.136)), (' B  52  ASN  ND2', ' B  83  LEU HD12', -0.413, (21.939, -0.365, -21.645)), (' B 208  HIS  CD2', ' B 209  CYS  SG ', -0.413, (-7.126, 7.04, -12.756)), (' B  69  LEU HD12', ' B  72  TYR  CZ ', -0.413, (11.664, 13.767, -22.596)), (' B 110  THR  CG2', ' B 110  THR  O  ', -0.412, (13.746, 2.558, -36.026)), (' B  58  GLY  N  ', ' B  59  PRO  CD ', -0.41, (22.471, 10.843, -20.785)), (' A 201  MET  O  ', ' A 202  ALA  C  ', -0.408, (8.067, -22.412, 4.396)), (' A 185  VAL HG21', ' A 201  MET  CE ', -0.408, (4.57, -24.0, -0.749)), (' A 178  ASP  CA ', ' A 179  ASN  HB2', -0.406, (15.175, -18.619, 11.952)), (' A 207  ASN  ND2', ' A 210  GLY  HA2', -0.405, (5.702, -32.426, 4.809)), (' A  58  GLY  HA2', ' A  62  ASN  O  ', -0.403, (-6.292, -41.057, -15.663)), (' A 122  LEU  O  ', ' A 126  VAL HG23', -0.403, (14.015, -27.16, -3.709)), (' A  38  MET  HE2', ' A 107  ALA  HA ', -0.401, (9.134, -30.019, -25.126)), (' A 115  ILE  HA ', ' A 116  PRO  HD2', -0.4, (15.132, -36.977, -4.176))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
