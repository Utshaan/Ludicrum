import rarbgapi

client = rarbgapi.RarbgAPI()

for t in client.search(search_string="dr strange"):
    print(t)