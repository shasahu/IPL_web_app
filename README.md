# IPL_web_app
IPL Data Analysis System is a Web Application which helps usersto analyze the IPL(2008-
2020) data. System contains many analysis done on already pre-processed data. User can create
there account and then login to the application. Admin option is provided to user. Admin user
can check log of any user. Admin can add/remove admin privileges to user and delete user
account. User can also add profile picture. It provide dynamic dashboard for user. The whole
application is user interactive. User can play around with different analysis. The streamlit
server is connected to database to fetch the data and do analysis. It provides different statistical
analysis and data analysis on the data. It visualizes the analysis. It provides flexibility to user
to choose between different analysis and visualize data accordingly.

For the Project, We have downloaded the dataset which contains two csv files from kaggle. Matches.csv
gives the details of match venue, location, Season, contesting team, about toss winner and toss
decision, match result, win got by runs or wickets, player of the match, details of all the three
umpires and match Winner etc. Ball by Ball.csv is the ball by ball data and the combination of
all the deliveries for all the matches from 2008-2020. It consists of different attributes Match
id, bowling team, batting team, batsmen, bowler, Nonstriker, no ball runs, penalty runs, Extra
runs, over, total runs etc. Innings tell if the first team was going on field or second one. Over
describes the current over number. Ball describes the current ball number of the current over.
We need to store this data into the database and read data from the database. Before Storing data
into the database if there is requirement of relevant pre-processing of data, then we pre-process
it and then store in the database. After that we need to create a Dashboard for visualization
part of different analysis. The Dashboard should have a login page setup where user can enter
his/her login details and can see the different visualizations. After login, users will be provided
option to choose between bowlers or batsman to show the above stats. This data is run through
various statistical algorithms, tools and visualization techniques to provide deeper insight and
pave way for recommendations to the player or team.

Application will also show top 4 most frequently access analysis by you. So you can directly access that analysis.

# Technologies Used
## Numpy
NumPy is a Python library used for working with arrays.
It also has functions for working in domain of linear algebra, fourier transform, and
matrices.
## Pandas
Pandas is a Python package providing fast, flexible, and expressive data structures designed to make working with “relational” or “labeled” data both easy andintuitive.
It aims to be the fundamental high-level building block for doing practical, real-world
data analysis in Python.
## Mysql Connector
MySQL Connector enables Python programs to access MySQL databases, using an API
that is compliant with the Python Database.
## SQL Alchemy
SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.
## Streamlit
Streamlit is an open-source python framework for building web apps for Machine Learning and Data Science. We can instantly develop web apps and deploy them easily using
Streamlit.
Streamlit allows you to write an app the same way you write a python code. Streamlit
makes it seamless to work on the interactive loop of coding and viewing results in the
web app.

# Some Examples

<img width="464" alt="Capture1" src="https://github.com/user-attachments/assets/677df2ba-e109-4f1d-b375-63150f7f9b54">


<img width="467" alt="Capture2" src="https://github.com/user-attachments/assets/b01a53ac-1d1a-4c9f-92c0-effab81bcbd3">


<img width="368" alt="Capture3" src="https://github.com/user-attachments/assets/32a1f8c2-02a6-4f8c-922d-a347087380dd">
