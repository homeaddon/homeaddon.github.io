# Copyright (C) 2023, Roman V. M.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
Example video plugin that is compatible with Kodi 20.x "Nexus" and above
"""
import os
import sys
from urllib.parse import urlencode, parse_qsl
from urllib.request import urlopen
import re
import json

import xbmcgui
import xbmcplugin
from xbmcaddon import Addon
from xbmcvfs import translatePath
import xbmc


# Get the plugin url in plugin:// notation.
URL = sys.argv[0]
# Get a plugin handle as an integer number.
HANDLE = int(sys.argv[1])
# Get addon base path
ADDON_PATH = translatePath(Addon().getAddonInfo('path'))
ICONS_DIR = os.path.join(ADDON_PATH, 'resources', 'images', 'icons')
FANART_DIR = os.path.join(ADDON_PATH, 'resources', 'images', 'fanart')
movieIcon = os.path.join(ICONS_DIR, 'movies.png')
movieFanart = os.path.join(FANART_DIR, 'movies.jpg')
searchIcon = os.path.join(ICONS_DIR, 'search.png')

apiKey = '&api_key=3f9d3354714885b67fd615366fc0b195'
apiLink = 'https://api.themoviedb.org/3/'

VIDEOS = [
    {
        'genre': 'Movies',
        'icon': os.path.join(ICONS_DIR, 'movies.png'),
        'fanart': os.path.join(FANART_DIR, 'movies.jpg'),
    },
    {
        'genre': 'TV Section',
        'icon': os.path.join(ICONS_DIR, 'tv.ico'),
        'fanart': os.path.join(FANART_DIR, 'movies.jpg'),
    },

]
#animation family = kids



genre = {28:"Action",
12:"Adventure",
16:"Animation",
35:"Comedy",
80:"Crime",
99:"Documentary",
18:"Drama",
10751:"Family",
14:"Fantasy",
36:"History",
27:"Horror",
10402:"Music",
9648:"Mystery",
10749:"Romance",
878:"Science Fiction",
10770:"TV Movie",
53:"Thriller",
10752:"War",
37:"Western",
10759:"Action & Adventure",
10762:"Kids",
10763:"News",
10764:"Reality",
10765:"Sci-Fi & Fantasy",
10766:"Soap",
10767:"Talk",
10768:"War & Politics"}


searchIndex = 0

def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.

    :param kwargs: "argument=value" pairs
    :return: plugin call URL
    :rtype: str
    """
    return '{}?{}'.format(URL, urlencode(kwargs))




def list_genres():
    """
    Create the list of movie genres in the Kodi interface.
    """
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(HANDLE, 'Media Types')
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(HANDLE, 'movies')
    # Get movie genres
    genres = VIDEOS
    # Iterate through genres
    for index, genre_info in enumerate(genres):
        # Create a list item with a text label.
        list_item = xbmcgui.ListItem(label=genre_info['genre'])
        # Set images for the list item.
        list_item.setArt({'icon': genre_info['icon'], 'fanart': genre_info['fanart']})
        # Set additional info for the list item using its InfoTag.
        # InfoTag allows to set various information for an item.
        # For available properties and methods see the following link:
        # https://codedocs.xyz/xbmc/xbmc/classXBMCAddon_1_1xbmc_1_1InfoTagVideo.html
        # 'mediatype' is needed for a skin to display info for this ListItem correctly.
        info_tag = list_item.getVideoInfoTag()
        info_tag.setMediaType('video')
        info_tag.setTitle(genre_info['genre'])
        info_tag.setGenres([genre_info['genre']])
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=listing&genre_index=0
        url = get_url(action='listing', genre_index=index)
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
    # Finish creating a virtual folder.
    xbmc.executebuiltin('Container.SetViewMode(55)')
    xbmcplugin.endOfDirectory(HANDLE)

