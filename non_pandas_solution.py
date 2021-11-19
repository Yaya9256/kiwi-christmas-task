import csv
from collections import defaultdict
import heapq
from dataclasses import dataclass, field
from typing import Any, List
from datetime import datetime, timedelta
import argparse


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    path: Any = field(compare=False)
    flights: Any = field(compare=False)

    def __repr__(self) -> str:
        """ structure:
          WIW -> ECV -> RCZ
         > JV042 WIW - > ECV  <departure> - <arrival>
         > GUAM4 ECV - > RCZ  <departure> - <arrival>
         """
        p = " -> ".join(self.path)
        d = [
            f"> {i['flight_no']} : {i['origin']} -> {i['destination']} " \
            f"{i['departure']} - {i['arrival']} - price: {i['final_price']}"
            for i in self.flights
        ]
        return "\n".join([p] + d)


def find_flights(csv_file, origin, destination, bags):
    # Create dict {origin : [{flight_details_1}, {flight_details_2,..}]}

    # ----------------- Data Load  --------------------
    d = defaultdict(list)
    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # add calculations for final price & change date format
            full_price = float(row['bag_price']) * bags
            final_price = full_price + float(row['base_price'])
            row['final_price'] = final_price
            row['arrival'] = datetime.fromisoformat(row['arrival'])
            row['departure'] = datetime.fromisoformat(row['departure'])
            row['bags_allowed'] = int(row['bags_allowed'])
            d[row['origin']].append(row)

    # --------------------- Simple validity check -------------------------

    # Exception for not matching input & file combination /garbage /mistake
    exist_from = d.get(origin)
    exist_to = destination in (e['destination'] for l in d.values() for e in l)
    if not exist_from or not exist_to:
        raise ValueError(f"The connection between {origin} & {destination} is "
                         f"not found in file {csv_file}")

    # --------------------- Path finding -------------------------

    # Initialize priority queue with starting point Airport
    queue: List[PrioritizedItem] = []
    heapq.heappush(
        queue,
        PrioritizedItem(
            priority=0,
            path=[origin],
            flights=[]
        )
    )

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
                if not timedelta(hours=1) <= departure_next - arrival_last \
                       <= timedelta(hours=6):
                    continue

            # if specific amount of bags is required
            if i['bags_allowed'] < bags:
                continue

            heapq.heappush(
                queue,
                PrioritizedItem(
                    priority=item.priority + i['final_price'],
                    path=item.path + [i['destination']],
                    flights=item.flights + [i]
                )
            )


if __name__ == '__main__':
    # Create and parse input arguments
    parser = argparse.ArgumentParser(description='Lists all flight '
                                                 'combinations for a selected '
                                                 'route between airports '
                                                 'A -> B, ordered by price')
    parser.add_argument('csv_file', type=str,
                        help='CSV file.')
    parser.add_argument('from_airport', type=str,
                        help='from airport shortcut')
    parser.add_argument('to_airport', type=str,
                        help='to airport shortcut')
    parser.add_argument('bags', default='1', type=int, nargs='?',
                        help='number of bags allowed')

    args = parser.parse_args()

    find_flights(args.csv_file,
                 args.from_airport.upper(),
                 args.to_airport.upper(),
                 args.bags)
