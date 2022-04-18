<html>
<head>
<meta http-equiv="Content-Language" content="en" />
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<title>search the GSA </title>
<link href="gsa.css" rel=stylesheet type="text/css" />
  
</head>
<body>
<?php
/*
 * This search page uses
 * 		gsa.css - stylesheet
 * 		gsa.xsl - XSL file
 * 			edit 'spage' value to match this file
 *   
 * 
 * 
ipcc_binc-callmgr-tech_collection= http://discdungeon.berbee.com/Berbee/lists/binc-callmgr-tech/

ipcc_binc-ciscotech_collection = http://discdungeon.berbee.com/Berbee/lists/binc-ciscotech/

ipcc_ipcc-team_collection  = http://discdungeon.berbee.com/Berbee/lists/ipcc-team/

ipcc_vvtwiki_collection  = https://discdungeon.berbee.com/vvtwiki/
*/
 
 /*
  * Parameters
  *  see http://code.google.com/apis/searchappliance/documentation/46/xml_reference.html
  * Required:
  * 	q - the input query
  * 	site - one of the collections to search
  * 		[selected by user]
  * 	client - A string that indicates a valid front end.
  * 		default_frontend [ only 1 currently]
  * 	output - Selects the format of the search results. 
  * 		xml_no_dtd
  * 
  * optional:
  * 
  * 	proxystylesheet
  * 		If the value of the output parameter is xml_no_dtd, the output format is 
  * 			modified by the proxystylesheet value as follows:
  *			omitted 
	
  *  	entqr - Reserved for internal use by the search appliance,
  * 		== 0
  * 	ud - Specifies whether results include ud tags.
  * 		== 1
  * 	
  * 	sort - Specifies a sorting method. 
  * 		Sort By Relevance (Default)
  * 		date:<direction>:<mode>:<format>
  * 
  * http://code.google.com/apis/searchappliance/documentation/46/xml_reference.html#request_sort
  * 
  * 	num - Maximum number of results to include in the search results.
  * 
  * 	oe - Sets the character encoding that is used to encode the results.
  * 		UTF-8
  * 	ie - Sets the character encoding that is used to interpret the query string. 
  * 		UTF-8
   * 
  * 	filter -
  * see:
  * http://code.google.com/apis/searchappliance/documentation/46/xml_reference.html#request_filter_auto
  * 
  * 	btnG - the submit button
  */
 /*
  * Configure
  */
 $collections = array( 'ipcc_binc-callmgr-tech_collection', 'ipcc_binc-ciscotech_collection',
 'ipcc_ipcc-team_collection',  'ipcc_vvtwiki_collection',
 'ipcc_collection',
 'dc_wiki_collection', 'default_collection', 'archive_collection'
 );
 
$collections = array( 'vvt_binc-callmgr-tech_collection', 'vvt_binc-ciscotech_collection',
 'vvt_ipcc-team_collection',  'vvt_vvtwiki_collection',
 'vvt_collection',
 'dc_wiki_collection', 'default_collection', 'archive_collection'
 );

$vvt_collections = array( 'vvt_binc-callmgr-tech_collection', 'vvt_binc-ciscotech_collection',
 'vvt_ipcc-team_collection',  'vvt_vvtwiki_collection'
 ); 
 
$xsl_filename = 'gsa.xsl';
 
 /*
  * Defaults 
  */
  $debug_on = 0;
  #$debug_on = 1;
  
  $filter = '0';
  
  if ( isset($_GET['filter'])) {
  	$filter = $_GET['filter'];
  }
  #dprint("f=$filter");
  
?>

<p>Search the GSA</p>
<form name="gs" method="GET" action="">
<table cellpadding="0" cellspacing="0">
   <tr>
      <td valign="middle"><font size="-1">
      <input type="text" name="q" size="32" maxlength="256" value="<?php echo $_GET['q']; ?>" />
      </font></td>
      <td valign="middle"><select name="site">
      <?php 
     
      foreach ($collections as $c) {
      	
      	print "<option value='$c'";
      	if ( $_GET['site'] == $c ) {
      		print " SELECTED";
      	}
		print ">$c</option>\n";
      }       
      ?>
            </select></td>
      <td valign="middle"><font size="-1">&nbsp;<input type="submit" name="btnG" value="Search"></font></td>

   </tr>
</table>
<!--
                  <input type="hidden" name="entqr" value="0">
                  <input type="hidden" name="ud" value="1">

                  <input type="hidden" name="sort" value="date:D:L:d1">
                  <input type="hidden" name="num" value="5">

                  <input type="hidden" name="sort" value="date:D:R:d1">

-->
				Filter?
                  <input type="radio" name="filter" value="1" 
                  <?php if ( $filter == '1' ) { print "CHECKED"; } ?> > Both
                  <input type="radio" name="filter" value="0"
                  <?php if ( $filter == '0' ) { print "CHECKED"; } ?> > None
                  <input type="radio" name="filter" value="s" 
                  <?php if ( $filter == 's' ) { print "CHECKED"; } ?> > Directories
                  <input type="radio" name="filter" value="p" 
                  <?php if ( $filter == 'p' ) { print "CHECKED"; } ?> > Snippets


                  <input type="hidden" name="output" value="xml_no_dtd">
                  <input type="hidden" name="oe" value="UTF-8">
                  <input type="hidden" name="ie" value="UTF-8">

                  <input type="hidden" name="client" value="default_frontend">                      
               </form>
  
