from tkintermapview import TkinterMapView
import googlemaps
from geopy.distance import geodesic

# Jangan ada yang make yahh :((
API_KEY = "AIzaSyD653qbfvijlwA6-6a6eQxMX3Q6fKpUasU"
SAME_NODE_DISTANCE = 0.00015
class MapView(TkinterMapView):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.gmaps : googlemaps.Client = googlemaps.Client(key=API_KEY)
        self.markers = []
        
        self.f_n = [] # adjacency matrix for real distance
        # data example : [
        # [0, 100, 200], 
        # [100, 0, 300], 
        # [200, 300, 0]
        # ]

        self.h_n = [] # adjacency matrix for heuristic distance (straight line distance)
                # data example : [
        # [0, 100, 200], 
        # [100, 0, 300], 
        # [200, 300, 0]
        # ]

        self.init_options()
    
    def init_options(self):
        self.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        self.set_address("Institut Teknologi Bandung")
        self.add_right_click_menu_command("Add Node", self.on_map_add_node, pass_coords=True)
    
    def on_map_add_node(self, coords):
        new_marker = self.set_marker(coords[0], coords[1], text="Node " + str(len(self.markers) + 1))
        self.markers.append(new_marker)

        # ASSUMPTION : Road is undirectional, path from A to B is the same as path from B to A
        # shorter path will be chosen if A to B and B to A have different distance

        # Add distance to all nodes to f_n (real distance)
        self.f_n.append([])
        j = len(self.markers) - 1
        for i in range(len(self.markers) - 1):
            distance = self.create_path(new_marker.position, self.markers[i].position)
            self.f_n[i].append(distance)
            self.f_n[j].append(distance)
        self.f_n[j].append(0)

        # Add distance to all nodes to h_n (heuristic, straight line distance)
        self.h_n.append([])
        j = len(self.markers) - 1
        for i in range(len(self.markers) - 1):
            distance = geodesic(new_marker.position, self.markers[i].position).meters
            self.h_n[i].append(distance)
            self.h_n[j].append(distance)
        self.h_n[j].append(0)
            
        self.parent.on_marker_added()

    def create_path(self, start, end):
        directionsA = self.gmaps.directions(start, end, mode="driving")
        directionsB = self.gmaps.directions(end, start, mode="driving")

        shorter_directions = directionsA if directionsA[0]["legs"][0]["distance"]["value"] <= directionsB[0]["legs"][0]["distance"]["value"] else directionsB

        steps = shorter_directions[0]["legs"][0]["steps"]

        starting_pos = (steps[0]["start_location"]["lat"], steps[0]["start_location"]["lng"])
        position_list = [starting_pos]
        for step in steps:
            position_list.append((step["end_location"]["lat"], step["end_location"]["lng"]))

        self.set_path(position_list, color = "#E1341E")
        return shorter_directions[0]["legs"][0]["distance"]["value"]