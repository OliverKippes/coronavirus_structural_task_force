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
data['rama'] = [('A', ' 892 ', 'GLY', 0.041156855223633326, (-24.652, 4.235, 17.089))]
data['omega'] = []
data['rota'] = [('A', ' 895 ', 'GLN', 0.21907057110740602, (-21.929000000000006, 7.816, 11.733999999999998)), ('A', ' 939 ', 'GLN', 0.0, (-12.506000000000002, 13.801, -53.043)), ('A', '1147 ', 'LEU', 0.042757746520165, (-23.927000000000003, 20.315, -73.517)), ('B', ' 895 ', 'GLN', 0.26585105516276086, (-3.2970000000000006, -2.947, -81.488)), ('B', ' 939 ', 'GLN', 0.0, (-2.822, 8.206, -16.683)), ('B', '1147 ', 'LEU', 0.04803000529907555, (8.56, 1.6210000000000004, 3.759999999999999))]
data['cbeta'] = []
data['probe'] = [(' A 941  LEU HD23', ' A1155  ALA  HB2', -0.626, (-18.656, 16.22, -54.474)), (' A 952  PHE  HB3', ' A1147  LEU HD11', -0.626, (-20.063, 18.172, -72.794)), (' B   4   CL CL  ', ' B 902  GLN  HG2', -0.604, (-1.623, -0.478, -72.016)), (' A 896  ASN  O  ', ' A 900  GLU  HG2', -0.581, (-21.887, 2.921, 6.729)), (' B 952  PHE  HB3', ' B1147  LEU HD11', -0.561, (4.606, 3.316, 2.615)), (' A1172  LYS  HG2', ' B 939  GLN  HG3', -0.544, (-4.634, 10.872, -19.452)), (' B 896  ASN  O  ', ' B 900  GLU  HG2', -0.541, (-7.567, -5.383, -77.213)), (' A 939  GLN  HG3', ' B1172  LYS  HG2', -0.525, (-8.692, 13.547, -50.75)), (' A1153  ILE  N  ', ' A1153  ILE HD12', -0.52, (-20.345, 22.105, -61.107)), (' B 969  VAL  O  ', ' B 973  VAL HG23', -0.519, (2.614, 1.613, 29.972)), (' A   1   CL CL  ', ' A 902  GLN  HG2', -0.503, (-20.709, 10.802, 1.615)), (' A 969  VAL  O  ', ' A 973  VAL HG23', -0.499, (-20.902, 14.985, -100.394)), (' B1153  ILE  N  ', ' B1153  ILE HD12', -0.494, (8.212, 5.664, -9.26)), (' A 964  SER  O  ', ' A 967  ASP  HB2', -0.494, (-19.249, 20.666, -93.117)), (' B 964  SER  O  ', ' B 967  ASP  HB2', -0.49, (6.243, 5.518, 22.818)), (' B 941  LEU HD23', ' B1155  ALA  HB2', -0.465, (2.674, 3.752, -15.82)), (' B 959  LEU  O  ', ' B 963  LEU  HG ', -0.463, (4.713, 2.967, 15.163)), (' B 945  VAL HG13', ' B1150  ILE HD13', -0.461, (3.764, 5.963, -6.892)), (' B 102  HOH  O  ', ' B1162  LYS  HE3', -0.445, (4.35, 18.015, -37.446)), (' B 952  PHE  HB3', ' B1147  LEU  CD1', -0.432, (5.206, 3.811, 2.636)), (' B  56  HOH  O  ', ' B 921  THR HG23', -0.431, (-9.453, 6.498, -43.012)), (' B 932  ASP  O  ', ' B 936  GLN  HG3', -0.427, (-6.436, 6.313, -23.556)), (' B1174  LEU  HA ', ' B1174  LEU HD23', -0.426, (-3.047, 8.226, -53.871)), (' A  85  HOH  O  ', ' B1176  GLU  HG2', -0.425, (-7.229, 14.591, -57.405)), (' B1160  ILE  HA ', ' B1163  GLU  OE2', -0.417, (2.364, 9.892, -33.797)), (' B 901  ASN  O  ', ' B 905  ILE HG13', -0.407, (-3.323, -3.691, -68.865)), (' A 952  PHE  HB3', ' A1147  LEU  CD1', -0.403, (-20.217, 18.646, -72.396)), (' A 966  LEU  HA ', ' A 966  LEU HD23', -0.401, (-20.932, 14.82, -93.725)), (' B 947  GLN  O  ', ' B 950  SER  HB3', -0.4, (-1.582, 8.793, -2.337))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
