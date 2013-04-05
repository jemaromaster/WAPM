$(document).ready(function() {
	/* Centrar pagina */
	var pagina = $("#pagina");
	var p_left = pagina.width();
	var p_top = pagina.height();
	
	if(p_left < $(document).width()){
		p_left = (-1)*p_left/2;
		pagina.css('left','50%');
		pagina.css('margin-left',p_left);
	}
	
	if(p_top < $(document).height()){
		p_top = (-1)*p_top/2;
		pagina.css('top','50%');
		pagina.css('margin-top',p_top);
	}
	
	/* Botones deslizantes de administracion*/
	$(".usuarios").live("click",function() {
		window.location = "usuarios.html";
	});
	$(".roles").live("click",function() {
		window.location = "roles.html";
	});
	$(".r-u").live("click",function() {
		window.location = "roles-usuario.html";
	});
	$(".header").hover(function() {
		$(".usuarios").css("top","100px");
		$(".roles").css("top","160px");
		$(".r-u").css("top","220px");
		$(".icono-adm").css("z-index","999");
	});
	$(document).click(function() {
		$(".icono-adm").css("z-index","0");
		$(".icono-adm").css("top","0px");
	});
});
