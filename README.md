# htx-ds-test

Documentation of any additional steps on top of the assessment instructions.

Task 2:
- (cv-valid-dev.csv is final data file)
- requirements.txt: Duplicate file of requirements.txt in main directory, solely for Docker conterisation purposes
- out.csv: Intermediate CSV output from cv-decode.py
- combine_results.ipynb: Intermediate code to join intermediate results out.csv with original cv-valid-dev to combine into final results

Task 3:
- subset_data.csv: Subset of training data, meant as convenient code checkpoint

Task 4:
- (Instructions mentioned answer can save as training-report.pdf, chose to represent answer as Notebook instead)
- task-4.ipynb: Notebook of Task 4 results

Task 5b:
- Encountered issues regarding provided Text embedding model
- This led to uninstallation and depreciation of various libaries to try to make it work, but still failed

NOTE: 
- After completing Task 5b, realised error in Notebook 2a; tried to correct it and re-run code
- But due to uninstallation and depreciation of various libaries (from process in Task 5b), same code which worked on local device no longer works, returning errors not seen before
- As error was only found on final day, there was not enough time to remedy the situation and fix the issue :(