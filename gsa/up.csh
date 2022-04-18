#!/bin/csh 

set ts = time.stamp

# get list of files,
# 	prepare for 'find' command
set namelist = `perl -n -e '$i++; print " -o " if $i > 1; print "-name $_ ";' f.list `
#echo new $namelist

# generate list of files newer than timestamp
set newlist =  ( `find .  \( $namelist \)  -newer $ts ` )
#echo new $newlist
#echo $#newlist
#exit

if ( $#newlist > 0 ) then
#echo new $newlist
foreach f ( $newlist ) 
  # make sure its readable
  chmod ugo+r $f
end

echo upload: $newlist
scp $newlist burleigh@172.30.229.220:public_html
touch $ts

endif




