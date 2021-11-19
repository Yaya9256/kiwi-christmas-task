import csv
from collections import defaultdict
import heapq
from dataclasses import dataclass, field
from typing import Any, List
from datetime import datetime, timedelta


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    path: Any = field(compare=False)
    flights: Any = field(compare=False)

    def __repr__(self) -> str:
        # WIW -> ECV -> RCZ
        # > JV042 WIW - > ECV  <departure> - <arrival>
        # > GUAM4 ECV - > RCZ  <departure> - <arrival>
        p = " -> ".join(self.path)
        d = [
            f"> {i['flight_no']} : {i['origin']} -> {i['destination']} " \
            f"{i['departure']} - {i['arrival']}"
            for i in self.flights
        ]
        return "\n".join([p]+d)


def find_flights(csv_file, origin, destination, bags=0):

    # Create dict {origin : [{flight_details_1}, {flight_details_2,..}]}
    d = defaultdict(list)
    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # add calculations
            full_price = float(row['bag_price']) * float(row['bags_allowed'])
            row['final_price'] = full_price
            d[row['origin']].append(row)

    # Initialize priority queue with starting point Airport
    queue: List[PrioritizedItem] = []
    heapq.heappush(queue,
                   # price=0, path=origin
                   PrioritizedItem(0, [origin], []))

    while queue:
        item = heapq.heappop(queue)
        # if final destination, continue listing other routes
        if item.path[-1] == destination:
            print(item)
            continue
        # check list of all connections from last Airport in queue
        for i in d[item.path[-1]]:
            # if Airport already in the path, continue
            if i['destination'] in item.path:
                continue

            # if difference between arrival and departure too small or big
            if item.flights:
                departure_next = i['departure']
                arrival_last = item.flights[-1]['arrival']
                d1 = datetime.fromisoformat(arrival_last)
                d2 = datetime.fromisoformat(departure_next)
                if not timedelta(hours=1) <= d2 - d1 <= timedelta(hours=6):
                    continue

            heapq.heappush(
                queue,
                PrioritizedItem(
                    priority=item.priority + i['final_price'],
                    path=item.path + [i['destination']],
                    flights=item.flights + [i]
                )
            )


# find_flights(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]))

find_flights('example0.csv', 'WIW', 'RFZ', 1)
