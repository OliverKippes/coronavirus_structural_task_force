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
data['rama'] = [('A', ' 154 ', 'TYR', 0.017932961762054944, (10.336999999999996, -11.601000000000004, -9.324))]
data['omega'] = []
data['rota'] = [('A', ' 235 ', 'MET', 0.2921933246328443, (20.823, 22.604000000000006, 0.6979999999999998))]
data['cbeta'] = [('A', '  41 ', 'HIS', ' ', 0.26162668466717176, (13.664000000000001, -5.607, 23.088999999999995)), ('A', ' 290 ', 'GLU', ' ', 0.26169712469230993, (8.498000000000003, 7.514000000000001, 0.025))]
data['probe'] = [(' A 294  PHE  CD2', ' A 710  HOH  O  ', -1.134, (15.92, 3.398, -8.762)), (' A 110  GLN  HG3', ' A 692  HOH  O  ', -1.048, (19.464, 0.84, -1.69)), (' A 294  PHE  HD2', ' A 710  HOH  O  ', -0.961, (15.801, 3.037, -7.743)), (' A 217  ARG  NH2', ' A 502  HOH  O  ', -0.883, (3.448, 12.225, -22.148)), (' A 236  LYS  HD3', ' A 820  HOH  O  ', -0.841, (17.598, 29.381, -1.627)), (' A 402  DMS  H23', ' A 668  HOH  O  ', -0.789, (3.684, -21.305, 6.701)), (' A  70  ALA  O  ', ' A  73 AVAL HG12', -0.773, (1.389, -23.117, 12.733)), (' A 404  K1G  N1 ', ' A 503  HOH  O  ', -0.689, (27.652, 20.049, -5.056)), (' A 228  ASN  ND2', ' A 504  HOH  O  ', -0.68, (29.811, 21.923, -7.199)), (' A  97  LYS  NZ ', ' A 402  DMS  H21', -0.613, (0.98, -20.353, 6.031)), (' A 228  ASN  ND2', ' A 507  HOH  O  ', -0.561, (27.743, 20.117, -7.52)), (' A 298  ARG  HG3', ' A 303  VAL  HB ', -0.507, (8.336, -3.944, -12.092)), (' A 109  GLY  HA2', ' A 200  ILE HD13', -0.506, (15.432, 8.094, 0.197)), (' A  40  ARG  HA ', ' A  87  LEU  HG ', -0.486, (16.211, -11.389, 20.46)), (' A  97  LYS  HZ2', ' A 402  DMS  H21', -0.485, (1.1, -20.13, 6.041)), (' A  19  GLN HE21', ' A 119  ASN  HB3', -0.473, (-0.113, -13.316, 18.637)), (' A 118  TYR  CE1', ' A 144  SER  HB3', -0.465, (1.741, -3.825, 15.58)), (' A 113  SER  O  ', ' A 149  GLY  HA2', -0.443, (8.733, -4.27, 4.148)), (' A  41  HIS  HE1', ' A 164  HIS  O  ', -0.436, (11.407, -3.11, 19.501)), (' A  97  LYS  HZ1', ' A 402  DMS  H21', -0.431, (0.64, -21.046, 6.379)), (' A 126  TYR  HE1', ' A 128  CYS  SG ', -0.428, (5.948, 1.615, 6.699)), (' A  19  GLN  NE2', ' A 119  ASN  HB3', -0.424, (-0.269, -13.53, 18.628)), (' A  90  LYS  HD2', ' A 783  HOH  O  ', -0.407, (20.708, -24.48, 15.737))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