def list_options(genre_index):

    options = [{"title": "Search", "icon": searchIcon, "fanart": movieFanart, "key": "search"},
               {"title": "Indian", "icon": movieIcon, "fanart": movieFanart, "key":"latest"},
               {"title": "English", "icon": movieIcon, "fanart": movieFanart, "key":"latest"}]

    # Iterate through options
    for index, options_info in enumerate(options):
        # Create a list item with a text label.
        list_item = xbmcgui.ListItem(label=options_info['title'])
        # Set images for the list item.
        list_item.setArt({'icon': options_info['icon'], 'fanart': options_info['fanart']})
        # Set additional info for the list item using its InfoTag.
        # InfoTag allows to set various information for an item.
        # For available properties and methods see the following link:
        # https://codedocs.xyz/xbmc/xbmc/classXBMCAddon_1_1xbmc_1_1InfoTagVideo.html
        # 'mediatype' is needed for a skin to display info for this ListItem correctly.
        info_tag = list_item.getVideoInfoTag()
        info_tag.setMediaType('video')
        info_tag.setTitle(options_info['title'])
        info_tag.setGenres([options_info['title']])
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=listing&genre_index=0

        if "search" in options_info['key']:
            url = get_url(action=options_info['key'], index=genre_index)
        else:
            url = get_url(action=options_info['key'], genre_index=genre_index, index=index)
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_VIDEO_YEAR)
    xbmc.executebuiltin('Container.SetViewMode(55)')
    xbmcplugin.endOfDirectory(HANDLE)
def latest(genre_index, latest_index):
    options = [{"title": "Popularity", "icon": movieIcon, "fanart": movieFanart, "key":"discover"},
               {"title": "Release Date", "icon": movieIcon, "fanart": movieFanart, "key":"discover"},
               {"title": "Rating", "icon": movieIcon, "fanart": movieFanart, "key":"discover"}]
    for discoveryIndex, options_info in enumerate(options):
        # Create a list item with a text label.
        list_item = xbmcgui.ListItem(label=options_info['title'])
        # Set images for the list item.
        list_item.setArt({'icon': options_info['icon'], 'fanart': options_info['fanart']})
        # Set additional info for the list item using its InfoTag.
        # InfoTag allows to set various information for an item.
        # For available properties and methods see the following link:
        # https://codedocs.xyz/xbmc/xbmc/classXBMCAddon_1_1xbmc_1_1InfoTagVideo.html
        # 'mediatype' is needed for a skin to display info for this ListItem correctly.
        info_tag = list_item.getVideoInfoTag()
        info_tag.setMediaType('video')
        info_tag.setTitle(options_info['title'])
        info_tag.setGenres([options_info['title']])
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=listing&genre_index=0
        url = get_url(action=options_info['key'], genre_index=genre_index, latest_index=latest_index, discoveryIndex=discoveryIndex, page=1)
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)

    # Add sort methods for the virtual folder items
    # Finish creating a virtual folder.
    xbmc.executebuiltin('Container.SetViewMode(55)')
    xbmcplugin.endOfDirectory(HANDLE)
