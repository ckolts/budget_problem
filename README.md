# Getting Started

To get started:
* Create a GitHub repository
* Add the following as collaborators to your Github: @BFreeNashville, @ronnielankford, @JoshCrosby
* Dig in!

# Background

Within Built, every Project has a budget which has an associated collection of budget items. These budget items represent costs associated with the construction of some collateral. Users can request cash "draws" against these budget items to fund the construction according to some allocated budget.

# Problem

Given the preconfigured Budgets and Draws services, process all draw requests according to the
solution requirements below:

### Solution Requirements

* Budget items cannot be overdrawn
* The drawable amount for budget items is determined by subtracting a budget item's `funded_to_date` from its `original_amount`
* Draw requests must be processed in ascending order of their `effective_date`
* The return value of your solution should print a mapping of budget IDs to a list of processed draw request IDs (e.g, `{int: List[int]}`) for all successfully processed draw requests.

### Instructions

* Run the Budgets and Draws services: `docker-compose up -d`
* Inspect the built-processors directory that has been provided for you
* Finish implementing the draw processor script that satisfies the solution requirements below
* Build the draw processor docker image that will be used when you want to execute the code you've written: `make build`
* Run the docker container defined in the built-processors directory to execute your solution: `make run`
* Unit test your solution
* Run your unit tests using the same docker container: `make test`

#### Example Output

```
{
    1: [10, 20, 30],
    2: [50, 60, 70],
    ...
}
```

# Services

You will need to interact with both the Budgets and Draws service to complete your solution. Both services are available internally on the docker network `built-network` and the `make run` command for the `built-processors` project will run it in the same network so no fiddling is required. Below are the available endpoints for the services:

### Budgets Service

NOTE: Externally, you can reach this service at http://localhost:5001

```
GET http://built-budgets/budgets/

[
  {
    "amount": "126000",
    "balance_remaining": "108500",
    "budget_id": 1
  },
  ...
]
```

```
GET http://built-budgets/items/

[
  {
    "budget_id": 1,
    "budget_item_id": 1,
    "funded_to_date": "2500",
    "original_amount": "5000"
  },
  ...
]
```

### Draws Service

NOTE: Externally, you can reach this service at http://localhost:5002

```
GET http://built-draws/requests/

[
  {
    "amount": "2000",
    "budget_id": 1,
    "budget_item_id": 1,
    "draw_request_id": 1,
    "effective_date": "11/20/2015"
  },
  {
    "amount": "1000",
    "budget_id": 1,
    "budget_item_id": 1,
    "draw_request_id": 2,
    "effective_date": "11/15/2015"
  },
  {
    "amount": "500",
    "budget_id": 1,
    "budget_item_id": 1,
    "draw_request_id": 3,
    "effective_date": "11/25/2015"
  },
  ...
]
```
