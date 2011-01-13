Building a new version for release is complicated due the use of PLY 
for creating Logo programs. For more detailed information on that 
aspect please see "READ-ME-OR-WEEP.txt". Also, on my dev machine at 
least, the "po/POTFILES.in" file seems to be ignored which causes 
"setup.py genpot" to scan files which we want exluded. So, to build a
new release first increment "activity_version" in activity/activity.info
then perform the following in a terminal/ shell from the "GoGo.activity"
directory (line numbers for reference only):

1) ./clean.sh

This removes all dynamically created files particularly optimised files 
created by PLY and which may raise problems when generating a new POT 
file. If "po/POTFILES.in" is being used by "setup.py genpot" on your 
system then skip this step but ensure "po/POTFILES.in" is upto date.
 
2) ./setup.py genpot

This creates a new POT file for translation/ localisation.

3) ./rebuild-compiler.sh

This ensures Python is not optimised and that files dynamically 
created by PLY are regenerated.
 
4) ./setup.py dist_xo

Finally, this creates a new XO bundle.
