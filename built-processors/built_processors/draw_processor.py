#!/usr/bin/env python3
from datetime import datetime
import requests

# BASE_URL = 'http://localhost'


BASE_URL = 'http://172.17.0.1'


class DrawProcessor:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url

    def draw_request_key(self, req) -> datetime:
        return datetime.strptime(req.get('effective_date'), '%m/%d/%Y')

    def get_budgets(self) -> dict:
        res = requests.get(f'{BASE_URL}:5001/budgets').json()
        budgets = dict()
        for budget in res:
            budget_id = budget.pop('budget_id')
            budgets[budget_id] = {key: int(val) for key, val in budget.items()}
        return budgets

    def get_budget_items(self) -> dict:
        res = requests.get(f'{BASE_URL}:5001/items').json()
        items = dict()
        for item in res:
            item_id = item.pop('budget_item_id')
            items[item_id] = item
        return items

    def get_draw_requests(self) -> dict:
        return requests.get(f'{BASE_URL}:5002/requests').json()

    def is_funded(self, req, items) -> bool:
        item = items.get(req.get('budget_item_id'))
        return int(item.get('original_amount')) - int(item.get('funded_to_date')) >= 0

    def handler(self) -> dict:
        # retrieve values from services
        budgets = self.get_budgets()
        items = self.get_budget_items()
        draw_requests = self.get_draw_requests()
        draw_requests.sort(key=self.draw_request_key)

        # process draw requests
        processed_requests = dict()
        for req in draw_requests:
            # obtain values from draw request
            amount = int(req.get('amount'))
            budget_id = req.get('budget_id')
            budget = budgets[budget_id].get('balance_remaining')
            req_id = req.get('draw_request_id')

            # process draw request if funds are available
            if self.is_funded(req, items) and amount <= budget:
                if processed_requests.get(budget_id, None):
                    processed_requests[budget_id].append(req_id)
                else:
                    processed_requests[budget_id] = [req_id]
                budgets[budget_id]['balance_remaining'] -= amount

        return processed_requests


if __name__ == '__main__':
    draw_processor = DrawProcessor(base_url='http://localhost')
    print(draw_processor.handler())
