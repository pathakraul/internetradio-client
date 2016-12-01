def download(url):
    response=requests.get(url, stream=True)
    with open("stream.pls", "wb") as handle:
        for data in response.iter_content():
            handle.write(data)


def check():
    x = []
    datafile = file('/home/rpathak/Downloads/tunein-station.pls')
    for line in datafile:
        if "File1=" in line:
            x = str(line)
            print x[6:-1]
