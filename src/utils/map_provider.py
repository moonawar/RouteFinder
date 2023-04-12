from tkintermapview import TkinterMapView, convert_coordinates_to_address, canvas_position_marker
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
        self.node_names = []

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
        place_name = convert_coordinates_to_address(coords[0], coords[1]).address.split(",")[0]
        for marker in self.markers:
            if (place_name == marker.text):
                place_name += f" ({len(self.markers)})"
        self.parent.nodeIndexOf[place_name] = len(self.markers)
        self.node_names.append(place_name)

        new_marker = self.set_marker(coords[0], coords[1], text = place_name, text_color="#07111F")
        self.markers.append(new_marker)

        # ASSUMPTION : Road is undirectional, path from A to B is the same as path from B to A
        # shorter path will be chosen if A to B and B to A have different distance

        # Add distance to all nodes to f_n (real distance)
        self.f_n.append([])
        j = len(self.markers) - 1
        for i in range(len(self.markers) - 1):
            distA, distB = self.create_path(j , i)
            self.f_n[i].append(distA)
            self.f_n[j].append(distB)
        self.f_n[j].append(0)

        # Add distance to all nodes to h_n (heuristic, straight line distance)
        self.h_n.append([])
        j = len(self.markers) - 1
        for i in range(len(self.markers) - 1):
            distance = geodesic(new_marker.position, self.markers[i].position).meters # euclidean distance
            self.h_n[i].append(distance)
            self.h_n[j].append(distance)
        self.h_n[j].append(0)
            
        self.parent.on_marker_added()

    def create_path(self, start, end, color = "#E1341E", bidirectional = True, width = 3):

        directionsA = self.gmaps.directions(self.markers[start].position, self.markers[end].position, mode="driving")
        stepsA = directionsA[0]["legs"][0]["steps"]


        starting_pos = (stepsA[0]["start_location"]["lat"], stepsA[0]["start_location"]["lng"])
        position_list = [starting_pos]
        for step in stepsA:
            position_list.append((step["end_location"]["lat"], step["end_location"]["lng"]))
        self.set_path(position_list, color = color, width = width)

        distA = directionsA[0]["legs"][0]["distance"]["value"]
        
        if (bidirectional):
            directionsB = self.gmaps.directions(self.markers[end].position, self.markers[start].position, mode="driving")
            stepsB = directionsB[0]["legs"][0]["steps"]

            starting_pos = (stepsB[0]["start_location"]["lat"], stepsB[0]["start_location"]["lng"])
            position_list = [starting_pos]
            for step in stepsB:
                position_list.append((step["end_location"]["lat"], step["end_location"]["lng"]))
            self.set_path(position_list, color = color, width = width)

            distB = directionsB[0]["legs"][0]["distance"]["value"]

            return distA, distB
        else:
            return distA, 0
        
    
    def draw_solution_route(self, list_of_node):
        for i in range(len(list_of_node) - 1):
            self.create_path(list_of_node[i], list_of_node[i+1], color = "#E2BD45", bidirectional = False, width = 9)