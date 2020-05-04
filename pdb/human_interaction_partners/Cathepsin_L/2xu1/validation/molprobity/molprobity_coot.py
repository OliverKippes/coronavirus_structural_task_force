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
data['rama'] = []
data['omega'] = []
data['rota'] = [('A', ' 120 ', 'LYS', 0.0, (24.945000000000004, -6.953, -20.692)), ('A', ' 156 ', 'CYS', 0.12556276701771088, (36.464, -21.333999999999996, -27.422)), ('A', ' 179 ', 'ASN', 0.0559759662419409, (37.303, -2.754999999999999, -28.626)), ('B', '  99 ', 'LYS', 0.02616650859228818, (-10.876000000000003, 20.352, -0.8909999999999998)), ('B', ' 103 ', 'LYS', 0.0, (-17.946, 16.588, 7.390999999999998)), ('B', ' 118 ', 'GLN', 0.29287913559962253, (13.944000000000003, -7.269, 7.764)), ('B', ' 156 ', 'CYS', 0.05205314901878525, (16.068, -6.129999999999999, -8.001)), ('C', '   3 ', 'ARG', 0.017679596172802587, (80.67600000000003, -24.766, -20.202)), ('C', ' 118 ', 'GLN', 0.10975886668209041, (74.826, -40.403, -17.528)), ('C', ' 156 ', 'CYS', 0.13082205153097576, (60.32300000000001, -35.416999999999994, -10.780999999999997)), ('D', ' 109 ', 'ASP', 0.12322269974938783, (74.508, -4.296000000000003, -50.49899999999999)), ('D', ' 155 ', 'ASP', 0.17635891608445436, (49.824, 6.458999999999998, -25.558)), ('D', ' 156 ', 'CYS', 0.05492158234119415, (51.942, 5.330999999999999, -28.592)), ('D', ' 184 ', 'LEU', 0.056839689774800514, (55.56000000000002, -10.250999999999998, -35.91))]
data['cbeta'] = [('B', ' 109 ', 'ASP', ' ', 0.3134476437711217, (-3.8040000000000007, 7.5040000000000004, 11.746)), ('C', ' 109 ', 'ASP', ' ', 0.2881510718538769, (69.08, -41.791000000000004, -40.194)), ('D', ' 109 ', 'ASP', ' ', 0.2574480742070318, (73.425, -4.035999999999998, -49.428))]
data['probe'] = [(' A2160  HOH  O  ', ' C 147  LYS  HE2', -1.083, (53.056, -14.441, -17.454)), (' C 195  MET  HE3', ' C2102  HOH  O  ', -1.052, (63.725, -19.7, -20.642)), (' A 147  LYS  HG2', ' C 147  LYS  HE3', -0.96, (53.975, -16.097, -18.147)), (' D 153  GLU  H  ', ' D 208  HIS  HE1', -0.817, (49.543, -0.131, -28.246)), (' D 153  GLU  H  ', ' D 208  HIS  CE1', -0.801, (49.525, 0.319, -29.056)), (' D  37  GLN HE22', ' D  40  ARG HH11', -0.783, (65.125, -9.028, -50.868)), (' B  37  GLN HE22', ' B  40  ARG HH11', -0.776, (-3.492, -2.674, 13.709)), (' B  41  LYS  HD2', ' B 220 BVAL HG22', -0.729, (-8.662, 3.659, 14.828)), (' A 117  LYS  HG3', ' A 213  SER  HA ', -0.678, (25.452, -17.958, -20.955)), (' C  37  GLN HE22', ' C  40  ARG HH11', -0.673, (75.737, -35.733, -36.369)), (' A 124  LYS  NZ ', ' A 128  THR HG21', -0.664, (22.647, -2.441, -11.293)), (' B  97  SER  O  ', ' B  99  LYS  HE2', -0.658, (-8.783, 19.799, -4.82)), (' C 192  GLU  HG3', ' C2140  HOH  O  ', -0.639, (51.841, -18.447, -29.457)), (' A 147  LYS  NZ ', ' A2161  HOH  O  ', -0.637, (57.286, -16.241, -21.385)), (' A 144  LEU HD11', ' C 144  LEU HD13', -0.624, (47.771, -27.215, -17.706)), (' A 108  ASN HD22', ' A 109  ASP  H  ', -0.595, (24.192, -19.346, 4.541)), (' D  96  GLU  HG3', ' D  99  LYS  NZ ', -0.581, (87.257, -1.187, -31.939)), (' D 168  VAL  CG2', ' D 184  LEU HD22', -0.566, (58.655, -12.393, -36.918)), (' D 208  HIS  HD2', ' D2126  HOH  O  ', -0.561, (47.943, 2.955, -32.686)), (' A 147  LYS  HD2', ' A2158  HOH  O  ', -0.555, (53.785, -18.913, -20.802)), (' D   7  TRP  CE2', ' D 130  GLY  HA2', -0.553, (60.166, -12.462, -46.447)), (' A 117  LYS  HE3', ' A 213  SER  OG ', -0.549, (26.286, -19.464, -22.599)), (' D 168  VAL HG22', ' D 184  LEU HD22', -0.541, (58.988, -11.669, -36.588)), (' A 124  LYS  HZ3', ' A 128  THR HG21', -0.526, (22.709, -1.92, -11.27)), (' B  44  ARG  HD2', ' B2066  HOH  O  ', -0.521, (-19.945, 1.007, 7.937)), (' B 195 AMET  HE1', ' B 200  LYS  HE2', -0.519, (0.353, -15.372, -7.686)), (' D  96  GLU  HG3', ' D  99  LYS  HZ3', -0.51, (87.239, -0.982, -32.206)), (' C   7  TRP  CE2', ' C 130  GLY  HA2', -0.509, (75.107, -30.181, -32.066)), (' B  41  LYS  HD2', ' B 220 AVAL HG12', -0.507, (-8.947, 3.205, 14.961)), (' A 124  LYS  HZ2', ' A 128  THR HG21', -0.5, (23.027, -3.119, -11.322)), (' D  41  LYS  HD2', ' D 220  VAL  CG1', -0.498, (72.696, -10.392, -52.524)), (' D  41  LYS  HD2', ' D 220  VAL HG11', -0.497, (72.654, -10.511, -52.024)), (' D 108  ASN  ND2', ' D2080  HOH  O  ', -0.493, (80.084, -10.064, -50.097)), (' C 195  MET  CE ', ' C2102  HOH  O  ', -0.486, (64.272, -19.474, -19.931)), (' A 180  ASN HD21', ' D 180  ASN HD21', -0.482, (42.404, -5.543, -30.054)), (' A 120 ALYS  HD3', ' A2142  HOH  O  ', -0.477, (24.766, -7.945, -24.303)), (' B  69  LEU HD12', ' B  72  TYR  CZ ', -0.473, (8.905, 11.957, 3.2)), (' B  96  GLU  OE2', ' B  99  LYS  NZ ', -0.463, (-10.294, 17.696, -6.354)), (' A 137  ASP  OD2', ' A 140  HIS  HE1', -0.462, (36.552, -23.89, -25.729)), (' A 123  MET  HE3', ' A 170  TYR  CE1', -0.444, (31.485, -1.921, -17.244)), (' C   9  GLU  HG2', ' C2019  HOH  O  ', -0.437, (72.854, -17.511, -30.598)), (' B  37  GLN  NE2', ' B  40  ARG HH11', -0.432, (-4.088, -1.911, 13.534)), (' C  41  LYS  HD2', ' C 220  VAL  CG1', -0.431, (73.136, -37.2, -43.513)), (' B  99  LYS  HB2', ' B  99  LYS  HE3', -0.425, (-10.65, 18.886, -2.91)), (' B   7  TRP  CE2', ' B 130  GLY  HA2', -0.421, (-3.794, -7.614, 8.864)), (' C 220  VAL HG13', ' C2082  HOH  O  ', -0.42, (71.681, -38.696, -44.018)), (' B  13  VAL  O  ', ' B2029  HOH  O  ', -0.416, (-12.204, -5.767, 1.459)), (' D  68  GLY  O  ', ' D1221  424  H8 ', -0.415, (68.269, 6.072, -35.461)), (' D 109  ASP  HB2', ' D 219  THR  O  ', -0.411, (72.149, -4.182, -50.539)), (' B 150  ILE HD11', ' B 173  GLU  HG3', -0.407, (4.376, -19.625, -4.022)), (' A 144  LEU HD12', ' C 145  PHE  HE1', -0.402, (47.984, -24.586, -16.513)), (' A 173  GLU  OE1', ' A 179  ASN  ND2', -0.4, (40.751, -1.468, -29.101)), (' B  41  LYS  HD2', ' B 220 BVAL  CG2', -0.4, (-8.995, 3.43, 14.519))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
