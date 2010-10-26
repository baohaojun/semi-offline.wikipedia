<?php

// fnatter 2006-11-02:
$wgCommandLineMode = true;
// make it not complain when we use a web-browser for testing
unset($_SERVER);

/**
 * Main wiki script; see docs/design.txt
 * @package MediaWiki
 */

$wgRequestTime = microtime(true);

# getrusage() does not exist on the Microsoft Windows platforms, catching this
if ( function_exists ( 'getrusage' ) ) {
	$wgRUstart = getrusage();
} else {
	$wgRUstart = array();
}

unset( $IP );
@ini_set( 'allow_url_fopen', 0 ); # For security...

if ( isset( $_REQUEST['GLOBALS'] ) ) {
	die( '<a href="http://www.hardened-php.net/index.76.html">$GLOBALS overwrite vulnerability</a>');
}

# Valid web server entry point, enable includes.
# Please don't move this line to includes/Defines.php. This line essentially
# defines a valid entry point. If you put it in includes/Defines.php, then
# any script that includes it becomes an entry point, thereby defeating
# its purpose.
define( 'MEDIAWIKI', true );

# Load up some global defines.

require_once( './includes/Defines.php' );

# Include this site setttings
require_once( './LocalSettings.php' );
$wgDebugLogGroups  = array(
    'bhj'	=> '/dev/tty',
);

// load ParserFunctions extension
if( file_exists("$IP/StartProfiler.php") ) {
	require_once( "$IP/StartProfiler.php" );
} else {
	require_once( "$IP/includes/ProfilerStub.php" );
}

# Prepare MediaWiki
require_once( 'includes/Setup.php' );
require_once("extensions/ParserFunctions/ParserFunctions.php");
require_once( "extensions/Cite/Cite.php" );
# Initialize MediaWiki base class
require_once( "includes/Wiki.php" );
$mediaWiki = new MediaWiki();

wfProfileIn( 'main-misc-setup' );
OutputPage::setEncodings(); # Not really used yet

# Query string fields
$action = $wgRequest->getVal( 'action', 'view' );
$title = $wgRequest->getVal( 'title' );

#
# Send Ajax requests to the Ajax dispatcher.
#
if ( $wgUseAjax && $action == 'ajax' ) {
	require_once( 'AjaxDispatcher.php' );

	$dispatcher = new AjaxDispatcher();
	$dispatcher->performAction();

	exit;
}

?>

<?php

$wgShowExceptionDetails = true;

include_once("includes/parser/Parser.php");
if (empty($argv[1]))
  $argv[1] = "intro.wikimarkup";


if ($argv[1] == "-") {
  $markup = "";
  while (!feof(STDIN))
    $markup .= fread(STDIN, 16384);
} else
  $markup = file_get_contents($argv[1]);

$newlineidx = strpos($markup, "\n");
$articletitle = trim(substr($markup, 0, $newlineidx));
$markup = substr($markup, $newlineidx + 1);

$p = new Parser();

$p->setHook( 'ref' , array( &$GLOBALS['hackCiteObj'], 'ref' ) );
$p->setHook( 'references' , array( &$GLOBALS['hackCiteObj'], 'references' ) );
$wgHooks['ParserClearState'][] = array( &$GLOBALS['hackCiteObj'], 'clearState' );

wfSetupParserFunctions();

$wgMessageCache->addMessage( 'pfunc_time_error', "Error: invalid time" );
$wgMessageCache->addMessage( 'pfunc_time_too_long', "Error: too many #time calls" );
$wgMessageCache->addMessage( 'pfunc_rel2abs_invalid_depth', "Error: Invalid depth in path: \"$1\" (tried to access a node above the root node)" );


$title = new Title();
$options = new ParserOptions(null); // 1st arg: $user
$options->setEditSection(false);
require('skins/Simple.php');
$options->setSkin(new SkinSimple());
$output_obj = $p->parse($markup, $title, $options);
$text = $output_obj->getText();
$text = preg_replace("/scripts\/index\.php\?title=([^&]*)&amp;action=edit/", "article/$1/", $text);
$text = preg_replace("/scripts\/index\.php\/([^\"]*)/", "article/$1/", $text); #woc

$out = $text;

?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type">
    <title><?php echo $articletitle ?></title>
  </head>
<body>
  <?php echo $out; ?>
</body>
</html>