def discover(genreIndex, latestIndex, discoveryIndex, page):
    xbmcplugin.setPluginCategory(HANDLE, "latest")
    xbmcplugin.setContent(HANDLE, 'movies')
    discoveryList = ["popularity.desc","primary_release_date.desc","vote_count.desc"]
    if genreIndex == 0:
        if latestIndex == 1:
            link = apiLink + "discover/movie?include_adult=false&include_video=false&vote_count.gte=50&with_origin_country=IN&sort_by=" + discoveryList[discoveryIndex] + apiKey + "&page=" + str(page)
        else:
            link = apiLink + "discover/movie?include_adult=false&include_video=false&vote_count.gte=50&sort_by=" + discoveryList[discoveryIndex] + apiKey + "&page=" + str(page)
        html = urlopen(link).read()
        movieInfo = json.loads(html)
        results = movieInfo["results"]
        page = movieInfo["page"]
        #totalPages = movieInfo["total_pages"]
        for row in results:
            list_item = xbmcgui.ListItem(label=row['title'])
            if row['backdrop_path']:
                list_item.setArt({'poster':"https://image.tmdb.org/t/p/original"+ row['poster_path'], 'fanart': "https://image.tmdb.org/t/p/original"+ row['backdrop_path'], 'banner':"https://image.tmdb.org/t/p/original"+ row['backdrop_path']})
            else:
                list_item.setArt({'poster':"https://image.tmdb.org/t/p/original"+ row['poster_path']})
            list_item.setRating("tmdb", row["vote_average"], row["vote_count"], True)
            info_tag = list_item.getVideoInfoTag()
            info_tag.setMediaType('movie')
            info_tag.setUniqueIDs({"tmdb": str(row["id"])}, "tmdb")
            info_tag.setTitle(row['title'])
            genres = []
            for r in row['genre_ids']:
                genres.append(genre[r])
            info_tag.setGenres(genres)
            info_tag.setPlot(row['overview'])
            info_tag.setYear(int(row['release_date'][:4]))
            list_item.setProperty('IsPlayable', 'true')
            is_folder = False
            url = get_url(action='play', video=row["title"], year=int(row['release_date'][:4]), latestIndex=latestIndex)
            xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
        list_item = xbmcgui.ListItem(label="Next Page")
        list_item.setArt({'icon': movieIcon, 'fanart': movieFanart})
        list_item.setProperty('SpecialSort', 'bottom')
        info_tag = list_item.getVideoInfoTag()
        info_tag.setTitle("Next Page")
        is_folder = True
        page += 1
        url = get_url(action="discover", genre_index=genreIndex, latest_index=latestIndex,
                      discoveryIndex=discoveryIndex, page=page)
        xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
    else:
        if latestIndex == 1:
            link = apiLink + "discover/tv?include_adult=false&include_null_first_air_dates=false&vote_count.gte=50&with_origin_country=IN&sort_by=" + \
                   discoveryList[discoveryIndex] + apiKey + "&page=" + str(page)
        else:
            link = apiLink + "discover/tv?include_adult=false&include_null_first_air_dates=false&vote_count.gte=50&sort_by=" + \
                   discoveryList[discoveryIndex] + apiKey + "&page=" + str(page)
        html = urlopen(link).read()
        movieInfo = json.loads(html)
        results = movieInfo["results"]
        page = movieInfo["page"]
        for row in results:
            list_item = xbmcgui.ListItem(label=row['name'])
            if row['backdrop_path']:
                list_item.setArt({'poster':"https://image.tmdb.org/t/p/original"+ row['poster_path'], 'fanart': "https://image.tmdb.org/t/p/original"+ row['backdrop_path'], 'banner':"https://image.tmdb.org/t/p/original"+ row['backdrop_path']})
            else:
                list_item.setArt({'poster':"https://image.tmdb.org/t/p/original"+ row['poster_path']})
            list_item.setRating("tmdb", row["vote_average"], row["vote_count"], True)
            info_tag = list_item.getVideoInfoTag()
            info_tag.setMediaType('movie')
            info_tag.setUniqueIDs({"tmdb": str(row["id"])}, "tmdb")
            info_tag.setTitle(row['name'])
            genres = []
            for r in row['genre_ids']:
                genres.append(genre[r])
            info_tag.setGenres(genres)
            info_tag.setPlot(row['overview'])
            info_tag.setYear(int(row['first_air_date'][:4]))
            list_item.setProperty('IsPlayable', 'false')
            is_folder = True
            #url = get_url(action='playtv', video=row["name"], year=int(row['first_air_date'][:4]), latestIndex=latestIndex)
            try:
                url = get_url(action='playtv', video=row["name"], year=int(row['first_air_date'][:4]), latestIndex=latestIndex, page=1,
                              poster=row['poster_path'], backdrop=row['backdrop_path'], id=row['id'],
                              plot=row['overview'])
            except:
                url = get_url(action='playtv', video=row["name"], year=0, latestIndex=latestIndex, page=1, poster=row['poster_path'],
                              backdrop=row['backdrop_path'], id=row['id'], plot=row['overview'])

            xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
        list_item = xbmcgui.ListItem(label="Next Page")
        list_item.setArt({'icon': movieIcon, 'fanart': movieFanart})
        list_item.setProperty('SpecialSort', 'bottom')
        info_tag = list_item.getVideoInfoTag()
        info_tag.setTitle("Next Page")
        is_folder = True
        page += 1
        url = get_url(action="discover", genre_index=genreIndex, latest_index=latestIndex,
                      discoveryIndex=discoveryIndex, page=page)
        xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
    xbmc.executebuiltin('Container.SetViewMode(51)')
    xbmcplugin.endOfDirectory(HANDLE)


