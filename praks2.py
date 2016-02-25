import os
import gzip
import urllib

import argparse

def humanize(bytes):
	if bytes < 1024:
		return "%d B" % bytes
	elif bytes < 1024 ** 2:
		return "%d kB" % (bytes / 1024)
	elif bytes < 1024 ** 3:
		return "%d MB" % (bytes / 1024 ** 2)
	elif bytes < 1024 ** 4:
		return "%d GB" % (bytes / 1024 ** 3)
	else:
		return "%.1f TB" % (bytes / 1024.0 ** 4)

parser = argparse.ArgumentParser(description='Apache log parser')
parser.add_argument('--path', help='Path to apache log files', 
	default="/var/log/apache2")
parser.add_argument('--top_urls', help="Find top URLs", action="store_true")
parser.add_argument('--geoip', help="Resolve IP-s to country codes", action="store_true")

args = parser.parse_args()
print("We are expecting logs from"), args.path
 
# Following is the directory with log files,
# On Windows substitute it where you downloaded the files
root = "/home/mlugus/logs"

keywords = "Windows", "Linux", "OS X", "Ubuntu", "Googlebot", "bingbot", "Android", "YandexBot", "facebookexternalhit"
d = {}
urls = {}
users = {}
total = 0
 
for filename in os.listdir(args.path):
    if not filename.startswith("access.log"):
        print "Skipping unknown file:", filename
        continue
    if filename.endswith(".gz"):
        fh = gzip.open(os.path.join(args.path, filename))
    else:
        fh = open(os.path.join(args.path, filename))
    print "Going to process:", filename
    for line in fh:
            total = total + 1
	    try:
		source_timestamp, request, response, referrer, _, agent, _ = line.split("\"")
		method, path, protocol = request.split(" ")
		_, status_code, content_lenght, _ =response.split(" ")
		content_lenght = int(content_lenght)
		path = urllib.unquote(path)
		if path.startswith("/~"):
			user, pask = path[2:].split("/",1)
			try:
				users[user] = users[user] + content_lenght
			except:
				users[user] = content_lenght
                url = "http://enos.itcollege.ee" + path
                try:
                        urls[url] = urls[url] + 1
                except:
                        urls[url] = 1
		for keyword in keywords:
		    if keyword in agent:
		        try:
		            d[keyword] = d[keyword] + 1
		        except KeyError:
		            d[keyword] = 1
		        break # Stop searching for other keywords
	    except ValueError:
		pass # This will do nothing, needed due to syntax

print "Total lines:", total
 
results = d.items()
results.sort(key = lambda item:item[1], reverse=True)
for keyword, hits in results:
    print keyword, "==>", hits, "(", hits * 100 / total, "%)"

print

results = users.items()
results.sort(key = lambda item:item[1], reverse=True)
for user, transfered_bytes in results[:5]:
    print user, "==>", humanize(transfered_bytes)

if args.top_urls:
	print
	print("Top 5 visited URL-s:")
	results = urls.items()
	results.sort(key = lambda item:item[1], reverse=True)
	for path, hits in results[:5]:
    		print "http://enos.itcollege.ee" + path, "==>", hits, "(", hits * 100 / total, "%)"












