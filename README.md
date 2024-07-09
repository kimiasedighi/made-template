# Exercise Badges

![](https://byob.yarr.is/kimiasedighi/made-template/score_ex1) ![](https://byob.yarr.is/kimiasedighi/made-template/score_ex2) ![](https://byob.yarr.is/kimiasedighi/made-template/score_ex3) ![](https://byob.yarr.is/kimiasedighi/made-template/score_ex4) ![](https://byob.yarr.is/kimiasedighi/made-template/score_ex5)

# Methods of Advanced Data Engineering Course
This repository contains both a data engineering project developed over the course of the semester and the exercises submitted throughout the semester. Before you begin, ensure you have Python and Jayvee installed.

## Project
### Climate Change Impact Analysis
This project aims to analyze the correlation between atmospheric CO2 concentrations and global surface temperatures over the past several decades. By leveraging advanced data engineering techniques, we will clean, preprocess, and analyze large datasets to identify trends and patterns that highlight the impact of human activities on climate change. The project includes developing data science workflows and performing in-depth analysis to support the hypothesis that rising CO2 levels are associated with increasing global temperatures.

## Exercises
Throughout the semester, exercises are completed using Jayvee and result in the following files:

1. `./exercises/exercise1.jv`
2. `./exercises/exercise2.jv`
3. `./exercises/exercise3.jv`
4. `./exercises/exercise4.jv`
5. `./exercises/exercise5.jv`

### Exercise Feedback
Automated exercise feedback is provided using a GitHub action defined in .github/workflows/exercise-feedback.yml.

To view each exercise feedback, navigate to Actions -> Exercise Feedback in the repository.

The exercise feedback is triggered whenever a change is made to files in the 'exercises' folder and pushed to GitHub. To see the feedback, open the latest GitHub Action run, then open the exercise-feedback job and the Exercise Feedback step. You should see command line output similar to this:

```sh
Found exercises/exercise1.jv, executing model...
Found output file airports.sqlite, grading...
Grading Exercise 1
	Overall points 17 of 17
	---
	By category:
		Shape: 4 of 4
		Types: 13 of 13
```
