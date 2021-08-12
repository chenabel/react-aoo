import requests


def texg():
    resule = requests.get('https://apis.map.qq.com/ws/direction/v1/driving/?from=39.915285,116.403857&to=39.915285,116.803857&waypoints=39.111,116.112;39.112,116.113&output=json&callback=cb&key=OB4BZ-D4W3U-B7VVO-4PJWW-6TKDJ-WPB77')
    print(resule.text)
texg()