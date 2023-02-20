import requests
import time
import threading

lt = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx'


def call_check_link(id, rt, i, type):
    download_thread = threading.Thread(target=check_link, args=(id, rt, i, type))
    download_thread.start()


def check_link(id, rt, i, type):
    time.sleep(10)
    link = requests.get(f'https://api.dbservices.to/v1.5/?action=process_redirect&rt={rt}').json()['data']['link']

    try:
        code = requests.head(link).status_code
    except:
        report_link(id, 'Website offline', link, i, type)
        return

    if code > 399:
        report_link(id, 'HTTP ' + str(code), link, i, type)
        return

    try:
        content = requests.get(link).text
        if 'WILLKOMMEN IM UNTERGRUND!' in content or 'File Not Found' in content:
            report_link(id, 'File not found', link, i, type)
        elif 'The file you are trying to download is no longer available' in content:
            report_link(id, 'File no longer available', link, i, type)
        elif 'File has expired' in content:
            report_link(id, 'File has expired', link, i, type)
        else:
            if 'bayfiles.com' in link or 'github.com' in link or 'unc0ver.dev' in link or 'userscloud.com' in link:
                return
            print('Unknown Status: ' + link)
    except:
        print('Failed to check status')


def report_link(link, reason, url, i, type):
    print(type + ' ' + str(i) + ': ' + reason + ': ' + requests.get(f'https://api.dbservices.to/v1.5/?action=report&type={type}&id={link}&reason={reason}&lt={lt}').text + ' - ' + url)


def call_check_app(app, i, type):
    download_thread = threading.Thread(target=check_app, args=(app, i, type))
    download_thread.start()


def check_app(app, i, type):
    trackid = app['trackid']
    print('Name: ' + app['name'])
    link_data = requests.get(f'https://api.dbservices.to/v1.5/?action=get_links&type={type}&trackids={trackid}').json()

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
                if link['host'] is not None and (link['host'] == 'mega.nz' or 'starfiles' in link['host'] or '.onion' in link['host']):
                    continue

                try:
                    response = requests.get('https://api.dbservices.to/v1.5/?action=process_redirect&t=' + link['link'].replace('ticket://', ''))
                    call_check_link(link['id'], response.json()['data']['redirection_ticket'], i, type)
                except:
                    print('Request Failed')


for type in ["books", "osx", "standalone", "cydia", "ios", "tvos"]:
    print(f'Type: {type}')
    page = 0
    i = 0
    while True:
        page += 1
        print(f'Page: {page}')
        apps = requests.get(f'https://api.dbservices.to/v1.5/?action=search&type={type}&page={page}&order=clicks_all').json()['data']

        if len(apps) == 0:
            break

        for app in apps:
            i += 1
            call_check_app(app, i, type)
            time.sleep(1)
