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
data['rama'] = [('A', ' 600 ', 'ASN', 0.03347357056653306, (24.713000000000005, 16.597999999999992, 10.017)), ('A', ' 636 ', 'SER', 0.013983289102261447, (16.241999999999997, 9.174, 32.36500000000001)), ('B', ' 518 ', 'ALA', 0.0194906, (7.613999999999995, 53.30799999999999, 33.979000000000006)), ('B', ' 600 ', 'ASN', 0.037371422917281585, (23.897999999999996, 57.321, 28.079)), ('B', ' 636 ', 'SER', 0.018579375686002965, (3.659999999999999, 60.006, 13.418000000000003))]
data['omega'] = [('A', ' 442 ', 'PRO', None, (18.240000000000002, 42.233, 3.769000000000001)), ('A', ' 491 ', 'GLY', None, (9.324, 25.451, 14.491)), ('B', ' 442 ', 'PRO', None, (28.095, 30.119, 36.005))]
data['rota'] = [('A', ' 399 ', 'THR', 0.057660000873072256, (-9.004, 17.436, 1.372)), ('A', ' 438 ', 'GLU', 0.0009728213236517174, (17.553000000000004, 37.085, -1.247)), ('A', ' 444 ', 'MET', 0.03786290311765041, (11.446, 43.903, 8.23)), ('A', ' 525 ', 'ILE', 0.02101771081271221, (10.966000000000001, 6.852999999999999, 17.742)), ('A', ' 562 ', 'ARG', 0.2517449484084324, (38.157000000000004, 11.963, 35.537000000000006)), ('A', ' 565 ', 'LYS', 0.02361570972968042, (42.274000000000015, 12.815999999999999, 32.139)), ('A', ' 570 ', 'GLN', 0.0, (36.193, 24.171, 25.341000000000008)), ('A', ' 636 ', 'SER', 0.0013399975614447612, (16.241999999999997, 9.174, 32.36500000000001)), ('A', ' 652 ', 'SER', 0.14857840767395963, (2.5559999999999996, 20.623, 20.006)), ('B', ' 393 ', 'CYS', 0.23809376759827586, (-0.07100000000000506, 35.548, 47.845)), ('B', ' 397 ', 'VAL', 0.00945159699767828, (1.9589999999999996, 48.128, 47.00500000000001)), ('B', ' 404 ', 'THR', 0.16203406572662596, (7.855, 48.071, 53.043)), ('B', ' 444 ', 'MET', 0.0, (20.467999999999993, 27.031000000000006, 35.133)), ('B', ' 517 ', 'GLU', 0.001208581777082628, (9.876000000000001, 51.546, 36.51500000000001)), ('B', ' 562 ', 'ARG', 0.2431914039048434, (20.464000000000002, 62.832, -0.28800000000000003)), ('B', ' 565 ', 'LYS', 0.018028271608327685, (25.804999999999996, 63.467, 0.35100000000000003)), ('B', ' 570 ', 'GLN', 2.7712248531029115e-05, (27.727, 51.57800000000001, 8.574))]
data['cbeta'] = [('A', ' 492 ', 'CYS', ' ', 0.35009689229533086, (13.535999999999994, 24.308, 18.514)), ('A', ' 541 ', 'GLU', ' ', 0.26117704976781936, (34.647000000000006, 5.75, 23.39)), ('A', ' 593 ', 'ILE', ' ', 0.2809803882598383, (18.319999999999993, 22.191, 17.509000000000004)), ('B', ' 397 ', 'VAL', ' ', 0.3413459747430906, (2.916999999999997, 47.76799999999999, 48.175)), ('B', ' 423 ', 'HIS', ' ', 0.30068960964153846, (16.505999999999997, 47.113, 35.169000000000004)), ('B', ' 542 ', 'GLU', ' ', 0.32528029717258833, (20.848999999999997, 72.844, 15.468)), ('B', ' 593 ', 'ILE', ' ', 0.3032228374179787, (16.511, 49.42, 24.621000000000006))]
data['probe'] = [(' B 435  SER  HB2', ' B2020  HOH  O  ', -0.782, (31.061, 38.404, 47.683)), (' B 551  MET  HG3', ' B 582  PHE  HB3', -0.66, (22.61, 52.401, 10.163)), (' A 551  MET  HG3', ' A 582  PHE  HB3', -0.635, (31.081, 22.529, 26.279)), (' A 547  MET  HE2', ' A 549  ILE HD11', -0.632, (27.529, 13.169, 26.76)), (' B 547  MET  HE2', ' B 549  ILE HD11', -0.62, (16.663, 59.665, 11.788)), (' B 518  ALA  HB3', ' B 519  PRO  HD3', -0.618, (5.238, 53.631, 35.033)), (' A 444  MET  HG2', ' B 612  THR  HA ', -0.618, (10.707, 47.355, 10.344)), (' B 549  ILE  CG2', ' B 557  MET  HE1', -0.594, (18.294, 55.395, 9.207)), (' B 563  LYS  HE3', ' B2045  HOH  O  ', -0.591, (16.469, 67.946, 7.073)), (' B 544  ARG  NE ', ' B2066  HOH  O  ', -0.59, (26.425, 67.625, 14.309)), (' B 589  VAL HG13', ' B 608  ILE HG22', -0.569, (13.82, 48.454, 19.746)), (' A 417  ILE HD11', ' A 445  VAL HG23', -0.565, (11.32, 40.989, 11.12)), (' B 549  ILE HG21', ' B 557  MET  HE1', -0.564, (19.065, 55.976, 9.232)), (' A 549  ILE  CG2', ' A 557  MET  HE1', -0.557, (29.778, 17.725, 28.741)), (' B 417  ILE HD11', ' B 445  VAL HG23', -0.55, (18.078, 29.332, 32.067)), (' A 400  THR  O  ', ' A 404  THR HG23', -0.543, (-6.411, 19.727, -2.3)), (' A 589  VAL HG13', ' A 608  ILE HG22', -0.543, (18.367, 22.165, 22.677)), (' A 570  GLN  NE2', ' A2061  HOH  O  ', -0.532, (37.011, 23.62, 19.895)), (' A 444  MET  HE3', ' B 611  VAL HG12', -0.528, (8.896, 48.705, 8.883)), (' B 558  ALA  HB1', ' B 562  ARG HH21', -0.511, (16.541, 58.061, -2.191)), (' B 436  PHE  HD1', ' B2021  HOH  O  ', -0.507, (27.092, 38.577, 48.232)), (' B 426  GLN  NE2', ' B2013  HOH  O  ', -0.505, (23.123, 44.336, 38.204)), (' A 549  ILE HG21', ' A 557  MET  HE1', -0.502, (30.145, 17.716, 29.153)), (' A 558  ALA  HB1', ' A 562  ARG HH21', -0.495, (34.489, 15.545, 38.977)), (' B 534  ARG  HG2', ' B2045  HOH  O  ', -0.478, (15.327, 68.375, 7.522)), (' A 625  ARG HH12', ' A 652  SER  H  ', -0.458, (3.98, 19.542, 18.508)), (' A 628  ARG  NH2', ' A1653  SO4  O2 ', -0.458, (15.097, 23.255, 10.705)), (' B 434  MET  HE1', ' B 454  ILE HD13', -0.452, (21.804, 40.897, 48.109)), (' A 417  ILE HG12', ' A2009  HOH  O  ', -0.448, (13.093, 37.669, 11.378)), (' B 487  TYR  HD2', ' B2039  HOH  O  ', -0.438, (6.334, 45.413, 39.251)), (' B 595  LYS  HG3', ' B2071  HOH  O  ', -0.437, (23.612, 46.332, 23.117)), (' A 573  ILE HD11', ' A 599  LEU HD21', -0.43, (30.246, 19.78, 15.314)), (' B 642  THR HG22', ' B2091  HOH  O  ', -0.429, (-0.877, 64.34, 25.046)), (' A 563  LYS  HE3', ' A2052  HOH  O  ', -0.429, (32.698, 4.892, 30.492)), (' B 462  LYS  HD3', ' B 495  TYR  HA ', -0.42, (7.016, 37.889, 28.435)), (' A 606  MET  HG2', ' A2081  HOH  O  ', -0.418, (19.918, 11.809, 29.205)), (' A 477  LYS  NZ ', ' A2035  HOH  O  ', -0.414, (5.777, 46.149, 7.291)), (' B 563  LYS  NZ ', ' B2058  HOH  O  ', -0.412, (18.419, 68.907, 7.497)), (' B 573  ILE HD11', ' B 599  LEU HD21', -0.41, (26.636, 55.233, 20.041)), (' A 524  GLU  HG3', ' A 526  LEU  H  ', -0.408, (12.456, 5.721, 15.506)), (' A 462  LYS  HD3', ' A 495  TYR  HA ', -0.407, (5.444, 30.583, 19.622)), (' B 544  ARG  NH2', ' B 579  ARG  HG3', -0.406, (27.697, 65.049, 15.567)), (' B 589  VAL  HA ', ' B 592  ILE HD12', -0.404, (15.89, 46.712, 19.159)), (' B 488  PRO  HD2', ' B 500  ALA  HB1', -0.4, (6.459, 39.151, 37.072))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
