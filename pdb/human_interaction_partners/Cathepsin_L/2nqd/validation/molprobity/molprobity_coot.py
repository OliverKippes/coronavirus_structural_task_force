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
data['rama'] = [('B', '   1 ', 'ALA', 0.0012432928439259938, (22.595, 0.7680000000000002, -5.752000000000002)), ('B', ' 178 ', 'ASP', 0.03270301389812848, (5.147000000000002, 6.581000000000001, -14.383))]
data['omega'] = []
data['rota'] = [('A', '   4 ', 'LYS', 0.0758281829435583, (-18.799999999999997, 22.125400000000003, 24.638800000000007)), ('A', '   5 ', 'VAL', 0.04954413940759332, (-19.257999999999996, 15.934000000000001, 24.195000000000007)), ('A', '   7 ', 'LYS', 0.0795707303434336, (-16.111, 10.159, 26.784)), ('B', '  60 ', 'GLN', 0.25304654309543306, (16.459, 7.448, 27.56800000000001)), ('B', ' 108 ', 'ASN', 0.10100822728071497, (26.23825, -6.358499999999999, 22.4435)), ('B', ' 156 ', 'CYS', 0.10299211501388851, (0.5869999999999994, 12.789000000000001, 3.6350000000000007)), ('B', ' 177 ', 'SER', 0.00929918548552188, (4.2570000000000014, 2.991, -15.406000000000004))]
data['cbeta'] = [('B', ' 108 ', 'ASN', 'A', 0.30180769530231444, (25.517, -5.674, 22.468)), ('B', ' 108 ', 'ASN', 'B', 0.3287826894930601, (25.247, -5.523, 23.014000000000006))]
data['probe'] = [(' A   4 ALYS  HD2', ' A  25 AGLN  OE1', -0.967, (-15.24, 19.838, 22.34)), (' B   6  ASP  O  ', ' B   9 BGLU  HG2', -0.829, (15.224, -9.676, -0.302)), (' B   1 BALA  CB ', ' B   1PBGLU  O  ', -0.804, (21.431, 1.991, -5.245)), (' B   1 BALA  HB3', ' B   1PBGLU  O  ', -0.797, (20.565, 2.491, -5.224)), (' B   8  ARG  NH2', ' B 184 BLEU HD21', -0.762, (9.349, -7.121, 0.337)), (' B 108 BASN  ND2', ' B1265  HOH  O  ', -0.741, (26.341, -6.427, 19.579)), (' B  40 BARG HH12', ' B 129  VAL  HA ', -0.713, (24.625, -2.683, 5.655)), (' B  66  ASN  ND2', ' B1001   CL CL  ', -0.69, (0.371, 7.625, 25.608)), (' B 117 BLYS  NZ ', ' B1255  HOH  O  ', -0.667, (15.369, 13.522, 11.184)), (' A   3 AHIS  HB2', ' A 702  HOH  O  ', -0.661, (-24.587, 21.409, 19.999)), (' B   1 BALA  HB3', ' B 123  MET  HE2', -0.661, (20.581, 2.151, -5.566)), (' A  63 BLYS  HE3', ' B  72  TYR  OH ', -0.655, (13.222, 13.03, 22.032)), (' A  58  PHE  HB2', ' A  70 BTHR HG22', -0.628, (-7.482, 15.291, 17.989)), (' B   8  ARG HH21', ' B 184 BLEU HD21', -0.627, (9.707, -7.756, 0.083)), (' A  21  LEU HD11', ' A  74  HIS  HB3', -0.594, (-19.769, 19.388, 12.729)), (' A  74  HIS  CE1', ' A 718  HOH  O  ', -0.545, (-17.031, 19.737, 15.24)), (' B 163  HIS  HA ', ' B1193  HOH  O  ', -0.538, (4.014, 5.053, 15.103)), (' A  63 BLYS  HE2', ' A 656  HOH  O  ', -0.525, (10.338, 13.393, 24.022)), (' A   3 AHIS  CE1', ' A  14  LEU  HG ', -0.525, (-25.715, 18.379, 24.437)), (' B 173  GLU  HG3', ' B 176 AGLU  OE1', -0.522, (2.556, -0.883, -8.81)), (' A  39 AGLU  HG2', ' A 636  HOH  O  ', -0.518, (-22.646, 0.493, 15.276)), (' A   3 BHIS  ND1', ' A  20  GLU  OE2', -0.49, (-27.087, 22.177, 20.805)), (' A   7  LYS  HD2', ' A 666  HOH  O  ', -0.481, (-11.942, 6.994, 24.791)), (' A  48  GLU  OE1', ' A  52 ATHR HG22', -0.475, (-25.111, 14.421, 5.094)), (' A   3 BHIS  HB2', ' A 702  HOH  O  ', -0.447, (-24.458, 21.533, 20.358)), (' B 168  VAL HG23', ' B 184 BLEU HD23', -0.443, (11.375, -5.789, 1.86)), (' A  48  GLU  OE1', ' A  52 BTHR HG23', -0.439, (-24.162, 14.389, 5.579)), (' A  63 BLYS  HG2', ' A 626  HOH  O  ', -0.438, (8.357, 14.719, 23.019)), (' A  58  PHE  HB2', ' A  70 BTHR  CG2', -0.437, (-7.66, 15.486, 17.998)), (' A   3 AHIS  CD2', ' A  16  VAL HG12', -0.418, (-27.223, 20.331, 21.545)), (' A   3 AHIS  HD2', ' A  16  VAL HG12', -0.417, (-27.378, 20.242, 21.087)), (' B   7  TRP  CE2', ' B 130  GLY  HA2', -0.415, (19.837, -4.935, 4.105)), (' A  63 ALYS  NZ ', ' A 700  HOH  O  ', -0.408, (13.592, 16.749, 22.575)), (' A  54  GLU  HB2', ' A  74  HIS  HB2', -0.405, (-18.012, 17.483, 10.863)), (' B   8  ARG  HD3', ' B 198  TYR  CZ ', -0.405, (8.92, -8.656, 4.882)), (' A   3 BHIS  CE1', ' A  20  GLU  OE2', -0.401, (-27.155, 22.426, 21.109))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
