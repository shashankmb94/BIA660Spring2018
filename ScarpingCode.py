#Code For Web Scraping
#Authors: Pratiba Dwivdi, Preeti Negi, Madhura, Shashank Mysore Bhagwan
#We pledge our honor that we have abided by the Stevens Honor System
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 14:37:33 2018

@author: prees
"""

from bs4 import BeautifulSoup
#from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import csv

executable_path = 'C:/Users/prees/Desktop/2nd Term/BIA-660-Web/Project/chromedriver.exe'

driver = webdriver.Chrome(executable_path=executable_path)

# Wait to let webdriver complete the initialization
driver.wait = WebDriverWait(driver, 5)



def getReviews(page_url):
    reviews = []
    try:
        if page_url != None:
            driver.get(page_url)
            review_summary= driver.find_element_by_xpath('//*[@id="review-summary"]/div/div/div[1]/span[3]')
            print(review_summary.text.split()[0].split("(")[1])
            totalReviewsCount=int(review_summary.text.split()[0].split("(")[1])
            print("total reviews: " + str(totalReviewsCount))
            index = 1
            reviewsScraped=0
            scrapePage=1
            while(scrapePage):
                page_url_page = page_url + str(index)
                print (page_url_page)
                driver.get(page_url_page)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                divs = soup.select("div.review-item-feedback")
                if len(divs) == 0:
                    print ("Crap")
                    page_url = None
                else:
                    for idx, div in enumerate(divs):
                        print ("\n")
                        rating = None
                        comment = None
                        review = []
                        rating_tmp = div.select("div.table div.row div.review-item-header.col-md-8.col-sm-8.col-xs-12 div.row div.ratings-stars.col-md-9.col-sm-9 div.c-ratings-reviews.v-medium span.c-reviews span.c-review-average")
                        # get rating
                        if rating_tmp != []:
                           
                            rating = rating_tmp[0].get_text()
                            newrating=rating.replace(u"\xe2\x80\x99","'")
                            print(newrating)

                        comment_tmp = div.select("div.clearfix.comment-wrapper div.review-wrapper.col-sm-9 div.review-content.row p.pre-white-space")
                        # get review
                        if comment_tmp != []:
                            comment = comment_tmp[0].get_text()
                            newcomment=comment.replace(u"\xe2\x80\x99","'")
                            print (newcomment)
                        review = [newrating, newcomment]
                        reviews.append(review)
                        reviewsScraped=reviewsScraped+1
                        #print("total reviews scraped : " + str(reviewsScraped))
                        if reviewsScraped >= totalReviewsCount:
                            scrapePage= 0;
                            break;
                index=index+1
    except Exception as inst:
        print(inst)
    print ("\n\n Stored Reviews in the list:", reviews)
    driver.close()
    return reviews

def save(reviews):
    file_name = "New_2.csv"
    with open(file_name, "w") as f:
        writer = csv.writer(f, dialect = 'excel')
        writer.writerow(['Rating', 'Detailed review of the product'])
        writer.writerows(reviews)
        
    f.close()

if __name__ == "__main__":
    
    # URLs which we want to collect from
    
 
    page_url_arr = ["https://www.bestbuy.com/site/reviews/apple-ipad-latest-model-with-wifi-cellular-32gb-at-t-gold/5618123?page="]
    
    for page_url in page_url_arr:
        reviews = getReviews(page_url)
        save(reviews)