def getusersearch():
    kb = xbmc.Keyboard('default', 'heading')
    kb.setDefault('')
    kb.setHeading('Please enter the media title and optionally its year eg: Avengers (2019)')
    kb.setHiddenInput(False)
    kb.doModal()
    if (kb.isConfirmed()):
        search_term = kb.getText()
        return search_term
    else:
        return False



def search(query, index):
    if index == 0:
        xbmcplugin.setPluginCategory(HANDLE, "search")
        xbmcplugin.setContent(HANDLE, 'movies')
        if "(" in query:
            query = query.split()
            year = query[-1][1:5]
            query = query[:-1]
            query = " ".join(query)
            link = "https://api.themoviedb.org/3/search/movie?include_adult=false&language=en-US&query="+ query.replace(" ", "+") +"&year="+ year + apiKey
        else:
            link = "https://api.themoviedb.org/3/search/movie?include_adult=false&language=en-US&query=" + query.replace(
                " ", "+") + apiKey
        html = urlopen(link).read()
        movieInfo = json.loads(html)
        results = movieInfo["results"]
        #page = movieInfo["page"]
        #totalPages = movieInfo["total_pages"]
        for row in results:
            list_item = xbmcgui.ListItem(label=row['title'])
            if row['backdrop_path']:
                list_item.setArt({
                                  'fanart': "https://image.tmdb.org/t/p/original" + row['backdrop_path'],
                                  'banner': "https://image.tmdb.org/t/p/original" + row['backdrop_path']})
            if row['poster_path']:
                list_item.setArt({'poster': "https://image.tmdb.org/t/p/original" + row['poster_path']})
            list_item.setRating("tmdb", row["vote_average"], row["vote_count"], True)
            info_tag = list_item.getVideoInfoTag()
            info_tag.setMediaType('movie')
            info_tag.setUniqueIDs({"tmdb": str(row["id"])}, "tmdb")
            info_tag.setTitle(row['title'])
            genres = []
            for r in row['genre_ids']:
                genres.append(genre[r])
            info_tag.setGenres(genres)
            info_tag.setPlot(row['overview'])
            try:
                info_tag.setYear(int(row['release_date'][:4]))
            except:
                pass
            list_item.setProperty('IsPlayable', 'false')
            is_folder = True
            try:
                url = get_url(action='play', video=row["title"], year=int(row['release_date'][:4]), latestIndex=3, poster=row['poster_path'], backdrop=row['backdrop_path'], id=row['id'], plot=row['overview'])
            except:
                url = get_url(action='play', video=row["title"], year=0, latestIndex=3, poster=row['poster_path'], backdrop=row['backdrop_path'], id=row['id'], plot=row['overview'])
            xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
        xbmc.executebuiltin('Container.SetViewMode(51)')
        xbmcplugin.endOfDirectory(HANDLE)
        index = 1
        searchIndex = 1
    else:

        xbmcplugin.setPluginCategory(HANDLE, "search")
        xbmcplugin.setContent(HANDLE, 'movies')

        link = 'https://api.themoviedb.org/3/search/tv?&include_adult=false&language=en-US&page=1&query=' + query.replace(
                " ", "+") + apiKey

        html = urlopen(link).read()
        movieInfo = json.loads(html)
        results = movieInfo["results"]
        for row in results:
            list_item = xbmcgui.ListItem(label=row['name'])
            if row['backdrop_path']:
                list_item.setArt({
                                  'fanart': "https://image.tmdb.org/t/p/original" + row['backdrop_path'],
                                  'banner': "https://image.tmdb.org/t/p/original" + row['backdrop_path']})
            if row['poster_path']:
                list_item.setArt({'poster': "https://image.tmdb.org/t/p/original" + row['poster_path']})
            list_item.setRating("tmdb", row["vote_average"], row["vote_count"], True)
            info_tag = list_item.getVideoInfoTag()
            info_tag.setMediaType('movie')
            info_tag.setUniqueIDs({"tmdb": str(row["id"])}, "tmdb")
            info_tag.setTitle(row['name'])
            genres = []
            for r in row['genre_ids']:
                genres.append(genre[r])
            info_tag.setGenres(genres)
            info_tag.setPlot(row['overview'])
            try:
                info_tag.setYear(int(row['first_air_date'][:4]))
            except:
                pass
            list_item.setProperty('IsPlayable', 'false')
            is_folder = True
            try:
                url = get_url(action='playtv', video=row["name"], year=int(row['first_air_date'][:4]), latestIndex=3, poster=row['poster_path'], backdrop=row['backdrop_path'], id=row['id'], plot=row['overview'], page=1)
            except:
                url = get_url(action='playtv', video=row["name"], year=0, latestIndex=3, poster=row['poster_path'], backdrop=row['backdrop_path'], id=row['id'], plot=row['overview'], page=1)
            xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
        xbmc.executebuiltin('Container.SetViewMode(51)')
        xbmcplugin.endOfDirectory(HANDLE)


