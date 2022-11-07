# StartCode 2022: predict football matches
This application was created as a submission for a case presented by Sportradar on StartCode 2022. 
This application tries to predict what the end score of a football match is by using random forest regression. The project 
was created within 48 hours.  The app was created with Vue.js as frontend with an API created with FastAPI. The library sklearn
was used for creating the ai.

This project was created by: Arunan Gnanasekaran arunang2212@gmail.com, Trym
Gudvangen trym.gudvangen@gmail.com and Victor Sebastian Immanuel Kremmers Bugge
vkbugge@hotmail.com, as a solution for sportradars case presented on StartCode
2022.


## How to install and run application

In order to run the application, clone the project from the main branch. The cloned project will contain both a backend package and a frontend package.

The frontend package has a readme for how to install the components of the Vue framework and how to launch the GUI.

The backend contains a readme for a guide on how to install and run it.

When actually running the application, both the backend's local server and the frontend's GUI have to be launched. Therefore, the two packages need to be open in separate windows. 

Once the FastAPI server is up, add /reset to the URL, which will start the frontend. The frontend can also be started by pressing the restart button.

## Choice of Machine Learning Model

When choosing the machine learning model, the group broke down the requirements of the case: Predict final score based on data received during game.
From there, we noted the different factors that have to be taken into consideration:
 - We wanted the **score** to be a continuous variable
 - The **input data** is a mix of discrete and continuous variables
 - We had relatively **low training and testing data**
 - The data had **low variation**

Since we wanted a continuous variable as output, a regression was optimal. Furthermore, with the constraints the data placed, the model has to be quite flexible.

With all of this taken into consideration, a form for decision tree seemed wise. While researching options for the model, the random forest regression stood out due to its many advantages:

  - It can perform a **non-linear regression** (in case the input variables do not have a linear relationship with the output)
  - The model is **efficient on larger datasets** (flexible for the future)
  - It is **adaptable to outliers**

We also considered the disadvantages:

  - The model cannot predict values outside of the training set; it **cannot extrapolate**.
  - It can sometimes be hard to understand the results.

## Testing of Model

In order to test the model, we ran through different iterations where the importance the different features had on the result were calculated. Additionally,
we ran a very basic statistical analysis of the efficacy of the model to predict the outcome.

### 20% of the data used for Training

<img width="472" alt="Screen Shot 2022-11-02 at 3 42 34 PM" src="https://user-images.githubusercontent.com/59805439/199519643-d1c20ab1-9291-4877-90ae-330be716d014.png">

### 80% of the data used for Training
<img width="533" alt="Screen Shot 2022-11-02 at 3 46 26 PM" src="https://user-images.githubusercontent.com/59805439/199520683-f249418a-52c0-49f2-9e8d-b90b6e5c85e1.png">

### Final Iteration 
<img width="398" alt="image" src="https://user-images.githubusercontent.com/59805439/199518209-34c97b66-3e15-4516-a64d-0384c22f441e.png">
<br />
<img width="386" alt="image" src="https://user-images.githubusercontent.com/59805439/199518227-bb3436b2-d452-4280-8e46-dd4cdccfad16.png">


## Graphical User Interface
The final GUI looks as follows: </br>
<img width="925" alt="image" src="https://user-images.githubusercontent.com/59805439/199518927-c766b9ad-04ac-41e0-b90b-aa78ffb35744.png">

