import unittest
from unittest.mock import MagicMock

from built_processors.draw_processor import DrawProcessor


class DrawProcessorTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.processor = DrawProcessor()

    def test_draw_requests_are_sorted_by_date(self):
        draw_requests = [
            {
                "draw_request_id": 3,
                "effective_date": "12/15/2015"
            },
            {
                "draw_request_id": 1,
                "effective_date": "8/1/2015"
            },
            {
                "draw_request_id": 2,
                "effective_date": "10/1/2015"
            },
        ]
        result = self.processor.sort_draw_requests(draw_requests)
        self.assertEqual(result[0].get('draw_request_id'), 1)
        self.assertEqual(result[1].get('draw_request_id'), 2)
        self.assertEqual(result[2].get('draw_request_id'), 3)

    def test_is_drawable_with_sufficient_funding_passes(self):
        req = {'amount': '25',
               'budget_item_id': 3,
               }
        self.processor.items = {
            3: {'original_amount': '100',
                'funded_to_date': '50'
                }
        }
        result = self.processor.is_drawable(req=req)
        self.assertTrue(result)

    def test_is_drawable_with_insufficient_funding_fails(self):
        req = {'amount': '200',
               'budget_item_id': 3,
               }
        self.processor.items = {
            3: {'original_amount': '100',
                'funded_to_date': '50'
                }
        }
        result = self.processor.is_drawable(req=req)
        self.assertFalse(result)

    def test_drawable_requests_with_sufficient_budget_are_processed(self):
        resp_budgets = {1: {'balance_remaining': 1000}}
        resp_budget_items = {
            1: {
                "budget_id": 1,
                "funded_to_date": "250",
                "original_amount": "500"
            },
            2: {
                "budget_id": 1,
                "funded_to_date": "50",
                "original_amount": "100"
            }
        }
        resp_draw_requests = [
            {
                "amount": "250",
                "budget_id": 1,
                "budget_item_id": 1,
                "draw_request_id": 10,
                "effective_date": "11/15/2015"
            },
            {
                "amount": "40",
                "budget_id": 1,
                "budget_item_id": 2,
                "draw_request_id": 20,
                "effective_date": "11/20/2015"
            }]
        self.processor.service.get_budgets = MagicMock(return_value=resp_budgets)
        self.processor.service.get_budget_items = MagicMock(return_value=resp_budget_items)
        self.processor.service.get_draw_requests = MagicMock(return_value=resp_draw_requests)
        result = self.processor.handler()
        expected = {1: [10, 20]}
        self.assertEqual(expected, result)

    def test_only_drawable_requests_with_sufficient_budget_are_processed(self):
        resp_budgets = {1: {'balance_remaining': 1000}}
        resp_budget_items = {
            1: {
                "budget_id": 1,
                "funded_to_date": "250",
                "original_amount": "500"
            },
            2: {
                "budget_id": 1,
                "funded_to_date": "50",
                "original_amount": "100"
            }
        }
        resp_draw_requests = [
            {
                "amount": "350",
                "budget_id": 1,
                "budget_item_id": 1,
                "draw_request_id": 10,
                "effective_date": "11/15/2015"
            },
            {
                "amount": "50",
                "budget_id": 1,
                "budget_item_id": 2,
                "draw_request_id": 20,
                "effective_date": "11/20/2015"
            }]
        self.processor.service.get_budgets = MagicMock(return_value=resp_budgets)
        self.processor.service.get_budget_items = MagicMock(return_value=resp_budget_items)
        self.processor.service.get_draw_requests = MagicMock(return_value=resp_draw_requests)
        result = self.processor.handler()
        expected = {1: [20]}
        self.assertEqual(expected, result)

    def test_drawable_requests_with_insufficient_budget_are_not_processed(self):
        resp_budgets = {1: {'balance_remaining': 250}}
        resp_budget_items = {
            1: {
                "budget_id": 1,
                "funded_to_date": "250",
                "original_amount": "500"
            },
            2: {
                "budget_id": 1,
                "funded_to_date": "50",
                "original_amount": "100"
            }
        }
        resp_draw_requests = [
            {
                "amount": "250",
                "budget_id": 1,
                "budget_item_id": 1,
                "draw_request_id": 10,
                "effective_date": "11/15/2015"
            },
            {
                "amount": "40",
                "budget_id": 1,
                "budget_item_id": 2,
                "draw_request_id": 20,
                "effective_date": "11/20/2015"
            }]
        self.processor.service.get_budgets = MagicMock(return_value=resp_budgets)
        self.processor.service.get_budget_items = MagicMock(return_value=resp_budget_items)
        self.processor.service.get_draw_requests = MagicMock(return_value=resp_draw_requests)
        result = self.processor.handler()
        expected = {1: [10]}
        self.assertEqual(expected, result)

    def test_results_are_mapped_by_budget_id(self):
        resp_budgets = {1: {'balance_remaining': 1000},
                        2: {'balance_remaining': 1000}}
        resp_budget_items = {
            1: {
                "budget_id": 1,
                "funded_to_date": "250",
                "original_amount": "500"
            },
            2: {
                "budget_id": 1,
                "funded_to_date": "50",
                "original_amount": "100"
            },
            3: {
                "budget_id": 2,
                "funded_to_date": "200",
                "original_amount": "400"
            },
            4: {
                "budget_id": 2,
                "funded_to_date": "100",
                "original_amount": "200"
            }
        }
        resp_draw_requests = [
            {
                "amount": "250",
                "budget_id": 1,
                "budget_item_id": 1,
                "draw_request_id": 10,
                "effective_date": "11/15/2015"
            },
            {
                "amount": "40",
                "budget_id": 1,
                "budget_item_id": 2,
                "draw_request_id": 20,
                "effective_date": "11/20/2015"
            },
            {
                "amount": "300",
                "budget_id": 2,
                "budget_item_id": 3,
                "draw_request_id": 30,
                "effective_date": "11/20/2015"
            },
            {
                "amount": "50",
                "budget_id": 2,
                "budget_item_id": 4,
                "draw_request_id": 40,
                "effective_date": "11/20/2015"
            },
        ]
        self.processor.service.get_budgets = MagicMock(return_value=resp_budgets)
        self.processor.service.get_budget_items = MagicMock(return_value=resp_budget_items)
        self.processor.service.get_draw_requests = MagicMock(return_value=resp_draw_requests)
        result = self.processor.handler()
        expected = {1: [10, 20], 2: [40]}
        self.assertEqual(expected, result)
