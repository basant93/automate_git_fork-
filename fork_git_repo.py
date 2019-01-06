from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import subprocess
import os

def check_response(resp):

    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            )


def get_content(url):

    try:
        with closing(get(url, stream=True)) as resp:
            if check_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        print("Bad url/content error")
        return None



def main():
    #url = "hck.re/crowdstrike"
    url = 'https://s3-ap-southeast-1.amazonaws.com/he-public-data/crowdstriked6215ff.html'
    web_page_content = get_content(url)
    with open("web_page.html", "wb") as f:
        #f.write(web_page_content)
        html = BeautifulSoup(web_page_content, 'html.parser')

        repo_branch_list  = []
        for td in html.select('td'):
            repo_branch_list.append(td.text)
        
        print(repo_branch_list)
        for repo_index in range(0, len(repo_branch_list), 3):

            new_branch_name = repo_branch_list[repo_index + 2] 
            change_directory  = "cd crowdstrikeDir"+ str(repo_index)
            #subprocess.call(["git", "pull"])
            #os.system("git clone -b " + repo_branch_list[repo_index + 2] +" "+ repo_branch_list[repo_index + 1])
            #os.system("git clone --single-branch -b " + repo_branch_list[repo_index + 2] +" "+ repo_branch_list[repo_index + 1])
            os.system("mkdir crowdstrikeDir"+ str(repo_index))
            os.system(change_directory)
            os.system(change_directory +" && git init")
            os.system(change_directory +" && git remote add origin " + repo_branch_list[repo_index + 1])

            os.system(change_directory +" && git clone " + repo_branch_list[repo_index + 1])
            os.system(change_directory +" && git fetch && git checkout master")
            os.system(change_directory +" && git checkout -b " + new_branch_name)

            url = 'https://s3-ap-southeast-1.amazonaws.com/he-public-data/index837f27d.js'
            web_page_content = get_content(url)
            print(web_page_content)
            with open("add_web_page.html", "wb") as f:
                f.write(web_page_content)
            os.system(change_directory +" && git add . " )
            os.system(change_directory +" && git commit -m  \" Adding a web page content for the task \"  " )

            os.system(change_directory +" && git push origin  "+ new_branch_name )
                #html = BeautifulSoup(web_page_content, 'html.parser')

            # os.system("git fetch  "   + repo_branch_list[repo_index + 1])

            # os.system("git checkout " + repo_branch_list[repo_index + 2])

            # os.system("git checkout -b " + new_branch_name)

            # os.system("git checkout " + new_branch_name)
            os.system("cd ..")

            print("hello script")

            #os.system("sudo ")




            print(repo_branch_list[repo_index + 1])
            print(repo_branch_list[repo_index + 2])



        #print(html)

    #raw_html = open('web_page.html').read()
    




if __name__ == '__main__':
    main()
