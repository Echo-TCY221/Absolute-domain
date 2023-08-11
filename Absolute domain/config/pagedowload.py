"""
图片下载程序
receive type : -> list
"""
import requests
import os
import time


class DownloadImage:
    @staticmethod
    def count_files(folder_path):
        count = len(os.listdir(folder_path))
        return count

    @staticmethod
    def download_images(image_urls, save_dir):
        count = 0
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        else:
            count = DownloadImage.count_files(save_dir)
            print(f"目标文件夹已存在，有{count}个文件。开始从第{count + 1}个文件后添加...")
        try:
            for i, image_url in enumerate(image_urls, start=count):
                response = requests.get(image_url)
                file_ext = os.path.splitext(image_url)[-1]
                file_path = os.path.join(save_dir, f"image_{i}{file_ext}")
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                    print(f"下载完成第{i}个文件")
                    time.sleep(1)
        except Exception as e:
            print(f"下载失败: {e}")

    @staticmethod
    def run(image_urls, save_dir):
        DownloadImage.download_images(image_urls, save_dir)
        print('图片下载完成！')