def play_tv(path, year, index, page, poster='', backdrop='', id='', plot=''):
    title1 = path
    if "Grey" in path:
        path = path.replace("Grey's","Grey")
    if "Asur" in path:
        path = path.replace("Asur", "Asur: Welcome to Your Dark Side")
    if "Scam" in path:
        path = path.replace("2 -",'2:')
    page -= 1
    nextPage = False
    html = urlopen(
        "http://www.dmasti.pk/search/index/" + str(24*page) + "?keyword=" + path.replace(" ", "+").replace("&",
                                                                                                      "%26")).read().decode(
        "utf8")
    i = re.findall('<a class="name" href="(.*?)" >(.*?)</a>', html)
    years = re.findall('<div class="quality">(.*?)</div>', html)
    season = re.findall('<div class="quality2">(.*?)</div>', html)
    if "http://www.dmasti.pk/search/index/" in html:
        nextPage = True
        pageNext = int(re.findall('<li class="active"><a href="#">(.*?)</a></li><li>', html)[0]) + 1
    shows = []
    for row in range(len(i)):
        try:
            if ('tvshow' in i[row][0]) and ('Episode' in years[row]):
                show = {"link": i[row][0], "title": i[row][1], "episode": years[row], "season": season[row]}
                shows.append(show)
        except:
            pass
    dialog = xbmcgui.Dialog()
    if not i:
        dialog.ok('Not Found', 'Media maybe unreleased or not found on the local server.')
    else:
        if index == 3:
            for row in shows:
                playitem = xbmcgui.ListItem(row['title'] + " " + row['season'] + " " + row['episode'])
                if backdrop:
                    playitem.setArt({
                        'fanart': "https://image.tmdb.org/t/p/original" + backdrop,
                        'banner': "https://image.tmdb.org/t/p/original" + backdrop})
                if poster:
                    playitem.setArt({'poster': "https://image.tmdb.org/t/p/original" + poster})
                info_tag = playitem.getVideoInfoTag()
                info_tag.setMediaType('movie')
                info_tag.setPlot(plot)
                info_tag.setUniqueIDs({"tmdb": str(id)}, "tmdb")
                info_tag.setYear(year)
                info_tag.setTitle(row['title'])
                xbmcplugin.setPluginCategory(HANDLE, "latest")
                xbmcplugin.setContent(HANDLE, 'movies')
                html = urlopen(row["link"]).read().decode('latin-1')
                link = re.findall('<a href="(.*?)" class="vh_button red icon-down', html)[0].replace("N","n").replace(" ","%20")
                xbmcplugin.addDirectoryItem(handle=HANDLE,
                                            url=link,
                                            listitem=playitem)
            if nextPage:
                list_item = xbmcgui.ListItem(label="Next Page")
                list_item.setArt({'icon': movieIcon, 'fanart': movieFanart})
                list_item.setProperty('SpecialSort', 'bottom')
                info_tag = list_item.getVideoInfoTag()
                info_tag.setTitle("Next Page")
                is_folder = True
                url = get_url(action='playtv', video=title1, year=year,
                              latestIndex=index, page=pageNext,
                              poster=poster, backdrop=backdrop, id=id,
                              plot=plot)
                xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
            xbmc.executebuiltin('Container.SetViewMode(55)')
            xbmcplugin.endOfDirectory(HANDLE)
        else:
            for row in shows:
                playitem = xbmcgui.ListItem(row['title'] + " " + row['season'] + " " + row['episode'])
                if backdrop:
                    playitem.setArt({
                        'fanart': "https://image.tmdb.org/t/p/original" + backdrop,
                        'banner': "https://image.tmdb.org/t/p/original" + backdrop})
                if poster:
                    playitem.setArt({'poster': "https://image.tmdb.org/t/p/original" + poster})
                info_tag = playitem.getVideoInfoTag()
                info_tag.setMediaType('movie')
                info_tag.setPlot(plot)
                info_tag.setUniqueIDs({"tmdb": str(id)}, "tmdb")
                info_tag.setYear(year)
                info_tag.setTitle(row['title'])
                xbmcplugin.setPluginCategory(HANDLE, "latest")
                xbmcplugin.setContent(HANDLE, 'movies')
                html = urlopen(row["link"]).read().decode('latin-1')
                link = re.findall('<a href="(.*?)" class="vh_button red icon-down', html)[0].replace("N","n").replace(" ","%20")
                xbmcplugin.addDirectoryItem(handle=HANDLE,
                                            url=link,
                                            listitem=playitem)
            if nextPage:
                list_item = xbmcgui.ListItem(label="Next Page")
                list_item.setArt({'icon': movieIcon, 'fanart': movieFanart})
                list_item.setProperty('SpecialSort', 'bottom')
                info_tag = list_item.getVideoInfoTag()
                info_tag.setTitle("Next Page")
                is_folder = True
                url = get_url(action='playtv', video=title1, year=year,
                              latestIndex=index, page=pageNext,
                              poster=poster, backdrop=backdrop, id=id,
                              plot=plot)
                xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
            xbmc.executebuiltin('Container.SetViewMode(55)')
            xbmcplugin.endOfDirectory(HANDLE)

