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
data['rama'] = [('B', '   7 ', 'TRP', 0.03804509472980318, (3.3779999999999992, -22.691, -74.02700000000003))]
data['omega'] = []
data['rota'] = [('A', '  13 ', 'VAL', 0.20991002748815538, (0.9509999999999997, -19.72, -27.21)), ('A', '  34 ', 'LEU', 0.07509381958316957, (-2.404, -11.412000000000004, -22.647)), ('A', ' 120 ', 'LYS', 0.27264273524122473, (18.376000000000005, -5.417000000000002, -27.568)), ('A', ' 148 ', 'GLU', 0.24458373820277404, (8.974, -19.566000000000006, -45.442)), ('A', ' 155 ', 'ASP', 0.16925326788614473, (11.817, -1.468, -48.63)), ('A', ' 156 ', 'CYS', 0.05492158234119415, (10.357, -1.9440000000000002, -45.146)), ('A', ' 184 ', 'LEU', 0.13159139142028714, (9.849999999999996, -15.739000000000003, -34.31900000000002)), ('B', '  22 ', 'CYS', 0.23864546372080225, (-8.536, -3.431, -58.763)), ('B', ' 120 ', 'LYS', 0.10708276619929959, (-11.541, -32.66300000000001, -72.599)), ('B', ' 141 ', 'GLU', 0.21666861555541192, (-8.129, -18.50400000000001, -48.49)), ('B', ' 148 ', 'GLU', 0.010353080077433343, (2.942, -25.132999999999992, -54.503)), ('B', ' 156 ', 'CYS', 0.05492158234119415, (-14.513000000000002, -25.059, -55.016)), ('B', ' 159 ', 'GLU', 0.016950964132640967, (-20.427999999999997, -23.250000000000007, -61.301)), ('B', ' 160 ', 'ASP', 0.0029592019110501726, (-19.363, -20.182, -59.305)), ('B', ' 184 ', 'LEU', 0.0335584668655377, (-0.666, -24.862000000000005, -65.562))]
data['cbeta'] = []
data['probe'] = [(' B  38  MET  HE2', ' B 107  ALA  HA ', -0.861, (-2.164, -7.059, -82.466)), (' A 207  ASN  ND2', ' A 210  GLY  HA2', -0.829, (12.174, -0.335, -36.667)), (' B 219  THR  HA ', ' B 261  HOH  O  ', -0.773, (-7.688, -16.382, -83.656)), (' B  34  LEU HD22', ' B  48  LEU HD11', -0.74, (-2.999, -8.869, -78.56)), (' A  20  GLY  O  ', ' A 300  NSZ  H5 ', -0.737, (-8.403, -9.932, -42.715)), (' B 108  ASN  ND2', ' B 109  ASP  H  ', -0.737, (-9.068, -7.936, -82.993)), (' A 147  LYS  HD2', ' B 269  HOH  O  ', -0.725, (4.745, -18.399, -52.949)), (' B 108  ASN HD22', ' B 109  ASP  H  ', -0.717, (-8.822, -7.174, -82.753)), (' A 108  ASN HD22', ' A 109  ASP  H  ', -0.697, (-6.53, -7.241, -17.032)), (' B 207  ASN  ND2', ' B 210  GLY  HA2', -0.69, (-15.544, -25.832, -64.231)), (' B  74  PHE  CZ ', ' B 218  PRO  HD3', -0.69, (-9.412, -13.824, -76.256)), (' A 174  SER  HB2', ' A 254  HOH  O  ', -0.662, (22.104, -25.467, -40.626)), (' A 221  HOH  O  ', ' A 300  NSZ H133', -0.658, (-3.018, 1.208, -40.537)), (' A 153  GLU  H  ', ' A 208  HIS  CE1', -0.654, (13.313, -6.105, -44.92)), (' A 207  ASN HD21', ' A 210  GLY  HA2', -0.646, (11.539, -0.104, -35.919)), (' B  74  PHE  HB3', ' B 264  HOH  O  ', -0.644, (-11.898, -11.399, -79.256)), (' B  34  LEU HD23', ' B  38  MET  HG2', -0.638, (-2.709, -10.597, -80.0)), (' B  77  VAL HG12', ' B 108  ASN  ND2', -0.632, (-9.022, -6.051, -82.421)), (' B  38  MET  HE2', ' B 107  ALA  CA ', -0.625, (-2.627, -7.48, -82.235)), (' A  92  GLU  OE2', ' A  96  GLU  HG3', -0.621, (-20.886, -9.723, -33.663)), (' B   7  TRP  CE2', ' B 130  GLY  HA2', -0.615, (-0.34, -23.028, -77.25)), (' B 118  GLN  HB2', ' B 252  HOH  O  ', -0.61, (-16.692, -30.317, -73.925)), (' B  49  SER  OG ', ' B  89  TYR  HB3', -0.609, (-2.84, 0.207, -72.519)), (' A 146  TYR  CE2', ' A 199  VAL HG23', -0.601, (7.725, -15.509, -43.074)), (' B 137  ASP  OD2', ' B 140  HIS  HE1', -0.59, (-14.55, -21.788, -54.836)), (' B  25  CSD  HB3', ' B 221  HOH  O  ', -0.587, (-7.954, -11.669, -63.857)), (' B  37  GLN  NE2', ' B 129  VAL HG12', -0.586, (-4.864, -19.456, -79.686)), (' B  77  VAL HG12', ' B 108  ASN HD22', -0.585, (-9.169, -6.67, -81.715)), (' B  97  SER  O  ', ' B  99  LYS  HG3', -0.582, (-7.93, 7.352, -71.092)), (' B  38  MET  CE ', ' B 107  ALA  HA ', -0.565, (-1.986, -7.718, -83.431)), (' A 146  TYR  CZ ', ' A 199  VAL HG23', -0.559, (8.577, -15.538, -42.635)), (' B  34  LEU HD22', ' B  48  LEU  CD1', -0.556, (-3.481, -8.351, -77.629)), (' B  60  GLN  HG2', ' B  76  TYR  HA ', -0.553, (-15.548, -4.163, -77.516)), (' B 120  LYS  HB3', ' B 120  LYS  NZ ', -0.548, (-13.797, -33.293, -73.788)), (' A 101  ASN  OD1', ' A 103  LYS  HB3', -0.548, (-20.829, -13.615, -17.131)), (' B  48  LEU HD13', ' B  83  LEU HD23', -0.545, (-4.456, -6.236, -77.033)), (' B 108  ASN  ND2', ' B 109  ASP  N  ', -0.544, (-8.742, -7.919, -83.502)), (' A 108  ASN HD22', ' A 109  ASP  N  ', -0.538, (-6.563, -7.511, -16.544)), (' B 187  ASN  HB3', ' B 230  HOH  O  ', -0.537, (-0.759, -14.369, -60.558)), (' B  91  TYR  CZ ', ' B  93  ALA  HA ', -0.53, (-5.115, -1.481, -62.373)), (' B 160  ASP  CG ', ' B 160  ASP  O  ', -0.528, (-18.158, -19.406, -57.71)), (' B  38  MET  HE2', ' B 107  ALA  CB ', -0.525, (-2.482, -7.733, -81.806)), (' B   7  TRP  NE1', ' B 130  GLY  HA2', -0.525, (-0.745, -23.225, -76.52)), (' B  52  ASN  C  ', ' B  52  ASN HD22', -0.522, (-8.152, 0.125, -73.308)), (' A 207  ASN  CG ', ' A 210  GLY  HA2', -0.521, (12.346, -1.347, -36.206)), (' A 109  ASP  HA ', ' A 220  VAL  HA ', -0.521, (-2.583, -8.202, -15.564)), (' B  37  GLN HE22', ' B 129  VAL HG12', -0.518, (-4.833, -20.078, -79.765)), (' B 108  ASN HD22', ' B 109  ASP  N  ', -0.514, (-8.183, -7.74, -82.819)), (' A 108  ASN  ND2', ' A 109  ASP  H  ', -0.509, (-7.04, -6.752, -16.462)), (' B 206  ARG  HD2', ' B 270  HOH  O  ', -0.509, (-14.563, -34.889, -58.683)), (' A  96  GLU  HG3', ' A 230  HOH  O  ', -0.508, (-20.256, -9.688, -32.322)), (' A 200  LYS  HD3', ' A 272  HOH  O  ', -0.502, (13.133, -20.912, -38.73)), (' A 193  TRP  CH2', ' A 199  VAL  HB ', -0.501, (5.312, -14.31, -41.486)), (' B  34  LEU  O  ', ' B  34  LEU HD23', -0.5, (-3.367, -11.362, -79.144)), (' A  85  SER  HB3', ' A 106  VAL HG21', -0.499, (-12.171, -16.968, -21.403)), (' B  49  SER  HG ', ' B  89  TYR  HB3', -0.498, (-2.244, 0.202, -72.08)), (' B 104  TYR  O  ', ' B 106  VAL HG13', -0.498, (0.6, -0.593, -80.903)), (' A 300  NSZ  H15', ' B 145  PHE  CZ ', -0.495, (-4.079, -13.8, -46.735)), (' A 145  PHE  HZ ', ' B 400  NSZ  H15', -0.494, (-2.181, -11.653, -53.514)), (' B 138  ALA  HB1', ' B 143  PHE  CD2', -0.49, (-7.604, -17.835, -56.67)), (' A 187  ASN  HB3', ' A 246  HOH  O  ', -0.486, (-0.234, -15.502, -39.58)), (' B  60  GLN  HG2', ' B  76  TYR  CA ', -0.482, (-15.189, -4.701, -77.163)), (' A  74  PHE  CZ ', ' A 218  PRO  HD3', -0.479, (-0.205, -6.872, -24.081)), (' B  63  GLU  CG ', ' B 400  NSZ  H55', -0.478, (-19.539, -4.352, -65.138)), (' A 145  PHE  CZ ', ' B 400  NSZ  H15', -0.477, (-1.838, -11.411, -53.386)), (' B 164  GLY  O  ', ' B 221  HOH  O  ', -0.475, (-7.737, -12.924, -64.599)), (' B 101  ASN  OD1', ' B 103  LYS  HB3', -0.474, (-1.663, 6.503, -82.283)), (' B  58  GLY  N  ', ' B  59  PRO  CD ', -0.473, (-16.625, 0.368, -72.96)), (' A   7  TRP  CE2', ' A 130  GLY  HA2', -0.47, (8.114, -15.487, -23.116)), (' A  34  LEU  HB3', ' A  48  LEU  CD1', -0.463, (-5.052, -11.997, -23.202)), (' A 160  ASP  O  ', ' A 160  ASP  OD1', -0.463, (5.088, 1.485, -42.085)), (' B 207  ASN HD21', ' B 210  GLY  HA2', -0.463, (-15.956, -25.995, -64.539)), (' A  25  CSD  OD2', ' A 163  HIS  HA ', -0.459, (-1.731, -4.79, -38.349)), (' B  20  GLY  O  ', ' B 400  NSZ  H5 ', -0.459, (-5.806, -6.287, -57.417)), (' A 153  GLU  O  ', ' A 156  CYS  HB2', -0.456, (12.256, -3.873, -45.471)), (' A  63  GLU  HG2', ' A 300  NSZ  H55', -0.454, (-9.716, 3.692, -33.852)), (' A 153  GLU  HG3', ' A 156  CYS  N  ', -0.452, (10.707, -2.947, -46.972)), (' A 161  MET  HE3', ' A 213  SER  HB2', -0.448, (8.353, 0.357, -34.447)), (' B 113  VAL HG23', ' B 219  THR HG23', -0.448, (-11.855, -17.727, -82.516)), (' B 220  VAL  OXT', ' B 220  VAL HG23', -0.446, (-5.362, -14.669, -85.844)), (' B  78  GLN  NE2', ' B 110  THR  O  ', -0.443, (-14.718, -10.72, -85.08)), (' B 122  LEU  O  ', ' B 126  VAL HG23', -0.442, (-7.266, -26.533, -73.817)), (' B  46  ILE  N  ', ' B  46  ILE HD12', -0.44, (4.882, -8.737, -79.371)), (' A  73  ALA  O  ', ' A  77  VAL HG23', -0.435, (-7.797, -4.903, -23.006)), (' A 108  ASN  ND2', ' A 109  ASP  N  ', -0.432, (-6.921, -7.083, -16.203)), (' A 153  GLU  O  ', ' A 208  HIS  HE1', -0.43, (13.583, -4.871, -45.066)), (' A 153  GLU  N  ', ' A 208  HIS  CE1', -0.43, (13.292, -6.639, -45.108)), (' B 186  LYS  HB2', ' B 198  TYR  CE2', -0.429, (1.33, -18.54, -66.397)), (' A 135  ALA  O  ', ' A 161  MET  HG2', -0.427, (6.329, -2.312, -36.021)), (' B 172  PHE  CD1', ' B 172  PHE  N  ', -0.426, (1.518, -34.562, -66.368)), (' B 129  VAL HG11', ' B 217  TYR  CD2', -0.424, (-7.515, -20.251, -79.54)), (' B 119  GLU  OE1', ' B 204  ASP  HA ', -0.423, (-11.246, -32.694, -65.259)), (' A  58  GLY  N  ', ' A  59  PRO  CD ', -0.421, (-14.62, 1.752, -26.718)), (' B  37  GLN  HG3', ' B 218  PRO  O  ', -0.42, (-6.967, -15.849, -80.669)), (' A 141  GLU  HG3', ' B 192  GLU  HG3', -0.42, (5.18, -9.293, -53.897)), (' B 199  VAL HG22', ' B 201  MET  HG3', -0.419, (-3.773, -23.899, -59.944)), (' A 153  GLU  C  ', ' A 155  ASP  H  ', -0.419, (12.628, -4.131, -47.537)), (' A 101  ASN  HB3', ' A 104  TYR  HD2', -0.418, (-20.358, -12.918, -20.267)), (' B 173  GLU  HA ', ' B 237  HOH  O  ', -0.418, (5.537, -35.199, -62.525)), (' B 115  ILE HG23', ' B 116  PRO  HD2', -0.417, (-14.242, -26.09, -76.363)), (' B 138  ALA  HA ', ' B 255  HOH  O  ', -0.417, (-10.126, -20.163, -55.538)), (' A 120  LYS  HB3', ' A 120  LYS  NZ ', -0.416, (19.795, -3.289, -26.318)), (' A  34  LEU HD13', ' A  48  LEU HD13', -0.412, (-6.582, -11.172, -22.28)), (' B  34  LEU HD21', ' B 107  ALA  HB1', -0.41, (-3.868, -8.84, -80.24)), (' B  13  VAL HG12', ' B  14  THR  O  ', -0.41, (4.091, -14.78, -69.411)), (' A 110  THR  N  ', ' A 219  THR  O  ', -0.41, (-2.559, -6.057, -15.576)), (' A  28  PHE  CD2', ' A  50  GLU  HG2', -0.408, (-7.895, -11.805, -32.474)), (' A  78  GLN  NE2', ' A 110  THR  C  ', -0.408, (-3.199, -1.675, -15.033)), (' A   3  ARG  HG3', ' A   3  ARG HH11', -0.406, (24.085, -20.31, -28.013)), (' A 166  LEU  HB3', ' A 186  LYS  HB3', -0.403, (2.317, -13.872, -32.152)), (' A  52  ASN  OD1', ' A  83  LEU HD12', -0.402, (-13.21, -9.216, -23.329)), (' A  67  GLY  HA2', ' A 300  NSZ  O39', -0.402, (-6.605, -0.67, -36.738)), (' A  70  MET  HG2', ' A 133  SER  HB3', -0.402, (0.54, -6.05, -29.295)), (' A  60  GLN  HG2', ' A  76  TYR  N  ', -0.401, (-8.788, 0.258, -22.75)), (' B 168  VAL HG23', ' B 184  LEU HD13', -0.401, (1.938, -23.273, -68.197)), (' B  29  SER  HB3', ' B  70  MET  CG ', -0.401, (-9.923, -12.961, -69.144))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
