<?php

# This file was automatically generated by the MediaWiki installer.
# If you make manual changes, please keep track in case you need to
# recreate them later.
#
# See includes/DefaultSettings.php for all configurable settings
# and their default values, but don't forget to make changes in _this_
# file, not there.
#
# Further documentation for configuration settings may be found at:
# http://www.mediawiki.org/wiki/Manual:Configuration_settings

# If you customize your file layout, set $IP to the directory that contains
# the other MediaWiki files. It will be used as a base to locate files.

# We define this to allow the configuration file to be explicitly 
# located in /etc/mediawiki.
# Change this if you are setting up multisite wikis on your server.

if( defined( 'MW_INSTALL_PATH' ) ) {
	$IP = MW_INSTALL_PATH;
} else {
	$IP = dirname( __FILE__ );
}

$path = array( $IP, "$IP/includes", "$IP/languages" );
set_include_path( implode( PATH_SEPARATOR, $path ) . PATH_SEPARATOR . get_include_path() );

require_once( "$IP/includes/DefaultSettings.php" );

# If PHP's memory limit is very low, some operations may fail.
# ini_set( 'memory_limit', '20M' );

if ( $wgCommandLineMode ) {
	if ( isset( $_SERVER ) && array_key_exists( 'REQUEST_METHOD', $_SERVER ) ) {
		die( "This script must be run from the command line\n" );
	}
}
## Uncomment this to disable output compression
# $wgDisableOutputCompression = true;

$wgSitename         = "Bhj";

## The URL base path to the directory containing the wiki;
## defaults for all runtime URL paths are based off of this.
## For more information on customizing the URLs please see:
## http://www.mediawiki.org/wiki/Manual:Short_URL
$wgScriptPath       = "/scripts";
$wgScriptExtension  = ".php";

## UPO means: this is also a user preference option

$wgEnableEmail      = true;
$wgEnableUserEmail  = true; # UPO

$wgEmergencyContact = "baohaojun@gmail.com";
$wgPasswordSender = "baohaojun@gmail.com";

$wgEnotifUserTalk = true; # UPO
$wgEnotifWatchlist = true; # UPO
$wgEmailAuthentication = true;

## Database settings
$wgDBtype           = "null";
$wgDBserver         = "localhost";
$wgDBname           = "wikidb";
$wgDBuser           = "bhj";
$wgDBpassword       = "xxxxx";

# Postgres specific settings
$wgDBport           = "5432";
$wgDBmwschema       = "mediawiki";
$wgDBts2schema      = "public";

## Shared memory settings
$wgMainCacheType = CACHE_NONE;
$wgMemCachedServers = array();

## To enable image uploads, make sure the 'images' directory
## is writable, then set this to true:
$wgEnableUploads       = false;
$wgUseImageMagick = true;
$wgImageMagickConvertCommand = "/usr/bin/convert";

## If you use ImageMagick (or any other shell command) on a
## Linux server, this will need to be set to the name of an
## available UTF-8 locale
$wgShellLocale = "en_US.utf8";

## If you want to use image uploads under safe mode,
## create the directories images/archive, images/thumb and
## images/temp, and make them all writable. Then uncomment
## this, if it's not already uncommented:
# $wgHashedUploadDirectory = false;

## If you have the appropriate support software installed
## you can enable inline LaTeX equations:
$wgUseTeX           = false;

$wgLocalInterwiki   = strtolower( $wgSitename );

$wgLanguageCode = "en";

$wgSecretKey = "2dd6734f6c512324aaca14aa3d588688a74506f24fe277de7fe839a36279116a";

## Default skin: you can change the default skin. Use the internal symbolic
## names, ie 'standard', 'nostalgia', 'cologneblue', 'monobook':
$wgDefaultSkin = 'monobook';

## For attaching licensing metadata to pages, and displaying an
## appropriate copyright notice / icon. GNU Free Documentation
## License and Creative Commons licenses are supported so far.
# $wgEnableCreativeCommonsRdf = true;
$wgRightsPage = ""; # Set to the title of a wiki page that describes your license/copyright
$wgRightsUrl = "";
$wgRightsText = "";
$wgRightsIcon = "";
# $wgRightsCode = ""; # Not yet used

$wgDiff3 = "/usr/bin/diff3";

# When you make changes to this configuration file, this will make
# sure that cached pages are cleared.
$wgCacheEpoch = max( $wgCacheEpoch, gmdate( 'YmdHis', @filemtime( __FILE__ ) ) );
$wgArticlePath      = "/wiki/$1";  # Virtual path. This directory MUST be different from the one used in $wgScriptPath
$wgUsePathInfo      = true;        # Enable use of pretty URLs
$wgUseTeX           = true;
$wgTexvc            = "/usr/bin/texvc";

$wgUseTidy = true;
$wgTidyBin = '/usr/bin/tidy';   
$wgTidyConf = $IP.'/extensions/tidy/tidy.conf';

$wgForeignFileRepos[] = array(
   'class'                   => 'ForeignAPIRepo',
   'name'                    => 'shared',
   'apibase'                 => 'http://commons.wikimedia.org/w/api.php',
   'fetchDescription'        => true, // Optional
   'descriptionCacheExpiry'  => 0,
   'apiThumbCacheExpiry'     => 0,
);

$wgUseFileCache = true; /* default: false */
$wgFileCacheDirectory = "$IP/cache";
$wgShowIPinHeader = false; 

## Shared memory settings
$wgMessageCacheType = CACHE_ACCEL;
$wgCacheDirectory = "$IP/msg_cache";
$wgParserCacheType = CACHE_ACCEL;
# File cache!
$wgUseGzip = true;
$wgEnableSidebarCache = true;
# NO DB HITS!
$wgDisableCounters = true;
$wgMiserMode = true;
# Text cache
$wgCompressRevisions = true;
$wgRevisionCacheExpiry = 3*24*3600;
$wgParserCacheExpireTime = 14*24*3600;
