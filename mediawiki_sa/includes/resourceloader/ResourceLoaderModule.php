<?php
/**
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along
 * with this program; if not, write to the Free Software Foundation, Inc.,
 * 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
 * http://www.gnu.org/copyleft/gpl.html
 *
 * @file
 * @author Trevor Parscal
 * @author Roan Kattouw
 */

defined( 'MEDIAWIKI' ) || die( 1 );

/**
 * Abstraction for resource loader modules, with name registration and maxage functionality.
 */
abstract class ResourceLoaderModule {
	
	/* Protected Members */

	protected $name = null;
	
	// In-object cache for file dependencies
	protected $fileDeps = array();
	// In-object cache for message blob mtime
	protected $msgBlobMtime = array();

	/* Methods */

	/**
	 * Get this module's name. This is set when the module is registered
	 * with ResourceLoader::register()
	 *
	 * @return Mixed: name (string) or null if no name was set
	 */
	public function getName() {
		return $this->name;
	}

	/**
	 * Set this module's name. This is called by ResourceLodaer::register()
	 * when registering the module. Other code should not call this.
	 *
	 * @param $name String: name
	 */
	public function setName( $name ) {
		$this->name = $name;
	}

	/**
	 * Get whether CSS for this module should be flipped
	 */
	public function getFlip( $context ) {
		return $context->getDirection() === 'rtl';
	}

	/**
	 * Get all JS for this module for a given language and skin.
	 * Includes all relevant JS except loader scripts.
	 *
	 * @param $context ResourceLoaderContext object
	 * @return String: JS
	 */
	public function getScript( ResourceLoaderContext $context ) {
		// Stub, override expected
		return '';
	}

	/**
	 * Get all CSS for this module for a given skin.
	 *
	 * @param $context ResourceLoaderContext object
	 * @return array: strings of CSS keyed by media type
	 */
	public function getStyles( ResourceLoaderContext $context ) {
		// Stub, override expected
		return '';
	}

	/**
	 * Get the messages needed for this module.
	 *
	 * To get a JSON blob with messages, use MessageBlobStore::get()
	 *
	 * @return array of message keys. Keys may occur more than once
	 */
	public function getMessages() {
		// Stub, override expected
		return array();
	}
	
	/**
	 * Get the group this module is in.
	 * 
	 * @return string of group name
	 */
	public function getGroup() {
		// Stub, override expected
		return null;
	}

	/**
	 * Get the loader JS for this module, if set.
	 *
	 * @return Mixed: loader JS (string) or false if no custom loader set
	 */
	public function getLoaderScript() {
		// Stub, override expected
		return false;
	}

	/**
	 * Get a list of modules this module depends on.
	 *
	 * Dependency information is taken into account when loading a module
	 * on the client side. When adding a module on the server side,
	 * dependency information is NOT taken into account and YOU are
	 * responsible for adding dependent modules as well. If you don't do
	 * this, the client side loader will send a second request back to the
	 * server to fetch the missing modules, which kind of defeats the
	 * purpose of the resource loader.
	 *
	 * To add dependencies dynamically on the client side, use a custom
	 * loader script, see getLoaderScript()
	 * @return Array of module names (strings)
	 */
	public function getDependencies() {
		// Stub, override expected
		return array();
	}
	
	/**
	 * Get the files this module depends on indirectly for a given skin.
	 * Currently these are only image files referenced by the module's CSS.
	 *
	 * @param $skin String: skin name
	 * @return array of files
	 */
	public function getFileDependencies( $skin ) {
		// Try in-object cache first
		if ( isset( $this->fileDeps[$skin] ) ) {
			return $this->fileDeps[$skin];
		}

		$dbr = wfGetDB( DB_SLAVE );
		$deps = $dbr->selectField( 'module_deps', 'md_deps', array(
				'md_module' => $this->getName(),
				'md_skin' => $skin,
			), __METHOD__
		);
		if ( !is_null( $deps ) ) {
			return $this->fileDeps[$skin] = (array) FormatJson::decode( $deps, true );
		}
		return $this->fileDeps[$skin] = array();
	}
	
	/**
	 * Set preloaded file dependency information. Used so we can load this
	 * information for all modules at once.
	 * @param $skin string Skin name
	 * @param $deps array Array of file names
	 */
	public function setFileDependencies( $skin, $deps ) {
		$this->fileDeps[$skin] = $deps;
	}
	
	/**
	 * Get the last modification timestamp of the message blob for this
	 * module in a given language.
	 * @param $lang string Language code
	 * @return int UNIX timestamp, or 0 if no blob found
	 */
	public function getMsgBlobMtime( $lang ) {
		if ( !count( $this->getMessages() ) )
			return 0;
		
		$dbr = wfGetDB( DB_SLAVE );
		$msgBlobMtime = $dbr->selectField( 'msg_resource', 'mr_timestamp', array(
				'mr_resource' => $this->getName(),
				'mr_lang' => $lang
			), __METHOD__
		);
		$this->msgBlobMtime[$lang] = $msgBlobMtime ? wfTimestamp( TS_UNIX, $msgBlobMtime ) : 0;
		return $this->msgBlobMtime[$lang];
	}
	
	/**
	 * Set a preloaded message blob last modification timestamp. Used so we
	 * can load this information for all modules at once.
	 * @param $lang string Language code
	 * @param $mtime int UNIX timestamp or 0 if there is no such blob
	 */
	public function setMsgBlobMtime( $lang, $mtime ) {
		$this->msgBlobMtime[$lang] = $mtime;
	}
	
	/* Abstract Methods */
	
	/**
	 * Get this module's last modification timestamp for a given
	 * combination of language, skin and debug mode flag. This is typically
	 * the highest of each of the relevant components' modification
	 * timestamps. Whenever anything happens that changes the module's
	 * contents for these parameters, the mtime should increase.
	 *
	 * @param $context ResourceLoaderContext object
	 * @return int UNIX timestamp
	 */
	public function getModifiedTime( ResourceLoaderContext $context ) {
		// 0 would mean now
		return 1;
	}
}
