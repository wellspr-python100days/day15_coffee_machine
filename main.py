MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    },
}

drinks = {0: "espresso", 1: "latte", 2: "cappuccino"}

resources = {
    "water": {"qt": 1000, "unit": "ml"},
    "milk": {"qt": 1000, "unit": "ml"},
    "coffee": {"qt": 1000, "unit": "ml"},
}

cash = {"value": 10.00}

operations = []


def print_report():
    print("\n***Machine's resources report***\n")

    for resource in resources:
        quantity = resources[resource]["qt"]
        unit = resources[resource]["unit"]
        print(f"{resource.title()}: {quantity}{unit}")

    print(f"\nOperations: ")
    for op in operations:
        print(
            f"drink: {op['sold']['drink']} - received: {op['sold']['money_received']}"
        )

    print(f"\nCash: ${cash['value']:.2f}")
    print("***end of report***")


def get_ingredients(option):
    drink = drinks[option]
    return MENU[drink]["ingredients"]


def get_cost(option):
    drink = drinks[option]
    return MENU[drink]["cost"]


def make_drink(option):
    ingredients = get_ingredients(option)

    for ingredient in ingredients:
        resources[ingredient]["qt"] -= ingredients[ingredient]


def check_resources(option):
    ingredients = get_ingredients(option)
    depleted = []

    for ingredient in ingredients:
        if resources[ingredient]["qt"] < ingredients[ingredient]:
            depleted.append(ingredient)

    if len(depleted) > 0:
        print("Sorry, there is not enough: ")
        for item in depleted:
            print(item)
        return False
    return True


def sum_cents(coins: dict):
    return (
        0.01 * coins["penny"]
        + 0.05 * coins["nickel"]
        + 0.1 * coins["dime"]
        + 0.25 * coins["quarter"]
    )


def check_payment(option, coins: dict):
    cost = get_cost(option)
    money_received = sum_cents(coins)

    if money_received < cost:
        print("Sorry, that's not enough money. Money refunded.")
        return False
    else:
        cash["value"] += cost
        change = money_received - cost

        operations.append(
            {"sold": {"drink": drinks[option], "money_received": money_received}}
        )

        if change > 0:
            print(f"Here's the change: ${change:.2f}")

        return True


coins_plurals = {
    "quarter": "quarters",
    "dime": "dimes",
    "nickel": "nickels",
    "penny": "pennies",
}


def machine():
    MACHINE_ON = True

    while MACHINE_ON:

        try:
            print("\nMenu: \n")
            for n in range(0, 3):
                print(f"{n} - {drinks[n]} (${get_cost(n):.2f})")

            option = input("\n> ")

            if option in ["0", "1", "2"]:
                int_option = int(option)
                drink = drinks[int_option]
                cost = get_cost(int_option)

                if check_resources(int_option):
                    print("Please insert the number of coins in the order: ")
                    money_inserted = {}

                    for piece in ["quarter", "dime", "nickel", "penny"]:
                        value = input(f"> {coins_plurals[piece].title()} > ")
                        try:
                            value = int(value)
                        except:
                            value = 0
                        money_inserted[piece] = value

                    if check_payment(int_option, money_inserted):
                        print(f"\nPreparing a {drink}...\nHere is your drink.")
                        make_drink(int_option)

            elif option == "report":
                print_report()

            elif option == "off":
                MACHINE_ON = False

            else:
                print("Invalid option.")
        except:
            pass

machine()
