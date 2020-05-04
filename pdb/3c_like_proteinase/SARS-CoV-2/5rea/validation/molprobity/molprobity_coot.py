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
data['rama'] = [('A', ' 154 ', 'TYR', 0.026528730791439678, (10.323, -11.49, -9.357))]
data['omega'] = []
data['rota'] = [('A', '  22 ', 'CYS', 0.1035706196514256, (9.009, -14.654999999999996, 25.889)), ('A', '  27 ', 'LEU', 0.2680608051002066, (5.751000000000003, -9.792999999999996, 19.147)), ('A', '  72 ', 'ASN', 0.03848519786946442, (-2.519999999999999, -22.229999999999993, 15.748000000000001)), ('A', ' 279 ', 'ARG', 0.0, (-1.5950000000000002, 23.162, -7.263))]
data['cbeta'] = [('A', ' 231 ', 'ASN', ' ', 0.2752306001393036, (23.975, 20.821999999999996, -4.678))]
data['probe'] = [(' A 110  GLN  HG3', ' A 742  HOH  O  ', -0.814, (19.339, 0.643, -1.534)), (' A 197  ASP  HA ', ' A 582  HOH  O  ', -0.661, (15.762, 12.942, 7.117)), (' A 279  ARG  HG3', ' A 279  ARG HH11', -0.65, (1.575, 25.43, -8.681)), (' A  72  ASN  C  ', ' A  72  ASN HD22', -0.643, (-2.365, -24.483, 15.117)), (' A 221  ASN  ND2', ' A 267  SER  HA ', -0.577, (11.308, 24.466, -13.454)), (' A  70  ALA  O  ', ' A  73 AVAL HG12', -0.57, (0.758, -22.834, 12.89)), (' A 118  TYR  CE1', ' A 144  SER  HB3', -0.562, (1.613, -3.731, 15.404)), (' A 404  JGP  C04', ' A 732  HOH  O  ', -0.557, (-4.547, 27.718, -8.828)), (' A 298  ARG  HG3', ' A 303  VAL  HB ', -0.549, (8.547, -3.968, -12.084)), (' A  40  ARG  HB2', ' A  82 AMET  HE2', -0.546, (18.584, -10.269, 21.752)), (' A 115  LEU HD11', ' A 122  PRO  HB3', -0.53, (0.31, -8.839, 6.177)), (' A  40  ARG  HA ', ' A  87  LEU  HG ', -0.522, (16.463, -11.316, 20.434)), (' A  95  ASN  OD1', ' A 502  HOH  O  ', -0.512, (5.629, -22.309, 5.867)), (' A  54  TYR  HB3', ' A  82 AMET  HE1', -0.506, (20.507, -9.841, 24.118)), (' A 228  ASN  ND2', ' A 522  HOH  O  ', -0.469, (28.647, 19.629, -7.953)), (' A 279  ARG  HG3', ' A 279  ARG  NH1', -0.459, (1.461, 25.872, -8.428)), (' A  22 BCYS  HB2', ' A  42  VAL HG22', -0.441, (9.932, -12.752, 23.889)), (' A 199  THR HG21', ' A 239  TYR  CZ ', -0.44, (12.022, 17.656, -1.43)), (' A  95  ASN  HB3', ' A  98  THR  OG1', -0.439, (10.299, -21.339, 5.318)), (' A 101  TYR  HA ', ' A 157  VAL  O  ', -0.436, (14.423, -13.247, -0.52)), (' A 279  ARG  NH2', ' A 533  HOH  O  ', -0.431, (2.684, 29.341, -10.775)), (' A 404  JGP  C05', ' A 732  HOH  O  ', -0.428, (-3.884, 28.266, -8.413)), (' A 188  ARG  HG2', ' A 190  THR HG23', -0.422, (18.009, 3.17, 26.972)), (' A 121  SER  HA ', ' A 122  PRO  HD3', -0.417, (-0.639, -13.058, 10.59)), (' A 109  GLY  HA2', ' A 200  ILE HD13', -0.413, (14.741, 8.171, 0.507))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
