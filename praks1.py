fh = open("access.log")
count = 0
keywords = "Windows", "Linux", "Mac", "Ubuntu", "Android", "bingbot", "Googlebot", "facebookexternalhit"
d = {"Windows":0, "Linux":0, "Mac":0, "Ubuntu":0, "facebookexternalhit":0, "Googlebot":0, "Android":0, "bingbot":0}

for line in fh:
	count = count + 1
	try:
		source_timestamp, request, response, _, _, agent, _ = line.split("\"")
		method, path, protocol = request.split(" ")
		#print("user visited URL: enos.itcollege.ee" + path)
		#print("agent: " + agent)
		for keyword in keywords:
			if keyword in agent:
				d[keyword] = d.get(keyword, 0) + 1
				break
	except ValueError:
		pass
	
print("Total requests: ", count)
print(d["Windows"])
print(d["Linux"])
print(d["Mac"])
print(d)
total = sum(d.values())
print("Total lines with keywords", total)
l = d.items()
# l.sort(key = lambda (keyword, hits):-hits) # on sama mis, pyyton kolmes alumine
l.sort(key = lambda t:t[1], reverse=True)
for key, value in l:
	print key, "==>", value, "(", value * 100 / total, "%)"



