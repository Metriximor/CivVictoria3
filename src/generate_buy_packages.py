import rubicon_parser as paradox
from utils import write_to_file
from math import pow, ceil

# Pop needs can:
# Grow up to a max (logarithmic function)
# Grow exponentially (exponential function)
def need_grow_exponentially(x: int, base = 15, exponent = 4, rate_of_growth = 0.065, horizontal_offset = 2):
    return ceil(base + pow(exponent, (rate_of_growth * x) + horizontal_offset))

# Grow up and then grows down (parabola)
pop_needs = paradox.load("common/pop_needs/civ_needs.txt")
buy_packages = paradox.load("common/buy_packages/civ_buy_packages.txt")

for i in range(1, 100):
    # Access the buy_packages
    wealth_level = f"wealth_{i}"
    goods = {}
    for pop_need in pop_needs:
        goods[pop_need] = need_grow_exponentially(i, 15, 4, 0.065, 2)
    # Assign calculated goods to buy_packages
    buy_packages[wealth_level]["goods"] = goods

write_to_file("src/output/civ_buy_packages.txt", paradox.dumps(buy_packages))
