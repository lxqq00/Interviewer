import pickle
import random
import re
import threading
import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import yaml

out_file_name = '牛客网校招.md'

try:
    with open('data.pickle', 'rb') as f:
        yaml_data = pickle.load(f)
        if yaml_data is None:
            yaml_data = []
        print('读取到已经保存的页面数据')

        data_map = {}
        for data in yaml_data:
            url = str(data['url'])
            url = re.sub(r'\?sourceSSR=\S+$', '', url)
            data_map[url] = data
        yaml_data.clear()
        with open(out_file_name, 'w+',encoding="utf8") as f:
            for k, v in data_map.items():
                yaml_data.append(v)
                print("---"*30, file=f, flush=True)
                print(str(v).replace("\\n", "\n"), file=f, flush=True)
                print("---"*30, file=f, flush=True)
except Exception as e:
    yaml_data = []


chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")
driver = webdriver.Chrome(chrome_options=chrome_options)
# driver.implicitly_wait(30)


# 1. 获取浏览器的全部标签页
def get_all_handles():
    windows = driver.window_handles
    return windows

# 2. 获取当前标签页


def get_current_handle():
    return driver.current_window_handle

# 3. 切换标签页


def switch_to_window(handle):
    driver.switch_to.window(handle)


# 4. 关闭标签页
lock = threading.Lock()


def close_window():
    with lock:
        # 关闭指定标签页
        driver.close()
        all_handles = get_all_handles()
        h = random.sample(all_handles, 1)
        switch_to_window(h[0])

# 关闭全部标签页


def close_all_windows():
    handles = get_all_handles()
    for handle in handles:
        close_window(handle)

# 5. 打开新的标签页


def open_new_window(url):
    js = 'window.open("%s");' % url
    driver.execute_script(js)

# 6. 切换到新的标签页


def switch_to_new_window():
    handles = get_all_handles()
    for handle in handles:
        if handle != get_current_handle():
            switch_to_window(handle)
            break

# 7. 切换到上一个标签页


def switch_to_previous_window():
    handles = get_all_handles()
    for i in range(len(handles)):
        if handles[i] == get_current_handle():
            if i == 0:
                switch_to_window(handles[len(handles) - 1])
            else:
                switch_to_window(handles[i - 1])
            break


is_close = False


def input_cmd_loop():
    # with open('data.yaml', 'w') as f:
    # yaml_data = yaml.load(f, Loader=yaml.FullLoader)
    last_page = None
    # 在一个死循环中，读取等待键盘输入字符
    while True:
        cmd = input("""请输入控制命令字符，并回车确认：
            "c"（close）关闭应用、
            "q"（quit）关闭当前页面、
            "j"（jump）跳过当前页面、
            "s"（save）将页面的内容保存、
            "u"（unsave）将最后一个保存的页面取消保存、
            "n"(new)将最后一个取消保存的页面并根据url重新在浏览器中访问:\n""")
        if cmd == 'q':
            # 关闭浏览器的当前页面，并顺延切换到下一个页面
            close_window()
        elif cmd == 's':
            # switch_current_handle()
            h = get_current_handle()
            driver.switch_to.window(h)
            current_url = driver.current_url
            current_url = re.sub(r'\?sourceSSR=\S+$', '', current_url)
            try:
                # 记录当前页面的主体内容
                current_text = driver.find_element(
                    # By.XPATH, "//div[@class='tw-flex']/../../section"
                    By.XPATH, "//section[@class='post-content-box tw-relative']"
                ).text
            except Exception as e:
                current_text = driver.find_element(
                    By.XPATH, "//div[@class='tw-flex']/../../section"
                ).text
            # 记录当前页面的url和主体内容
            yaml_data.append({'url': current_url, 'text': current_text})
            # # 将记录的数据序列化到文件中
            # yaml.dump(yaml_data, f)
            # 通过pickle保存yaml_data
            with open('data.pickle', 'wb') as f:
                pickle.dump(yaml_data, f, True)
        elif cmd == 'u':
            # 取消保存最后一个保存的页面
            last_page = yaml_data.pop()
            # # 将记录的数据序列化到文件中
            # yaml.dump(yaml_data, f)
            # 通过pickle保存yaml_data
            with open('data.pickle', 'wb') as f:
                pickle.dump(yaml_data, f, True)
        elif cmd == 'n':
            # 将最后一个取消保存的页面(输入u时会取消保存一个页面)并根据url重新创建一个新标签页在浏览器中访问
            # 获取最后一个取消保存的页面的url
            if last_page is not None:
                last_url = last_page['url']
            else:
                print('没有取消保存的页面')
                continue
            # 创建新标签页
            open_new_window(last_url)
        elif cmd == 'c':
            # 关闭应用
            global is_close
            is_close = True
            return
        elif cmd == 'j':
            # 跳过当前页面，切到下一个页面
            switch_to_previous_window()


def main():

    # 数据结构为
    """
        -   url: http://xxx.xxx.xxx
            text: 正文内容
    """
    # 1. 打开浏览器
    # 已经在浏览器中打开了需要的页面，所以这里不需要再打开浏览器了
    # driver.get('https://www.baidu.com')
    # driver.maximize_window()

    # 记录前一个页面的url
    last_window_handle = None
    # 切换到当前页面
    driver.switch_to.window(get_current_handle())

    # 每隔0.1秒，就检查当前页面是不是发送了变化，如果是，且新页面的url是否是已经被记录的url，就自动的关闭了当前页面，顺延的切换到下一个浏览器标签页中
    while True:
        # 等待0.1秒
        time.sleep(0.1)

        lock.acquire()
        # # 获取当前页面
        current_window_handle = get_current_handle()

        # 如果当前页面记录的上一个页面不一样，就记录当前页面的url和主体内容
        if current_window_handle != last_window_handle:

            # 记录当前页面的url
            last_window_handle = current_window_handle

            current_url = driver.current_url
            for data in yaml_data:
                # 对比当前页面的url是否是已经被记录的url，如果是已经被记录的url，就关闭当前页面，顺延的切换到下一个浏览器标签页中
                if data["url"] == current_url:
                    print(f'当前页面已经有记录，关闭当前页面：{current_url}')

                    # 如果浏览器只有一个打开的标签页就不做任何操作，否则就关闭当前的标签页
                    if len(get_all_handles()) != 1:
                        lock.release()
                        # 关闭当前的页面
                        close_window()
                        lock.acquire()
                    break
        lock.release()
        if is_close == True:
            # # 关闭浏览器
            # driver.quit()
            return


# urls = [
# "https://www.nowcoder.com/discuss/480904008291328000",
# "https://www.nowcoder.com/discuss/479050135792562176",
# ]
# # 如果有很多已知的面试经验页面url，可以在这里添加
# for url in urls:
#     open_new_window(url)


if __name__ == '__main__':
    # 启动多个线程
    t1 = threading.Thread(target=main)
    t1.start()
    # 启动输入命令的线程
    t2 = threading.Thread(target=input_cmd_loop)
    t2.start()

    # 等待t1线程结束
    t1.join()
    # 等待t2线程结束
    t2.join()
