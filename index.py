from time import sleep
from requests import get, head
from threading import Thread

lt = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx'
hosts = []


def call_check_link(id, rt, i, type, host):
    thread = Thread(target=check_link, args=(id, rt, i, type, host))
    thread.start()


def check_link(id, rt, i, type, host):
    link = get(f'https://api.dbservices.to/v1.5/?action=process_redirect&rt={rt}').json()['data']['link']

    try:
        code = head(link).status_code
    except:
        # report_link(id, 'Website offline', link, i, type)
        return

    if code > 399 and code < 500:
        if code == 403 and 'mediafire' not in link:
            return
        report_link(id, f'HTTP {code}', link, i, type)
        return

    try:
        content = get(link).text
        for check in ['File not available', 'Your potential download link is INVALID', 'WILLKOMMEN IM UNTERGRUND!', 'This file does not exist', 'File Not Found', 'File not found', 'File was not found', 'This document was not found in the system', 'Ничего не найдено', 'The file you are trying to download is no longer available', 'File has expired', 'File was deleted', 'file does not exist', 'Related Searches', 'Invalid Download Link', 'File has been removed', 'The file was removed by administrator', ' THE FILE YOU WERE LOOKING FOR DOESN\'T EXIST.', 'Can\'t find file. Please check URL.', 'File does not exist', 'The file you are trying to access is no longer available publicly.', 'The file you are looking for does not exist!', 'We\'re having a terrible day', 'Download Error', 'There are no files', 'Invalid SSL certificate', 'THE FILE YOU WERE LOOKING FOR DOESN\'T EXIST', 'Page not found']:
            if check in content and 'dailyuploads.net' not in link:
                if 'userscloud.com' in link and check == 'File not found':
                    continue
                report_link(id, check, link, i, type)
                return
        # Dead Sites
        if any(host in link for host in ['dailyuploads.cc', 'filewinds', 'siri-on', 'mirrorupload', 'uploadhero', 'filedwon', 'easports', 'hugefiles', 'yfile.co', 'filefactory', 'filesquick', 'share-online', 'fiberupload', 'files2upload', 'uploadlw', '24uploading', 'datafilehost', 'filecloud', 'gg.gg', 'letitbit', 'megaload', 'mediafree', 'up09', 'uploadable', 'sinhro', 'nornar', 'limelinx', 'themediastorage', 'dix3', 'minihost', 'ul.to', 'media1fire', 'ifile', 'd-h.st', 'openload', 'bytejunk', 'cyberlocker', 'kingfiles', 'putlocker', 'filepup', 'megashares', 'fastsonic', 'uploadship', 'oboom', 'copy', 'multiupload', 'fileom', 'xunlei', 'filetug', 'dld.to', 'joycloud', 'dfiles.ru', 'lumfile', 'fatfiles', 'fileshack', 'filebox', 'iosandroiddl', 'filemonkey', 'eazyfiles', 'Sendspace', 'Supershare', 'sendspace', 'junocloud', 'FilePup', 'lemuploads', 'hulkload', 'sendit', 'linkbucks', 'filenuke', '180upload', 'fileserve', 'datafile', 'shareflare', 'project-free-upload', 'lazytool', '91rb', 'hipfile', 'queenshare', 'fileflyer', 'filescdn', 'openload', 'fileaddict', 'filepup', 'filedais', 'filescdn', 'chayfile', 'cloudshares', 'filedrivex', 'bitshare', 'uploaded', 'bleencraxx', 'hotfile', 'uploadocean', 'filevice']):
            report_link(id, 'Website down', link, i, type)
            return
        if 'bit.ly' in link:
            report_link(id, 'Link shortener', link, i, type)
            return

        if 'itunes.apple.com' in link:
            report_link(id, 'Itunes Link', link, i, type)
            return
        # print(f'Unknown Status: {link}')

        if host not in hosts:
            hosts.append(host)
            print(link)
    except:
        print('Failed to check status')


def report_link(link, reason, url, i, type):
    reason = reason + ' . AppDB Link Reporter . Contact Quix 3parsa3 (at) gmail.com if this is incorrect'
    print(f"{type} {i}: {reason}: {get(f'https://api.dbservices.to/v1.5/?action=report&type={type}&id={link}&reason={reason}&lt={lt}').text} - {url}")


def call_check_app(app, i, type):
    thread = Thread(target=check_app, args=(app, i, type))
    thread.start()


def check_app(app, i, type):
    trackid = app['trackid']
    link_data = get(f'https://api.dbservices.to/v1.5/?action=get_links&type={type}&trackids={trackid}&lt={lt}').json()
    if link_data['data'] is None:
        return

    for app_id, app in link_data['data'].items():
        final_app = []
        try:
            for ver, links in app.items():
                final_app.append(links)
        except:
            for links in app:
                final_app.append(links)

        for links in final_app:
            for link in links:
                if len(link['reports']) > 0:
                    continue
                # if link['host'] is not None and (link['host'] == 'mega.nz' or 'starfiles' in link['host'] or '.onion' in link['host']):
                if link['host'] is not None and (link['host'] == 'mega.nz' or any(so in link['host'] for so in ['starfiles', '.onion'])):
                    continue

                if link['link'] == '@':
                    continue
                response = get('https://api.dbservices.to/v1.5/?action=process_redirect&t=' + link['link'].replace('ticket://', ''))
                try:
                    call_check_link(link['id'], response.json()['data']['redirection_ticket'], i, type, link['host'])
                except:
                    print('RT failed')
                sleep(1)


for type in ["ios", "cydia", "books", "tvos", "osx", "standalone"]:
    print(f'Type: {type}')
    page = 0
    i = 0
    while True:
        page += 1
        print(f'Page: {page}')
        apps = get(f'https://api.dbservices.to/v1.5/?action=search&type={type}&page={page}&order=clicks_all').json()['data']

        if len(apps) == 0:
            break

        for app in apps:
            i += 1
            call_check_app(app, i, type)
            sleep(1)