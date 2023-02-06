import rubicon_parser as paradox
from utils import write_to_file
from math import pow, ceil

# Pop needs can:
# Grow up to a max (logarithmic function)
# Grow exponentially (exponential function)
def need_grow_exponentially(x: int, base = 15.0, exponent = 4, rate_of_growth = 0.065, horizontal_offset = 2):
    return max(0, ceil(base + pow(exponent, (rate_of_growth * x) + horizontal_offset)))

# Grow up and then grows down (parabola)
pop_needs = paradox.load("common/pop_needs/civ_needs.txt")
buy_packages = paradox.load("common/buy_packages/civ_buy_packages.txt")

for i in range(1, 100):
    # Access the buy_packages
    wealth_level = f"wealth_{i}"
    goods = {}
    goods["popneed_simple_food"] = need_grow_exponentially(i, 15, 4, 0.065, 2)
    if i > 3:
        goods["popneed_wood"] = need_grow_exponentially(i, 12, 4, 0.059, 2)
    if i > 6:
        goods["popneed_tools"] = need_grow_exponentially(i, 10, 4, 0.035, 2)
    if i > 13:
        goods["popneed_ingots"] = need_grow_exponentially(i, 0, 4, 0.065, 2)
    # Assign calculated goods to buy_packages
    buy_packages[wealth_level]["goods"] = goods

write_to_file("src/output/civ_buy_packages.txt", paradox.dumps(buy_packages))
