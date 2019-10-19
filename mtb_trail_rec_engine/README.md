# MTB Trail Recommendation Engine

## Problem & Value Statement

One of the big issues when travelling with your mountain bike is determining what trails to ride. It is decidedly a first world problem, but the consequences of choosing wrong can be problematic. Say you fly to your destination, pack your bike, pay for baggage, rent a car you can throw your bike into, and finally get to the trailhead that was selected after hours and hours of scouring reviews and suggested rides in the area. You kick off only to discover the trails are too hard/easy/boring/short/long/hot/cold/etc. After finishing your disappointing ride with a local beer and lamenting about all the money that you wasted to get here, you decide that there has to be a better way.

## Modeling Plan & Deliverable

The data will be scraped from trailforks.com’s U.S. mountain bike trail database. Since the data will be scraped there will be a significant amount of cleaning involved. Not every trail page has the same information on it so there will likely be some imputation needed as well. Another potential source of error are broken links. In order to capture the number of trails that were not scraped, I will need to build an error log into the scraper so that those links can be revisited at a later time.

I want to build a trail recommender system that will take basic trail statistics, descriptions, and ratings to match the rider to 5-10 new trails they haven’t ridden. These will be region specific so that the rider can input the state where they are and instantly get matched with a list of trails to explore. In order to accomplish this I will build a recommendation engine using collaborative filtering and content based models and compare the two to determine the best recommendation model.

The end result of the model would provide the user with a list of new trails in any state they want to visit. When they ride and rate new trails, the model can be updated with the new information and provide better recommendations over time. I would want to put these recommendations in two places on the site, a dedicated ride recommendation page and on the user's home page. That way there is an easy way for the user to see new trail options and a place that is dedicated to discover new and recommended trails anywhere in the U.S.. The dedicated recommendation page could be used as a quick look trip planning tool for mountain bike vacations.

## Project Goals

Scrape trail data and ratings from trailforks.com U.S. trail region
	Evaluate error log of broken trail links

Data loading and preprocessing 
  	Breaking out location into separate columns
  	Fill na values were needed and check for duplicates
  	Cleaning of text columns
EDA - build a picture of how trails are distributed across the country and what trail stats matter for their rating and total ride count
Feature Engineering - create additional features to better characterize the trails in the dataset
Modeling
  	Build and evaluate collaborative filtering and content based models
  	Evaluate recommendations and choose model type for production
  	Summarize future work and usability of the model in production

## Potential Problems

Since access to user data is denied from the trailforks robots file, the volume of user data to test predictions with will be limited. There is a work around where I will scrape usernames from comments and rating votes for each trail in the U.S. That dataset will be inherently biased because it won’t include the users that do not rate or comment on trails. Since I intend this modeling endeavour to be representative of an MVP and not an EVP, this should be enough to build.


The thought here is that in a full production environment you would have access to each users ride logs and full spectrum of activity on the site, which would enrich the model. In my implementation, the scraped user data will be a proof of concept to show the potential functionality of this type of recommendation engine.
