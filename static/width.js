(function(){
    function computed(){
        let win=document.documentElement.clientHeight || document.body.clientHeight;
        let des=812;
        if (win>des){
            document.documentElement.style.fontSize="100px"
            return;
        }
        document.documentElement.style.fontSize=win/des*100+"px"
    }
    computed();
    window.onresize=function (){
        computed();
    }
})();