<?php
	$site_type = 'dev';
	$site_type = 'dcb';
	$debug_on = true;
	
	ini_set('include_path', ini_get('include_path') . PATH_SEPARATOR . '../deldev');
	require_once('/usr/local/etc/deldev/db_conf.php');
	
?>