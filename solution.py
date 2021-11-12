import pandas as pd
from typing import Any, List
from collections import defaultdict
from dataclasses import dataclass, field
from pprint import pprint
import heapq

data = pd.read_csv('example0.csv')


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    path: Any = field(compare=False)
    flights: Any = field(compare=False)
    # path: List[str, ...] = field(compare=False)

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


def find_flights(origin, destination, bags=0, back=False):
    # Preparation
    source = data[data['bags_allowed'] >= bags]
    final_price = source['base_price'] + (source['bag_price'] * bags)
    source['final_price'] = final_price
    print(source)
    d = defaultdict(list)
    # list of dictionaries
    for i in source.to_dict(orient='records'):
        print(i)
        A = i.get('origin')
        print(A)
        d[A].append(i)

    queue: List[PrioritizedItem] = []
    heapq.heappush(queue,
                   PrioritizedItem(0, [origin], []))  # cena=0, cesta=origin
    # [PrioritizedItem(0, [origin])]

    while queue:
        item = heapq.heappop(queue)
        if item.path[-1] == destination:
            pprint(item)
            continue
        for i in d[item.path[-1]]:
            if i['destination'] in item.path:
                continue
            heapq.heappush(
                queue,
                PrioritizedItem(
                    priority=item.priority + i['final_price'],
                    path=item.path + [i['destination']],
                    flights=item.flights + [i]
                )
            )


find_flights('WIW', 'RFZ', 2)

