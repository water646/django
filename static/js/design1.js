

var bt=document.getElementById('send');
var zj=document.getElementById('zhongjian');
bt.addEventListener('click',()=>sendMess(bt));  //不能直接写上函数，要写箭头函数，否则会直接调用

function sendMess(button) 
{
    var ipt=button.parentNode.children[0];
    var val=ipt.value;  //获取输入框的内容到val
    if(val=='')     return;
    ipt.value='';

    const para=document.createElement("p");
    para.style="display:inline-block; position:relative; bottom:7px; left:3px";
    para.textContent=`${val}`;  //创建p标签的para，内容为val变量

    var kuang=document.createElement('div');
    const img=document.createElement('img');


    img.src="headimg.png";
    img.style="height: 40px; width:40px; display:inline-block; position:relative; top:5px";
    kuang.style="margin:5px; border: 1px solid aqua; height:50px; width:1000px";
    kuang.appendChild(img);
    kuang.appendChild(para);    //把图片和文字拼起来


    zj.appendChild(kuang);   //向zj这个div插入段落

}