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

But PHP variable can't use .(dot). But this variable is different: it uses _(underscore) and .(dot).(https://stackoverflow.com/questions/1057622/dot-in-variable-name)
Since it has both, the character [ will turn into _ and the .(dot) will not turn.
So the final expression will be ?sekai[game.run

Since we can control the serailized values and there is a bug in "C:" of the serialized string that it does not trigger __wakeup function : https://bugs.php.net/bug.php?id=81151
To trigger the destruct function the payload will be = 'C:10:"Sekai_Game":0:{}'

Since we trigger only the __destruct function we are able to get the key.
https://bugs.php.net/bug.php?id=81151

## References
https://medium.com/swlh/exploiting-php-deserialization-56d71f03282a
