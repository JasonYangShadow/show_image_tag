import requests
import json
import argparse
import logging
import concurrent.futures

url = 'https://registry.hub.docker.com/v2/repositories'
#url_tag = 'https://registry.hub.docker.com/v2/repositories/biocontainers/samtools/tags'

class Base:

    def __init__(self, repo, worker_count):
        self.__repo_url = '%s/%s/' %(url, repo)
        self.__worker_count = worker_count

    def __async_process(self, all_tags = False):
        #worker
        logging.debug('prepare works with count: %d', self.__worker_count)
        with concurrent.futures.ThreadPoolExecutor(max_workers = self.__worker_count) as executor:
            #start looping images info
            resp = requests.get(self.__repo_url)
            if resp.status_code == 200:
                json_content = resp.json()
                if 'count' in json_content:
                    self.__count = json_content['count']
                    logging.debug('found %d images needed to be processed', self.__count)
                while 'results' in json_content and len(json_content['results']) > 0:
                    for item in json_content['results']:
                        item_dict = {}
                        item_dict['namespace'] = item['namespace']
                        item_dict['name'] = item['name']
                        executor.submit(self.__worker, item_dict, all_tags)
                    #loop for next page
                    if json_content['next'] is not None:
                        resp = requests.get(json_content['next'])
                        if resp.status_code == 200:
                            json_content = resp.json()
                        else:
                            raise Exception('send request to %s failed with code %d' % (json_conent['next'], resp.status_code))
                    else:
                        break
            else:
                raise Exception('send request to %s failed with code %d' % (self.__repo_url, resp.status_code))

    def __worker(self, image, all_tags = False):
        logging.debug('working on processing tag info of image: %s', image['name'])
        self.__add_tags(image, all_tags)
        #mark task done
        if all_tags:
            print(image)
        else:
            print('%s/%s:%s' %(image['namespace'], image['name'], image['tags'][0]['name']))

    def __list_images(self):
        resp = requests.get(self.__repo_url)
        if resp.status_code == 200:
            image_list = []
            json_content = resp.json()
            if 'count' in json_content:
                self.__count = json_content['count']

            while 'results' in json_content and len(json_content['results']) > 0:
                for item in json_content['results']:
                    item_dict = {}
                    item_dict['namespace'] = item['namespace']
                    item_dict['name'] = item['name']
                    image_list.append(item_dict)
                if json_content['next'] is not None:
                    resp = requests.get(json_content['next'])
                    if resp.status_code == 200:
                        json_content = resp.json()
                    else:
                        raise Exception('send request to %s failed with code %d' % (json_conent['next'], resp.status_code))
                else:
                    break

            return image_list
        else:
            raise Exception('send request to %s failed with code %d' % (self.__repo_url, resp.status_code))

    def __add_tags(self, image, all_tags = False):
        tag_url = '%s/%s/%s/tags' % (url, image['namespace'], image['name'])
        resp = requests.get(tag_url)
        if resp.status_code == 200:
            image['tags'] = []
            json_content = resp.json()
            if 'count' in json_content:
                image['tag_count'] = json_content['count']

            if all_tags:
                while 'results' in json_content and len(json_content['results']) > 0:
                    for item in json_content['results']:
                        tag_info = {}
                        tag_info['name'] = item['name']
                        tag_info['size'] = item['full_size']
                        tag_info['architecture'] = item['images'][0]['architecture']
                        tag_info['os'] = item['images'][0]['os']
                        tag_info['last_updated'] = item['last_updated']
                        tag_info['digest'] = item['images'][0]['digest']
                        image['tags'].append(tag_info)
                    if json_content['next'] is not None:
                        resp = requests.get(json_content['next'])
                        if resp.status_code == 200:
                            json_content = resp.json()
                        else:
                            raise Exception('send request to %s failed with code %d' % (json_content['next'], resp.status_code))
                    else:
                        break
            else:
                if 'results' in json_content and len(json_content['results']) > 0:
                    results = json_content['results']
                    tag_info = {}
                    tag_info['name'] = results[0]['name']
                    tag_info['size'] = results[0]['full_size']
                    tag_info['architecture'] = results[0]['images'][0]['architecture']
                    tag_info['os'] = results[0]['images'][0]['os']
                    tag_info['last_updated'] = results[0]['last_updated']
                    tag_info['digest'] = item['images'][0]['digest']
                    image['tags'].append(tag_info)

    def run(self, all_tags = False):
        image_list = self.__list_images()
        if len(image_list) > 0:
            for image in image_list:
                self.__add_tags(image, all_tags)
        return image_list

    def thread_run(self, all_tags = False):
        self.__async_process(all_tags)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--repo', help = 'target repository on Dockerhub', required = True)
    parser.add_argument('-a','--all', action = "store_true", default = False, help = 'print all tags of target images')
    parser.add_argument('-t','--thread', action = "store_true", default = False, help = 'use multiple threads to run')
    parser.add_argument('-d','--debug', action = "store_true", default = False, help = 'output debug info')
    args = vars(parser.parse_args())
    if args['debug']:
        logging.basicConfig(level = logging.DEBUG)
    else:
        logging.basicConfig(level = logging.INFO)

    b = Base(args['repo'], 10)
    if args['thread']:
        b.thread_run(args['all'])
    else:
        image_list = b.run(args['all'])
        if args['all']:
            print(image_list)
        else:
            if len(image_list) > 0:
                for image in image_list:
                    print('%s/%s:%s' %(image['namespace'], image['name'], image['tags'][0]['name']))

if __name__ == "__main__":
    main()

