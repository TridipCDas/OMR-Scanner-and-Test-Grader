# OMR-Scanner-and-Test-Grader

A simple bubble sheet scanner  built using OMR,OpenCV and Python. It scans the OMR sheet and grading is done accordingly with respect to given answer key.

Following steps were followed while building it:

1. Detect the OMR sheet in an image.
2. Apply a perspective transform to extract the top-down view of the sheet.
3. Extract the set of bubbles (i.e., the possible answer choices) from the perspective transformed sheet.
4. Sort the questions/bubbles into rows.
5. Determine the marked (i.e., “bubbled in”) answer for each row.
6. Lookup the correct answer in our answer key to determine if the user was correct in their choice.
7. Repeat for all questions in the sheet.

Output is shown below:


![testGrader](https://user-images.githubusercontent.com/40006730/87180280-df793b00-c2fd-11ea-9441-965cb8718d2f.png)

