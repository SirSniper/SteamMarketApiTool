import steam_market_api

test_item = MarketItem('AK-47 | Aquamarine Revenge (Minimal Wear)', 730, 'USD')

print(test_item.get_lowest_price())
print(test_item.get_volume())
print(test_item.get_median_price())

names = ['AWP | Asiimov (Minimal Wear)', 'AK-47 | Aquamarine Revenge (Minimal Wear)', 'P90 | Asiimov (Well-Worn)']

steam_items = steam_market_api.get_lowest_of_each(names, 730, 'USD')

print(steam_items['AK-47 | Aquamarine Revenge (Minimal Wear)'])