<hr>
 
<p>Search the GSA</p>  

<form name="gs" method="GET" action="">
<p> Select one or more collections:
     <?php   
      foreach ($vvt_collections as $c) {
      	print "<br /><input type='checkbox' name='slist[]' value='$c'";
      	if (is_array($_GET['slist'] ) &&  in_array($c, $_GET['slist'])  ) {
      		print " CHECKED";
      	}
		print " />$c\n";
      }       
      ?>
</p>
<table cellpadding="0" cellspacing="0">
   <tr>
      <td valign="middle"><font size="-1">
      <input type="text" name="q" size="32" maxlength="256" value="<?php echo $_GET['q']; ?>" />
      </font></td>
      <td valign="middle">
 
      </td>
      <td valign="middle"><font size="-1">&nbsp;<input type="submit" name="btnG" value="Search"></font></td>
   </tr>
</table>

<!--
                  <input type="hidden" name="entqr" value="0">
                  <input type="hidden" name="ud" value="1">


                  <input type="hidden" name="sort" value="date:D:L:d1">
                  <input type="hidden" name="num" value="5">

                  <input type="hidden" name="sort" value="date:D:R:d1">

-->
				Filter?
                  <input type="radio" name="filter" value="1" 
                  <?php if ( $filter == '1' ) { print "CHECKED"; } ?> > Both
                  <input type="radio" name="filter" value="0"
                  <?php if ( $filter == '0' ) { print "CHECKED"; } ?> > None
                  <input type="radio" name="filter" value="s" 
                  <?php if ( $filter == 's' ) { print "CHECKED"; } ?>> Directories
                  <input type="radio" name="filter" value="p" 
                  <?php if ( $filter == 'p' ) { print "CHECKED"; } ?>> Snippets


                  <input type="hidden" name="output" value="xml_no_dtd">
                  <input type="hidden" name="oe" value="UTF-8">
                  <input type="hidden" name="ie" value="UTF-8">

                  <input type="hidden" name="client" value="default_frontend">                      
               </form>
               
  
<?php
ini_set( 'display_errors', TRUE);

if ( ! empty($_SERVER['QUERY_STRING']) ) {
	$url = 'http://search.berbee.com/search?' . $_SERVER['QUERY_STRING'];
	###require('gsa_util.php');
	
	// build URL for GSA
	/*
	$url = 'http://search.berbee.com/search?';
	$search_parameters = array('q', 'client', 'output', 
		'site',
		'entqr', 'ud', 'sort' );
	foreach ( $_GET as $name => $value) {
		if ( in_array($name, $search_parameters)) {
			$url .= '&' . $name . '=' . $value;
		}
	}
	*/
	
	if ( isset($_GET['slist'])) {
		dprint("URL before: $url  ");
		// multiple sites selected
		// assume its an array
		if ( is_array($_GET['slist'])) {
		$slist = $_GET['slist'];
		dprint("slist = " . print_r($slist, TRUE) );	
		$sites = join($_GET['slist'], '|');
		}
		else {
			$sites = $_GET['slist'];
		}
		$url = preg_replace('/site=[^\&]+/', '',  $url);
		$url .= '&site=' . $sites;
		
		#$url = preg_replace('/\&slist[^\&]+/', '',  $url);
		#$url = preg_replace('/\?slist[^\&]+\&?/', '?',  $url);
		
	}
	# debug
	dprint("Get: $url  ");

	$page = get_search_results( $url );   # requires php-curl;
	
	dprint(" got page size=" . strlen($page) );
	
	if ( empty( $_GET['proxystylesheet'])) {
		# this should be the default
		$html = xsl_transform( $page );		
	}
	else {
		$html = $page;
	}
	/*
	 * display the results;
	 * expect a block of HTML (sans  html, head, body tags)
	 */
	print "$html";
?>
<!-- for testing only -->
<p> Raw data from query</p>
  <form  method="get">
  
  <textarea name="page" rows="10" cols="50" wrap="off">
  <?php print $page; ?>
  </textarea>
  </form>

<?php
} # END-if 

function dprint( $text ) {
	global $debug_on;
	if ( $debug_on) {
		echo "<div class='debug'>$text</div>\n";
	}
}



# --------------------------------
function get_search_results( $url ) {

$ch = curl_init( $url);

curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
curl_setopt($ch, CURLOPT_HEADER, 0);

$body = curl_exec($ch);
if ( ! $body ) {
	die("curl $url failed");
}
curl_close($ch);

return $body;

}


# --------------------------------
function xsl_transform( $xml_string ) {

	global $xsl_filename;
	
	$doc = new DOMDocument();
 	$xsl = new XSLTProcessor();

 	$doc->load($xsl_filename);
    $xsl->importStyleSheet($doc);

    $doc->loadXML($xml_string);
    return $xsl->transformToXML($doc);

}


?>

 
</body>
</html>
  