def play_video(path, year, index, poster='', backdrop='', id='', plot=''):
    title1 = path
    if "Godzilla" in path:
        path = path.replace(".", "")
    if ("Wednesday" in path) or ("Bang Bang" in path):
        path = path.replace("!", "")
    if "bali" in path:
        path = path.replace('ā','aa')
    if "Brahm" in path:
        path = path.replace('ā', 'a')
    if (("Iron Man") in path and (year == 2008)) or (("Spider-Man") in path and (year == 2002)) or (("Twilight" in path) and (year == 2008)):
        path = path + " (Dual Audio)"
    if ("Philosopher's" in path):
        path = path.replace("Philosopher's", "Sorcerer's")
    path = path.replace("·", "-")
    if (len(path) <= 3):
        link = "http://www.dmasti.pk/movies"
        html = urlopen(link + "?c="+path[0]+"&y="+ str(year)).read().decode("utf8")
        i = re.findall('<a class="name" href="(.*?)" >(.*?)</a>', html)
        years = [str(year)] * len(i)
        if index != 2:
            movieType = ["Indian"] * len(i)
        else:
            movieType = [""] * len(i)
        if "http://www.dmasti.pk/movies/index/48" in html:
            html = urlopen(link + "/index/48" + "?c="+path[0]+"&y="+ str(year)).read().decode("utf8")
            for row in re.findall('<a class="name" href="(.*?)" >(.*?)</a>', html):
                i.append(row)
            years = [str(year)] * len(i)
            if index != 2:
                movieType = ["Indian"] * len(i)
            else:
                movieType = [""] * len(i)
    else:
        html = urlopen("http://www.dmasti.pk/search?keyword="+path.replace(" ","+").replace("&","%26")).read().decode("utf8")
        i = re.findall('<a class="name" href="(.*?)" >(.*?)</a>', html)
        years = re.findall('<div class="quality">(.*?)</div>', html)
        movieType = re.findall('<div class="quality2">(.*?)</div>', html)
    dialog = xbmcgui.Dialog()
    path = path.replace(" (Dual Audio)", "")
    if not i:
        dialog.ok('Not Found', 'Media maybe unreleased or not found on the local server.')
    else:
        for row in range(len(i)):
            title = i[row][1]
            if "3D" not in title:
                title = re.sub(r'\([^()]*\)', ' ', title).strip().replace(" - Voleuses", "")
                try:
                    print(title, path)
                    print(years[row], str(year))
                    print((title == path), (years[row] == str(year)))
                    if (index != 2) & (("Indian" in movieType[row]) or ("Dub" in movieType[row])):
                        if (title == path) & (years[row] == str(year)):
                            html = urlopen(i[row][0]).read().decode('latin-1')
                            link = re.findall('<a href="(.*?)" class="vh_button red icon-down', html)[0]
                    elif (index == 2) & ("Indian" not in movieType[row]):
                        if (title == path) & (years[row] == str(year)):
                            html = urlopen(i[row][0]).read().decode('latin-1')
                            link = re.findall('<a href="(.*?)" class="vh_button red icon-down', html)[0]
                    elif (index == 3):
                        if (title == path) & (years[row] == str(year)):

                            html = urlopen(i[row][0]).read().decode('latin-1')
                            link = re.findall('<a href="(.*?)" class="vh_button red icon-down', html)[0]
                except IndexError:
                    pass

    if index == 3:
        xbmcplugin.setPluginCategory(HANDLE, "search")
        xbmcplugin.setContent(HANDLE, 'movies')
        list_item = xbmcgui.ListItem(label=title1)
        list_item.setProperty('IsPlayable', 'true')
        is_folder = False
        url = get_url(action='playLink', link=link)
        if backdrop:
            list_item.setArt({
                'fanart': "https://image.tmdb.org/t/p/original" + backdrop,
                'banner': "https://image.tmdb.org/t/p/original" + backdrop})
        if poster:
            list_item.setArt({'poster': "https://image.tmdb.org/t/p/original" + poster})
        info_tag = list_item.getVideoInfoTag()
        info_tag.setMediaType('movie')
        info_tag.setPlot(plot)
        info_tag.setUniqueIDs({"tmdb": str(id)}, "tmdb")
        info_tag.setYear(year)
        info_tag.setTitle(title1)
        xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
        xbmc.executebuiltin('Container.SetViewMode(502)')
        xbmcplugin.endOfDirectory(HANDLE)

    else:
        play_item = xbmcgui.ListItem(offscreen=True)
        play_item.setPath(link)
        # Pass the item to the Kodi player.
        xbmcplugin.setResolvedUrl(HANDLE, True, listitem=play_item)
        xbmcplugin.endOfDirectory(HANDLE)

