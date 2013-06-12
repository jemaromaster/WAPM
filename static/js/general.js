// JavaScript Document

function checkEmail(value)
{
     var filter = /([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9._-]+)/gi;
     if(!filter.test(value))
     {
	    return false;
     }
	return true;
}



 function submitForm()
 {
	 var form=document.getElementById("frm_guest");
	 var send=true;
 if (form.name.value=="")
		{
		  alert("Please enter your name");
			send=false;
		}else if(form.comment.value=="")
		{
			alert("Please enter your comment!");
			send=false;
			}else if(form.email.value=="")
		{
		  alert("Please enter your email address!");
			send=false;
		}else if(!form.email.value=="")
	  {
		if (!checkEmail(form.email.value))
		{
			alert("Please enter a correct email address!")
			send=false;
			}
		}
	
		
   if(send==true)
		{
		  form.submit();
		}
 }

			var menuids=new Array("verticalmenu") //Enter id(s) of UL menus, separated by commas
			var submenuoffset=-2 //Offset of submenus from main menu. Default is -2 pixels.
			
			function createcssmenu(){
			for (var i=0; i<menuids.length; i++){
			  var ultags=document.getElementById(menuids[i]).getElementsByTagName("ul")
			    for (var t=0; t<ultags.length; t++){
			    var spanref=document.createElement("span")
					spanref.className="arrowdiv"
					spanref.innerHTML="&nbsp;&nbsp;"
					ultags[t].parentNode.getElementsByTagName("a")[0].appendChild(spanref)
			    ultags[t].parentNode.onmouseover=function(){
			    this.getElementsByTagName("ul")[0].style.left=this.parentNode.offsetWidth+submenuoffset+"px"
			    this.getElementsByTagName("ul")[0].style.display="block"
			    }
			    ultags[t].parentNode.onmouseout=function(){
			    this.getElementsByTagName("ul")[0].style.display="none"
			    }
			    }
			  }
			}
		function changeLang(lang)
		{
			var frm = document.getElementById('frmLang');
			frm.lang.value = lang;
			frm.submit();
		}	
		
	$(document).ready(
		function()
		{

			createcssmenu();
			
		}
	);