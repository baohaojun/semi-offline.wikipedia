<?php
#
# SpecialLastUserLogin Mediawiki extension
# 
# Original by Justin G. Cramer and Danila Ulyanov 22.11.2005
# 
# Extended by Thomas Klein
#
# http://www.mediawiki.org/
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or 
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
# http://www.gnu.org/copyleft/gpl.html

/**
* ChangeLog
*
* 04.04.2006 1.0.4
*  - Fixed problems with MediaWiki 1.6
*
* 29.03.2006 1.0.3
*  - Fixed problems with varibale $_COOKIE and $PHPSELF
*  - Translation to german
*  - Insert style cellpadding in table
*
* 20.12.2005 1.0.2
*  - The code checked the user authorizes
*
* 09.12.2005 1.0.1
*  - Make a link to the user page
*
* 30.11.2005 1.0.0
*  - Release of the first version
*/

if( !defined( 'MEDIAWIKI' ) ) {
  die();
}

require_once "$IP/includes/SpecialPage.php";

$wgExtensionFunctions[] = "wfLastUserLogin";
$wgExtensionFunctions[] = "wfUpdateUserTouched";

$wgExtensionCredits['specialpage'][] = array(
                                            'name' => 'LastUserLogin',
                                            'description' => 'Displays the last time a user logged in',
                                            'url' => 'http://meta.wikimedia.org/wiki/SpecialLastUserLoginEx',
                                            'author' => 'Justin G. Cramer, Danila Ulyanov, Thomas Klein',
                                            'version'=>'1.0.4');

function wfUpdateUserTouched() {
  global $wgDBprefix, $wgOut, $wgDBname;
  if (isset($_COOKIE) && isset($_COOKIE["{$wgDBname}_{$wgDBprefix}UserID"])) {
      $db = &wfGetDB(DB_SLAVE);
      $query = "UPDATE {$wgDBprefix}user SET user_touched = '".wfTimestamp(TS_MW)."' WHERE user_id = ".intval($_COOKIE["{$wgDBname}_{$wgDBprefix}UserID"]);
      $db->doQuery($query);
  }
}

function wfLastUserLogin() {

  class SpecialLastUserLogin extends SpecialPage {
  function SpecialLastUserLogin() {
    SpecialPage::SpecialPage('LastUserLogin', 'block');
  }

  function execute() {
    global $wgDBprefix, $wgOut, $wgLang, $PHPSELF;
    global $wgUser;
    
    if ( ! $wgUser->isAllowed('block') ) {
      $wgOut->permissionRequired('block');
      return;
    }
    
    $this->setHeaders();
    $skin = $wgUser->getSkin( );

    $wgOut->setPagetitle( wfMsg( 'lastuserlogin' ) );
    
    $db = &wfGetDB(DB_SLAVE);
    $style = 'style="border:1px solid #000;text-align:left;"';
    $fields = array('user_name'=>'lastuserlogin_userid',
                    'user_real_name'=>'lastuserlogin_username',
                    'user_email'=>'lastuserlogin_useremail',
                    'user_touched'=>'lastuserlogin_lastlogin'
                    );
    //get order by and check it
    if(isset($_REQUEST['order_by'])){
        if(isset($fields[$_REQUEST['order_by']])){
          $orderby = $_REQUEST['order_by'];
        }else{
          $orderby = 'user_name';
        }               
    }else{
       $orderby = 'user_name';
    }       
    
    //get order type and check it
    if(isset($_REQUEST['order_type'])){
      if($_REQUEST['order_type']=='DESC'){
        $ordertype = $_REQUEST['order_type'];
      }else{
        $ordertype = 'ASC';
      }               
    }else{
      $ordertype = 'ASC';
    }       
  
    $query = "SELECT user_name, user_real_name, user_email, user_touched FROM ".$wgDBprefix."user ORDER BY ".$orderby." ".$ordertype;
    $ordertype = $ordertype=='ASC'?'DESC':'ASC';
   
    if ($result = $db->doQuery($query)) {
      $out = '<table width="100%" cellpadding="3" '.$style.'><tr>';
    
      foreach($fields as $key=>$value){
        $out .= '<th '.$style.'><a href="?order_by='.$key.'&order_type='.$ordertype.'">'.wfMsg( $value ).'</a></th>';
      }
    
      $out .= "<th $style>".wfMsg( 'lastuserlogin_daysago' )."</th>";
      $out .= '</tr>';
    
      while ($row = $db->fetchRow($result)) {
        $out .= '<tr>';
        foreach($fields as $key=>$value){
    
        if ($key == "user_touched") {
          $style = 'style="border:1px solid #000"';
          $out .= "<td $style>".$wgLang->timeanddate( wfTimestamp(TS_MW, $row[$key]), true).
                  '</td><td style="border: 1px solid #000; text-align:right;">'.
                  $wgLang->formatNum(round((mktime() - wfTimestamp(TS_UNIX, $row[$key]))/3600/24, 2), 2)."</td>";
        } else {
          if ($key == "user_name") {
            $userPage = Title::makeTitle( NS_USER, htmlspecialchars($row[$key]));
            $name = $skin->makeLinkObj( $userPage, htmlspecialchars( $userPage->getText() ) );

            $out .= '<td '.$style.'>'.$name.'</a></td>';          
          } else { 
            $out .= '<td '.$style.'>'.htmlspecialchars($row[$key]).' </td>';
          }
        }
      }
    
      $out .= '</tr>';
    }
        }
    $out .= '</table>';
    $wgOut->addHTML( $out );
    
    }
  }
  
  SpecialPage::addPage( new SpecialLastUserLogin );
  
  global $wgMessageCache, $wgLanguageCode;
  
  if ($wgLanguageCode == 'de') {
    $wgMessageCache->addMessage('lastuserlogin' ,'Letzte Anmeldungen');
    $wgMessageCache->addMessage('lastuserlogin_userid', 'Anmeldename');
    $wgMessageCache->addMessage('lastuserlogin_username', 'Benutzername');
    $wgMessageCache->addMessage('lastuserlogin_useremail', 'E-Mail-Adresse');
    $wgMessageCache->addMessage('lastuserlogin_lastlogin', 'Letzte Anmeldung');
    $wgMessageCache->addMessage('lastuserlogin_daysago', 'Tage');
  }
  else {
    $wgMessageCache->addMessage('lastuserlogin' ,'Last User Login');
    $wgMessageCache->addMessage('lastuserlogin_userid', 'User ID');
    $wgMessageCache->addMessage('lastuserlogin_username', 'User Name');
    $wgMessageCache->addMessage('lastuserlogin_useremail', 'User Email');
    $wgMessageCache->addMessage('lastuserlogin_lastlogin', 'Last Login');
    $wgMessageCache->addMessage('lastuserlogin_daysago', 'Days Ago');
  }
}

?>
