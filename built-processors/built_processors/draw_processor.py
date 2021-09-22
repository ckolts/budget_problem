#!/usr/bin/env python3
from datetime import datetime
import requests

BUDGETS_URL = 'http://built-budgets'
DRAWS_URL = 'http://built-draws/'


class DrawProcessor:
    def __init__(self):
        self.budgets_url = BUDGETS_URL
        self.draws_url = DRAWS_URL
        self.budgets = dict()
        self.items = dict()

    def get_budgets(self) -> dict:
        res = requests.get(f'{BUDGETS_URL}/budgets').json()
        budgets = dict()
        for budget in res:
            budget_id = budget.pop('budget_id')
            budgets[budget_id] = {key: int(val) for key, val in budget.items()}
        return budgets

    def get_budget_items(self) -> dict:
        res = requests.get(f'{BUDGETS_URL}/items').json()
        items = dict()
        for item in res:
            item_id = item.pop('budget_item_id')
            items[item_id] = item
        return items

    def get_draw_requests(self) -> list:
        return requests.get(f'{DRAWS_URL}/requests').json()

    def sort_draw_requests(self, draw_requests: list) -> list:
        def draw_request_key(req: dict) -> datetime:
            return datetime.strptime(req.get('effective_date'), '%m/%d/%Y')

        draw_requests.sort(key=draw_request_key)
        return draw_requests

    def is_drawable(self, req: dict) -> bool:
        item = self.items.get(req.get('budget_item_id'))
        amount_requested = int(req.get('amount'))
        drawable_amount = int(item.get('original_amount')) - int(item.get('funded_to_date'))
        return amount_requested <= drawable_amount

    def handler(self) -> dict:
        # retrieve values from services
        self.budgets = self.get_budgets()
        self.items = self.get_budget_items()
        _draw_requests = self.get_draw_requests()
        draw_requests = self.sort_draw_requests(_draw_requests)

        # process draw requests
        processed_requests = dict()
        for req in draw_requests:
            # obtain values from draw request
            amount = int(req.get('amount'))
            budget_id = req.get('budget_id')
            budget = self.budgets[budget_id].get('balance_remaining')
            req_id = req.get('draw_request_id')

            # process draw request if funds are available
            if self.is_drawable(req) and amount <= budget:
                if processed_requests.get(budget_id, None):
                    processed_requests[budget_id].append(req_id)
                else:
                    processed_requests[budget_id] = [req_id]
                self.budgets[budget_id]['balance_remaining'] -= amount

        return processed_requests


if __name__ == '__main__':
    draw_processor = DrawProcessor()
    print(draw_processor.handler())
