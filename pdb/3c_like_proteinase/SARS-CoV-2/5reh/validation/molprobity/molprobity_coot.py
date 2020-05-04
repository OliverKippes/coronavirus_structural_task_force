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
data['rama'] = [('A', '  46 ', 'SER', 0.0021805056440755057, (10.426000000000009, -3.287, 30.088999999999995)), ('A', ' 154 ', 'TYR', 0.02482830119339128, (10.386000000000003, -11.479000000000001, -9.582))]
data['omega'] = []
data['rota'] = [('A', '  46 ', 'SER', 0.09136366667260555, (10.426000000000009, -3.287, 30.088999999999995)), ('A', '  73 ', 'VAL', 0.06938678852657258, (0.6390000000000002, -24.739, 15.512)), ('A', ' 216 ', 'ASP', 0.17980456643236914, (1.1369999999999991, 16.621, -14.876)), ('A', ' 235 ', 'MET', 0.16919782524046426, (21.371000000000006, 22.522, 0.947)), ('A', ' 276 ', 'MET', 0.011994558564296945, (3.3549999999999995, 24.973, -5.458))]
data['cbeta'] = []
data['probe'] = [(' A 110  GLN  HG3', ' A 675  HOH  O  ', -1.138, (19.274, 0.926, -1.721)), (' A 294  PHE  CD2', ' A 692  HOH  O  ', -0.835, (16.038, 2.744, -8.504)), (' A  45  THR  O  ', ' A  47  GLU  N  ', -0.803, (11.273, -3.972, 31.513)), (' A 109  GLY  HA2', ' A 200  ILE HD13', -0.766, (15.504, 8.129, 0.149)), (' A  45  THR  O  ', ' A  48  ASP  N  ', -0.719, (13.294, -4.355, 31.755)), (' A 166  GLU  OE1', ' A 501  HOH  O  ', -0.716, (5.941, 4.516, 20.267)), (' A 115  LEU HD11', ' A 122  PRO  HB3', -0.662, (0.257, -8.641, 6.162)), (' A  47  GLU  N  ', ' A  47  GLU  OE1', -0.641, (10.344, -3.569, 32.13)), (' A 238  ASN  ND2', ' A 510  HOH  O  ', -0.589, (19.582, 21.247, 4.728)), (' A 221 AASN HD22', ' A 270  GLU  HG3', -0.588, (11.914, 26.893, -12.939)), (' A  45  THR  C  ', ' A  47  GLU  H  ', -0.578, (11.161, -4.679, 31.649)), (' A 290  GLU  OE1', ' A 503  HOH  O  ', -0.557, (6.908, 6.811, 1.541)), (' A 221 AASN  ND2', ' A 270  GLU  HG3', -0.54, (12.366, 27.012, -13.104)), (' A  48  ASP  OD1', ' A 504  HOH  O  ', -0.525, (17.189, -6.576, 32.745)), (' A 298  ARG  HD2', ' A 402  DMS  O  ', -0.52, (7.455, -1.21, -8.077)), (' A 298  ARG  HG3', ' A 303  VAL  HB ', -0.505, (8.52, -3.175, -11.874)), (' A 101  TYR  HA ', ' A 157  VAL  O  ', -0.487, (14.751, -13.101, -0.626)), (' A  19  GLN HE21', ' A 119  ASN HD22', -0.487, (0.291, -12.543, 19.636)), (' A 298  ARG  NH1', ' A 524  HOH  O  ', -0.487, (12.441, -1.715, -8.926)), (' A 137  LYS  HE3', ' A 197  ASP  OD2', -0.482, (11.006, 12.228, 8.207)), (' A 294  PHE  HB3', ' A 524  HOH  O  ', -0.476, (13.621, -0.825, -9.538)), (' A  45  THR  C  ', ' A  47  GLU  N  ', -0.469, (11.33, -4.482, 31.46)), (' A 217  ARG  HD2', ' A 779  HOH  O  ', -0.467, (1.747, 18.43, -20.838)), (' A 104  VAL  O  ', ' A 160  CYS  HA ', -0.465, (17.924, -5.659, 3.988)), (' A 256  GLN  NE2', ' A 530  HOH  O  ', -0.464, (10.546, 4.929, -23.145)), (' A 199  THR HG21', ' A 239  TYR  CZ ', -0.458, (12.292, 17.751, -1.372)), (' A  40  ARG  HA ', ' A  87  LEU  HG ', -0.458, (16.388, -11.269, 20.552)), (' A 113  SER  O  ', ' A 149  GLY  HA2', -0.457, (8.773, -3.973, 4.171)), (' A  69  GLN HE21', ' A  72  ASN  HA ', -0.457, (-1.507, -20.788, 16.913)), (' A  86  VAL HG13', ' A 179  GLY  HA2', -0.448, (18.875, -7.537, 14.053)), (' A 227  LEU  HA ', ' A 227  LEU HD23', -0.447, (23.505, 19.103, -10.074)), (' A  41  HIS  HE1', ' A 164  HIS  O  ', -0.44, (11.548, -3.084, 19.073)), (' A  40  ARG  CZ ', ' A  54  TYR  CD2', -0.432, (20.715, -6.352, 23.238)), (' A  40  ARG  HD3', ' A  85  CYS  HA ', -0.422, (20.152, -7.932, 19.818)), (' A  49  MET  CE ', ' A 798  HOH  O  ', -0.422, (12.953, -1.675, 24.066)), (' A  36  VAL HG21', ' A  68  VAL HG11', -0.421, (9.746, -19.773, 14.839)), (' A 114  VAL  O  ', ' A 125  VAL  HA ', -0.416, (2.997, -3.491, 4.695)), (' A  28  ASN  O  ', ' A 146  GLY  HA3', -0.416, (8.782, -9.662, 15.031)), (' A 276  MET  HB3', ' A 276  MET  HE3', -0.406, (2.141, 22.476, -6.016)), (' A 110  GLN  CG ', ' A 675  HOH  O  ', -0.401, (19.446, 1.516, -0.808))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
