<?
$size=$argv[1];
echo 'Finding Squares of Size ' . $size . "\n";

$se=fopen('php://stderr','w+');

$words=file("words_len_".$size);

$egrid=array_fill(0,$size,array_fill(0,$size,null));

foreach($words as $k=>$word) {
	$words[$k]=trim($word);	
    for ($i=1;$i<$size;$i++) {
         $map[substr($words[$k],0,$i)][]=$words[$k];
    }
}
//unset($words);

foreach ($map['z'] as $word) {
    dbg('Trying ' . $word);
    $grid=$e_grid;
    $grid[0]=preg_split('//', $word, -1, PREG_SPLIT_NO_EMPTY);
    for ($i=1;$i<$size;$i++) {
        $grid[$i][0]=$grid[0][$i];
    }
    echo formatGrid($grid);
    run($grid,1);
}

function run($grid,$row) {
    global $size;
    if ($row==$size) {
        echo "###SOLVED\n";
        echo formatGrid($grid);
    } else {
        global $map;
        $prefix='';
        for ($i=0;$i<$row;$i++) {
            $prefix.=$grid[$row][$i];
        }
        //now get all words with that prefix
        dbg('getting words prefixed:' . $prefix.'.');
        
        if (array_key_exists($prefix,$map)) {
            $words=$map[$prefix];
            foreach ($words as $word) {
                //now fill it
                dbg($word);
                $grid[$row]=preg_split('//', $word, -1, PREG_SPLIT_NO_EMPTY);
                for ($i=$row;$i<$size;$i++) {
                    $grid[$i][$row]=$grid[$row][$i];
                }
                
                //echo formatGrid($grid);
                run($grid,$row+1);
                //break;
            }
        }
    }
    status($row);
}

function formatGrid($grid) {
    $out="---------------\n";
    foreach ($grid as $line) {
        
        foreach ($line as $char) {
            $out .='|'.$char;
        }
        $out.="|\n";
    }
    $out.="---------------\n";
    return $out;
}
function dbg($string) {
    //echo $string . "\n";
}

$i = 0;
function status($string) {
    global $se;
    global $i;
    ++$i;
    if ($i % 1000 == 0) {
        fputs($se,date("H:i:s").': '.$i.' '.$string."\n");
    }
}
?>