def playLink(link):

    play_item = xbmcgui.ListItem(offscreen=True)
    play_item.setPath(link)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(HANDLE, True, listitem=play_item)

query = ""
def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring: URL encoded plugin paramstring
    :type paramstring: str
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if not params:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of video categories
        list_genres()
    elif params['action'] == 'listing':
        # Display the list of videos in a provided category.
        list_options(int(params['genre_index']))
    elif params['action'] == 'play':
        # Play a video from a provided URL.
        try:
            play_video(params['video'], int(params['year']), int(params['latestIndex']), params["poster"], params["backdrop"], params['id'], params['plot'])
        except:
            play_video(params['video'], int(params['year']), int(params['latestIndex']))
    elif params['action'] == 'latest':
        latest(int(params["genre_index"]), int(params["index"]))
    elif params['action'] == 'search':
        search(getusersearch(), int(params["index"]))
    elif params['action'] == 'discover':
        discover(int(params["genre_index"]),int(params["latest_index"]),int(params["discoveryIndex"]), int(params["page"]))
    elif params['action'] == 'playtv':
        try:
            play_tv(params['video'], int(params['year']), int(params['latestIndex']), int(params["page"]), params["poster"], params["backdrop"], params['id'], params['plot'])
        except:
            play_tv(params['video'], int(params['year']), int(params['latestIndex']), int(params["page"]))
    elif params['action'] == 'playLink':
        playLink(params["link"])
    else:
        # If the provided paramstring does not contain a supported action
        # we raise an exception. This helps to catch coding errors,
        # e.g. typos in action names.
        raise ValueError(f'Invalid paramstring: {paramstring}!')


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
