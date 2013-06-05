// JavaScript Document
$(document).ready(function(){
	$("#search-form li").last().hide();
	if( $.browser.msie && $.browser.version == 6 ) {
		$(".list_image ul li a .litpic").css({
			"display":"block",
			"font-size":"188px",
			"font-family":"Arial"
		});

		$("#img_content #imgbox li img").each(function() {
			var imw = $(this).width(),
				imh = $(this).height();
			if ( imw < imh ) {
				$(this).css({"height":"500px"});
			} else if ( imw > imh && imw >= 680 ) {
				$(this).css({"width":"680px"});
			};
		});

		$(".list_image ul li a .litpic img").each(function() {
			var imw = $(this).width(),
				imh = $(this).height();
			if ( imw > imh ) {
				$(this).css({"width":"206px","height":"auto"});
			} else if ( imw < imh ) {
				$(this).css({"width":"auto","height":"208px"});
			}
		});
	};

});
$(function(){
	$("#searchbox .tabbtnul li").click(function() {
		$(".tabbtnul").find("li").removeClass("this");
		$(this).addClass("this");
		$("#search-form").find ("li").hide();
		$( "." + $(this).attr("id") + "con" ).show();
	});
	$(".list_image ul li a").hover(function() {
		$(this).find(".info").animate({bottom:'0px'},"fast");
	},function() {
		$(this).find(".info").animate({bottom:'-60px'},"fast");
	});
	/*
	$("#total").text( $("#img_content #imgbox li").length );
	$("#img_content #imgbox li").each(function(i) {
		if ( $(this).hasClass("this") ) {
			$("#now").text( i + 1 );
		};
	});*/
	$("#img_prev").hover(function() {
		$(this).find("span").animate({opacity:1},250);
	},function() {
		$(this).find("span").animate({opacity:0},250);
	});
	$("#img_next").hover(function() {
		$(this).find("span").animate({opacity:1},250);
	},function() {
		$(this).find("span").animate({opacity:0},250);
	});
	/*
	$("#img_prev").click(function() {
		$("#img_content #imgbox li").each(function(i) {

			if ( $(this).hasClass("this") ) {
				if ( i == 0 ) {
					alert("这是第一张图片！");
					return false;
				};
				$(this).prev().addClass("this");
				$(this).removeClass("this");
				var imgw = $(this).prev().find("img").width(),
					imgh = $(this).prev().find("img").height();
				if ( imgw < imgh && imgh > 500 ) {
					$(this).prev().find("img").css("height","500px");
				} else if ( imgw > imgh  && imgw > 680 ) {
					$(this).prev().find("img").css("width","680px");
				};
				var num = parseInt( $("#now").text());
				$("#now").text( num - 1 );
				return false;
			};

		});

	});*/
	/*
	$("#img_next").click(function() {
		$("#img_content #imgbox li").each(function() {

			if ( $(this).hasClass("this") ) {
				$(this).next().addClass("this");
				$(this).removeClass("this");
				var imgw = $(this).next().find("img").width(),
					imgh = $(this).next().find("img").height();
				if ( imgw < imgh && imgh > 500 ) {
					$(this).next().find("img").css("height","500px");
				} else if ( imgw > imgh  && imgw > 680 ) {
					$(this).next().find("img").css("width","680px");
				};
				var num = parseInt( $("#now").text());
				$("#now").text( num + 1 );
				return false;
			};
			if ( $("#now").text() == $("#total").text() ) {
				alert("这最后一张图片！");
				return false;
			};

		});
	});*/
});