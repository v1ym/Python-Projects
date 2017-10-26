from random import shuffle
from bs4 import BeautifulSoup
import urllib2, traceback, time, sys
import libtorrent as lt

search_for = "baby driver"
temp_dir = 'C:\Users\The Archangel\Documents\GitHub\practice'
def search_string(search):
    search = search.split(" ")

    keywords = ""
    for word in search:
        if not (word == search[0]):
            keywords = keywords + "%20" + word
        else:
            keywords = keywords + word

    url = "https://thepiratebay.org/search/" + keywords + "/0/99/0"
    return url
def download(magnet):
    ses = lt.session()
    ses.listen_on(6881, 6891)
    params = {
        'save_path': temp_dir,
    }

    handle = lt.add_magnet_uri(ses, magnet, params)

    print("Downloading Metadata (this may take a while)")
    while (not handle.has_metadata()):
        try:
            print '.',
            time.sleep(.5)
        except KeyboardInterrupt:
            print("Aborting...")
            ses.pause()
            sys.exit(0)
        except Exception, E:
            traceback.print_exc()

    print("Done")

    torinfo = handle.get_torrent_info()
    torfile = lt.create_torrent(torinfo)

    print(torinfo.name() + ".torrent")

    s = handle.status()
    while (not s.is_seeding):
            s = handle.status()

            state_str = ['queued', 'checking', 'downloading metadata', \
                    'downloading', 'finished', 'seeding', 'allocating']
            print '%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
                    (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
                    s.num_peers, state_str[s.state])

            time.sleep(1)
torrents = dict()
downloadable_torrent = dict()
runner_up = dict()

trusted_uploaders = [
    "ettv",
    "TvTeam",
    "makintos13"]

'''
#must spoof headers to crawl site
url = search_string(search_for)
request = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib2.urlopen(request).read()
soup = BeautifulSoup(html, 'html.parser')
'''
#file saved for testing
f = open('testhtml.html', 'r')
html = f.read()
f.close()
soup = BeautifulSoup(html, 'html.parser')

#build the list of potential torrents from trusted uploaders, found from the above search string
potential_links = []
for link in soup.find_all('tr', {'class': ''}):
    try:
        uploader = link.find('font').contents[1].text
        if (uploader in trusted_uploaders):
            potential_links.append(link)
    except: continue


#only run downloader if there are potential links
if (potential_links):
    #convert each potential torrent into a key filled with information about the torrent

    for i in range(len(potential_links)):
        #get the row out of the table, row_length is easier seeds/leachers
        row_content = potential_links[i].select('td')
        row_length = len(row_content)

        #cut it up and split it into usable cuts of meat
        info = potential_links[i].find('font').contents[0].encode('utf-8').split(',')

        torrents[i] = {}
        size = info[1].split('\ ')
        torrents[i]['size'] = size[0][1:]
        torrents[i]['name'] = potential_links[i].find('div', {'class': 'detName'}).text[1:-1]
        torrents[i]['seeds'] = int(row_content[row_length - 2].text)
        torrents[i]['leachers'] = int(row_content[row_length - 1].text)
        torrents[i]['upload_date'] = info[0]
        torrents[i]['magnet'] = potential_links[i].find('a', {'title': "Download this torrent using magnet"}).get('href')
        torrents[i]['uploader'] = potential_links[i].find('font').contents[1].text

        #grabbing the most (downloadable_torrent) and second most (runner_up) seeded torrents
        if not (downloadable_torrent):
            downloadable_torrent = torrents[i]
        elif (torrents[i]['seeds'] > downloadable_torrent['seeds']):
            runner_up = downloadable_torrent
            downloadable_torrent = torrents[i]
        elif ((torrents[i]['seeds'] < downloadable_torrent['seeds']) and not (runner_up)):
            runner_up = torrents[i]
        elif ((torrents[i]['seeds'] < downloadable_torrent['seeds']) and (torrents[i]['seeds'] > runner_up['seeds'])):
            runner_up = torrents[i]

    #printing for debugging
    for i in torrents:
        print str(i) + " -- " + str(torrents[i]['seeds']) + " -- " + torrents[i]['uploader'] + " -- " + torrents[i]['name']

    print ""
    print "Torrent found:"
    print downloadable_torrent['name']
    print "Seeds:" + str(downloadable_torrent['seeds'])
    print str(downloadable_torrent['size'])
    print ""
    choice = raw_input("Do you want to download this file (Y/N)? >> ")

    if (choice == "y"):
        magnet = downloadable_torrent['magnet']
        download(magnet)
    elif(choice == "n"):
        print ""
        print "Torrent found:"
        print runner_up['name']
        print "Seeds:" + str(runner_up['seeds'])
        print str(runner_up['size'])
        print ""
        second_choice = raw_input("Would you like to download the runner up (Y/N)? >> ")
        if (second_choice == "y"):
            magnet = runner_up['magnet']
            download(magnet)
        else:
            print "First and second choice not taken"
    else:
        print "Error, Y/N not chosen correctly"

else:
    print search_for
    print "There were no potential torrents"


#testing below
#############################################################
'''
#get the link, of course
link = soup.find('tr', {'class':''})

#get the row out of the table, row_length is easier seeds/leachers
row_content = link.select('td')
row_length = len(row_content)

#cut it up and split it into usable cuts of meat
info = link.find('font').contents[0].encode('utf-8').split(',')
uploader = link.find('font').contents[1].text
upload_date = info[0]
size = info[1].split('\ ')
size = size[0][1:]
seeds = row_content[row_length - 2].text
leachers = row_content[row_length - 1].text
name = link.find('div', {'class': 'detName'}).text[1:-1]
magnet = link.find('a', {'title': "Download this torrent using magnet"}).get('href')
'''
