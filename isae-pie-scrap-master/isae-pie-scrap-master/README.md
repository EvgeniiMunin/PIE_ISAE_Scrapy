# TechTrends (Scraper module)
Scraper module for the TechTrends project.

TechTrends is a prototype tool for deriving insights on the trends of aerospatial technologies through the exploration of news articles on the web. It manages its extraction and storage and allows for visual exploration of their evolution along time, as well as filtering by tags and companies.


See also the repositories for the whole project:
- [TechTrends (Front-end module)](https://github.com/sergira/tech-trends-fe)
- [TechTrends (Back-end module)](https://github.com/sergira/tech-trends-backend)

## Motivation
This tool was developed for the project *Integrating Data Modelling, Data Management and Data Analysis in a Concurrent Engineering Environment*, proposed by the **CTO of Technology Planning and Roadmapping (XP)** at **Airbus**. It was done in the framework of the *Project Ingénierie et Entrepreneuriat* of the *Diplôme Ingénieur* at the university [ISAE-Supaéro](https://www.isae-supaero.fr/en/), France.

## Current and future functionalities
Due to the work load restriction imposed by the university, the following functionalities were implemented:

1. Automatically scrap news sources and institutional websites to get information related to topics of interest
2. Format and collect the information into a Database
3. Provide a user interface linked to the Database in order to visualize the information

leaving the following planned functionalities left for future work. Some hints at how to tackle them are proposed:

4. Automatic tagging of articles
    - Methods considered were *[Latent Dirichlet Allocation](https://arxiv.org/pdf/1711.04305.pdf)* and *[TextRank](https://web.eecs.umich.edu/%7Emihalcea/papers/mihalcea.emnlp04.pdf)*
    - For the moment, tags are randomly assigned for front-end demonstration purposes.
5. Sentiment analysis
    - [Andrew L. Maas](https://ai.stanford.edu/~amaas/papers/wvSent_acl2011.pdf) proposes a method for polarity and subjectivity analysis using IMDB reviews as labeled data.
6. Exploration of other types of documents
    - Academic articles
    - Patents
    - Social media posts

## Architecture
The project is composed by three interdependant modules, as well as a PostGreSQL database:
- Scraping module
- Back-end module
- Front-end module
![architecture](https://github.com/sergira/isae-pie-scrap/blob/master/readme_images/architecture.png)

### Scraping module
Automatically crawls and extracts content of target websited, formatting it and storing it to the database.

It is based on the [Scrapy project](https://github.com/scrapy/scrapy), an open-source general purpose web crawling framework for automatic web exploration and data extraction. It provides with easily configurable pipelines and allows for database integration.

The files describing the extraction procedure for each target are called *Spiders* and must be tailored to each website:

![scrapy1](https://github.com/sergira/isae-pie-scrap/blob/master/readme_images/scrapy1.png)

For more information, refer to the [Scrapy project documentation website](https://doc.scrapy.org/en/latest/index.html).

### Front-end
Provides with a responsive chart displaying the monthly aggregation of news article entries, allowing for time interval selection, filtering by company and tag and reactive to mouse interaction.

It has been developed on the `Angular` web framework, along with the plotting library `chart.js`.

![frontend](https://github.com/sergira/isae-pie-scrap/blob/master/readme_images/frontend.png)

### Back-end
Provides with an API that allows for queries to the database, as well as filtering by URL keyword arguments. Based on the `Django` web python framework with `Django-Rest-Framework` on top. 

The filtering functionality is heavily inspired on [Clinton Dreisbach's *Call for service*](https://github.com/cndreisbach/call-for-service) web app. CFS Analytics is copyright 2016 RTI International and is licensed under the GNU Public License 3.0.

## Back-end deployment on virtual machine
Once the virtual machine is created, run from the `SSH` shell:

```bash
sudo apt-get update
sudo apt-get install -y git nginx
```

Set Nginx up by replacing **manually** the `Ngix` conf file at `/etc/nginx/sites-enabled/default` with the following text:

```text
server { 
    listen 80; 
    server_name pie71_vm; 

    location / { 
        proxy_set_header   X-Forwarded-For $remote_addr;
        proxy_set_header   Host $http_host;
        proxy_pass         http://127.0.0.1:4200;
    }
}
```

Reload Nginx:
```
sudo nginx -s reload
```

Clone the project repository:

```
cd && git clone <REPO URL>
cd ./tech-trends-backend
```

Install python dependencies:
```
sudo apt-get install python3-pip -y
pip3 install -r requirements.txt
```

Make sure that the */tech_trends_backend/settings/__init__.py* file refers to the virtual machine configuration file (*vm.py*) and configure the `DATABASE` variable accordingly to your production schema (database IP, user, password, etc.).

Launch the server:
```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserve
```

# Contributors

* **[Sergi Rocamora](https://github.com/sergira)** - product owner, web architect and full stack developer
* **[Marco Scarpetta](https://github.com/marcoscarp)** - project manager and web scraper developer
* **Manfredo Martinino** - web scraper developer
* **[Evgenii Munin](https://github.com/EvgeniiMunin)** - web scraper developer
* **[Jun (Octave) Yao](https://github.com/octaveyao)** - web scraper developer
* **Marc Tortosa** - web scraper developer

# License 
GNU General Public License v3.0. See [LICENSE](https://github.com/sergira/isae-pie-scrap/blob/master/LICENSE.md) for the full text of the license.