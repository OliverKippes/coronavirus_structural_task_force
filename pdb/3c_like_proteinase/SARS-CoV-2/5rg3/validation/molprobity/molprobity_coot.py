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
data['rama'] = [('A', ' 154 ', 'TYR', 0.009835778904092575, (10.358000000000002, -11.486, -9.437))]
data['omega'] = []
data['rota'] = [('A', '   1 ', 'SER', 0.14725158213289657, (-2.049, 5.595, -16.386)), ('A', '  27 ', 'LEU', 0.2226161756402255, (5.940999999999999, -9.830999999999998, 19.242000000000004))]
data['cbeta'] = []
data['probe'] = [(' A 110  GLN  HG3', ' A 695  HOH  O  ', -1.073, (19.239, 0.734, -1.724)), (' A 294  PHE  CD2', ' A 703  HOH  O  ', -0.968, (16.242, 3.315, -8.556)), (' A 163  HIS  NE2', ' A 404  DMS  H21', -0.922, (7.42, 0.301, 15.76)), (' A 236  LYS  NZ ', ' A 501  HOH  O  ', -0.786, (14.89, 31.687, -0.3)), (' A 294  PHE  HD2', ' A 703  HOH  O  ', -0.669, (15.736, 2.584, -7.513)), (' A 403  DMS  H23', ' A 661  HOH  O  ', -0.642, (3.414, -21.26, 6.851)), (' A  70  ALA  O  ', ' A  73 AVAL HG12', -0.626, (0.72, -22.788, 12.788)), (' A 288  GLU  OE1', ' A 502  HOH  O  ', -0.602, (5.884, 10.771, -1.347)), (' A 298  ARG  HG3', ' A 303  VAL  HB ', -0.59, (8.312, -3.88, -12.113)), (' A 166  GLU  HB2', ' A 404  DMS  H22', -0.582, (7.422, 2.183, 17.754)), (' A  69  GLN HE21', ' A  72  ASN  HA ', -0.561, (-1.485, -20.741, 16.689)), (' A 221 AASN  ND2', ' A 267  SER  HA ', -0.555, (11.688, 24.024, -13.258)), (' A 163  HIS  NE2', ' A 404  DMS  C2 ', -0.54, (7.282, 0.56, 16.316)), (' A 143  GLY  CA ', ' A 405  T9P  C9 ', -0.527, (4.505, -5.896, 19.208)), (' A 109  GLY  HA2', ' A 200  ILE HD13', -0.524, (15.387, 8.167, 0.343)), (' A  19  GLN HE21', ' A 119  ASN HD22', -0.513, (0.733, -12.633, 19.449)), (' A 165  MET  SD ', ' A 186  VAL  O  ', -0.49, (16.32, 1.457, 20.213)), (' A 101  TYR  HA ', ' A 157  VAL  O  ', -0.489, (14.446, -12.796, -0.521)), (' A  19  GLN  NE2', ' A 119  ASN HD22', -0.481, (0.202, -12.949, 19.659)), (' A 236  LYS  HE3', ' A 237  TYR  CE2', -0.475, (15.132, 28.456, -0.756)), (' A  86  VAL HG13', ' A 179  GLY  HA2', -0.458, (18.459, -8.001, 14.268)), (' A 143  GLY  C  ', ' A 405  T9P  C9 ', -0.456, (4.807, -5.524, 18.679)), (' A 110  GLN  NE2', ' A 509  HOH  O  ', -0.449, (15.533, 1.002, -3.127)), (' A 286  LEU  C  ', ' A 286  LEU HD12', -0.424, (4.715, 16.595, -1.664)), (' A 113  SER  O  ', ' A 149  GLY  HA2', -0.424, (8.802, -4.138, 4.166)), (' A 115  LEU HD11', ' A 122  PRO  HB3', -0.412, (0.519, -8.876, 6.142)), (' A 166  GLU  HB2', ' A 404  DMS  C2 ', -0.411, (7.164, 2.212, 17.755)), (' A  31  TRP  CD2', ' A  95  ASN  HB2', -0.411, (8.988, -21.343, 8.683)), (' A 143  GLY  HA2', ' A 405  T9P  C9 ', -0.404, (4.461, -6.008, 19.807)), (' A  40  ARG  HA ', ' A  87  LEU  HG ', -0.4, (16.444, -11.218, 20.871))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
