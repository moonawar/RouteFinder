from tkintermapview import TkinterMapView

class MapView(TkinterMapView):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_options()
    
    def init_options(self):
        self.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        self.set_address("Institut Teknologi Bandung")
        self.add_right_click_menu_command("Add Node", self.on_map_add_node, pass_coords=True)
    
    def on_map_add_node(self, coords):
        new_marker = self.set_marker(coords[0], coords[1], text="Node " + str(len(self.parent.markers) + 1))
        self.parent.markers.append(new_marker)
        self.parent.on_marker_added()