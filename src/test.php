<?php

$command = escapeshellcmd('/src/subnit.py');
$output = shell_exec($command);
echo $output;
?>