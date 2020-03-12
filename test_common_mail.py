from mylib.advertisement_image_factory import AdvertisementImageFactory
from pyppeteer import launch
from pyppeteer import launcher
import asyncio
import requests
import os
launcher.AUTOMATION_ARGS.remove("--enable-automation")


async def dialog_control(dialog):
    await dialog.accept()


async def proxy_send_mail(proxies):
    browser = await launch({
        'headless': False,
        'dumpio': True,
        'autoClose': False,
        'args': [
            '--no-sandbox',
            '--window-size=1366,850',
            f'--proxy-server={proxies}'
        ]})
    page = await browser.newPage()
    await page.setViewport({'width': 1366, 'height': 768})
    await page.setJavaScriptEnabled(enabled=True)
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'
    )
    await page.goto('http://icanhazip.com/')
    await asyncio.sleep(2)
    # 登录
    await page.goto('https://mailv.zmail300.cn/webmail/login.php')
    while not await page.querySelector('#inputUser'):
        pass
    await page.type('#inputUser', 'baoan@haihong-china.com')
    await page.type('#inputPassword', 'dj888888')
    while not await page.querySelector('#form_container > div.login > form > div:nth-child(5) > button'):
        pass
    await page.click('#form_container > div.login > form > div:nth-child(5) > button')
    # 邮件
    await asyncio.sleep(2)
    await page.click('#mail\:nav_service > li.title-change.clearfix > div:nth-child(2) > a > span')
    await page.waitForSelector('#mail_compose_send_input_to')
    await page.type('#mail_compose_send_input_to', '914081010@qq.com')
    await page.click('#mail_compose_subject')
    await page.type('#mail_compose_subject', '我爱你没道理')
    await page.waitForSelector('#cke_1_contents > iframe')
    frame = page.frames
    await page.click('#cke_1_contents > iframe')
    await frame[2].waitForSelector('#compose_add_sign')
    await frame[2].type('#compose_add_sign', '我顶你个肺')
    await page.click('#cke_26')
    await asyncio.sleep(1)
    await page.waitForSelector('#cke_Upload_126')
    await page.click('#cke_Upload_126')
    frame = page.frames
    upload_img = await frame[3].querySelector('#cke_121_fileInput_input')
    factory = AdvertisementImageFactory()
    ad_img = factory.get_yin_he_ad()
    await upload_img.uploadFile(ad_img)
    page.on('dialog', dialog_control)
    # 删除广告缓存图片
    os.remove(ad_img)
    await page.click('#cke_124_uiElement')
    await asyncio.sleep(1)
    await page.click('#cke_153_label')
    await page.waitForSelector('#mail_compose_send')
    await page.click('#mail_compose_send')
    await page.waitForSelector('#mail_compose_send_now_1_button')
    await page.click('#mail_compose_send_now_1_button')
    await asyncio.sleep(10)
    print('发送成功！')


def get_proxies(num):
    url = f'http://http.tiqu.alicdns.com/getip3?num={num}&type=1&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&' \
          f'cs=0&lb=1&sb=0&pb=4&mr=1&regions=&gm=4'
    response = requests.get(url=url)
    data = str(response.text).strip().split('\r\n')
    print(len(data))
    return data


tasks = []
for proxy in get_proxies(2):
    tasks.append(asyncio.ensure_future(proxy_send_mail(proxy)))

asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))
