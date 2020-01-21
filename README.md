Docker Hub hosts many Docker Images, but sometimes it is a bit of hard to list all images under a specific org along with their associated tags.

**This tool works for this.**

1. Install Python3.7+, Python3-pip

2. pip3 install -r requirements.txt

3. python main.py -r target_org  -> list all images with their latest tag

4. python main.py -r target_org --all -> list all images with their all tags and info

   
   
   ### Single Process processing:
   
   1. show all images with latest tag
   
   ```
   python main.py -r jasonyangshadow
   
   output:
   jasonyangshadow/ubuntu:latest  
   jasonyangshadow/cuda:ont  
   jasonyangshadow/porg:latest  
   jasonyangshadow/buildenv:0.3  
   jasonyangshadow/pyinstaller:v0.1  
   ```

   2. show all images with all tags  

   ```
    python main.py -r jasonyangshadow --all
   
   output:
   [{'namespace': 'jasonyangshadow', 'name': 'ubuntu', 'tags': [{'name': 'latest', 'size': 67201057, 'architecture': 'amd64', 'os': 'linux', 'last_updated': '2018-10-03T06:49:37.882614Z'}, {'name': 'java8', 'size': 175430362, 'architecture': 'amd64', 'os': 'linux', 'last_updated': '2019-07-22T07:28:52.086866Z'}, {'name': '16.04', 'size': 113737821, 'architecture': 'amd64', 'os': 'linux', 'last_updated': '2019-06-28T02:51:37.214321Z'}, {'name': 'test', 'size': 67221472, 'architecture': 'amd64', 'os': 'linux', 'last_updated': '2018-12-03T11:14:15.911344Z'}, {'name': '3', 'size': 73370947, 'architecture': 'amd64', 'os': 'linux', 'last_updated': '2018-05-20T12:51:08.937708Z'}], 'tag_count': 5}, {'namespace': 'jasonyangshadow', 'name': 'cuda', 'tags': [{'name': 'ont', 'size': 3129562143, 'architecture': 'amd64', 'os': 'linux', 'last_updated': '2019-04-18T17:47:58.470328Z'}], 'tag_count': 1}, {'namespace': 'jasonyangshadow', 'name': 'porg', 'tags': [{'name': 'latest', 'size': 219412169, 'architecture': 'amd64', 'os': 'linux', 'last_updated': '2017-11-02T07:16:09.055225Z'}, {'name': '2', 'size': 219412169, 'architecture': 'amd64', 'os': 'linux', 'last_updated': '2017-11-02T07:16:06.894337Z'}, {'name': '1', 'size': 126628782, 'architecture': 'amd64',
      'os': 'linux', 'last_updated': '2017-11-02T07:15:30.508031Z'}], 'tag_count': 3}, {'namespace': 'jasonyangshadow', 'name': 'buildenv', 'tags': [{'name': '0.3', 'size': 434095562, 'architecture': 'amd64', 'os': 'linux', 'last_updated': '2019-08-16T07:57:53.278465Z'}, {'name': '0.2', 'size': 342127169, 'architecture': 'amd64', 'os': 'linux', 'last_updated': '2019-08-14T01:35:45.318789Z'}, {'name': '0.1', 'size': 232316216, 'architecture': 'amd64', 'os': 'linux', 'last_updated': '2019-08-09T08:47:56.468761Z'}], 'tag_count': 3}, {'namespace': 'jasonyangshadow', 'name': 'pyinstaller', 'tags': [{'name': 'v0.1', 'size': 215196108, 'architecture': 'amd64', 'os': 'linux', 'last_updated': '2019-08-16T07:53:11.237751Z'}], 'tag_count': 1}]
   
   ```
   
   ### Multiple Threads Processing
   
   1. show images with latest tag:
   
      ```
      python main.py -r jasonyangshadow --thread
      
      output:
      jasonyangshadow/ubuntu:latest
      jasonyangshadow/pyinstaller:v0.1
      jasonyangshadow/buildenv:0.3
      jasonyangshadow/cuda:ont
      jasonyangshadow/porg:latest
      ```

   2. show images with all tags:

   ```
   python main.py -r jasonyangshadow --thread --all
   
   output:
   {'namespace': 'jasonyangshadow', 'name': 'cuda', 'tags': [{'name': 'ont', 'size': 3129562143, 'architecture': 'amd64', 'os': 'linux', 'last_updated': '2019-04-18T17:47:58.470328Z'}], 'tag_count': 1}
   {'namespace': 'jasonyangshadow', 'name': 'ubuntu', 'tags': [{'name': 'latest', 'size': 67201057, 'architecture': 'amd64', 'os': 'linux', 'last_updated': '2018-10-03T06:49:37.882614Z'}, {'name': 'java8', 'size': 175430362, 'architecture': 'amd64', 'os': 'linux', 'last_updated': '2019-07-22T07:28:52.086866Z'}, {'name': '16.04', 'size': 113737821, 'architecture': 'amd64', 'os': 'linux', 'last_updated': '2019-06-28T02:51:37.214321Z'}, {'name': 'test', 'size': 67221472, 'architecture': 'amd64', 'os': 'linux', 'last_updated': '2018-12-03T11:14:15.911344Z'}, {'name': '3', 'size': 73370947, 'architecture': 'amd64', 'os': 'linux', 'last_updated': '2018-05-20T12:51:08.937708Z'}], 'tag_count': 5}
   {'namespace': 'jasonyangshadow', 'name': 'pyinstaller', 'tags': [{'name': 'v0.1', 'size': 215196108, 'architecture': 'amd64', 'os': 'linux', 'last_updated': '2019-08-16T07:53:11.237751Z'}], 'tag_count': 1}
   {'namespace': 'jasonyangshadow', 'name': 'porg', 'tags': [{'name': 'latest', 'size': 219412169, 'architecture': 'amd64', 'os': 'linux', 'last_updated': '2017-11-02T07:16:09.055225Z'}, {'name': '2', 'size': 219412169, 'architecture': 'amd64', 'os': 'linux', 'last_updated': '2017-11-02T07:16:06.894337Z'}, {'name': '1', 'size': 126628782, 'architecture': 'amd64', 'os': 'linux', 'last_updated': '2017-11-02T07:15:30.508031Z'}], 'tag_count': 3}
   {'namespace': 'jasonyangshadow', 'name': 'buildenv', 'tags': [{'name': '0.3', 'size': 434095562, 'architecture': 'amd64', 'os': 'linux', 'last_updated': '2019-08-16T07:57:53.278465Z'}, {'name': '0.2', 'size': 342127169, 'architecture': 'amd64', 'os': 'linux', 'last_updated': '2019-08-14T01:35:45.318789Z'}, {'name': '0.1', 'size': 232316216, 'architecture': 'amd64', 'os': 'linux', 'last_updated': '2019-08-09T08:47:56.468761Z'}], 'tag_count': 3}
   ```

   
