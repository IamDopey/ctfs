# Sekai Game Start

## Description

Hey it's our Sekai Game – try to make it start!!

## Hint

```

 <?php
include('./flag.php');
class Sekai_Game{
    public $start = True;
    public function __destruct(){
        if($this->start === True){
            echo "Sekai Game Start Here is your flag ".getenv('FLAG');
        }
    }
    public function __wakeup(){
        $this->start=False;
    }
}
if(isset($_GET['sekai_game.run'])){
    unserialize($_GET['sekai_game.run']);
}else{
    highlight_file(__FILE__);
}

?> 


```

## Solution

It seems like in the first run it enters in the else statement highlight_file().
I need to make a get request to the page with some serialized data in the variable 'sekai_game.run'.

Note: I cant make a request with that variable name

Conversely, unserialize() checks for the presence of a function with the magic name __wakeup(). 
If present, this function can reconstruct any resources that the object may have. 

The objective here is to try and send an serialized payload and then try to trigger the __destruct function
so we can get the flag.

NOTE: I DONT KNOW...
