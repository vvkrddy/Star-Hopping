
![ScreenShot](Images/ss_editor.png)

# Interface

Target text field takes the values of Right Ascension, Declination and Field of View in degrees; all seperated by spaces OR common name, messier ID, etc  <br /><br /> In the case of latter, a fixed FoV of 20 degrees is considered


# Instructions for Creating Hops for Messiers
Click on CREATE HOP button. Next, in the prompt, enter the messier object you would like to create hops for. The format for input is 'm' followed by number.<br />
The plot isn't affected with this. Now, the user can either zoom-in, -out; or use the rectangle zoom tool or can enter the messier number with FoV in the search text field.<br /><br />
BUT THE EVERYTIME YOU NOTICE AN UNWANTED HOP IN THE DISPLAY ABOVE THE PLOT, CLICK UNDO. THIS HAPPENS SINCE THE MOUSE CLICKS(LEFT BUTTON) WHILE ZOOMING USING THE DEFAULT NAVIGATION BUTTONS ARE ALSO RECORDED AS A CLICKS FOR HOP CLICK. <br />NEXT UPDATE SHOULD SEE A CHANGE IN THIS BEHAVIOUR.<br /><br />
Since the messier object is selected, hops must be recorded in the order towards the messier object minus the messier object.<br />
So, if a star A and Star B are selected; the hopping is from A to B to Messier Object.<br /><br />
Each time a marker star(the one used for hopping) is selected by the user, it's reflected above the plot in the form of a list.<br /><br />
Anytime a user decides to undo the last hop, UNDO HOP button is to be clicked. The removal of last marker star is also reflected in the display above plot. <br /><br />
Once the user is done with selecting all marker stars for a given messier, FINISH HOP button is to be clicked.<br /><br />
A pickled dictionary hop.pkl is saved at the end of a finished hop. NO EMPTY TEXT FILE IS REQUIRED. THE PROGRAMS CHECKS FOR THE hop.pkl AND CREATES ONE IF NONE EXISTS, in the working directory. <br /><br />
