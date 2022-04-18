<html>
<head>
<meta http-equiv="Content-Language" content="en" />
<meta name="GENERATOR" content="PHPEclipse 1.0" />
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<title>Router Pages</title>
<link href="../styles/report.css" rel="stylesheet" type="text/css"/>
<link href="../styles/deldev.css" rel="stylesheet" type="text/css"/>
<link href="../styles/deldev2.css" rel="stylesheet" type="text/css"/>

<style type="text/css">@import url(../jscal/calendar-win2k-1.css);</style>
<script type="text/javascript" src="../jscal/calendar.js"></script>
<script type="text/javascript" src="../jscal/lang/calendar-en.js"></script>
<script type="text/javascript" src="../jscal/calendar-setup.js"></script>
</head>
<body >
<div class='hdr'>
	<div class='logo1'><img src='../img/cdw_white_sm.gif' /></div>
	<h1>Wiki  Usage Report</h1>
	<div class="clr"></div>
</div>
<div class='main'>
<?php

	// set paths here:
	require_once("config_inc.php");
	
	require_once('utils.php');  // assuming path is set

	require_once('deldevdb.php');
	require_once('reportutils.php');
	
	dprint("path: " . ini_get('include_path') );
	/*
	 * Configure
	 */
	$selected_pages = array('Data_Router_IOS_Standards', 'Software_Life_Cycle_Management') ;
	
	//$debug_on = 1;
 #echo " You are: " . $_SERVER['PHP_AUTH_USER']; echo "<p>"; 

	// Default - entire date range
	$dates = deldev_row_query( "select min(date) 'from', max(date) 'to' from wikipage");
	if ( ! $dates ) {
		raise_error("query failed");
	}
	
	// Default - entire range 
	$from = $dates['from'];
	$to = $dates['to'];
	$date_clause = ''; 
	$wh_date_clause = ''; 
	// select range:
	if ( isset($_POST['from_date'])) {
	
	$from = $_POST['from_date'];
	$to = $_POST['to_date'];
	
	$date_clause = " and date >= '$from' and date <= '$to' ";
	$wh_date_clause = " where date >= '$from' and date <= '$to' "; 
	}
	
	# $date_clause = "  wikilog.date >= $from_date AND wikilog.date <= $to_date ";
#	print "<h2>Summary of Wiki Queries from " . $dates['from'] . " to " . $dates['to' ] . "</h2>";
	print "<h2>Summary of Selected Wiki Page Access  from $from  to $to </h2>";
	print "<p>(range is " . $dates['from'] . " to " . $dates['to' ] . " )"; ?>

<input type='hidden' id='min_date' name='min_date' value="<?php echo $dates['from'];?>"/>
<input type='hidden' id='max_date' name='max_date' value="<?php echo $dates['to']; ?> "/>
<form method="POST" action=>
   <button id="frombtn">Edit From</button>
   <input type="text" id="from" name="from_date"  value="<?php echo $from; ?>"/>
   
    <button id="tobtn">Edit To</button>
   <input type="text" id="to" name="to_date"  value="<?php echo $to; ?>" />

  <input type="submit" class="submit button" name="update" value="Update range" />
</form>

<script type="text/javascript">
  Calendar.setup(
    {
      inputField  : "from",         // ID of the input field
      ifFormat    : "%Y-%m-%d",    // the date format
      button      : "frombtn" ,      // ID of the button
      onSelect :  function(calendar, date) {
          var e = document.getElementById('min_date');
          mindate = e.value;
          e = document.getElementById('max_date');
          maxdate = e.value;

          //alert("compare min=" + mindate + " date=" + date)
          if ( date < mindate || date > maxdate ) {
              alert("date must be in range " + mindate + "  -- " + maxdate );
              return false;
          }
	      // TO DO: check that 'to' >= 'from'
	      // else error? set to = from?  
    	   var input_field = document.getElementById("from");
    	  input_field.value = date;
    	}
    	   
    }
    );
     Calendar.setup(
		 {
		      inputField  : "to",         // ID of the input field
		      ifFormat    : "%Y-%m-%d",    // the date format
		      button      : "tobtn",       // ID of the button
		      onSelect :  function(calendar, date) {
		          var e = document.getElementById('min_date');
		          mindate = e.value;
		          e = document.getElementById('max_date');
		          maxdate = e.value;

		          //alert("compare min=" + mindate + " date=" + date)
		          if ( date < mindate || date > maxdate ) {
		              alert("date must be in range " + mindate + "  -- " + maxdate );
		              return false;
		          }
		      // TO DO: check that 'to' >= 'from'
		      // else error? set to = from?
		    	   var input_field = document.getElementById("to");
		    	  input_field.value = date;
		    	}
		    }
	);
</script>
<?php
	
	foreach ( $selected_pages as $page ) { 
		$np = deldev_count_query("select count(*) from wikipage where page like '$page'  $date_clause ");
		print "<p>$np Total hits for $page </p>";

	deldev_list_report_table( 'Page access for: ' . $page ,
	"select count(*) num, min(wikipage.date) from_date, " .
				"max(wikipage.date) to_date, staff.name, staff.title, staff.branch  " .
				"from wikipage " .
				"left outer join staff on wikipage.fkstaff = staff.id " .
				"where page like '$page'  $date_clause group by staff.name"
	);
	}
	
?>		
	

<div class='footer'>
 <div class="hr"> &nbsp;</div>
 <p class="version_footer">v1.0</p>
 <p>Send comments / questions / bugs to <a href="mailto:ciscodeldevsupport@il.cdw.com">Cisco Practice Development Team</a></p>
 </div>
</div><!-- END main --> 
<div class='hdr'>
	<div class='logo2'><img src='../img/Gold_partner.jpg' /></div>
</div>
</body>
</html>
  