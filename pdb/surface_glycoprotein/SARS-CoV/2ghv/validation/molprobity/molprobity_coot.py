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
data['rama'] = [('C', ' 321 ', 'ASN', 0.030779620735590874, (13.28, 2.3659999999999997, -1.467)), ('E', ' 321 ', 'ASN', 0.030275381029537692, (19.558, 1.592, 27.665))]
data['omega'] = [('C', ' 470 ', 'PRO', None, (-0.9740000000000002, -41.171, -26.504)), ('E', ' 467 ', 'CYS', None, (-8.384, -29.491, 54.136)), ('E', ' 470 ', 'PRO', None, (-2.074, -36.321, 57.177))]
data['rota'] = [('E', ' 320 ', 'THR', 0.09825199044271278, (20.617, 4.476, 25.372)), ('E', ' 377 ', 'LEU', 0.19319241257765918, (8.842000000000004, -9.094, 15.305999999999997)), ('E', ' 382 ', 'VAL', 0.030361591211964915, (7.2490000000000006, -6.902000000000002, 24.842)), ('E', ' 395 ', 'ARG', 0.2285429318550678, (3.019999999999999, -28.052, 22.526)), ('E', ' 402 ', 'THR', 0.0027198671887163073, (-5.513, -28.353, 26.837)), ('E', ' 417 ', 'MET', 0.1509843270845085, (-0.4579999999999999, -11.942, 19.815)), ('E', ' 455 ', 'ILE', 0.0031239483318825393, (1.997, -20.275, 43.437)), ('E', ' 458 ', 'VAL', 0.15654358870529494, (-2.0080000000000005, -26.216000000000008, 49.659)), ('E', ' 485 ', 'THR', 0.10617220040522245, (20.394000000000005, -37.391, 30.924)), ('E', ' 489 ', 'ILE', 0.04259992759474601, (13.636, -35.813, 23.65)), ('E', ' 502 ', 'GLU', 0.017778579616708576, (2.463, -5.080000000000001, 23.606)), ('C', ' 353 ', 'SER', 0.28291392621873956, (1.257, -0.08899999999999997, 6.787)), ('C', ' 356 ', 'TYR', 0.11479684863153815, (-3.2819999999999987, -5.314, 3.717)), ('C', ' 377 ', 'LEU', 0.21100029906324846, (13.141000000000002, -11.221, 12.22)), ('C', ' 382 ', 'VAL', 0.03360568080097437, (15.706, -11.828999999999999, 2.797)), ('C', ' 386 ', 'SER', 0.10722215826181322, (5.509000000000001, -17.658, -2.634)), ('C', ' 395 ', 'ARG', 0.21875840725336815, (2.769999999999999, -28.862, 7.24)), ('C', ' 433 ', 'THR', 0.009519535524304956, (-17.832, -24.086, -8.542999999999997)), ('C', ' 489 ', 'ILE', 0.0636371899216762, (-10.102, -26.292, 6.266)), ('C', ' 502 ', 'GLU', 0.04508351473018598, (20.084000000000003, -15.441, 3.124))]
data['cbeta'] = []
data['probe'] = [(' E 323  CYS  SG ', ' E 348  CYS  SG ', -0.779, (14.187, -2.933, 24.507)), (' E  12  HOH  O  ', ' E 427  ASN  HB2', -0.743, (22.829, -28.217, 27.08)), (' E 330  ASN HD21', ' E 356  TYR  H  ', -0.666, (23.479, -14.368, 25.897)), (' C 426  ARG  NH1', ' C 485  THR HG23', -0.626, (-16.579, -19.727, 0.377)), (' C 330  ASN HD21', ' C 355  LEU  HA ', -0.579, (0.113, -4.161, 1.488)), (' C 431  THR HG22', ' C 433  THR  H  ', -0.562, (-17.518, -21.46, -7.81)), (' E 358  SER  HA ', ' E 360  PHE  CE2', -0.541, (23.955, -21.73, 19.242)), (' E 330  ASN  ND2', ' E 356  TYR  H  ', -0.532, (23.489, -14.951, 26.286)), (' E 335  PRO  HG2', ' E 386  SER  O  ', -0.512, (10.208, -18.885, 34.303)), (' C 357  ASN  O  ', ' C 358  SER  HB2', -0.492, (-6.778, -7.816, 4.87)), (' C 377  LEU  CD2', ' E 377  LEU HD22', -0.491, (9.398, -13.148, 13.707)), (' E 453  ARG  CZ ', ' E 455  ILE HD11', -0.49, (4.519, -17.561, 40.176)), (' E 453  ARG  HG2', ' E 455  ILE HD12', -0.481, (2.534, -17.919, 40.366)), (' E 453  ARG  CZ ', ' E 455  ILE  CD1', -0.475, (4.295, -17.281, 40.661)), (' C 426  ARG HH11', ' C 485  THR HG23', -0.469, (-16.174, -20.079, 0.616)), (' E 431  THR  CG2', ' E 433  THR HG22', -0.446, (22.835, -36.293, 38.556)), (' E 381  ASN  C  ', ' E 381  ASN HD22', -0.446, (6.602, -3.847, 24.787)), (' C 112  HOH  O  ', ' C 395  ARG  HD2', -0.429, (0.981, -32.671, 5.078)), (' E 323  CYS  HG ', ' E 348  CYS  CB ', -0.415, (15.612, -1.869, 25.02)), (' C 375  ASN  H  ', ' C 375  ASN  ND2', -0.412, (18.924, -10.391, 15.571)), (' C 325  PHE  CE1', ' C 345  ILE HD13', -0.402, (9.822, -8.736, 2.054))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
