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
data['rama'] = [('A', ' 154 ', 'TYR', 0.017688589607863008, (10.302, -11.542, -9.341))]
data['omega'] = []
data['rota'] = [('A', '   1 ', 'SER', 0.15435457788045764, (-1.951000000000001, 5.611, -16.433)), ('A', '  27 ', 'LEU', 0.26283447319673403, (5.772000000000006, -9.794, 19.267)), ('A', '  46 ', 'SER', 0.004019992775283754, (9.105000000000004, -2.729999999999999, 30.170000000000005)), ('A', ' 190 ', 'THR', 0.2213051422602244, (16.283, 6.148999999999998, 26.418)), ('A', ' 216 ', 'ASP', 0.2562403477916863, (0.8049999999999984, 16.221, -14.859)), ('A', ' 216 ', 'ASP', 0.2562403477916863, (0.8049999999999984, 16.221, -14.859))]
data['cbeta'] = []
data['probe'] = [(' A 110  GLN  HG3', ' A 693  HOH  O  ', -0.991, (19.568, 1.024, -1.601)), (' A 217  ARG  NH2', ' A 502  HOH  O  ', -0.723, (3.799, 12.157, -21.769)), (' A 288  GLU  OE1', ' A 501  HOH  O  ', -0.662, (5.686, 10.62, -1.602)), (' A 110  GLN  NE2', ' A 505  HOH  O  ', -0.598, (15.707, 0.556, -3.272)), (' A 118  TYR  CE1', ' A 144  SER  HB3', -0.551, (2.14, -2.977, 15.27)), (' A  47  GLU  N  ', ' A  47  GLU  OE1', -0.541, (9.305, -3.1, 32.21)), (' A 101  TYR  HA ', ' A 157  VAL  O  ', -0.527, (14.381, -12.882, -0.578)), (' A 127  GLN  NE2', ' A 519  HOH  O  ', -0.511, (9.349, -0.035, -2.836)), (' A  52  PRO  HD2', ' A 188  ARG  HG3', -0.493, (18.115, -0.103, 27.51)), (' A  47  GLU  CD ', ' A  47  GLU  H  ', -0.473, (9.401, -3.942, 33.289)), (' A 104  VAL  O  ', ' A 160  CYS  HA ', -0.473, (17.859, -5.544, 4.014)), (' A  95  ASN  HB3', ' A  98  THR  OG1', -0.465, (10.182, -21.372, 5.243)), (' A  40  ARG  HA ', ' A  87  LEU  HG ', -0.46, (16.444, -11.589, 20.61)), (' A 298  ARG  HG3', ' A 303  VAL  HB ', -0.456, (8.151, -3.53, -11.821)), (' A 115  LEU HD11', ' A 122  PRO  HB3', -0.454, (0.259, -9.196, 6.44)), (' A  86  VAL HG13', ' A 179  GLY  HA2', -0.449, (18.509, -8.058, 14.346)), (' A  70  ALA  O  ', ' A  73 CVAL HG12', -0.445, (0.962, -23.221, 13.016)), (' A  70  ALA  O  ', ' A  73 AVAL HG12', -0.443, (0.692, -22.793, 12.943)), (' A 404  T7A  O1 ', ' A 404  T7A  S  ', -0.422, (5.55, -5.034, 20.802)), (' A 249  ILE HG22', ' A 293  PRO  HG2', -0.419, (17.332, 6.867, -9.577)), (' A  41  HIS  HE1', ' A 164  HIS  O  ', -0.415, (11.572, -3.11, 19.557)), (' A  76  ARG  O  ', ' A  91  VAL  HA ', -0.415, (12.283, -25.226, 16.64)), (' A  19  GLN  NE2', ' A 119  ASN  HB3', -0.411, (-0.401, -13.375, 18.903)), (' A 113  SER  O  ', ' A 149  GLY  HA2', -0.4, (8.767, -4.158, 4.202)), (' A  36  VAL HG21', ' A  68  VAL HG11', -0.4, (9.163, -20.218, 14.834))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
