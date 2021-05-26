"""
 This program help to search jobs from seek.com website.

 It query the jobs by given job type and location. And visit each page of search result and find
 the jobs with at least one given keyword in their job description. The number of jobs in the result is
 limited by user preference.

 Initially, it get search query parameters from the user:
            Job Type - type of the job you seek,
            Where - location you prefer to work,
            Keywords - required words in the job description,
            Results Limit - number of jobs want to see in the search result

  The results will be shown as list of key-value pairs ([keywords], link to the job) and sorted in ascending order
 based on keyword. Each key-value pair represent the matching keywords and job link

"""

__author__ = "Chaluka Salgado"
__copyright__ = "Copyright 2021 @ Kamikaze"
__email__ = "chaluka.salgado@gmail.com"
__date__ = "18-Apr-2021"
__updated__ = "25-Apr-2021"
__version__ = "2.0"

import requests
from bs4 import BeautifulSoup
import string
from Struct.Trie import PrefixTrie


class SeekJobSearch:
    DOMAIN_URL = "https://www.seek.com.au"
    SEARCH_PAGE_LIMIT = 15

    def __init__(self):
        self.url = None
        self.filtered_jobs = []
        self.results_limit = 0
        self.limit_flag = True
        self.job_type = None
        self.where = None
        self.page = 1
        self.keywords = []

    def __set_url(self):
        """
            sets the search  URL (i.e., (self.url)) with respect to the search page
            E.g. https://www.seek.com.au/software-engineer-jobs/in-melbourne?page=2
        """

        if self.page == 1:
            self.url = self.DOMAIN_URL + "/" + self.job_type + "-jobs/in-" + self.where
        else:
            self.url = self.DOMAIN_URL + "/" + self.job_type + "-jobs/in-" + self.where + "?page=" + str(self.page)
        self.page += 1

    def __str__(self):
        return self.job_type.upper() + " jobs in " + self.where.upper() + " with at least one of the keywords : " \
               + str(self.keywords) + " in the job description."

    def __print_menu(self):
        print("=" * 100)
        print(" " * 30 + "Welcome to Job Finder on SEEK.com")
        print(" " * 25 + "Enter the following information correctly")
        print("=" * 100)

    def __print_results(self):
        print("=" * 100)
        print(self)
        print("{} Jobs Found".format(len(self.filtered_jobs)))
        print("=" * 100)
        for job in self.filtered_jobs:
            print(job)
        print("=" * 100)

    def __get_query_parameters(self):
        """
            get search query parameters from the user
            job_type - type of the job,
            where - location of the job,
            keywords - relative keywords,
            results_limit - number of search results
        """

        self.__print_menu()
        default = True if input("Proceed with default values(Y/N) : ").lower() == 'y' else False
        if not default:
            job_type = input("Job Type : ")
            where = input("Where : ")
            keywords = input("Keywords (separated by comma) : ")
            while True:
                try:
                    self.results_limit = int(input("Results Limit (# of jobs in the result) : "))
                    break
                except ValueError:
                    print("Limit must be a number..!! ")
            print("----- Successful ----")
        else:
            job_type = "software engineer"
            where = "melbourne"
            keywords = "python, c"
            self.results_limit = 10

        return job_type, where, keywords

    def __set_attributes(self):
        """
            Clear and set all the instance variables
        """
        job_type, where, keywords = self.__get_query_parameters()
        self.job_type = "-".join(job_type.split())
        self.where = "-".join(where.split())
        self.keywords = [keyword.strip() for keyword in keywords.split(",")]
        self.keywords.sort()

    def __get_html_parser(self, url: str):
        """
            Return the html parser object for a given URL
        """
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup

    def __get_job_links(self):
        """
            This collects the matching jobs by visiting the pages of the seek.com website.
        """
        self.__set_url()
        soup = self.__get_html_parser(self.url)
        print("-- Searching on : ", self.url)
        jobs = soup.find_all('a', {'data-automation': 'jobTitle'})

        for job in jobs:
            job_link = job['href']
            job_url = self.DOMAIN_URL + job_link

            matching_skills = self.__filter_jobs(job_url)
            if matching_skills:
                self.filtered_jobs.append((matching_skills, job.text, job_url))

            if self.results_limit <= len(self.filtered_jobs):
                self.limit_flag = False
                break

    def __replace_all(str_line: str):
        for char in string.punctuation:
            str_line = str_line.replace(char, " ")

        return str_line

    def __filter_jobs(self, job_url: str):
        """
            This filters the jobs by the given keywords. The jobs with given keywords in their job description is
            returned.
        """
        soup = self.__get_html_parser(job_url)
        results = soup.find('div', {'data-automation': 'jobAdDetails'})  # {'class': 'FYwKg WaMPc_4'})
        listed_items = results.find_all('li')
        job_description = PrefixTrie()

        for item in listed_items:
            line = SeekJobSearch.__replace_all(item.text)
            for ext_str in line.split():
                try:
                    if ext_str:
                        job_description.insert_word(ext_str.lower())
                except IndexError:
                    # handle inserting non-alphabetical words
                    pass

        matching_skills = []
        for keyword in self.keywords:
            if job_description.prefix_search(keyword.lower()):
                matching_skills.append(keyword)

        return matching_skills

    def find_jobs(self):
        """
            Search and print the matching jobs on seek.com
        """
        while True:
            self.__set_attributes()
            page_searches = 0
            continue_flag = True
            while self.limit_flag:
                self.__get_job_links()
                page_searches += 1
                if page_searches > self.SEARCH_PAGE_LIMIT:
                    break

            self.filtered_jobs.sort(key=lambda x: x[0])

            self.__print_results()

            if input("End the search and exit(Y/N) : ").lower() == 'y':
                return True


if __name__ == "__main__":
    w = SeekJobSearch()
    w.find_jobs()
