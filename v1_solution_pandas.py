import pandas as pd
from typing import Any, List
from collections import defaultdict
from dataclasses import dataclass, field
import heapq
from datetime import datetime, timedelta
import sys


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


def find_flights(csv, origin, destination, bags=0):
    # Preparation
    data = pd.read_csv(csv)
    source = data[data['bags_allowed'] >= bags]
    final_price = source['base_price'] + (source['bag_price'] * bags)
    source.loc[:, 'final_price'] = final_price

    d = defaultdict(list)
    # Create dict where {origin : [{flight_details_1}, {flight_details_2,..}]}
    for i in source.to_dict(orient='records'):
        start_from = i.get('origin')
        d[start_from].append(i)

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


find_flights(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]))

#python -m solution example0.csv WIW RFZ 1
#python -m solution example1.csv DHE NIZ 1
#python -m solution example2.csv YOT GXV 1
#python -m solution example3.csv WUE JBN 1
