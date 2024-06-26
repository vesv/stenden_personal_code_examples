import networkx as nx  # library for manipulating data into networks
import matplotlib.pyplot as plt  # module for creating graphs
import csv  # import that lets us read excel spreadsheets
import os  # utility module letting us interact with the operating system


def validate(G, station1, station2):  # function that checks whether input route is valid
    if station1 not in list(G.nodes()) or station2 not in list(G.nodes()):  # if either stations aren't listed, returns
        print("Invalid station(s)")  # false
        return False
    elif station1 == station2:
        print("Please input different stations.")
        return False
    else:
        return True


def find_path(G, station1, station2):
    # dictionary of colours that match their line
    colourDictionary = {
        "Jubilee": 'grey',
        "Central": 'red',
        "Piccadilly": 'darkblue',
        "Hammersmith & City": 'pink',
        "Circle": 'yellow',
        "District": 'green',
        "Northern": 'black',
        "Victoria": 'dodgerblue',
        "Waterloo & City": 'aquamarine',
        "Metropolitan": 'purple',
        "Bakerloo": 'brown'
    }
    # uses dijkstras to find all weighted shortest path
    Paths = nx.shortest_simple_paths(G, station1,
                                     station2)  # the algorithm finds the shortest route between two stations
    amount = 0
    for counter, Path in enumerate(Paths):
        amount += 1
        print("Path:", Path)
        # finds individual weights between nodes of the path found
        # as well as total weight of a path
        totalPathTime = 0
        listOfPathWeight = []
        for i in range(0, len(Path) - 1):
            if Path[i + 1] in nx.all_neighbors(G, Path[i]):
                listOfPathWeight.append(G.get_edge_data(Path[i], Path[i + 1]))
                listOfPathWeight[i] = listOfPathWeight[i]['weight']
                totalPathTime += listOfPathWeight[i]

        print("Time it will take in minutes:", totalPathTime)
        print("")
        # listOfPathWeight must match size of Path for the bars or 'bins' to match x axis
        # this adds a filler to match size
        listOfPathWeight.append(0)
        # creates a list of lines
        stationLines = []
        for i in range(0, len(stations)):
            startStation = stations[i][1]
            lineKey = stations[i][0]
            destinationStation = stations[i][2]
            if stations[i][2] != "":
                stationLines.append([lineKey, startStation, destinationStation])
        listOfColours = []
        for i in range((len(Path) - 1)):
            for v in range(len(stationLines)):
                if Path[i] in stationLines[v][1] and Path[i + 1] in stationLines[v][2] \
                        or Path[i + 1] in stationLines[v][1] and Path[i] in stationLines[v][2]:
                    listOfColours.append(colourDictionary[stationLines[v][0]])

        for i in range(len(listOfColours)):
            if len(listOfColours) >= len(listOfPathWeight):
                if i == len(listOfColours) - 1 and listOfColours[i] != listOfColours[i - 1]:
                    # listOfColours.pop(i)
                    break
                elif len(listOfColours) - len(listOfPathWeight) == 0:
                    listOfColours.pop(i + 1)
                elif len(listOfColours) - i > 2:
                    if listOfColours[i] == listOfColours[i + 2] \
                            and listOfColours[i] != listOfColours[i + 1]:
                        listOfColours.pop(i + 1)

        # creates histogram for path
        fig, ax = plt.subplots()
        data, bins, patches = ax.hist(Path, weights=listOfPathWeight,
                                      bins=len(listOfPathWeight) - 1,
                                      edgecolor="black")
        for i in range(len(listOfPathWeight) - 1):
            colour = listOfColours[i]
            patches[i].set_fc(colour)
        plt.setp(ax.get_xticklabels(), rotation=30, ha='right')
        plt.xlabel("Stations")
        plt.ylabel("Time (mins)")
        amount -= 1

        if counter == 2:
            break
    plt.show()


def delete_path(G, start, finish):
    Path = nx.dijkstra_path(G, start, finish)
    closed_lines = []
    for i in range(len(Path) - 1):
        weight = G[Path[i]][Path[i + 1]]['weight']
        G.remove_edge(Path[i], Path[i + 1])
        if nx.has_path(G, Path[i], Path[i + 1]):
            closed_lines.append([Path[i], Path[i + 1]])
            pass
        else:
            G.add_edge(Path[i], Path[i + 1], weight=weight)
            print("Deletion is not feasible between:", Path[i], "and", Path[i + 1])
            print("because there is no other path")

    print("The lines that have been deleted are:", closed_lines)
    print("")

    find_path(G, station1, station2)


G = nx.Graph()

stations = []
# should be "London Underground data.csv" in the parent folder.
if not os.path.exists("London Underground data.csv"):
    print("Save as csv file in parent folder.")

with open(("London Underground data.csv"), newline="", errors="ignore") as file:
    reader = csv.reader(file, delimiter=",")
    for row in reader:
        stations.append(row)

for i in range(0, len(stations)):
    if stations[i][2] == "":
        G.add_node(stations[i][1])

for i in range(len(stations)):
    if stations[i][2] != "":
        G.add_edge(stations[i][1], stations[i][2], weight=int(stations[i][3]))

answer = input("Do you want to [delete] a route or [find] a route? ")
Go = False

while answer != "delete" and answer != "find":
    answer = input("Do you want to [delete] a route or [find] a route? ")

if answer == "delete":
    station1 = input("Choose first station: ")
    station2 = input("Choose second station: ")

    while not validate(G, station1, station2):
        station1 = input("Choose first station: ")
        station2 = input("Choose second station: ")
    delete_path(G, station1, station2)
elif answer == "find":
    station1 = input("Choose first station: ")
    station2 = input("Choose second station: ")

    while not validate(G, station1, station2):
        station1 = input("Choose first station: ")
        station2 = input("Choose second station: ")
    print("Showing the 3 shortest paths...")
    find_path(G, station1, station2)

# Draw the graph or network with the edge weights.
"""
pos=nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, font_weight='bold')
edge_weight = nx.get_edge_attributes(G,'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_weight)
"""
