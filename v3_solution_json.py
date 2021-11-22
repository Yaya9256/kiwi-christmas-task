import csv
from collections import defaultdict
import heapq
from dataclasses import dataclass, field
from typing import Any, List, Dict
from datetime import datetime, timedelta
import argparse
import json


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    path: List[str] = field(compare=False)
    flights: List[Dict[str, Any]] = field(compare=False)

    def output(self):  # -> str:
        """
        Structure of json flight information"""
        return {
            'flights': self.flights,
            'origin': self.path[0],
            'destination': self.path[-1],
            'bags_allowed': min(i['bags_allowed'] for i in self.flights),
            'total_price': sum(i['final_price'] for i in self.flights),
            'travel_time': self.flights[-1]['arrival'] -
                           self.flights[0]['departure']
        }


def load_data(csv_file: str, bags: int) -> Dict[str, List[Dict[str, Any]]]:
    """
    Initialize dict with starting point
    Calculate final_price for flight including baggage
    Change date format for visualization
    """

    airport_departures = defaultdict(list)
    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if bags > int(row['bags_allowed']):
                continue

            # add calculations for final price & change date format
            full_price = float(row['bag_price']) * bags
            final_price = full_price + float(row['base_price'])
            row['final_price'] = final_price
            row['arrival'] = datetime.fromisoformat(row['arrival'])
            row['departure'] = datetime.fromisoformat(row['departure'])
            airport_departures[row['origin']].append(row)
    return airport_departures


def path_finder(
        airport_departures: Dict[str, List[Dict[str, Any]]],
        origin: str,
        destination: str,
) -> None:
    """
    Initialize priority queue with starting point Airport shortcut.
    Priority queue orders inputs by final_price and continue searching till
    destination is reached.
    """

    queue: List[PrioritizedItem] = []
    heapq.heappush(
        queue,
        PrioritizedItem(
            priority=0,
            path=[origin],
            flights=[]
        )
    )
    output = []
    while queue:
        item = heapq.heappop(queue)
        # if final destination, continue listing other routes
        if item.path[-1] == destination:
            output.append(item.output())
            continue

        # check list of all connections from last Airport in queue
        for i in airport_departures[item.path[-1]]:
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

            heapq.heappush(
                queue,
                PrioritizedItem(
                    priority=item.priority + i['final_price'],
                    path=item.path + [i['destination']],
                    flights=item.flights + [i]
                )
            )
    print(json.dumps(output, indent=4, default=str))


if __name__ == '__main__':
    # Create and parse input arguments
    parser = argparse.ArgumentParser(description='Lists all flight '
                                                 'combinations for a selected '
                                                 'route between airports '
                                                 'A -> B, ordered by price')
    parser.add_argument('csv_file',
                        type=str,
                        help='CSV file.')
    parser.add_argument('from_airport',
                        type=str,
                        help='from airport shortcut')
    parser.add_argument('to_airport',
                        type=str,
                        help='to airport shortcut')
    parser.add_argument('bags',
                        default='1',
                        type=int,
                        nargs='?',
                        help='number of bags allowed')

    args = parser.parse_args()

    airport_departures = load_data(args.csv_file, args.bags)

    path_finder(
        airport_departures,
        args.from_airport.upper(),
        args.to_airport.upper()
    )
