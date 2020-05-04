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
data['rama'] = [('A', ' 154 ', 'TYR', 0.014382336998539517, (10.267000000000001, -11.580999999999996, -9.359))]
data['omega'] = []
data['rota'] = [('A', '   1 ', 'SER', 0.22590281312855545, (-1.9680000000000009, 5.613, -16.387)), ('A', '  27 ', 'LEU', 0.26245153513226704, (5.793000000000001, -9.862999999999996, 19.162)), ('A', '  47 ', 'GLU', 0.22192986957170688, (11.315999999999999, -2.85, 33.572)), ('A', ' 216 ', 'ASP', 0.15995766250386828, (0.9060000000000006, 16.314, -14.856000000000002)), ('A', ' 236 ', 'LYS', 0.2579830283875967, (18.861, 25.799999999999994, 1.639))]
data['cbeta'] = []
data['probe'] = [(' A 110  GLN  HG3', ' A 701  HOH  O  ', -0.963, (19.572, 0.916, -1.678)), (' A 140  PHE  O  ', ' A 405  DMS  H11', -0.795, (3.981, 1.964, 16.158)), (' A 405  DMS  H22', ' A 600  HOH  O  ', -0.752, (5.072, 1.49, 19.806)), (' A  50  LEU  O  ', ' A 188  ARG  NE ', -0.732, (18.221, 2.539, 29.038)), (' A 217  ARG  NH2', ' A 502  HOH  O  ', -0.723, (3.634, 12.383, -21.688)), (' A 294  PHE  CD2', ' A 683  HOH  O  ', -0.71, (15.984, 2.704, -8.412)), (' A  70  ALA  O  ', ' A  73 AVAL HG12', -0.663, (0.863, -22.845, 12.75)), (' A 404  T47  C  ', ' A 405  DMS  H23', -0.655, (5.894, -1.488, 18.23)), (' A 166  GLU  HB2', ' A 405  DMS  H12', -0.637, (6.376, 3.153, 17.62)), (' A  47  GLU  N  ', ' A  47  GLU  OE1', -0.606, (9.283, -3.408, 32.501)), (' A 288  GLU  OE1', ' A 501  HOH  O  ', -0.601, (5.654, 10.423, -1.53)), (' A 166  GLU  HB2', ' A 405  DMS  C1 ', -0.564, (6.632, 2.633, 17.831)), (' A 118  TYR  CE1', ' A 144  SER  HB3', -0.534, (1.748, -3.828, 15.419)), (' A 403  DMS  H23', ' A 689  HOH  O  ', -0.515, (3.166, -21.72, 7.264)), (' A 221 AASN  ND2', ' A 267  SER  HA ', -0.514, (11.272, 24.414, -13.523)), (' A 187  ASP  HA ', ' A 404  T47 CL1 ', -0.5, (15.246, -1.054, 21.138)), (' A  49  MET  HE2', ' A 404  T47  C10', -0.497, (12.737, -2.04, 23.64)), (' A  40  ARG  HA ', ' A  87  LEU  HG ', -0.496, (16.575, -11.398, 20.611)), (' A 109  GLY  HA2', ' A 200  ILE HD13', -0.492, (15.432, 8.163, 0.278)), (' A 298  ARG  HG3', ' A 303  VAL  HB ', -0.487, (8.755, -3.889, -12.147)), (' A 115  LEU HD11', ' A 122  PRO  HB3', -0.471, (0.364, -9.02, 6.057)), (' A 236  LYS  HD3', ' A 813  HOH  O  ', -0.47, (18.323, 29.292, -1.187)), (' A  49  MET  HE2', ' A 404  T47  C9 ', -0.461, (12.794, -1.479, 23.792)), (' A  47  GLU  CD ', ' A  47  GLU  H  ', -0.46, (9.358, -4.364, 33.465)), (' A 165  MET  HE3', ' A 404  T47 CL1 ', -0.454, (14.061, 0.073, 21.27)), (' A 113  SER  O  ', ' A 149  GLY  HA2', -0.452, (9.167, -4.169, 4.426)), (' A 199  THR HG21', ' A 239  TYR  CZ ', -0.439, (12.407, 17.724, -1.296)), (' A  31  TRP  CD2', ' A  95  ASN  HB2', -0.438, (9.015, -21.439, 8.648)), (' A 298  ARG  HD2', ' A 402  DMS  O  ', -0.434, (7.814, -1.742, -8.216)), (' A 141  LEU  C  ', ' A 405  DMS  H21', -0.432, (3.252, -0.863, 18.235)), (' A 101  TYR  HA ', ' A 157  VAL  O  ', -0.426, (14.498, -12.885, -0.32)), (' A 249  ILE HG22', ' A 293  PRO  HG2', -0.424, (17.65, 6.95, -9.922)), (' A 221 AASN HD21', ' A 267  SER  HA ', -0.423, (11.723, 24.148, -13.043)), (' A  86  VAL HG13', ' A 179  GLY  HA2', -0.422, (18.402, -7.888, 14.436)), (' A 137  LYS  NZ ', ' A 197  ASP  OD2', -0.421, (10.526, 12.169, 7.528)), (' A  41  HIS  HE1', ' A 164  HIS  O  ', -0.421, (11.569, -3.232, 19.388)), (' A 141  LEU  O  ', ' A 405  DMS  H21', -0.42, (3.752, -0.753, 17.856))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
